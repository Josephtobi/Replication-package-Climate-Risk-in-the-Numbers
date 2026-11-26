"""Quick climate-term page locator for coding support."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data" / "extracted_text"

TERMS = [
    r"climate",
    r"carbon",
    r"emission",
    r"greenhouse",
    r"\bghg\b",
    r"net[- ]?zero",
    r"decarbon",
    r"energy transition",
    r"IFRS S[12]",
    r"ISSB",
    r"decommission",
    r"impairment",
    r"expected credit loss|\bECL\b",
    r"key audit matter|\bKAM\b",
]


def search_file(path: Path, max_hits: int = 40) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = re.split(r"=== PAGE (\d+) ===\n", text)
    # pages: ['', '1', content, '2', content, ...]
    print(f"\n=== {path.name} ===")
    count = 0
    for i in range(1, len(pages), 2):
        page_no = pages[i]
        content = pages[i + 1]
        low = content.lower()
        if not any(re.search(t, low, re.I) for t in TERMS):
            continue
        # find first matching line
        for line in content.splitlines():
            if any(re.search(t, line, re.I) for t in TERMS):
                snippet = " ".join(line.split())[:160]
                if snippet:
                    print(f"p{page_no}: {snippet}")
                    count += 1
                    break
        if count >= max_hits:
            print("...truncated...")
            break


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern", nargs="?", default="*-ar-FY2025.txt")
    ap.add_argument("--max", type=int, default=30)
    args = ap.parse_args()
    files = sorted(EXTRACTED.glob(args.pattern))
    for f in files:
        search_file(f, args.max)


if __name__ == "__main__":
    main()
