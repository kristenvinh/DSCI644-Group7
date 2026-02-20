import os, json, time, argparse, re
from pathlib import Path

import pandas as pd
from openai import OpenAI

FIELDS = [
    "job_title",
    "company_name",
    "location",
    "salary",
    "salary_type",
    "job_description",
    "job_tags",
    "job_url",
]

SYSTEM = """You extract structured job fields from cleaned HTML snippets of We Work Remotely job cards.

Return JSON with this exact schema:
{
  "items": [
    {
      "i": <integer index provided by user>,
      "job_title": <string>,
      "company_name": <string>,
      "location": <string>,
      "salary": <number or null>,
      "salary_type": <"hourly"|"monthly"|"yearly"|"Not Listed">,
      "job_description": <string or "Not Listed">,
      "job_tags": <string>,
      "job_url": <string>
    },
    ...
  ]
}

Rules:
- If salary missing: salary=null and salary_type="Not Listed".
- If a field missing: use "Not Listed" (except salary).
- Do not add extra keys.
"""

def load_clean_cards(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["cards_clean_html"]

def coerce_item(obj):
    out = {k: obj.get(k, None) for k in FIELDS}
    # normalize salary fields
    if out["salary"] in ("Not Listed", "", "None"):
        out["salary"] = None
    if not out.get("salary_type"):
        out["salary_type"] = "Not Listed"
    if out["salary"] is None:
        out["salary_type"] = "Not Listed"
    if not out.get("job_description"):
        out["job_description"] = "Not Listed"
    return out

def batch_prompt(batch, start_index):
    # Keep prompt compact: provide (i, html) pairs
    lines = []
    for j, html in enumerate(batch):
        i = start_index + j
        lines.append(f"ITEM {i}:\n{html}\n")
    return "\n".join(lines)

def parse_batch(client: OpenAI, batch, start_index, model="gpt-4.1-mini", retries=3):
    for attempt in range(1, retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": batch_prompt(batch, start_index)},
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )
            data = json.loads(resp.choices[0].message.content)

            items = data.get("items", [])
            # Map by index i so order is stable even if model reorders
            by_i = {int(it["i"]): it for it in items if "i" in it}

            results = []
            for j in range(len(batch)):
                i = start_index + j
                it = by_i.get(i)
                if not it:
                    # safe fallback if missing
                    results.append({k: "Not Listed" for k in FIELDS} | {"salary": None, "salary_type": "Not Listed"})
                else:
                    results.append(coerce_item(it))
            return results

        except Exception as e:
            print(f"[ERROR] Batch start={start_index} attempt={attempt}: {type(e).__name__}: {e}")
            # optional: dump the batch prompt for debugging
            if attempt == retries:
                Path("data/parsed").mkdir(parents=True, exist_ok=True)
                with open(f"data/parsed/failed_batch_{start_index}.txt", "w", encoding="utf-8") as f:
                    f.write(batch_prompt(batch, start_index)[:200000])  # cap so file isn't huge

                return [
                    {k: "Not Listed" for k in FIELDS} | {"salary": None, "salary_type": "Not Listed"}
                    for _ in batch
                ]
            time.sleep(1.5 * attempt)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_clean", default="data/cleaned/wwr_cards_clean.json")
    ap.add_argument("--out_csv", default="data/parsed/wwr_jobs.csv")
    ap.add_argument("--limit", type=int, default=250)
    ap.add_argument("--batch_size", type=int, default=10)
    ap.add_argument("--model", default="gpt-4o-mini")
    ap.add_argument("--filter_data_scientist", action="store_true",
                    help="After parsing, keep only rows whose title contains 'data scientist'")
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set. Set it in PowerShell: setx OPENAI_API_KEY \"...\" then reopen terminal.")

    client = OpenAI(api_key=api_key)

    cards = load_clean_cards(args.in_clean)[:args.limit]
    all_rows = []

    for start in range(0, len(cards), args.batch_size):
        batch = cards[start:start + args.batch_size]
        rows = parse_batch(client, batch, start_index=start, model=args.model)
        all_rows.extend(rows)
        print(f"Parsed {min(start + len(batch), len(cards))}/{len(cards)}")

    df = pd.DataFrame(all_rows, columns=FIELDS)

    if args.filter_data_scientist:
        df = df[df["job_title"].astype(str).str.contains("data scientist", case=False, na=False)]

    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out_csv, index=False)
    print(f"Wrote {len(df)} rows -> {args.out_csv}")

if __name__ == "__main__":
    main()