"""Agreement between the version 1.0 first score and the version 1.0 second pass.

This does not describe the published version 1.1 index. The comparison uses
score against recode_score in data/coded/evidence_log.csv.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEED = 42
EVID = ROOT / "data" / "coded" / "evidence_log.csv"
OUT = ROOT / "outputs" / "tables" / "table_reliability_summary.csv"


def quadratic_weighted_kappa(y1: np.ndarray, y2: np.ndarray, n_cats: int = 4) -> float:
    """Cohen's kappa with quadratic weights for ordinal 0-3."""
    o = np.zeros((n_cats, n_cats), dtype=float)
    for a, b in zip(y1, y2):
        o[int(a), int(b)] += 1
    o /= o.sum()
    hist1 = o.sum(axis=1)
    hist2 = o.sum(axis=0)
    e = np.outer(hist1, hist2)
    w = np.zeros((n_cats, n_cats))
    for i in range(n_cats):
        for j in range(n_cats):
            w[i, j] = ((i - j) ** 2) / ((n_cats - 1) ** 2)
    num = (w * o).sum()
    den = (w * e).sum()
    if den == 0:
        return 1.0
    return 1.0 - num / den


def unweighted_kappa(y1: np.ndarray, y2: np.ndarray, n_cats: int = 4) -> float:
    o = np.zeros((n_cats, n_cats), dtype=float)
    for a, b in zip(y1, y2):
        o[int(a), int(b)] += 1
    o /= o.sum()
    po = np.trace(o)
    pe = np.outer(o.sum(axis=1), o.sum(axis=0)).trace()
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)


def main() -> None:
    evid = pd.read_csv(EVID, dtype=str, keep_default_na=False)
    recoded = evid[(evid["recode_score"].str.strip() != "") & (evid["score"].str.upper() != "NA")]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if recoded.empty:
        pd.DataFrame(
            [
                {
                    "subset_n_firms": 0,
                    "n_indicator_pairs": 0,
                    "exact_agreement_pct": "",
                    "within_one_pct": "",
                    "unweighted_kappa": "",
                    "weighted_kappa_quad": "",
                    "ci_95_lower": "",
                    "ci_95_upper": "",
                    "meets_80pct_threshold": "pending_recode",
                    "note": "recode_score empty; run after 2-week blind recode of 5 firms",
                }
            ]
        ).to_csv(OUT, index=False)
        print("No recodes yet; wrote pending placeholder", OUT)
        return

    y1 = recoded["score"].astype(float).to_numpy()
    y2 = recoded["recode_score"].astype(float).to_numpy()
    exact = float((y1 == y2).mean() * 100)
    within = float((np.abs(y1 - y2) <= 1).mean() * 100)
    kw = quadratic_weighted_kappa(y1, y2)
    ku = unweighted_kappa(y1, y2)

    rng = np.random.default_rng(SEED)
    boots = []
    n = len(y1)
    for _ in range(10000):
        idx = rng.integers(0, n, n)
        boots.append(quadratic_weighted_kappa(y1[idx], y2[idx]))
    lo, hi = np.percentile(boots, [2.5, 97.5])

    pd.DataFrame(
        [
            {
                "subset_n_firms": recoded["firm_id"].nunique(),
                "n_indicator_pairs": len(recoded),
                "exact_agreement_pct": round(exact, 2),
                "within_one_pct": round(within, 2),
                "unweighted_kappa": round(ku, 3),
                "weighted_kappa_quad": round(kw, 3),
                "ci_95_lower": round(float(lo), 3),
                "ci_95_upper": round(float(hi), 3),
                "meets_80pct_threshold": "yes" if exact >= 80 else "no",
                "note": "Version 1.0 first score against the version 1.0 second pass. Not the published version 1.1 index.",
            }
        ]
    ).to_csv(OUT, index=False)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
