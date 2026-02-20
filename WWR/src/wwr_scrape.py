import time
import json
import re
import argparse
from pathlib import Path

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


def save_json(obj, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def shave_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # strip all attributes (class/id/data-*)
    for tag in soup.find_all(True):
        tag.attrs = {}

    s = str(soup)
    s = re.sub(r">\s+<", "><", s)     # collapse whitespace between tags
    s = re.sub(r"\s+", " ", s).strip()
    return s


def scroll_to_load(driver, rounds=10, pause=1.2):
    last_h = 0
    for _ in range(rounds):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        h = driver.execute_script("return document.body.scrollHeight;")
        if h == last_h:
            break
        last_h = h


def click_view_all_if_present(driver):
    """
    On WWR search pages, you may see a button like:
    'View all 65 All Other Remote jobs'
    Clicking it expands the full list.
    """
    try:
        # Look for any link/button that starts with "View all"
        elems = driver.find_elements(By.XPATH, "//*[self::a or self::button][contains(., 'View all')]")
        if not elems:
            return False

        # Click the first one that is displayed
        for el in elems:
            if el.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.5)
                try:
                    el.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", el)
                time.sleep(2.0)
                return True

        return False
    except Exception:
        return False


def extract_job_cards(page_source: str):
    soup = BeautifulSoup(page_source, "html.parser")

    cards = []
    # WWR listings are typically in <section class="jobs"> <li> ... <a href="/remote-jobs/...">
    for li in soup.select("section.jobs li"):
        a = li.select_one("a[href*='/remote-jobs/']")
        if a:
            cards.append(str(li))

    # Fallback: sometimes structure changes; just find anchors to remote-jobs and use parent containers
    if not cards:
        anchors = soup.select("a[href*='/remote-jobs/']")
        for a in anchors:
            parent = a.find_parent("li") or a.find_parent("article") or a
            cards.append(str(parent))

    # De-dup while preserving order
    seen = set()
    uniq = []
    for c in cards:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--url",
        default="https://weworkremotely.com/remote-jobs/search?term=data+scientist&sort=Any+Time",
        help="WWR search URL (recommended: /remote-jobs/search?term=...)"
    )
    ap.add_argument("--target", type=int, default=250)
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--out_raw", default="data/raw/wwr_cards_raw.json")
    ap.add_argument("--out_clean", default="data/cleaned/wwr_cards_clean.json")
    args = ap.parse_args()

    driver = uc.Chrome(headless=args.headless)

    try:
        driver.get(args.url)
        time.sleep(4)

        # If "View all ..." exists, click it to expand results
        clicked = click_view_all_if_present(driver)
        if clicked:
            # after expanding, scroll again
            scroll_to_load(driver, rounds=6, pause=1.2)

        # scroll to load more items if any
        scroll_to_load(driver, rounds=10, pause=1.3)

        resolved_url = driver.current_url
        cards = extract_job_cards(driver.page_source)

        # if still low, scroll a bit more
        if len(cards) < args.target:
            scroll_to_load(driver, rounds=10, pause=1.3)
            cards = extract_job_cards(driver.page_source)

        cards = cards[:args.target]
        cleaned_cards = [shave_html(h) for h in cards]

        save_json(
            {
                "source_url_input": args.url,
                "source_url_resolved": resolved_url,
                "count": len(cards),
                "cards_html": cards,
            },
            args.out_raw
        )

        save_json(
            {
                "source_url_resolved": resolved_url,
                "count": len(cleaned_cards),
                "cards_clean_html": cleaned_cards,
            },
            args.out_clean
        )

        print(f"Resolved URL: {resolved_url}")
        print(f"Saved raw -> {args.out_raw}")
        print(f"Saved cleaned -> {args.out_clean}")

    finally:
        # avoid WinError 6 on Windows
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
