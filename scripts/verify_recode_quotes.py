"""Check second-pass quotes sit on the stated extract page. Read-only."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECODE = ROOT / "data" / "coded" / "recode_pass2.csv"
EXTRACTED = ROOT / "data" / "extracted_text"


def norm(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\ufb01", "fi").replace("\ufb02", "fl").replace("\u0394", "delta")
    text = text.replace("\u20a6", "n")
    return re.sub(r"\s+", " ", text).strip().lower()


def main() -> None:
    with RECODE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    print("rows", len(rows))
    bad = 0
    for row in rows:
        path = EXTRACTED / row["doc_file"]
        text = path.read_text(encoding="utf-8", errors="replace")
        parts = re.split(r"=== PAGE (\d+) ===\n", text)
        page = {}
        for i in range(1, len(parts), 2):
            page[parts[i]] = parts[i + 1]
        content = page.get(row["extract_page"], "")
        quote = norm(row["verbatim_quote"])
        words = len(row["verbatim_quote"].split())
        # drop a short tail if punctuation differs
        needle = quote[:80]
        ok = needle in norm(content)
        flag = "OK" if ok else "MISSING"
        if not ok or words > 60:
            bad += 1
            print(f"{flag} words={words} {row['firm_id']} {row['indicator']} p.{row['extract_page']}")
            if not ok:
                print("  ", quote[:120])
        else:
            print(f"OK words={words} {row['firm_id']} {row['indicator']} p.{row['extract_page']} score={row['score']}")
    print("problems", bad)


if __name__ == "__main__":
    main()
