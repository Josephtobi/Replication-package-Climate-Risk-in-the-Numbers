"""Validate the coded files and compute the published Connectivity Index.

The index uses codebook version 1.1, in outputs/v11/evidence_v11.csv.
The score column in data/coded/evidence_log.csv is the version 1.0 first pass
and is not the published index. Run scripts/06_score_v11.py first.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEED = 42
np.random.seed(SEED)

RUBRIC = json.loads((ROOT / "config" / "rubric_definition.json").read_text(encoding="utf-8"))
EVID = ROOT / "data" / "coded" / "evidence_log.csv"
PUBLISHED = ROOT / "outputs" / "v11" / "evidence_v11.csv"
OUT = ROOT / "outputs" / "tables" / "table_master_firm_scores.csv"

INDICATORS = ["C1", "C2", "C3", "C4", "C5a", "C5b", "C6", "C7"]


def sector_max(sector: str, c4_na: bool) -> float:
    if sector == "Banking":
        return 12.0
    if sector == "Telecoms":
        return 15.0 if c4_na else 18.0
    return 18.0


def tier_of(ci: float) -> str:
    if ci <= 0:
        return "Tier 4 Silent"
    if ci <= 33:
        return "Tier 3 Boilerplate"
    if ci <= 66:
        return "Tier 2 Partial"
    return "Tier 1 Connected"


def main() -> None:
    evid = pd.read_csv(EVID, dtype=str, keep_default_na=False)
    if not PUBLISHED.exists():
        raise SystemExit("Missing outputs/v11/evidence_v11.csv. Run scripts/06_score_v11.py first.")
    published = pd.read_csv(PUBLISHED, dtype=str, keep_default_na=False)

    assert evid["firm_id"].nunique() == 14, "Expected 14 firms in evidence_log"
    assert published["firm_id"].nunique() == 14, "Expected 14 firms in the version 1.1 file"
    non_na = evid[evid["score"].str.upper() != "NA"]
    missing_q = non_na[non_na["verbatim_quote"].str.strip() == ""]
    if len(missing_q):
        raise SystemExit(f"Missing quotes on the version 1.0 score column: {len(missing_q)} rows")
    needs_quote = published[published["score"].isin(["1", "2", "3"])]
    missing_v11 = needs_quote[needs_quote["verbatim_quote"].str.strip() == ""]
    if len(missing_v11):
        raise SystemExit(f"Missing version 1.1 quotes: {len(missing_v11)} rows")

    rows = []
    for fid, g in published.groupby("firm_id"):
        company = g["company"].iloc[0]
        sector = g["sector"].iloc[0]
        adoption = g["adoption_group"].iloc[0]
        scores = {}
        for ind in INDICATORS + ["A1"]:
            sub = g[g["indicator"] == ind]
            if sub.empty:
                scores[ind] = "NA"
            else:
                scores[ind] = sub["score"].iloc[0]

        c4_na = str(scores.get("C4", "")).upper() == "NA"
        smax = sector_max(sector, c4_na)
        raw = 0.0
        for ind in INDICATORS:
            val = scores[ind]
            if str(val).upper() == "NA" or val == "":
                continue
            raw += float(val)
        ci = round(raw / smax * 100, 2)
        count3 = sum(1 for ind in INDICATORS if str(scores[ind]) == "3")
        rows.append(
            {
                "firm_id": fid,
                "company": company,
                "sector": sector,
                "adoption_group": adoption,
                "codebook": "1.1",
                **{ind: scores[ind] for ind in INDICATORS},
                "raw_score": raw,
                "sector_max": smax,
                "connectivity_index": ci,
                "tier": tier_of(ci),
                "A1": scores["A1"],
                "count_score_3": count3,
            }
        )

    master = pd.DataFrame(rows)
    # overall rank with tie-breaks: CI, C7, count3, A1
    master["C7_num"] = pd.to_numeric(master["C7"], errors="coerce").fillna(-1)
    master["A1_num"] = pd.to_numeric(master["A1"], errors="coerce").fillna(-1)
    master = master.sort_values(
        ["connectivity_index", "C7_num", "count_score_3", "A1_num", "firm_id"],
        ascending=[False, False, False, False, True],
    ).reset_index(drop=True)
    master["overall_rank"] = np.arange(1, len(master) + 1)
    # shared ranks if identical key fields
    key = master[["connectivity_index", "C7_num", "count_score_3", "A1_num"]].astype(float)
    master["overall_rank"] = key.apply(tuple, axis=1).rank(method="min", ascending=False).astype(int)

    master["sector_rank"] = master.groupby("sector")["connectivity_index"].rank(
        method="min", ascending=False
    ).astype(int)
    master = master.drop(columns=["C7_num", "A1_num"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    master.sort_values("overall_rank").to_csv(OUT, index=False)
    print(master.sort_values("overall_rank")[
        ["firm_id", "company", "connectivity_index", "tier", "overall_rank"]
    ].to_string(index=False))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
