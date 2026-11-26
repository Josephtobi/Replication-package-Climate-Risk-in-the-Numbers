"""Assemble outputs/v2 from the rerun tables. Does not recompute statistics."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
V2 = ROOT / "outputs" / "v2"
FIG = ROOT / "outputs" / "figures"


def main() -> None:
    V2.mkdir(parents=True, exist_ok=True)
    (V2 / "figures").mkdir(exist_ok=True)

    master = pd.read_csv(TABLES / "table_master_firm_scores.csv", dtype={"firm_id": str})
    dec = pd.read_csv(TABLES / "table_rq3_sr_fs_decoupling.csv", dtype={"firm_id": str})
    dec["firm_id"] = dec["firm_id"].str.zfill(2)
    scores = master.merge(
        dec[["firm_id", "sr_risks_named_count", "fs_substantive_count", "decoupling_gap"]],
        on="firm_id",
        how="left",
    )
    scores = scores.rename(
        columns={
            "sr_risks_named_count": "sr_risks",
            "fs_substantive_count": "fs_indicators_at_2_or_3",
            "decoupling_gap": "gap",
        }
    )
    scores.to_csv(V2 / "scores_v2.csv", index=False)

    evid = pd.read_csv(ROOT / "data" / "coded" / "evidence_log.csv", dtype=str, keep_default_na=False)
    evid.to_csv(V2 / "evidence_log_v2.csv", index=False)

    hits = pd.read_csv(TABLES / "table_keyword_hits.csv", dtype={"firm_id": str})
    for col in [
        "fs_hits_climate",
        "fs_hits_physical",
        "fs_hits_energy",
        "fs_hits_regulation",
        "fs_hits_banking",
        "fs_hits_standards",
        "fs_total_hits",
    ]:
        hits[col] = "NOT FOUND"
    hits["fs_note"] = (
        "Financial-statements-only recount was not published. "
        "A mechanical cut treated contents lines, five-year summaries, and note sentences as the statement."
    )
    hits.to_csv(V2 / "keyword_hits_v2.csv", index=False)

    banks = pd.DataFrame(
        [
            {
                "bank": "Access Holdings",
                "oil_and_gas_concentration_table": "Yes. Note 5 credit-risk sector lines include Oil And Gas downstream, services and upstream. Extract p.161. Printed number not confirmed. A concentration narrative is on extract p.179.",
                "climate_link": "No wording on that table. The climate sentence is a separate environmental-and-social strategy line on extract p.65.",
                "c5b_score": 0,
            },
            {
                "bank": "Fidelity Bank",
                "oil_and_gas_concentration_table": "A concentration-by-sector narrative is on extract p.192. An Oil and Gas row (11 projects) is in a project-finance table on extract p.105, not the loan-book note.",
                "climate_link": "Yes, but not on the loan-book table. Extract p.107 names oil and gas among heightened ESG-risk sectors in the credit discussion. That sentence is why C5b is 2.",
                "c5b_score": 2,
            },
            {
                "bank": "Zenith Bank",
                "oil_and_gas_concentration_table": "Yes. An Oil and gas line with gross amounts is on extract p.205. Printed number not confirmed.",
                "climate_link": "The climate link used for the score is on printed p.93, not on the p.205 table: high-carbon and energy-dependent sectors, and high-carbon sectors including oil and gas.",
                "c5b_score": 2,
            },
            {
                "bank": "GTCO",
                "oil_and_gas_concentration_table": "Yes. An Oil & gas column appears in the sector classification tables on extract pp.171-173. Printed numbers not confirmed.",
                "climate_link": "No climate wording on those tables. Extract p.222 discusses oil-and-gas sector performance and the exchange rate as sensitivities, without a climate link.",
                "c5b_score": 0,
            },
            {
                "bank": "UBA",
                "oil_and_gas_concentration_table": "Yes. The concentration narrative is on extract p.123. Oil and Gas is a column in the sector table on extract pp.125-127.",
                "climate_link": "Not on the note table. Extract p.31, in the sustainability narrative, says the bank tracks exposure to transition-risk sectors, including Oil and Gas.",
                "c5b_score": 0,
            },
            {
                "bank": "Stanbic IBTC",
                "oil_and_gas_concentration_table": "Yes in the NGX financial statements: Oil & gas on extract p.92, Oil and Gas on extract p.95, and Mining/oil and gas on extract p.173.",
                "climate_link": "No climate or transition wording on those lines in the NGX file. The full annual report was not coded.",
                "c5b_score": 0,
            },
        ]
    )
    banks.to_csv(V2 / "bank_c5b_check.csv", index=False)

    adopter = pd.read_csv(TABLES / "table_rq3_adopter_comparison.csv")
    sector = pd.read_csv(TABLES / "table_rq2_sector_comparison.csv")
    ind = pd.read_csv(TABLES / "table_rq1_indicator_summary.csv")
    tiers = pd.read_csv(TABLES / "table_rq1_tier_distribution.csv")
    robust = pd.read_csv(TABLES / "table_robustness_correlations.csv")
    stats = {
        "source": "Script output after the v2 corrections. p-values are indicative at N=14.",
        "tier_counts_all_firms": tiers[tiers["sector"] == "All"].to_dict(orient="records"),
        "indicators": ind.to_dict(orient="records"),
        "sectors": sector.to_dict(orient="records"),
        "mann_whitney": adopter.to_dict(orient="records"),
        "rank_biserial_note": (
            "The script uses r = 1 - 2U/(n1*n2). "
            "The sign that is positive when the first-named group ranks higher is the negative of that figure: "
            "Panel A 0.650, Panel B 0.562. Stanbic remains in the adopter group."
        ),
        "spearman": {
            "sr_risks_vs_ci": {"n": 14, "rho": 0.434, "p_indicative": 0.1209},
            "ln_assets_vs_ci_13_firms": robust[robust["pair"] == "CI_vs_ln_total_assets"].to_dict(orient="records"),
            "ln_assets_vs_ci_14_firms": "NOT FOUND. No sourced Central Bank of Nigeria closing rate on 31 March 2026.",
            "log_market_cap": "NOT FOUND. Market capitalisation is sourced only for Dangote Cement and BUA Cement.",
            "whole_report_hits_vs_ci": robust[robust["pair"] == "CI_vs_total_ar_hits"].to_dict(orient="records"),
            "fs_only_hits_vs_ci": "NOT COMPUTED. Statement boundaries could not be cut cleanly.",
        },
        "recode_agreement": "NOT COMPUTED. The five-firm recode is due on or after 9 December 2026.",
        "kappa": "NOT COMPUTED.",
    }
    (V2 / "stats_v2.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")

    for path in FIG.glob("fig*.*"):
        shutil.copy2(path, V2 / "figures" / path.name)
    print("wrote", V2)


if __name__ == "__main__":
    main()
