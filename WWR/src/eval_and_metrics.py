import argparse
import json
import re
import subprocess
from pathlib import Path

import pandas as pd

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

def norm_text(x) -> str:
    """Normalize strings for comparison."""
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return ""
    s = str(x).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def norm_salary(x):
    """Normalize salary to float if possible, else None."""
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = str(x).strip()
    if s == "" or s.lower() in {"not listed", "none", "null"}:
        return None
    # remove currency symbols/commas
    s = re.sub(r"[^0-9.\-]", "", s)
    try:
        return float(s)
    except Exception:
        return None

def compare_field(field: str, pred_val, gt_val) -> bool:
    """Field-specific equality."""
    if field == "salary":
        return norm_salary(pred_val) == norm_salary(gt_val)
    return norm_text(pred_val) == norm_text(gt_val)

def ensure_cols(df: pd.DataFrame) -> pd.DataFrame:
    for c in FIELDS:
        if c not in df.columns:
            df[c] = None
    return df[FIELDS]

def run_radon(src_dir: str, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    cc_path = out_dir / "radon_cc.txt"
    raw_path = out_dir / "radon_raw.txt"

    # If radon isn't installed, these will fail; that's okay.
    with open(cc_path, "w", encoding="utf-8") as f:
        subprocess.run(["radon", "cc", "-s", "-a", src_dir], stdout=f, stderr=subprocess.STDOUT, check=False)

    with open(raw_path, "w", encoding="utf-8") as f:
        subprocess.run(["radon", "raw", "-s", src_dir], stdout=f, stderr=subprocess.STDOUT, check=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred_csv", default="data/parsed/wwr_jobs.csv")
    ap.add_argument("--gt_csv", default="data/ground_truth/wwr_ground_truth_20.csv")
    ap.add_argument("--n", type=int, default=20, help="How many rows to evaluate (default 20).")
    ap.add_argument("--src_dir", default="scraper", help="Directory to run radon on.")
    ap.add_argument("--out_dir", default="data/metrics")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load predictions + ground truth
    pred = pd.read_csv(args.pred_csv)
    gt = pd.read_csv(args.gt_csv)

    pred = ensure_cols(pred)
    gt = ensure_cols(gt)

    n = min(args.n, len(pred), len(gt))
    if n == 0:
        raise SystemExit("No rows to evaluate. Check your CSV paths and contents.")

    pred_n = pred.iloc[:n].reset_index(drop=True)
    gt_n = gt.iloc[:n].reset_index(drop=True)

    # Field accuracies
    field_matches = {f: 0 for f in FIELDS}
    per_row_all_correct = []
    per_row_mismatch_count = []

    for i in range(n):
        all_ok = True
        mismatches = 0
        for f in FIELDS:
            ok = compare_field(f, pred_n.loc[i, f], gt_n.loc[i, f])
            if ok:
                field_matches[f] += 1
            else:
                all_ok = False
                mismatches += 1
        per_row_all_correct.append(all_ok)
        per_row_mismatch_count.append(mismatches)

    field_accuracy = {f: field_matches[f] / n for f in FIELDS}
    overall_all_fields_correct = sum(per_row_all_correct) / n

    # Save metrics JSON
    metrics = {
        "n_evaluated": n,
        "field_accuracy": field_accuracy,
        "all_fields_correct_rate": overall_all_fields_correct,
    }

    with open(out_dir / "accuracy.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Save per-row report
    report = gt_n.copy()
    report = report.add_prefix("gt_")
    pred_rep = pred_n.copy().add_prefix("pred_")
    merged = pd.concat([report, pred_rep], axis=1)
    merged["all_fields_correct"] = per_row_all_correct
    merged["mismatch_count"] = per_row_mismatch_count
    merged.to_csv(out_dir / "per_row_report.csv", index=False)

    # Run radon
    run_radon(args.src_dir, out_dir)

    print(f"✅ Saved accuracy -> {out_dir / 'accuracy.json'}")
    print(f"✅ Saved row report -> {out_dir / 'per_row_report.csv'}")
    print(f"✅ Saved radon outputs -> {out_dir / 'radon_cc.txt'} and {out_dir / 'radon_raw.txt'}")

if __name__ == "__main__":
    main()
