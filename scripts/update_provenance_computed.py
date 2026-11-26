"""Append computed-output rows to provenance.csv."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "data" / "provenance.csv"
COLS = [
    "series_id",
    "description",
    "source",
    "url",
    "accessed",
    "vintage",
    "license",
    "unit",
    "bucket",
    "file",
    "inputs",
    "notes",
]


def main() -> None:
    rows = []
    if PROV.exists():
        with PROV.open(encoding="utf-8-sig", newline="") as f:
            rows = [r for r in csv.DictReader(f) if r.get("bucket") != "computed"]

    if not any(r.get("bucket") == "downloaded" for r in rows):
        for pdf in sorted((ROOT / "data" / "raw_pdfs").rglob("*-FY2025.pdf")):
            rows.append(
                {
                    "series_id": f"pdf-{pdf.stem.lower()}",
                    "description": pdf.name,
                    "source": "company IR / NGX",
                    "url": "see config/download_manifest.json",
                    "accessed": "2026-11-25",
                    "vintage": "FY2025",
                    "license": "issuer copyright; research use",
                    "unit": "PDF document",
                    "bucket": "downloaded",
                    "file": pdf.relative_to(ROOT).as_posix(),
                    "inputs": "",
                    "notes": "",
                }
            )

    today = date.today().isoformat()
    computed = [
        (
            "computed-master-scores",
            "Master firm CI scores",
            "scripts/01_load_and_validate.py",
            "",
            today,
            "FY2025",
            "research",
            "index",
            "computed",
            "outputs/tables/table_master_firm_scores.csv",
            "evidence_log,firm_profiles,rubric",
            "",
        ),
        (
            "computed-keyword-hits",
            "AR keyword hit counts",
            "scripts/02_keyword_counts.py",
            "",
            today,
            "FY2025",
            "research",
            "count",
            "computed",
            "outputs/tables/table_keyword_hits.csv",
            "extracted_text,search_terms",
            "",
        ),
        (
            "computed-rq-tables",
            "RQ1-4 and robustness tables",
            "scripts/04_descriptives_tests.py",
            "",
            today,
            "FY2025",
            "research",
            "table",
            "computed",
            "outputs/tables/",
            "table_master_firm_scores,firm_profiles,table_keyword_hits",
            "indicative p-values",
        ),
        (
            "computed-figures",
            "Publication figures fig1-5",
            "scripts/05_figures.py",
            "",
            today,
            "FY2025",
            "research",
            "figure",
            "computed",
            "outputs/figures/",
            "table_master_firm_scores,firm_profiles",
            "",
        ),
    ]
    for item in computed:
        rows.append(dict(zip(COLS, item)))

    with PROV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"provenance rows: {len(rows)}")


if __name__ == "__main__":
    main()
