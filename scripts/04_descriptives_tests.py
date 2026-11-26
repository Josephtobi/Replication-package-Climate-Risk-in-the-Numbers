"""RQ1–RQ4 descriptives and indicative non-parametric tests."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
SEED = 42
np.random.seed(SEED)
TABLES = ROOT / "outputs" / "tables"
MASTER = TABLES / "table_master_firm_scores.csv"
PROF = ROOT / "data" / "coded" / "firm_profiles.csv"
HITS = TABLES / "table_keyword_hits.csv"

INDICATORS = ["C1", "C2", "C3", "C4", "C5a", "C5b", "C6", "C7", "A1"]


def epsilon_sq(h: float, n: int) -> float:
    if n <= 1:
        return float("nan")
    return h / (n - 1)


def rank_biserial(u: float, n1: int, n2: int) -> float:
    return 1 - (2 * u) / (n1 * n2)


def main() -> None:
    m = pd.read_csv(MASTER, keep_default_na=False)
    p = pd.read_csv(PROF, keep_default_na=False)
    h = pd.read_csv(HITS, keep_default_na=False)
    df = m.merge(p[["firm_id", "total_assets_ngn_bn", "sr_risks_named_count", "auditor_tier", "auditor_name"]], on="firm_id")
    df = df.merge(h[["firm_id", "total_ar_hits"]], on="firm_id")
    df["ci"] = df["connectivity_index"].astype(float)
    df["sr_risks_named_count"] = pd.to_numeric(df["sr_risks_named_count"], errors="coerce").fillna(0)
    df["total_assets_ngn_bn"] = pd.to_numeric(df["total_assets_ngn_bn"], errors="coerce")

    # RQ1 indicator summary
    rows = []
    for ind in INDICATORS:
        vals = pd.to_numeric(df[ind], errors="coerce").dropna()
        if vals.empty:
            continue
        rows.append(
            {
                "indicator": ind,
                "n": int(vals.shape[0]),
                "count_0": int((vals == 0).sum()),
                "count_1": int((vals == 1).sum()),
                "count_2": int((vals == 2).sum()),
                "count_3": int((vals == 3).sum()),
                "mean": round(float(vals.mean()), 3),
                "sd": round(float(vals.std(ddof=1)) if len(vals) > 1 else 0, 3),
                "median": float(vals.median()),
                "iqr": round(float(vals.quantile(0.75) - vals.quantile(0.25)), 3),
            }
        )
    ind_sum = pd.DataFrame(rows).sort_values("mean")
    ind_sum["indicator_rank_worst_to_best"] = range(1, len(ind_sum) + 1)
    ind_sum.to_csv(TABLES / "table_rq1_indicator_summary.csv", index=False)

    tier = (
        df.groupby(["tier", "sector"]).size().reset_index(name="n")
        if False
        else df.groupby("tier").size().reset_index(name="n")
    )
    tier["pct"] = (tier["n"] / tier["n"].sum() * 100).round(1)
    tier_sec = df.groupby(["sector", "tier"]).size().reset_index(name="n")
    tier_out = pd.concat(
        [tier.assign(sector="All"), tier_sec],
        ignore_index=True,
    )
    tier_out.to_csv(TABLES / "table_rq1_tier_distribution.csv", index=False)

    # RQ2 Kruskal-Wallis
    groups = [g["ci"].to_numpy() for _, g in df.groupby("sector")]
    if len(groups) >= 2 and all(len(g) for g in groups):
        h_stat, p_kw = stats.kruskal(*groups)
    else:
        h_stat, p_kw = float("nan"), float("nan")
    rq2 = (
        df.groupby("sector")["ci"]
        .agg(n="count", median_ci="median", min_ci="min", max_ci="max", iqr=lambda x: x.quantile(0.75) - x.quantile(0.25))
        .reset_index()
    )
    rq2["kruskal_H"] = round(float(h_stat), 3)
    rq2["kruskal_p_indicative"] = round(float(p_kw), 4)
    rq2["epsilon_sq"] = round(epsilon_sq(float(h_stat), len(df)), 3)
    rq2["note"] = "p-values are indicative at N=14"
    rq2.to_csv(TABLES / "table_rq2_sector_comparison.csv", index=False)

    # RQ3 Mann-Whitney two panels
    panels = []
    # Panel A Phase 1 vs rest
    a = df[df["adoption_group"] == "Phase 1"]["ci"]
    b = df[df["adoption_group"] != "Phase 1"]["ci"]
    if len(a) and len(b):
        u, p = stats.mannwhitneyu(a, b, alternative="two-sided", method="exact")
        panels.append(
            {
                "panel": "A_Phase1_vs_rest",
                "group": "Phase 1",
                "n": len(a),
                "median_ci": float(a.median()),
                "iqr": float(a.quantile(0.75) - a.quantile(0.25)),
                "range": f"{a.min()}-{a.max()}",
                "mannwhitney_U": float(u),
                "p_indicative": float(p),
                "rank_biserial_r": round(rank_biserial(float(u), len(a), len(b)), 3),
            }
        )
        panels.append(
            {
                "panel": "A_Phase1_vs_rest",
                "group": "Non-Phase 1",
                "n": len(b),
                "median_ci": float(b.median()),
                "iqr": float(b.quantile(0.75) - b.quantile(0.25)),
                "range": f"{b.min()}-{b.max()}",
                "mannwhitney_U": float(u),
                "p_indicative": float(p),
                "rank_biserial_r": round(rank_biserial(float(u), len(a), len(b)), 3),
            }
        )
    # Panel B all adopters vs non
    adopters = df[df["adoption_group"].isin(["Phase 1", "Voluntary"])]["ci"]
    non = df[df["adoption_group"] == "Non-adopter"]["ci"]
    if len(adopters) and len(non):
        u, p = stats.mannwhitneyu(adopters, non, alternative="two-sided", method="exact")
        for label, ser in [("All adopters", adopters), ("Non-adopters", non)]:
            panels.append(
                {
                    "panel": "B_Adopters_vs_Non",
                    "group": label,
                    "n": len(ser),
                    "median_ci": float(ser.median()),
                    "iqr": float(ser.quantile(0.75) - ser.quantile(0.25)),
                    "range": f"{ser.min()}-{ser.max()}",
                    "mannwhitney_U": float(u),
                    "p_indicative": float(p),
                    "rank_biserial_r": round(rank_biserial(float(u), len(adopters), len(non)), 3),
                }
            )
    pd.DataFrame(panels).to_csv(TABLES / "table_rq3_adopter_comparison.csv", index=False)

    # SR-FS decoupling
    def fs_substantive(row):
        n = 0
        for ind in ["C1", "C2", "C3", "C4", "C5a", "C5b", "C6", "C7"]:
            v = pd.to_numeric(row[ind], errors="coerce")
            if pd.notna(v) and v >= 2:
                n += 1
        return n

    df["fs_substantive_count"] = df.apply(fs_substantive, axis=1)
    df["decoupling_gap"] = df["sr_risks_named_count"] - df["fs_substantive_count"]
    rho, p_rho = stats.spearmanr(df["sr_risks_named_count"], df["ci"])
    dec = df[
        ["firm_id", "company", "adoption_group", "sr_risks_named_count", "fs_substantive_count", "decoupling_gap", "ci"]
    ].copy()
    dec["spearman_rho_sr_ci"] = round(float(rho), 3)
    dec["spearman_p_indicative"] = round(float(p_rho), 4)
    dec.to_csv(TABLES / "table_rq3_sr_fs_decoupling.csv", index=False)

    # RQ4 auditor KAMs
    a1 = pd.to_numeric(df["A1"], errors="coerce")
    rq4 = (
        df.assign(A1_num=a1)
        .groupby(["auditor_tier", "A1_num"])
        .size()
        .reset_index(name="n")
    )
    rq4_sec = df.assign(A1_num=a1).groupby(["sector", "A1_num"]).size().reset_index(name="n")
    rq4_firm = df[["firm_id", "company", "sector", "auditor_name", "auditor_tier", "A1"]].copy()
    rq4_firm.to_csv(TABLES / "table_rq4_auditor_kams.csv", index=False)
    # also write summary counts
    pd.concat(
        [
            rq4.assign(breakdown="auditor_tier"),
            rq4_sec.assign(breakdown="sector", auditor_tier=""),
        ],
        ignore_index=True,
    ).to_csv(TABLES / "table_rq4_auditor_kams_summary.csv", index=False)

    # Robustness Spearman
    rob = []
    assets = df.dropna(subset=["total_assets_ngn_bn"])
    if len(assets) >= 3:
        rho_a, p_a = stats.spearmanr(np.log(assets["total_assets_ngn_bn"]), assets["ci"])
        rob.append(
            {
                "pair": "CI_vs_ln_total_assets",
                "n": len(assets),
                "spearman_rho": round(float(rho_a), 3),
                "p_indicative": round(float(p_a), 4),
                "note": "Airtel Africa is excluded. Its assets are in US dollars and were not converted. p is indicative.",
            }
        )
    rho_h, p_h = stats.spearmanr(df["total_ar_hits"], df["ci"])
    rob.append(
        {
            "pair": "CI_vs_total_ar_hits",
            "n": len(df),
            "spearman_rho": round(float(rho_h), 3),
            "p_indicative": round(float(p_h), 4),
            "note": "indicative",
        }
    )
    pd.DataFrame(rob).to_csv(TABLES / "table_robustness_correlations.csv", index=False)
    print("Wrote RQ tables to", TABLES)


if __name__ == "__main__":
    main()
