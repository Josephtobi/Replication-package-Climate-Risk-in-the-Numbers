"""Count climate search-term hits in annual-report extracts only."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data" / "extracted_text"
TERMS = json.loads((ROOT / "config" / "search_terms.json").read_text(encoding="utf-8"))
SAMPLE = pd.read_csv(ROOT / "config" / "sample_firms.csv", dtype=str)
OUT = ROOT / "outputs" / "tables" / "table_keyword_hits.csv"
PAGE_LOG = ROOT / "outputs" / "logs" / "keyword_page_hits.csv"


def count_group(text: str, terms: list[str]) -> int:
    total = 0
    low = text.lower()
    for term in terms:
        # word-boundary-ish for short tokens
        if " " in term or "-" in term:
            total += len(re.findall(re.escape(term.lower()), low))
        else:
            total += len(re.findall(rf"\b{re.escape(term.lower())}\b", low))
    return total


def main() -> None:
    rows = []
    page_rows = []
    for _, firm in SAMPLE.iterrows():
        fid, slug, company, sector = firm["firm_id"], firm["slug"], firm["company"], firm["sector"]
        path = EXTRACTED / f"{fid}-{slug}-ar-FY2025.txt"
        if not path.exists():
            print(f"MISSING {path.name}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        # strip page markers for counting
        body = re.sub(r"=== PAGE \d+ ===\n", "\n", text)
        counts = {f"hits_{k}": count_group(body, v) for k, v in TERMS.items()}
        # map names to locked columns
        row = {
            "firm_id": fid,
            "company": company,
            "sector": sector,
            "hits_climate": counts["hits_climate"],
            "hits_physical": counts["hits_physical_risk"],
            "hits_energy": counts["hits_energy_price"],
            "hits_regulation": counts["hits_regulation"],
            "hits_banking": counts["hits_banking"],
            "hits_standards": counts["hits_standards"],
        }
        row["total_ar_hits"] = sum(row[k] for k in row if k.startswith("hits_"))
        rows.append(row)

        # page-level log for climate group only
        parts = re.split(r"=== PAGE (\d+) ===\n", text)
        for i in range(1, len(parts), 2):
            page_no, content = parts[i], parts[i + 1]
            h = count_group(content, TERMS["climate"])
            if h:
                page_rows.append(
                    {"firm_id": fid, "page": page_no, "hits_climate": h}
                )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    pd.DataFrame(page_rows).to_csv(PAGE_LOG, index=False)
    print(pd.DataFrame(rows).to_string(index=False))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
