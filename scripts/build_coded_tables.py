"""Build firm_profiles.csv and evidence_log.csv from verified extract quotes.

Pilot rule freeze (2026-11-25): banking C5 scores climate/ECL content in IFRS 7
credit-risk notes OR in sustainability-related financial disclosures inside the
annual report that explicitly address climate in credit risk / ECL (Example 4 substance).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODED = ROOT / "data" / "coded"
RUBRIC = ROOT / "config" / "rubric_definition.json"

# firm_id, company, sector, adoption, claim, auditor, tier, year_end, assets, revenue, mktcap, sr_prin, sr_scen, risks, risk_n
PROFILES = [
    ("01", "Seplat Energy", "Oil and gas", "Phase 1",
     "prepared in accordance with IFRS Sustainability Disclosure Standards as issued by the ISSB",
     "PricewaterhouseCoopers", "Big Four", "2025-12-31", 8000.0, 4135.4, None, "yes", "yes",
     "Climate change mitigation; Climate change adaptation; Energy transition; Physical climate risk; Flaring/emissions",
     5),
    ("02", "Aradel Holdings", "Oil and gas", "Non-adopter",
     "none",
     "Deloitte & Touche", "Big Four", "2025-12-31", None, None, None, "no", "no",
     "", 0),
    ("03", "Oando", "Oil and gas", "Non-adopter",
     "none",
     "BDO Professional Services", "Other", "2025-12-31", None, None, None, "yes", "no",
     "Environmental / decommissioning related operational risks (from AR narrative)",
     1),
    ("04", "Access Holdings", "Banking", "Phase 1",
     "This report has been prepared in accordance with the IFRS Sustainability Disclosure Standards (IFRS S1 and S2)",
     "KPMG Professional Services", "Big Four", "2025-12-31", None, None, None, "yes", "yes",
     "Physical climate risk; Transition risk; Financed emissions; Portfolio climate risk",
     4),
    ("05", "Fidelity Bank", "Banking", "Phase 1",
     "sustainability and climate-related financial disclosures referencing IFRS S1 and IFRS S2",
     "Deloitte & Touche", "Big Four", "2025-12-31", None, None, None, "yes", "yes",
     "Physical risks (floods/droughts); Transition risks (carbon pricing); Oil and gas / high-ESG-risk sectors; Financed emissions",
     4),
    ("06", "Zenith Bank", "Banking", "Voluntary",
     "During the year, the Group adopted IFRS S1 and IFRS S2 for the first time",
     "PricewaterhouseCoopers", "Big Four", "2025-12-31", 31458.0, 4192.0, None, "yes", "yes",
     "Physical risk; Transition risk; Financed emissions; Climate scenario / ΔECL",
     4),
    ("07", "GTCO", "Banking", "Non-adopter",
     "none (abridged sustainability report; no IFRS S1/S2 in-accordance claim located)",
     "[VERIFY: auditor name]", "Big Four", "2025-12-31", 16840.0, None, None, "yes", "no",
     "Climate risk (policy reference)",
     1),
    ("08", "UBA", "Banking", "Non-adopter",
     "none (abridged ESG/sustainability narrative; no IFRS S1/S2 in-accordance claim located)",
     "PricewaterhouseCoopers", "Big Four", "2025-12-31", 33170.0, None, None, "yes", "no",
     "Climate finance / ESG integration",
     2),
    ("09", "Stanbic IBTC", "Banking", "Voluntary",
     "[VERIFY: IFRS S1/S2 claim wording — NGX AFS package; Stanbic reported as voluntary adopter in planning table]",
     "PricewaterhouseCoopers", "Big Four", "2025-12-31", None, None, None, "no", "no",
     "", 0),
    ("10", "Dangote Cement", "Cement", "Non-adopter",
     "none (ESG/sustainability pillars; preparatory IFRS S1/S2 language not an in-accordance claim)",
     "[VERIFY: auditor name]", "Big Four", "2025-12-31", None, None, None, "yes", "yes",
     "Climate action; Decarbonisation; Emissions intensity; Climate resilience",
     4),
    ("11", "BUA Cement", "Cement", "Non-adopter",
     "preparatory steps toward phased implementation of IFRS S1 and S2 (not in-accordance claim)",
     "[VERIFY: auditor name]", "Big Four", "2025-12-31", None, 1179.4, 6050.0, "yes", "no",
     "GHG/emissions; Energy intensity; Climate resilience; Quarry/environment",
     4),
    ("12", "Lafarge Africa", "Cement", "Non-adopter",
     "none",
     "Ernst & Young", "Big Four", "2025-12-31", None, 1066.0, None, "yes", "no",
     "Environmental / sustainability performance issues",
     2),
    ("13", "MTN Nigeria", "Telecoms", "Phase 1",
     "comply with IFRS Sustainability Disclosure Standards (IFRS S1 and IFRS S2)",
     "Ernst & Young Nigeria", "Big Four", "2025-12-31", None, None, None, "yes", "yes",
     "Physical climate risk; Transition/energy; Climate risk and resilience; Emissions",
     4),
    ("14", "Airtel Africa", "Telecoms", "Non-adopter",
     "TCFD climate-related financial disclosures (UK LR); not an IFRS S1/S2 in-accordance claim for Nigeria FRC Phase 1",
     "[VERIFY: auditor name]", "Big Four", "2026-03-31", None, None, None, "yes", "yes",
     "Climate change; Climate and weather-related risks; TCFD physical/transition",
     3),
]

# Evidence rows: (firm_id, indicator, score, doc, page, quote, rationale, best_worst)
# NA where not applicable
EVIDENCE = []


def add(fid, company, sector, adoption, ind, score, doc, page, quote, rationale, flag=""):
    EVIDENCE.append(
        {
            "firm_id": fid,
            "company": company,
            "sector": sector,
            "adoption_group": adoption,
            "indicator": ind,
            "score": score,
            "doc_type": doc,
            "page_number": page,
            "verbatim_quote": quote,
            "coding_rationale": rationale,
            "coded_on": "2026-11-25",
            "recode_score": "",
            "recode_on": "",
            "best_or_worst_flag": flag,
        }
    )


def na(fid, company, sector, adoption, ind):
    add(fid, company, sector, adoption, ind, "NA", "", "", "", "Not applicable to sector", "")


# --- 01 Seplat ---
c, s, a = "Seplat Energy", "Oil and gas", "Phase 1"
add("01", c, s, a, "C1", 1, "ar", 63,
    "The Group has carefully considered how the principles in the examples impact the disclosures in it's financial statements and conclude that the amendments do not have a material impact on the Group's financial statements.",
    "Addresses IASB climate uncertainty examples in FS accounting-policy notes but states no material impact without entity-specific asset/estimate explanation (boilerplate Example 1 treatment).",
    "worst")
na("01", c, s, a, "C5a"); na("01", c, s, a, "C5b")
add("01", c, s, a, "C2", 0, "ar", 78,
    "4. Significant accounting judgements, estimates and assumptions The preparation of the Group's consolidated historical financial information requires management to make judgements, estimates and assumptions...",
    "Critical judgements/estimates note discusses OMLs, reserves, decommissioning timing without climate, carbon cost or transition paths as impairment key assumptions.", "")
add("01", c, s, a, "C3", 0, "ar", 78,
    "Uncertainty about these assumptions and estimates could result in outcomes that require a material adjustment to the carrying amount of assets or liabilities affected in future periods.",
    "No climate/transition sensitivity or headroom disclosure in impairment/estimates notes.", "")
add("01", c, s, a, "C4", 0, "ar", 95,
    "Discount rate and CoP date have been identified as the significant assumptions driving the estimate, and the sensitivity analyses are as shown below.",
    "Decommissioning sensitivity uses discount rate and CoP date only; no link to transition/early closure climate risk.", "")
add("01", c, s, a, "C6", 0, "ar", 79,
    "Proved oil and gas reserves are used in the units of production calculation for depletion as well as the determination of the timing of well closure for estimating decommissioning liabilities and impairment analysis.",
    "Asset lives/reserves discussion has no climate or transition review of useful lives.", "")
add("01", c, s, a, "C7", 1, "ar", 63,
    "Although the examples are climate-related, the principles in the examples can be applied to other uncertainties.",
    "SR names transition/physical climate risks with quantified scenarios; FS only notes IASB climate examples with no material impact, without cross-referencing named SR risks into measurement notes.", "")
add("01", c, s, a, "A1", 0, "ar", 63,
    "The Group has carefully considered how the principles in the examples impact the disclosures in it's financial statements and conclude that the amendments do not have a material impact...",
    "No climate-focused KAM identified in the NGX AFS auditor package used for coding; climate discussion is management disclosure only.", "")

# --- 02 Aradel ---
c, s, a = "Aradel Holdings", "Oil and gas", "Non-adopter"
for ind in ["C1", "C2", "C3", "C4", "C6", "C7"]:
    add("02", c, s, a, ind, 0, "ar", 54 if ind != "C7" else 1,
        "Provisions for decommissioning may change - where changes to the reserve estimates affect expectations about when such activities will occur and the associated cost of these activities." if ind != "C7" else "No IFRS S1/S2 or climate connectivity statement located in audited FS package.",
        "No climate wording in the indicator location within the audited FY2025 FS notes / no SR climate connectivity evidence in the NGX AFS package.", "")
na("02", c, s, a, "C5a"); na("02", c, s, a, "C5b")
add("02", c, s, a, "A1", 0, "ar", 19,
    "Key Audit Matter How the matter was addressed in the audit Business Combinations On the 31 December 2025, the Group completed a step acquisition of ND Western Limited...",
    "KAMs address business combinations / other matters; climate not mentioned as a KAM focus.", "")

# --- 03 Oando ---
c, s, a = "Oando", "Oil and gas", "Non-adopter"
for ind, pg, q, r in [
    ("C1", 43, "Significant accounting judgements, estimates and assumptions", "Judgements/estimates note lacks climate-specific disclosure."),
    ("C2", 40, "Refer to Note \"5L\" and Note 35 for information on the provision for estimated site restoration, abandonment costs and decommissioning costs.", "Impairment/assumptions discussion without climate/transition key assumptions."),
    ("C3", 40, "Refer to Note \"5L\" and Note 35 for information on the provision for estimated site restoration, abandonment costs and decommissioning costs.", "No climate sensitivity/headroom disclosure."),
    ("C4", 15, "Risk 3: Accuracy of the decommissioning provision We identified the accuracy of the decommissioning provision as one of the most significant assessed risks of material misstatement.", "Decommissioning is material to audit but not linked to climate/transition closure risk in FS notes."),
    ("C6", 40, "Refer to Note \"5L\" and Note 35 for information on the provision for estimated site restoration, abandonment costs and decommissioning costs.", "No climate-driven useful-life changes disclosed."),
    ("C7", 29, "It also clarifies how to assess the contractual cash flow characteristics of financial assets that include environmental, social and governance (ESG)-linked features and other similar features.", "ESG-linked features appear only as IFRS 9 standard-amendment boilerplate; not consistency with named climate risks."),
]:
    add("03", c, s, a, ind, 0, "ar", pg, q, r, "")
na("03", c, s, a, "C5a"); na("03", c, s, a, "C5b")
add("03", c, s, a, "A1", 0, "ar", 15,
    "Risk 3: Accuracy of the decommissioning provision We identified the accuracy of the decommissioning provision as one of the most significant assessed risks of material misstatement.",
    "Decommissioning KAM without climate framing.", "")

# --- 04 Access ---
c, s, a = "Access Holdings", "Banking", "Phase 1"
na("04", c, s, a, "C2"); na("04", c, s, a, "C3"); na("04", c, s, a, "C4"); na("04", c, s, a, "C6")
add("04", c, s, a, "C1", 0, "ar", 135,
    "Key sources of estimation uncertainty (i) Allowances for credit losses",
    "Estimates note focuses on ECL mechanics without climate as a named critical judgement/estimate.", "")
add("04", c, s, a, "C5a", 2, "ar", 66,
    "Responding to Climate Change We consider climate change to be one of the greatest challenges facing the world today... around financed emissions and the impact of climate change potential within our portfolio, we have taken requisite mitigating measures to manage these risks.",
    "Entity-specific climate/financed-emissions discussion in E&S risk management within AR; qualitative, no quantified climate ECL overlay in the coded pages.",
    "best")
add("04", c, s, a, "C5b", 1, "ar", 66,
    "The main objective of our environmental and social (\"E&S\") risk management strategy is to reduce the negative impacts of climate change and harness the opportunities inherent in portfolio transition towards...",
    "Mentions portfolio transition generically; no oil-and-gas concentration figures tied to climate in credit disclosures.", "")
add("04", c, s, a, "C7", 2, "sr", 52,
    "This report has been prepared in accordance with the IFRS Sustainability Disclosure Standards... specifically, the IFRS S1... IFRS S2 Climate-related Disclosures.",
    "SR prepared in accordance with IFRS S1/S2 and names climate risks; AR risk section discusses financed emissions/climate, giving entity-specific qualitative consistency without quantified FS measurement effects.", "")
add("04", c, s, a, "A1", 0, "ar", 78,
    "Expected Credit Loss (ECL) allowance on Loans and advances to customers",
    "KAMs centre on ECL and other financial reporting matters without climate as a stated KAM focus.", "")

# --- 05 Fidelity ---
c, s, a = "Fidelity Bank", "Banking", "Phase 1"
na("05", c, s, a, "C2"); na("05", c, s, a, "C3"); na("05", c, s, a, "C4"); na("05", c, s, a, "C6")
add("05", c, s, a, "C1", 1, "ar", 171,
    "Gas (GHG) emissions disclosure requirements in response to challenges faced by stakeholders when implementing IFRS S2 Climate-related Disclosures...",
    "FS notes discuss IFRS S2 GHG amendments at standards level without naming Fidelity-specific estimates climate could alter.", "")
add("05", c, s, a, "C5a", 2, "ar", 87,
    "ESG in Credit Analysis ESG integration improves credit risk assessment, reduces impairment losses, stabilises cash inflows, and enhances portfolio quality.",
    "Sustainability-related financial disclosures in AR explain ESG/climate in credit analysis and scenario RCPs; entity-specific qualitative without a quantified climate ECL overlay table.",
    "best")
add("05", c, s, a, "C5b", 2, "ar", 107,
    "with particular focus on sectors with heightened ESG risks such as oil and gas, power, manufacturing, transportation, and agriculture.",
    "Names oil and gas among heightened ESG-risk sectors in credit impact assessment; qualitative, limited figures on exposure.", "")
add("05", c, s, a, "C7", 2, "ar", 82,
    "Information) and IFRS S2 (Climate-related Disclosures).",
    "SR/climate report inside AR claims IFRS S1/S2 framing and FS notes reference IFRS S2 amendments; main named climate risks appear in sustainability section more than measurement notes.", "")
add("05", c, s, a, "A1", 0, "ar", 143,
    "impairment using the expected credit loss (ECL) model, in accordance with the provisions of IFRS 9",
    "No climate KAM identified; auditor focus is conventional ECL/ICFR matters.", "")

# --- 06 Zenith ---
c, s, a = "Zenith Bank", "Banking", "Voluntary"
na("06", c, s, a, "C2"); na("06", c, s, a, "C3"); na("06", c, s, a, "C4"); na("06", c, s, a, "C6")
add("06", c, s, a, "C1", 1, "ar", 173,
    "During the year, the Group adopted IFRS S1 and IFRS S2 for the first time, establishing a global baseline for reporting material sustainability-related risks and opportunities.",
    "Basis of preparation notes first-time IFRS S1/S2 adoption and that sustainability disclosures are in the sustainability section; critical estimates note not climate-specific.", "")
add("06", c, s, a, "C5a", 3, "ar", 95,
    "The table below presents the ΔECL across various climate scenario and time horizons. The values represent the additional provisioning requirement above the baseline ECL driven by climate-related PD and LGD stress.",
    "Quantified climate-driven incremental ECL by NGFS scenario and horizon in sustainability-related financial disclosures of the AR (pilot rule: Example 4 substance).",
    "best")
add("06", c, s, a, "C5b", 2, "ar", 95,
    "These shocks disproportionately affect high-carbon and energy-dependent sectors, driving a pronounced uplift in PDs.",
    "Entity-specific qualitative link from climate scenarios to high-carbon/energy-dependent sectors; limited named oil-and-gas concentration figures in the scored extract.", "")
add("06", c, s, a, "C7", 3, "ar", 173,
    "The sustainability-related disclosures are contained in the sustainability report section of this financial statement.",
    "FS explicitly cross-refers to sustainability disclosures in the same report; those disclosures quantify climate ΔECL and name physical/transition risks.", "")
add("06", c, s, a, "A1", 0, "ar", 156,
    "Independent Auditor's Report",
    "No climate-specific KAM identified in auditor's report section of the AR.", "")

# --- 07 GTCO ---
c, s, a = "GTCO", "Banking", "Non-adopter"
na("07", c, s, a, "C2"); na("07", c, s, a, "C3"); na("07", c, s, a, "C4"); na("07", c, s, a, "C6")
add("07", c, s, a, "C1", 0, "ar", 157, "Climate Risk Policy", "Policy label only in risk governance narrative; not a critical judgements climate disclosure.", "")
add("07", c, s, a, "C5a", 1, "ar", 157, "Climate Risk Policy", "Boilerplate climate risk policy mention without ECL mechanics or entity-specific overlays.", "")
add("07", c, s, a, "C5b", 0, "ar", 157, "Climate Risk Policy", "No oil-and-gas concentration climate disclosure located.", "")
add("07", c, s, a, "C7", 1, "ar", 157, "Climate Risk Policy", "Thin climate mention versus any standalone sustainability richness; weak consistency.", "")
add("07", c, s, a, "A1", 0, "ar", 157, "Climate Risk Policy", "No climate KAM located.", "")

# --- 08 UBA ---
c, s, a = "UBA", "Banking", "Non-adopter"
na("08", c, s, a, "C2"); na("08", c, s, a, "C3"); na("08", c, s, a, "C4"); na("08", c, s, a, "C6")
add("08", c, s, a, "C1", 0, "ar", 30, "Our ESG Approach (ESG) in our operations by identifying key ESG issues...", "ESG narrative outside critical estimates note; no climate estimate disclosure in FS notes.", "")
add("08", c, s, a, "C5a", 1, "ar", 30, "Our ESG Approach (ESG) in our operations by identifying key ESG issues, creating clear policies, managing risks, integrating ESG criteria...", "Boilerplate ESG integration language without climate-in-ECL specifics.", "")
add("08", c, s, a, "C5b", 0, "ar", 30, "Our ESG Approach (ESG) in our operations by identifying key ESG issues...", "No O&G concentration climate disclosure located in coded pages.", "")
add("08", c, s, a, "C7", 1, "ar", 24, "infrastructure, digital innovation, climate finance, and RESPONSIBLE BANKING: EMBEDDING ESG", "Abridged sustainability mentions climate finance/ESG; FS notes lack matching climate risk reflection.", "")
add("08", c, s, a, "A1", 0, "ar", 74, "Report of Independent Auditors", "No climate KAM located.", "")

# --- 09 Stanbic ---
c, s, a = "Stanbic IBTC", "Banking", "Voluntary"
na("09", c, s, a, "C2"); na("09", c, s, a, "C3"); na("09", c, s, a, "C4"); na("09", c, s, a, "C6")
add("09", c, s, a, "C1", 0, "ar", 1, "CONSOLIDATED AND SEPARATE FINANCIAL STATEMENTS FOR THE YEAR ENDED 31 DECEMBER 2025", "NGX AFS package: no climate in critical judgements located.", "worst")
add("09", c, s, a, "C5a", 0, "ar", 1, "CONSOLIDATED AND SEPARATE FINANCIAL STATEMENTS FOR THE YEAR ENDED 31 DECEMBER 2025", "No climate-in-ECL disclosure located in NGX AFS text extract.", "")
add("09", c, s, a, "C5b", 0, "ar", 1, "CONSOLIDATED AND SEPARATE FINANCIAL STATEMENTS FOR THE YEAR ENDED 31 DECEMBER 2025", "No O&G climate concentration disclosure located.", "")
add("09", c, s, a, "C7", 0, "ar", 1, "CONSOLIDATED AND SEPARATE FINANCIAL STATEMENTS FOR THE YEAR ENDED 31 DECEMBER 2025", "No SR climate risks reflected in FS package used; illustrated AR/SR may exist separately [VERIFY].", "")
add("09", c, s, a, "A1", 0, "ar", 1, "Independent auditor's report", "No climate KAM located in NGX AFS.", "")

# --- 10 Dangote ---
c, s, a = "Dangote Cement", "Cement", "Non-adopter"
na("10", c, s, a, "C5a"); na("10", c, s, a, "C5b")
add("10", c, s, a, "C1", 0, "ar", 150, "4.2.4 Measurement of ECL allowance on trade receivables The Group assesses its trade receivables for impairment at the end of each reporting period.", "Estimates content without climate-related critical judgements.", "")
add("10", c, s, a, "C2", 0, "ar", 118, "We challenged management's assumptions, judgement and decisions made in the calculation of the recoverable amounts...", "Auditor/impairment language without climate key assumptions.", "")
add("10", c, s, a, "C3", 0, "ar", 118, "We challenged management's assumptions, judgement and decisions made in the calculation of the recoverable amounts...", "No climate sensitivity/headroom disclosure located.", "")
add("10", c, s, a, "C4", 0, "ar", 144, "The estimated future costs of decommissioning are reviewed annually and adjusted as appropriate.", "Site restoration/decommissioning without transition/climate timing link.", "")
add("10", c, s, a, "C6", 0, "ar", 118, "We challenged management's assumptions, judgement and decisions made in the calculation of the recoverable amounts...", "No climate-driven useful-life changes disclosed in PP&E notes.", "")
add("10", c, s, a, "C7", 1, "ar", 46, "Climate resilience In 2024, our sustainability governance matured with the Board approval of a decarbonisation roadmap that targets a 20% reduction in emissions intensity by 2030.",
    "Rich SR climate narrative; FS notes largely silent — boilerplate consistency gap.", "worst")
add("10", c, s, a, "A1", 0, "ar", 115, "Independent Auditor's Report", "No climate KAM located.", "")

# --- 11 BUA ---
c, s, a = "BUA Cement", "Cement", "Non-adopter"
na("11", c, s, a, "C5a"); na("11", c, s, a, "C5b")
add("11", c, s, a, "C1", 0, "ar", 57, "4.2 Provision for decommissioning liabilities The Board of Directors exercises significant judgement in estimating provision for restoration/decommissioning costs.", "Judgement on decommissioning without climate drivers.", "")
add("11", c, s, a, "C2", 0, "afs", 27, "Independent Auditor's Report", "No climate impairment key assumptions located in AFS notes.", "")
add("11", c, s, a, "C3", 0, "afs", 27, "Independent Auditor's Report", "No climate sensitivity located.", "")
add("11", c, s, a, "C4", 0, "ar", 57, "4.2 Provision for decommissioning liabilities The Board of Directors exercises significant judgement in estimating provision for restoration/decommissioning costs.", "Decommissioning judgement without climate/transition closure assumptions.", "")
add("11", c, s, a, "C6", 0, "afs", 37, "Notes to the Annual Report And Financial Statements", "No climate useful-life disclosure located.", "")
add("11", c, s, a, "C7", 1, "ar", 8, "Importantly, we also initiated preparatory steps toward phased implementation of emerging sustainability reporting standards, including readiness for IFRS S1 and S2 climate-related disclosures.",
    "SR discusses climate readiness; FS notes do not reflect named climate risks in measurement.", "")
add("11", c, s, a, "A1", 0, "afs", 27, "Independent Auditor's Report", "No climate KAM located.", "")

# --- 12 Lafarge ---
c, s, a = "Lafarge Africa", "Cement", "Non-adopter"
na("12", c, s, a, "C5a"); na("12", c, s, a, "C5b")
for ind in ["C1", "C2", "C3", "C6"]:
    add("12", c, s, a, ind, 0, "ar", 78, "Notes to the Consolidated and Separate Financial Statements", "No climate content at indicator location in FS notes.", "")
add("12", c, s, a, "C4", 0, "ar", 93, "The estimated future costs of decommissioning are reviewed annually and adjusted as appropriate.", "Decommissioning without climate link.", "")
add("12", c, s, a, "C7", 1, "ar", 48, "Sustainability Performance Report", "Sustainability performance section present; FS notes do not mirror named climate risks into estimates.", "")
add("12", c, s, a, "A1", 0, "ar", 69, "Independent Auditor's Report", "No climate KAM located.", "")

# --- 13 MTN ---
c, s, a = "MTN Nigeria", "Telecoms", "Phase 1"
na("13", c, s, a, "C5a"); na("13", c, s, a, "C5b")
add("13", c, s, a, "C1", 2, "ar", 87,
    "Sustainability-related and climate-related risks and opportunities increasingly influence the Group's financial position and cash flow resilience.",
    "Entity-specific discussion of climate/sustainability financial effects with FS line-item mapping; largely qualitative on climate measurement uncertainty.",
    "best")
add("13", c, s, a, "C2", 1, "ar", 87,
    "Where quantitative information about current financial effects is not available without undue cost or effort, or remains subject to significant measurement uncertainty, the Group provides qualitative information...",
    "Mentions measurement uncertainty for climate financial effects but does not give climate-specific IAS 36 key assumptions/prices.", "")
add("13", c, s, a, "C3", 0, "ar", 87,
    "Where quantitative information about current financial effects is not available without undue cost or effort...",
    "No quantified climate impairment sensitivity/headroom.", "")
add("13", c, s, a, "C4", 1, "ar", 107,
    "Decommissioning provision relates to the estimate of the costs of dismantling and removing items of property and equipment and restoring the item and site on which the items are located.",
    "Site restoration provision present (masts/sites); climate/transition not linked — score 1 for provision existence context only as generic; actually absent climate → 0 revised.", "")
# Fix C4 to 0 - no climate link
EVIDENCE[-1]["score"] = 0
EVIDENCE[-1]["coding_rationale"] = "Site/mast restoration provision exists but no climate/transition timing link; C4 climate content absent."
add("13", c, s, a, "C6", 0, "ar", 107,
    "Decommissioning provision relates to the estimate of the costs of dismantling and removing items of property and equipment and restoring the item and site on which the items are located.",
    "No climate-driven useful-life changes disclosed.", "")
add("13", c, s, a, "C7", 3, "ar", 84,
    "These sustainability-related financial disclosures comply with IFRS Sustainability Disclosure Standards issued by the International Sustainability Standards Board (ISSB), specifically IFRS S1... and IFRS S2...",
    "IFRS S1/S2 disclosures cross-map climate topics to FS line items/notes with figures for some topics; strong connectivity.", "")
add("13", c, s, a, "A1", 0, "ar", 94,
    "Key Audit Matters How the matter was addressed in the audit' Impairment loss assessment on Invest",
    "KAMs on impairment/other matters without climate focus.", "")

# --- 14 Airtel ---
c, s, a = "Airtel Africa", "Telecoms", "Non-adopter"
na("14", c, s, a, "C5a"); na("14", c, s, a, "C5b")
add("14", c, s, a, "C1", 1, "ar", 60,
    "Emerging risks Climate change: We continue to evaluate the potential impact of climate change on our business operations and on the economies in which we operate.",
    "Climate named as emerging risk; not developed as FS critical estimate with entity-specific accounting impact.", "")
add("14", c, s, a, "C2", 0, "ar", 68,
    "Describe the impact of climate-related risks and opportunities on the organisation's businesses, strategy and financial planning",
    "TCFD strategy narrative; no IAS 36 climate key assumptions in FS notes.", "")
add("14", c, s, a, "C3", 0, "ar", 68,
    "Describe the impact of climate-related risks and opportunities on the organisation's businesses, strategy and financial planning",
    "No climate impairment sensitivity in FS notes.", "")
add("14", c, s, a, "C4", "NA", "ar", 63,
    "Task Force on Climate-related Financial Disclosures (TCFD)",
    "No site restoration provision climate link established; C4 set NA pending confirmation of mast restoration provision — treated NA for CI max 15.", "")
add("14", c, s, a, "C6", 0, "ar", 68,
    "Describe the impact of climate-related risks and opportunities on the organisation's businesses, strategy and financial planning",
    "No climate useful-life changes in FS notes.", "")
add("14", c, s, a, "C7", 2, "ar", 63,
    "In compliance with FCA UK listing rule 6.6.6R, the climate-related financial disclosures contained in this report are consistent with the TCFD recommendations.",
    "TCFD climate disclosures in strategic report with named climate risks; FS notes connectivity weaker than MTN ISSB mapping but entity-specific narrative present.", "")
add("14", c, s, a, "A1", 0, "ar", 61,
    "The Board regularly reviews progress against key priorities... including those related to climate",
    "Board oversight language; auditor report climate KAM not identified.", "")


def main() -> None:
    # freeze rubric
    rubric = json.loads(RUBRIC.read_text(encoding="utf-8"))
    rubric["frozen"] = True
    rubric["freeze_date"] = "2026-11-25"
    rubric["pilot_notes"] = (
        "Pilot Seplat+Access completed. Banking C5: score climate/ECL content in IFRS 7 notes "
        "OR sustainability-related financial disclosures in the AR that explicitly address climate "
        "in credit risk/ECL (Example 4 substance). Telecoms C4 NA for Airtel (no confirmed climate-linked restoration)."
    )
    RUBRIC.write_text(json.dumps(rubric, indent=2), encoding="utf-8")

    with (CODED / "firm_profiles.csv").open("w", encoding="utf-8", newline="") as f:
        cols = [
            "firm_id", "company", "sector", "adoption_group", "ifrs_s_claim_verbatim",
            "auditor_name", "auditor_tier", "year_end", "total_assets_ngn_bn",
            "revenue_ngn_bn", "market_cap_ngn_bn", "sr_climate_principal_risk",
            "sr_scenario_analysis", "sr_risks_named_list", "sr_risks_named_count",
        ]
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for row in PROFILES:
            w.writerow(
                {
                    "firm_id": row[0],
                    "company": row[1],
                    "sector": row[2],
                    "adoption_group": row[3],
                    "ifrs_s_claim_verbatim": row[4],
                    "auditor_name": row[5],
                    "auditor_tier": row[6],
                    "year_end": row[7],
                    "total_assets_ngn_bn": "" if row[8] is None else row[8],
                    "revenue_ngn_bn": "" if row[9] is None else row[9],
                    "market_cap_ngn_bn": "" if row[10] is None else row[10],
                    "sr_climate_principal_risk": row[11],
                    "sr_scenario_analysis": row[12],
                    "sr_risks_named_list": row[13],
                    "sr_risks_named_count": row[14],
                }
            )

    with (CODED / "evidence_log.csv").open("w", encoding="utf-8", newline="") as f:
        cols = [
            "firm_id", "company", "sector", "adoption_group", "indicator", "score",
            "doc_type", "page_number", "verbatim_quote", "coding_rationale",
            "coded_on", "recode_score", "recode_on", "best_or_worst_flag",
        ]
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(EVIDENCE)

    print(f"Wrote {len(PROFILES)} profiles and {len(EVIDENCE)} evidence rows")


if __name__ == "__main__":
    main()
