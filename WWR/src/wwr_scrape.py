import time
import json
import argparse
from pathlib import Path

import undetected_chromedriver as uc
from bs4 import BeautifulSoup


# -------------------------------
# CONFIG
# -------------------------------
DEFAULT_URL = "https://weworkremotely.com/categories/all-other-remote-jobs"


# -------------------------------
# HELPERS
# -------------------------------
def save_json(data, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def shave_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    for tag in soup.find_all(True):
        tag.attrs = {}

    return str(soup)


def scroll_page(driver, rounds=6):
    for _ in range(rounds):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.2)


# -------------------------------
# MAIN
# -------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--target", type=int, default=65)
    args = parser.parse_args()

    driver = uc.Chrome(headless=False, use_subprocess=True)

    print("Opening listing page...")
    driver.get(args.url)
    time.sleep(4)

    scroll_page(driver)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract job URLs
    links = []
    for a in soup.select("a[href^='/remote-jobs/']"):
        href = a.get("href")
        if href and "/remote-jobs/" in href:
            full = "https://weworkremotely.com" + href
            if full not in links:
                links.append(full)

    links = links[: args.target]
    print(f"Found {len(links)} job URLs")

    raw_html = []
    clean_html = []

    # Visit EACH job page
    for i, url in enumerate(links):
        print(f"[{i+1}/{len(links)}] Visiting {url}")
        driver.get(url)
        time.sleep(3)

        page = driver.page_source
        raw_html.append({
            "url": url,
            "html": page
        })

        clean_html.append(shave_html(page))

    driver.quit()

    # Save outputs
    save_json({
        "count": len(raw_html),
        "jobs": raw_html
    }, "data/raw/wwr_jobs_raw.json")

    save_json({
        "count": len(clean_html),
        "cards_clean_html": clean_html
    }, "data/cleaned/wwr_cards_clean.json")

    print("Saved FULL JOB HTML")
    print("data/raw/wwr_jobs_raw.json")
    print("data/cleaned/wwr_cards_clean.json")


if __name__ == "__main__":
    main()