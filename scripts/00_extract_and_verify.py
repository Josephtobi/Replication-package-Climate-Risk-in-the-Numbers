"""Extract page-marked text from Paper C PDFs and audit completeness."""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_pdfs"
EXTRACTED = ROOT / "data" / "extracted_text"
SOURCES = ROOT / "data" / "coded" / "sources.csv"
AUDIT = ROOT / "outputs" / "logs" / "extraction_audit.csv"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_pdf(pdf_path: Path, out_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    blocks: list[str] = []
    thin_pages: list[int] = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text") or ""
        if len(text.strip()) < 20:
            thin_pages.append(i)
        blocks.append(f"=== PAGE {i} ===\n{text}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(blocks), encoding="utf-8", errors="replace")
    result = {
        "pdf_page_count": len(doc),
        "extracted_page_count": len(doc),
        "thin_pages": thin_pages,
        "ocr_applied": "no",
    }
    doc.close()
    return result


def main() -> None:
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(RAW.rglob("*-FY2025.pdf"))
    audit_rows = []
    source_updates: dict[tuple[str, str], dict] = {}

    for pdf in pdfs:
        # 01-seplat-ar-FY2025.pdf
        m = re.match(r"^(\d{2})-([a-z]+)-([a-z]+)-FY2025\.pdf$", pdf.name)
        if not m:
            continue
        firm_id, slug, doc_type = m.groups()
        out = EXTRACTED / f"{firm_id}-{slug}-{doc_type}-FY2025.txt"
        print(f"Extract {pdf.name}")
        info = extract_pdf(pdf, out)
        digest = sha256_file(pdf)
        source_updates[(firm_id, doc_type)] = {
            "pdf_page_count": str(info["pdf_page_count"]),
            "extracted_page_count": str(info["extracted_page_count"]),
            "ocr_applied": info["ocr_applied"],
            "sha256_hash": digest,
            "path": str(pdf.relative_to(ROOT).as_posix()),
        }
        for p in info["thin_pages"]:
            audit_rows.append(
                {
                    "firm_id": firm_id,
                    "doc_type": doc_type,
                    "file": pdf.name,
                    "page": p,
                    "flag": "POTENTIAL_SCAN_OR_BLANK",
                    "sha256": digest,
                }
            )
        if not info["thin_pages"]:
            audit_rows.append(
                {
                    "firm_id": firm_id,
                    "doc_type": doc_type,
                    "file": pdf.name,
                    "page": "",
                    "flag": "OK",
                    "sha256": digest,
                }
            )

    # Rebuild / update sources.csv from filesystem
    sample = list(csv.DictReader((ROOT / "config" / "sample_firms.csv").open(encoding="utf-8")))
    firm_meta = {r["firm_id"]: r for r in sample}
    rows = []
    for pdf in pdfs:
        m = re.match(r"^(\d{2})-([a-z]+)-([a-z]+)-FY2025\.pdf$", pdf.name)
        if not m:
            continue
        firm_id, slug, doc_type = m.groups()
        meta = firm_meta.get(firm_id, {})
        upd = source_updates.get((firm_id, doc_type), {})
        rows.append(
            {
                "firm_id": firm_id,
                "company": meta.get("company", slug),
                "sector": meta.get("sector", ""),
                "doc_type": doc_type,
                "period_end": "2026-03-31" if firm_id == "14" else "2025-12-31",
                "source_url": "[see provenance / download_manifest]",
                "download_date": "2026-11-25",
                "audited": "yes" if doc_type in {"ar", "afs"} else "n/a",
                "pdf_page_count": upd.get("pdf_page_count", ""),
                "extracted_page_count": upd.get("extracted_page_count", ""),
                "ocr_applied": upd.get("ocr_applied", "no"),
                "sha256_hash": upd.get("sha256_hash", ""),
                "notes": f"local file {upd.get('path', pdf.name)}",
            }
        )

    with SOURCES.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "firm_id",
                "company",
                "sector",
                "doc_type",
                "period_end",
                "source_url",
                "download_date",
                "audited",
                "pdf_page_count",
                "extracted_page_count",
                "ocr_applied",
                "sha256_hash",
                "notes",
            ],
            lineterminator="\n",
        )
        w.writeheader()
        w.writerows(rows)

    with AUDIT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["firm_id", "doc_type", "file", "page", "flag", "sha256"],
            lineterminator="\n",
        )
        w.writeheader()
        w.writerows(audit_rows)

    print(f"Extracted {len(pdfs)} PDFs; wrote {SOURCES} and {AUDIT}")


if __name__ == "__main__":
    main()
