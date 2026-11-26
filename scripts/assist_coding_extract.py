"""Extract indicator-relevant climate snippets per firm for human/agent scoring."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data" / "extracted_text"
OUT = ROOT / "outputs" / "logs" / "coding_candidates.csv"

INDICATOR_PATTERNS = {
    "C1": [
        r"critical accounting",
        r"significant (accounting )?judgement",
        r"key (sources of )?estimation",
        r"IASB.*(climate|illustrative example)",
        r"illustrative examples",
        r"climate.*(judgement|estimate|assumption)",
    ],
    "C2": [
        r"impairment.*(climate|transition|carbon|emission)",
        r"(climate|transition|carbon).{0,80}impairment",
        r"key assumption",
        r"oil price.*(impairment|CGU)",
        r"carbon (cost|price|tax)",
    ],
    "C3": [
        r"sensitivity.*(climate|transition|carbon|headroom)",
        r"(climate|transition).{0,60}(sensitivity|headroom)",
        r"headroom",
    ],
    "C4": [
        r"decommission",
        r"restoration provision",
        r"asset retirement",
        r"closure.*(climate|transition)",
    ],
    "C5": [
        r"(climate|ESG).{0,80}(ECL|expected credit|credit risk)",
        r"(ECL|expected credit|credit risk).{0,80}(climate|ESG|environment)",
        r"oil and gas (exposure|concentration|portfolio)",
        r"sector concentration",
        r"overlay",
        r"financed emission",
    ],
    "C6": [
        r"useful life",
        r"PP&E|property, plant",
        r"(climate|transition).{0,60}(useful life|asset life|depreciation)",
    ],
    "C7": [
        r"IFRS S[12]",
        r"ISSB",
        r"connectivity",
        r"sustainability.report",
        r"climate.related risk",
    ],
    "A1": [
        r"key audit matter",
        r"climate",
        r"ESG",
    ],
}


def pages_of(path: Path) -> dict[int, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"=== PAGE (\d+) ===\n", text)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def first_quote(page_text: str, max_words: int = 55) -> str:
    words = page_text.split()
    # Prefer a sentence containing climate/ESG/IFRS S
    for sent in re.split(r"(?<=[.|;])\s+", page_text):
        if re.search(r"climate|ESG|IFRS S|ISSB|emission|transition|decommission|ECL", sent, re.I):
            w = sent.split()
            return " ".join(w[:max_words]).strip()
    return " ".join(words[:max_words]).strip()


def main() -> None:
    rows = []
    for ar in sorted(EXTRACTED.glob("*-ar-FY2025.txt")):
        firm_id = ar.name[:2]
        pages = pages_of(ar)
        for ind, pats in INDICATOR_PATTERNS.items():
            hits = []
            for n, content in pages.items():
                if any(re.search(p, content, re.I) for p in pats) and re.search(
                    r"climate|carbon|emission|ESG|IFRS S|ISSB|transition|decommission|ECL|impairment|useful life|key audit",
                    content,
                    re.I,
                ):
                    # tighten: page must have climate-ish OR be judgements/KAM page
                    climateish = bool(
                        re.search(
                            r"climate|carbon|emission|greenhouse|net.?zero|IFRS S[12]|ISSB|energy transition|financed emission",
                            content,
                            re.I,
                        )
                    )
                    structural = bool(
                        re.search(
                            r"significant accounting judgement|critical accounting|key audit matter|decommissioning|expected credit loss",
                            content,
                            re.I,
                        )
                    )
                    if not (climateish or (structural and ind in {"C1", "C4", "C5", "A1"})):
                        continue
                    hits.append((n, first_quote(content)))
            hits = hits[:5]
            for n, q in hits:
                rows.append(
                    {
                        "firm_id": firm_id,
                        "file": ar.name,
                        "indicator": ind,
                        "page": n,
                        "candidate_quote": q.replace("\n", " ")[:400],
                    }
                )
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["firm_id", "file", "indicator", "page", "candidate_quote"],
            lineterminator="\n",
        )
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} candidates to {OUT}")


if __name__ == "__main__":
    main()
