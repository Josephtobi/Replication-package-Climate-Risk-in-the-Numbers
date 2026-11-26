"""Apply the v2 corrections that the extracts support. Does not invent figures."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data" / "coded" / "evidence_log.csv"
PROF = ROOT / "data" / "coded" / "firm_profiles.csv"


def main() -> None:
    with EV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    fields = list(rows[0].keys())
    for extra in ("printed_page", "changed_in_v2"):
        if extra not in fields:
            fields.append(extra)

    for row in rows:
        row["changed_in_v2"] = ""
        page = (row.get("page_number") or "").strip()
        row["printed_page"] = (
            f"PDF p. {page} (printed number not confirmed)" if page else ""
        )
        if row["firm_id"] == "01" and row["indicator"] in {"C1", "C7"}:
            row["printed_page"] = "62"
        if row["firm_id"] == "06" and row["indicator"] in {"C5a", "C5b"}:
            row["printed_page"] = "93"
        if row["firm_id"] == "06" and row["indicator"] == "C7":
            row["page_number"] = "95"
            row["printed_page"] = "93"
            row["verbatim_quote"] = (
                "The table below presents the \u0394ECL across various climate "
                "scenario and time horizons. The values represent the additional "
                "provisioning requirement above the baseline ECL driven by "
                "climate-related PD and LGD stress."
            )
            row["coding_rationale"] = (
                "Score kept at 3. The notes cross-refer to the sustainability "
                "section (extract p.173, printed p.171). The quantified link from "
                "climate scenarios to credit losses is the \u0394ECL table on "
                "printed p.93. That table does not explain every named risk one by one."
            )
            row["changed_in_v2"] = "evidence quote and page replaced; score unchanged"
        if row["firm_id"] == "01" and row["indicator"] == "C1":
            row["verbatim_quote"] = (
                "The Group has carefully considered how the principles in the "
                "examples impact the disclosures in it's financial statements and "
                "conclude that the amendments do not have a material impact on "
                "the Group's financial statements."
            )
            row["changed_in_v2"] = "full sentence confirmed; printed page 62; score unchanged"
        if row["firm_id"] == "14" and row["indicator"] == "C4":
            row["score"] = "0"
            row["doc_type"] = "ar"
            row["page_number"] = "213"
            row["printed_page"] = "PDF p. 213 (printed number not confirmed)"
            row["verbatim_quote"] = (
                "Asset retirement obligations. The amount of future cash outflows "
                "to meet the asset retirement obligations are subject to inherent "
                "uncertainties due to limited availability of information on the "
                "amount of cost to be incurred in future."
            )
            row["coding_rationale"] = (
                "Note 27 records an asset retirement provision. No climate or "
                "transition wording is attached, so C4 applies and scores 0. "
                "The sector maximum becomes 18."
            )
            row["changed_in_v2"] = "NA to 0; provision exists without a climate link"

    with EV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with PROF.open(encoding="utf-8", newline="") as handle:
        profiles = list(csv.DictReader(handle))
        pfields = list(profiles[0].keys())
    for row in profiles:
        if row["firm_id"] == "03":
            row["sr_climate_principal_risk"] = "yes"
            row["sr_scenario_analysis"] = "no"
            row["sr_risks_named_list"] = (
                "Transition and climate-related risks (including regulatory "
                "developments); seasonal flooding"
            )
            row["sr_risks_named_count"] = "2"
    with PROF.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=pfields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(profiles)
    print("updated evidence and Oando profile")


if __name__ == "__main__":
    main()
