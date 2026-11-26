"""Copy second-pass scores into recode_score. Does not change the first score."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVID = ROOT / "data" / "coded" / "evidence_log.csv"
RECODE = ROOT / "data" / "coded" / "recode_pass2.csv"
DATE = "2026-11-25"


def main() -> None:
    with RECODE.open(encoding="utf-8", newline="") as handle:
        second = {(r["firm_id"], r["indicator"]): r["score"] for r in csv.DictReader(handle)}
    with EVID.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    filled = 0
    for row in rows:
        key = (row["firm_id"], row["indicator"])
        if key not in second:
            continue
        if row["score"].strip().upper() == "NA":
            raise SystemExit(f"Second pass scored an NA row: {key}")
        row["recode_score"] = second[key]
        row["recode_on"] = DATE
        filled += 1
        del second[key]
    if second:
        raise SystemExit(f"Unmatched second-pass rows: {sorted(second)}")
    if filled != 31:
        raise SystemExit(f"Expected 31 fills, got {filled}")
    with EVID.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"filled {filled} recode_score cells; score column untouched")


if __name__ == "__main__":
    main()
