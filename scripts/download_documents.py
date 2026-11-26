"""Download Paper C source PDFs from official IR/NGX URLs and update sources.csv + provenance.csv."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "download_manifest.json"
RAW = ROOT / "data" / "raw_pdfs"
SOURCES = ROOT / "data" / "coded" / "sources.csv"
PROVENANCE = ROOT / "data" / "provenance.csv"
CACHE = ROOT / "data" / "_download_cache"

SOURCE_COLS = [
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
]
PROV_COLS = [
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_key = hashlib.sha256(url.encode()).hexdigest()[:16]
    cache_path = CACHE / f"{cache_key}.pdf"
    if dest.exists() and dest.stat().st_size > 1000:
        print(f"SKIP exists: {dest.name}")
        return
    if cache_path.exists() and cache_path.stat().st_size > 1000:
        shutil.copy2(cache_path, dest)
        print(f"CACHE -> {dest.name}")
        return
    print(f"GET {url}")
    headers = {"User-Agent": "PaperC-research-agent/1.0 (academic; joseph.davies)"}
    with requests.get(url, headers=headers, stream=True, timeout=180) as r:
        r.raise_for_status()
        tmp = dest.with_suffix(".partial")
        with tmp.open("wb") as f:
            for chunk in r.iter_content(1024 * 256):
                if chunk:
                    f.write(chunk)
        tmp.replace(dest)
    shutil.copy2(dest, cache_path)
    print(f"OK {dest.name} ({dest.stat().st_size:,} bytes)")


def main() -> None:
    docs = json.loads(MANIFEST.read_text(encoding="utf-8"))["documents"]
    accessed = json.loads(MANIFEST.read_text(encoding="utf-8")).get(
        "accessed", date.today().isoformat()
    )
    source_rows: list[dict[str, str]] = []
    prov_rows: list[dict[str, str]] = []
    seen_files: dict[str, Path] = {}

    for doc in docs:
        firm_id = doc["firm_id"]
        slug = doc["slug"]
        doc_type = doc["doc_type"]
        folder = RAW / f"{firm_id}_{slug}"
        filename = f"{firm_id}-{slug}-{doc_type}-FY2025.pdf"
        dest = folder / filename
        url = doc["url"]

        # Reuse same bytes if identical URL already downloaded for this firm
        url_key = f"{firm_id}|{url}"
        if url_key in seen_files and seen_files[url_key].exists():
            folder.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.copy2(seen_files[url_key], dest)
                print(f"COPY {seen_files[url_key].name} -> {dest.name}")
        else:
            try:
                download(url, dest)
                seen_files[url_key] = dest
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL {filename}: {exc}")
                continue

        digest = sha256_file(dest) if dest.exists() else ""
        source_rows.append(
            {
                "firm_id": firm_id,
                "company": doc["company"],
                "sector": doc["sector"],
                "doc_type": doc_type,
                "period_end": doc["period_end"],
                "source_url": url,
                "download_date": accessed,
                "audited": doc.get("audited", ""),
                "pdf_page_count": "",
                "extracted_page_count": "",
                "ocr_applied": "no",
                "sha256_hash": digest,
                "notes": doc.get("notes", ""),
            }
        )
        rel = dest.relative_to(ROOT).as_posix()
        prov_rows.append(
            {
                "series_id": f"pdf-{firm_id}-{slug}-{doc_type}-fy2025",
                "description": f"{doc['company']} FY2025 {doc_type.upper()} PDF",
                "source": f"{doc['company']} IR / NGX",
                "url": url,
                "accessed": accessed,
                "vintage": doc["period_end"],
                "license": "issuer copyright; research use",
                "unit": "PDF document",
                "bucket": "downloaded",
                "file": rel,
                "inputs": "",
                "notes": doc.get("notes", ""),
            }
        )

    with SOURCES.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SOURCE_COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(source_rows)

    # Preserve existing provenance header and rewrite PDF rows by merging
    existing = []
    if PROVENANCE.exists():
        with PROVENANCE.open(encoding="utf-8-sig", newline="") as f:
            existing = [
                r
                for r in csv.DictReader(f)
                if not (r.get("series_id") or "").startswith("pdf-")
            ]
    with PROVENANCE.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PROV_COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(existing + prov_rows)

    print(f"Wrote {len(source_rows)} source rows")


if __name__ == "__main__":
    main()
