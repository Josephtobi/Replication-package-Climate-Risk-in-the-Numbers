"""Disagreement list and a split of A1 from the connectivity indicators."""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from importlib.machinery import SourceFileLoader

ROOT = Path(__file__).resolve().parents[1]
rel = SourceFileLoader("rel", str(ROOT / "scripts" / "03_reliability.py")).load_module()

EVID = ROOT / "data" / "coded" / "evidence_log.csv"
SECOND = ROOT / "data" / "coded" / "recode_pass2.csv"
OUT_DIFF = ROOT / "outputs" / "v2" / "recode_disagreements.csv"
OUT_SPLIT = ROOT / "outputs" / "v2" / "recode_reliability_split.csv"


def pack(rows: list[dict], label: str) -> dict:
    y1 = np.array([float(r["score"]) for r in rows])
    y2 = np.array([float(r["recode_score"]) for r in rows])
    exact = float((y1 == y2).mean() * 100) if len(rows) else float("nan")
    within = float((np.abs(y1 - y2) <= 1).mean() * 100) if len(rows) else float("nan")
    kw = rel.quadratic_weighted_kappa(y1, y2) if len(rows) else float("nan")
    ku = rel.unweighted_kappa(y1, y2) if len(rows) else float("nan")
    return {
        "subset": label,
        "n_pairs": len(rows),
        "exact_agreement_pct": round(exact, 2),
        "within_one_pct": round(within, 2),
        "unweighted_kappa": round(ku, 3),
        "weighted_kappa_quad": round(kw, 3),
    }


def main() -> None:
    with EVID.open(encoding="utf-8", newline="") as handle:
        evid = list(csv.DictReader(handle))
    with SECOND.open(encoding="utf-8", newline="") as handle:
        second = {(r["firm_id"], r["indicator"]): r for r in csv.DictReader(handle)}
    paired = [
        r
        for r in evid
        if r["recode_score"].strip() and r["score"].strip().upper() != "NA"
    ]
    diffs = []
    for row in paired:
        if row["score"] == row["recode_score"]:
            continue
        other = second[(row["firm_id"], row["indicator"])]
        diffs.append(
            {
                "firm_id": row["firm_id"],
                "company": row["company"],
                "indicator": row["indicator"],
                "first_score": row["score"],
                "second_score": row["recode_score"],
                "gap_second_minus_first": int(row["recode_score"]) - int(float(row["score"])),
                "first_extract_page": row["page_number"],
                "second_extract_page": other["extract_page"],
                "first_quote": row["verbatim_quote"],
                "second_quote": other["verbatim_quote"],
            }
        )
    OUT_DIFF.parent.mkdir(parents=True, exist_ok=True)
    with OUT_DIFF.open("w", encoding="utf-8", newline="") as handle:
        fields = list(diffs[0].keys()) if diffs else ["firm_id"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(diffs)
    conn = [r for r in paired if r["indicator"] != "A1"]
    a1 = [r for r in paired if r["indicator"] == "A1"]
    split = [pack(paired, "all_paired"), pack(conn, "connectivity_C1_to_C7"), pack(a1, "A1_only")]
    with OUT_SPLIT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(split[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(split)
    print("disagreements", len(diffs))
    for row in split:
        print(row)
    for row in diffs:
        print(row["firm_id"], row["company"], row["indicator"], row["first_score"], "->", row["second_score"])


if __name__ == "__main__":
    main()
