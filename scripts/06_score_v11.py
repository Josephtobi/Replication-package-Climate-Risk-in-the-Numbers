"""Recorded version 1.1 scores for all 14 firms.

These judgements were applied by an AI reviewer from the extracted reports
under config/codebook_v1.1.md. The script stores those scores and recomputes
the tests. It does not read a PDF and it does not change the version 1.0
score column. C1 to C6 count only inside the audited financial statements.
C7 may use a link from either place.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "v11"
PROF = ROOT / "data" / "coded" / "firm_profiles.csv"
HITS = ROOT / "outputs" / "tables" / "table_keyword_hits.csv"

# score, extract page, quote, rationale. NA rows omit quote.
ROWS = [
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "C1", "1", "63", "The Group has carefully considered how the principles in the examples impact the disclosures in it's financial statements and conclude that the amendments do not have a material impact on the Group's financial statements.", "Notes conclude the IASB climate examples have no material effect. Printed p.62."),
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "C2", "0", "71", "", "Impairment note checked. Commodity prices are not linked to transition."),
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "C3", "0", "79", "", "No climate sensitivity in the estimates note."),
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "C4", "0", "56", "", "A decommissioning provision is recorded. The note has no climate link."),
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "C5a", "NA", "", "", "Not a bank."),
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "C5b", "NA", "", "", "Not a bank."),
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "C6", "0", "79", "", "Useful-life note has no climate review."),
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "C7", "3", "35", "Based on the average production daily production and realized price, this translates to a $3 million (N5 billion) reduction in revenue (Note 9) and $1 million (N 1.5 billion) drop in gross profit for the period.", "Under the heading Climate change adaptation. Temperature-driven corrosion is tied to Note 9 with amounts."),
    ("01", "Seplat Energy", "Oil and gas", "Phase 1", "A1", "0", "", "", "The auditor's report is not in the NGX financial-results extract."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "C1", "0", "18", "", "No climate term in the financial statements, extract pp.18-100."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "C2", "0", "18", "", "No climate term in the financial statements."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "C3", "0", "18", "", "No climate term in the financial statements."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "C4", "0", "45", "", "Decommissioning liability is recorded, with no climate link."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "C5a", "NA", "", "", "Not a bank."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "C5b", "NA", "", "", "Not a bank."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "C6", "0", "18", "", "No climate term in the financial statements."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "C7", "0", "", "", "No climate sentence in this extract, so there is no link to the notes."),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter", "A1", "0", "19", "", "The key audit matter is a business combination. Climate is not mentioned."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "C1", "0", "29", "", "Note 3 describes the IASB examples and does not conclude on their effect on Oando's financial statements."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "C2", "0", "71", "", "Reserve price assumptions are not linked to climate."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "C3", "0", "71", "", "No climate sensitivity."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "C4", "0", "84", "", "Decommissioning provision is recorded, with no climate link."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "C5a", "NA", "", "", "Not a bank."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "C5b", "NA", "", "", "Not a bank."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "C6", "0", "45", "", "Useful-life note has no climate review."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "C7", "0", "40", "", "The annual report names climate risks and does not point them to a note or line item."),
    ("03", "Oando", "Oil and gas", "Non-adopter", "A1", "0", "12", "", "Auditor's report has no climate mention. The decommissioning key audit matter is not framed as climate."),
    ("04", "Access Holdings", "Banking", "Phase 1", "C1", "0", "76", "", "The only climate phrase inside the financial statements is a UK corporate climate responsibility levy in the tax note, extract p.221. That is a tax, not a judgement about climate risk."),
    ("04", "Access Holdings", "Banking", "Phase 1", "C2", "NA", "", "", "Bank."),
    ("04", "Access Holdings", "Banking", "Phase 1", "C3", "NA", "", "", "Bank."),
    ("04", "Access Holdings", "Banking", "Phase 1", "C4", "NA", "", "", "Bank."),
    ("04", "Access Holdings", "Banking", "Phase 1", "C5a", "0", "76", "", "No climate term in the credit-risk notes. Sustainability climate text is outside the financial statements."),
    ("04", "Access Holdings", "Banking", "Phase 1", "C5b", "0", "179", "", "Sector concentration note has no climate wording on the oil-and-gas line."),
    ("04", "Access Holdings", "Banking", "Phase 1", "C6", "NA", "", "", "Bank."),
    ("04", "Access Holdings", "Banking", "Phase 1", "C7", "0", "65", "", "Sustainability climate sentences do not point to a financial-statement note or line item."),
    ("04", "Access Holdings", "Banking", "Phase 1", "A1", "0", "76", "", "Auditor's report has no climate mention."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "C1", "0", "167", "", "Note 2.3 has no climate content. The IFRS S2 passage lists amendments and does not conclude on their effect."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "C2", "NA", "", "", "Bank."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "C3", "NA", "", "", "Bank."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "C4", "NA", "", "", "Bank."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "C5a", "0", "186", "", "The ECL note has no climate content. Climate stress testing is in the sustainability section."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "C5b", "0", "192", "", "The oil-and-gas concentration line has no climate link."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "C6", "NA", "", "", "Bank."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "C7", "1", "82", "IFRS Sustainability Disclosure Standards: We have applied IFRS S1 (General Requirements for Disclosure of Sustainability-related Financial Information) and IFRS S2 (Climate-related Disclosures) as issued by the International Sustainability Standards Board (ISSB).", "Adoption statement. It names no climate risk and does not point to a note."),
    ("05", "Fidelity Bank", "Banking", "Phase 1", "A1", "0", "142", "", "Auditor's report does not mention climate."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "C1", "0", "173", "", "The IFRS S1 and S2 sentence is an adoption statement, not a conclusion on climate in the judgements note."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "C2", "NA", "", "", "Bank."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "C3", "NA", "", "", "Bank."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "C4", "NA", "", "", "Bank."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "C5a", "0", "158", "", "No climate term in the notes, extract pp.158-309. The delta-ECL table is on extract p.95, before the auditor's report."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "C5b", "0", "205", "", "The oil-and-gas exposure line in the notes has no climate wording. The high-carbon sentence is on extract p.95."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "C6", "NA", "", "", "Bank."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "C7", "3", "95", "The table below presents the ΔECL across various climate scenario and time horizons. The values represent the additional provisioning requirement above the baseline ECL driven by climate-related PD and LGD stress.", "Orderly, Disorderly and Hothouse scenarios are mapped to incremental ECL amounts. Printed p.93. This is outside the notes, so it scores C7 and not C5a."),
    ("06", "Zenith Bank", "Banking", "Voluntary", "A1", "0", "158", "", "The extracted auditor's report does not mention climate."),
    ("07", "GTCO", "Banking", "Non-adopter", "C1", "0", "230", "", "Judgements note covers ECL and useful lives and does not mention climate."),
    ("07", "GTCO", "Banking", "Non-adopter", "C2", "NA", "", "", "Bank."),
    ("07", "GTCO", "Banking", "Non-adopter", "C3", "NA", "", "", "Bank."),
    ("07", "GTCO", "Banking", "Non-adopter", "C4", "NA", "", "", "Bank."),
    ("07", "GTCO", "Banking", "Non-adopter", "C5a", "0", "157", "", "The only climate phrase in the notes is the title Climate Risk Policy in a list of policies. It does not describe ECL, PD or LGD."),
    ("07", "GTCO", "Banking", "Non-adopter", "C5b", "0", "222", "", "Crude-oil price sensitivity is not a climate link."),
    ("07", "GTCO", "Banking", "Non-adopter", "C6", "NA", "", "", "Bank."),
    ("07", "GTCO", "Banking", "Non-adopter", "C7", "0", "157", "", "Climate Risk Policy is a name in a list of policies. It does not point a climate risk to a note or line item."),
    ("07", "GTCO", "Banking", "Non-adopter", "A1", "0", "118", "", "The readable key audit matter is loan impairment and does not mention climate."),
    ("08", "UBA", "Banking", "Non-adopter", "C1", "0", "82", "", "No climate term in the financial statements, extract pp.76-243."),
    ("08", "UBA", "Banking", "Non-adopter", "C2", "NA", "", "", "Bank."),
    ("08", "UBA", "Banking", "Non-adopter", "C3", "NA", "", "", "Bank."),
    ("08", "UBA", "Banking", "Non-adopter", "C4", "NA", "", "", "Bank."),
    ("08", "UBA", "Banking", "Non-adopter", "C5a", "0", "82", "", "No climate term in the financial statements."),
    ("08", "UBA", "Banking", "Non-adopter", "C5b", "0", "125", "", "The oil-and-gas column has no climate wording."),
    ("08", "UBA", "Banking", "Non-adopter", "C6", "NA", "", "", "Bank."),
    ("08", "UBA", "Banking", "Non-adopter", "C7", "0", "31", "", "Sustainability text on climate finance does not point to a financial-statement note."),
    ("08", "UBA", "Banking", "Non-adopter", "A1", "0", "76", "", "Little auditor text extracted. No climate sentence was found."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "C1", "0", "34", "", "No climate term in the NGX financial statements, extract pp.34-188."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "C2", "NA", "", "", "Bank."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "C3", "NA", "", "", "Bank."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "C4", "NA", "", "", "Bank. A site-restoration line in the notes is not scored for banks."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "C5a", "0", "34", "", "No climate term in the NGX financial statements."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "C5b", "0", "95", "", "Oil-and-gas lines have no climate wording."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "C6", "NA", "", "", "Bank."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "C7", "0", "", "", "The NGX file has no sustainability climate sentence to link."),
    ("09", "Stanbic IBTC", "Banking", "Voluntary", "A1", "0", "34", "", "Auditor's report has no climate mention."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "C1", "0", "149", "", "Judgements note has no climate conclusion."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "C2", "0", "150", "", "Impairment assumptions are discount and growth rates only."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "C3", "0", "150", "", "No climate sensitivity."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "C4", "0", "150", "", "Site-restoration provision is recorded, with no climate link."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "C5a", "NA", "", "", "Not a bank."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "C5b", "NA", "", "", "Not a bank."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "C6", "0", "151", "", "The change in useful lives is not given a climate reason."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "C7", "0", "46", "", "Decarbonisation text does not point to a financial-statement note or line item."),
    ("10", "Dangote Cement", "Cement", "Non-adopter", "A1", "1", "118", "We challenged management's assumptions, judgement and decisions made in the calculation of the recoverable amounts by comparing them with historical performance, industry trends and future projections, considering the uncertainties around macroeconomic factors and climate change.", "Climate is mentioned in passing inside the impairment key audit matter. It is not the subject of the matter."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "C1", "0", "42", "", "No climate term in the financial statements, extract pp.42-69."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "C2", "0", "42", "", "No climate term in the financial statements."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "C3", "0", "42", "", "No climate term in the financial statements."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "C4", "0", "45", "", "Decommissioning liability is recorded, with no climate link."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "C5a", "NA", "", "", "Not a bank."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "C5b", "NA", "", "", "Not a bank."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "C6", "0", "42", "", "No climate term in the financial statements."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "C7", "0", "8", "", "Preparatory IFRS S1 and S2 language does not point to a note or line item."),
    ("11", "BUA Cement", "Cement", "Non-adopter", "A1", "0", "42", "", "No climate sentence extracted from the auditor's report."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "C1", "0", "78", "", "Judgements note has no climate content."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "C2", "0", "96", "", "Impairment note has no climate assumption."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "C3", "0", "97", "", "No climate sensitivity."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "C4", "0", "135", "", "Site restoration provision is recorded, with no climate link."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "C5a", "NA", "", "", "Not a bank."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "C5b", "NA", "", "", "Not a bank."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "C6", "0", "91", "", "Useful-life policy has no climate review."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "C7", "0", "49", "", "Sustainability climate text does not point to a note or line item."),
    ("12", "Lafarge Africa", "Cement", "Non-adopter", "A1", "0", "69", "", "Auditor's report has no climate mention."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "C1", "0", "109", "", "Judgements note has no climate content."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "C2", "0", "120", "", "Goodwill impairment uses market capitalisation and has no climate path."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "C3", "0", "121", "", "Sensitivity is on share price, not climate."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "C4", "0", "107", "", "Network-site decommissioning provision is recorded, with no climate link."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "C5a", "NA", "", "", "Not a bank."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "C5b", "NA", "", "", "Not a bank."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "C6", "0", "103", "", "Useful-life review has no climate reason."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "C7", "3", "87", "The table below links material topics to relevant financial statement line items and note references.", "The same table maps flooding to Note 18 with an N81.0 million impairment, and heat stress to Note 18 and Note 10.1 with amounts. Printed pp.172-173."),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1", "A1", "0", "94", "", "Key audit matters are revenue and subsidiary impairment. Climate is not mentioned."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "C1", "0", "190", "", "Critical estimates note has no climate content."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "C2", "2", "205", "The nominal cash flows used in the impairment tests reflect the Group's current assessment of the impact of climate change and associated commitments the Group has made (refer to climate change disclosures (p63)).", "The impairment note names the Group's own cash flows and does not give a climate figure."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "C3", "2", "205", "Based on the analysis conducted so far, the Group is satisfied that the impact of climate change does not lead to an impairment as of 31 December 2025 and is adequately covered as part of the sensitivities disclosed below.", "Entity-specific statement that climate is covered by the sensitivities. No separate climate amount."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "C4", "0", "213", "", "Asset retirement obligations of $2 million are recorded, with no climate link."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "C5a", "NA", "", "", "Not a bank."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "C5b", "NA", "", "", "Not a bank."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "C6", "0", "184", "", "Useful-life policy has no climate review."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "C7", "3", "205", "The nominal cash flows used in the impairment tests reflect the Group's current assessment of the impact of climate change and associated commitments the Group has made (refer to climate change disclosures (p63)).", "The note points climate change to the climate disclosures and explains why it does not cause an impairment."),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter", "A1", "2", "171", "Management considered the impact of climate change on the impairment review performed on the group's assets. Management disclosed in note 16 that no reasonable possible change in any assumption underpinning the impairment review would lead to an impairment which includes the impact of climate change. We have assessed the appropriateness of this disclosure.", "The auditor assessed climate inside the impairment work. Marked unsure whether this is a key audit matter or a separate section."),
]


def sector_max(sector: str) -> float:
    return 12.0 if sector == "Banking" else 18.0


def tier_of(ci: float) -> str:
    if ci <= 0:
        return "Silent"
    if ci <= 33:
        return "Boilerplate"
    if ci <= 66:
        return "Partial"
    return "Connected"


def rank_biserial(u: float, n1: int, n2: int) -> float:
    return 1 - (2 * u) / (n1 * n2)


def main() -> None:
    evid = pd.DataFrame(
        ROWS,
        columns=["firm_id", "company", "sector", "adoption_group", "indicator", "score", "extract_page", "verbatim_quote", "rationale"],
    )
    inds = ["C1", "C2", "C3", "C4", "C5a", "C5b", "C6", "C7"]
    rows = []
    for fid, g in evid.groupby("firm_id", sort=False):
        scores = {r.indicator: r.score for r in g.itertuples()}
        raw = 0.0
        n3 = 0
        substantive = 0
        for ind in inds:
            val = scores[ind]
            if val == "NA":
                continue
            num = float(val)
            raw += num
            if num == 3:
                n3 += 1
            if num >= 2:
                substantive += 1
        smax = sector_max(g["sector"].iloc[0])
        ci = round(raw / smax * 100, 2)
        rows.append(
            {
                "firm_id": fid,
                "company": g["company"].iloc[0],
                "sector": g["sector"].iloc[0],
                "adoption_group": g["adoption_group"].iloc[0],
                **scores,
                "raw_score": raw,
                "sector_max": smax,
                "connectivity_index": ci,
                "tier": tier_of(ci),
                "count_score_3": n3,
                "fs_substantive": substantive,
            }
        )
    master = pd.DataFrame(rows)
    prof = pd.read_csv(PROF, dtype=str)
    prof["sr_risks"] = pd.to_numeric(prof["sr_risks_named_count"], errors="coerce").fillna(0)
    master = master.merge(prof[["firm_id", "sr_risks", "total_assets_ngn_bn"]], on="firm_id")
    master["gap"] = master["sr_risks"] - master["fs_substantive"]
    master["C7_num"] = pd.to_numeric(master["C7"], errors="coerce").fillna(-1)
    master["A1_num"] = pd.to_numeric(master["A1"], errors="coerce").fillna(-1)
    key = master[["connectivity_index", "C7_num", "count_score_3", "A1_num"]].astype(float)
    master["overall_rank"] = key.apply(tuple, axis=1).rank(method="min", ascending=False).astype(int)
    hits = pd.read_csv(HITS, dtype={"firm_id": str})
    master = master.merge(hits[["firm_id", "total_ar_hits"]], on="firm_id")
    master["assets"] = pd.to_numeric(master["total_assets_ngn_bn"], errors="coerce")

    def mw(a, b):
        u, p = stats.mannwhitneyu(a, b, alternative="two-sided", method="exact")
        return {
            "n1": int(len(a)),
            "n2": int(len(b)),
            "median1": round(float(np.median(a)), 2),
            "median2": round(float(np.median(b)), 2),
            "U": float(u),
            "p": float(p),
            "r_script": round(rank_biserial(float(u), len(a), len(b)), 3),
            "r_positive_when_first_group_higher": round(-rank_biserial(float(u), len(a), len(b)), 3),
        }

    ci = master["connectivity_index"].astype(float)
    phase = master["adoption_group"] == "Phase 1"
    adopter = master["adoption_group"].isin(["Phase 1", "Voluntary"])
    groups = [g["connectivity_index"].astype(float).to_numpy() for _, g in master.groupby("sector")]
    h_stat, p_kw = stats.kruskal(*groups)
    rho_sr, p_sr = stats.spearmanr(master["sr_risks"], ci)
    assets = master.dropna(subset=["assets"])
    rho_a, p_a = stats.spearmanr(np.log(assets["assets"]), assets["connectivity_index"])
    rho_h, p_h = stats.spearmanr(master["total_ar_hits"], ci)
    summary = {
        "kruskal_H": round(float(h_stat), 3),
        "kruskal_p": round(float(p_kw), 4),
        "epsilon_sq": round(float(h_stat) / (len(master) - 1), 3),
        "panel_a_phase1_vs_rest": mw(ci[phase], ci[~phase]),
        "panel_b_adopters_vs_non": mw(ci[adopter], ci[~adopter]),
        "spearman_sr_ci": {"n": 14, "rho": round(float(rho_sr), 3), "p": round(float(p_sr), 4)},
        "spearman_ln_assets_ci": {"n": int(len(assets)), "rho": round(float(rho_a), 3), "p": round(float(p_a), 4)},
        "spearman_hits_ci": {"n": 14, "rho": round(float(rho_h), 3), "p": round(float(p_h), 4)},
        "tiers": master["tier"].value_counts().to_dict(),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    evid.to_csv(OUT / "evidence_v11.csv", index=False)
    master.sort_values("overall_rank").to_csv(OUT / "scores_v11.csv", index=False)
    (OUT / "tests_v11.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(master.sort_values("overall_rank")[["overall_rank", "company", "connectivity_index", "tier", "C7", "A1", "gap"]].to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
