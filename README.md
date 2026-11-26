# Replication pack

Paper C, Climate Risk in the Numbers. A content analysis of FY2025 financial statements for 14 NGX Main Board firms, scored against the IASB November 2025 climate-uncertainty examples.

This folder is the package a reader can rerun. The published numbers are codebook version 1.1, dated 25 November 2026.

The version 1.0 scores and the version 1.1 scores were applied by an AI agent in Cursor, from the extracted annual reports. The passes are not a human coder and they are not the same-coder recode. Say so wherever the method is described.

## Two steps

Scoring is a reading judgement. Each applicable indicator has a score from 0 to 3, or NA where it does not apply. A score above 0 has a verbatim quote and a page. No script assigns those scores. The version 1.1 judgements are stored in `scripts/06_score_v11.py` and written to `outputs/v11/evidence_v11.csv`.

Calculation is the rest. Four scripts read those scores and write the index, the tests, and the figures. A reviewer needs Python and the packages in `requirements.txt`. A reviewer does not need an AI agent to rerun them.

## Rerun the published results

From this folder:

```bash
pip install -r requirements.txt
python scripts/06_score_v11.py
python scripts/01_load_and_validate.py
python scripts/03_reliability.py
python scripts/04_descriptives_tests.py
python scripts/05_figures.py
```

`06` writes `outputs/v11/`. `01` writes `outputs/tables/table_master_firm_scores.csv` from that file. `03` compares the version 1.0 first score with the version 1.0 second pass. It does not measure agreement under version 1.1. `04` writes the research-question tables. `05` writes figures 1 to 5, as SVG and 300 dpi PNG, to `outputs/figures/`.

Cite `outputs/tables/`. The seed for the kappa bootstrap is 42, set in `scripts/03_reliability.py`. Do not type over a number a script writes.

## What each script does

**Fetch the reports.** These need the PDFs, which are not in this pack.

- `download_documents.py` downloads the files from the investor-relations and NGX links and records the hash.
- `00_extract_and_verify.py` turns each PDF into page-marked text.

**Find the passages.** These also need the extracts.

- `search_climate_hits.py` lists pages where the climate terms appear.
- `assist_coding_extract.py` pulls short snippets into a candidate list.
- `02_keyword_counts.py` counts the terms across each whole annual report. The count already saved in `outputs/tables/table_keyword_hits.csv` is what `04` uses.

**Store the scores.**

- `build_coded_tables.py` holds the version 1.0 profiles and the first-pass score sheet.
- `apply_v2_corrections.py` and `build_v2_package.py` are the earlier correction pass. Their output is in `outputs/archive_v2/`.
- `06_score_v11.py` holds the published version 1.1 scores.
- `merge_recode_pass2.py` copies the five-firm second pass into `recode_score` and leaves the first score unchanged.
- `verify_recode_quotes.py` checks that each second-pass quote sits on the page it claims. It needs the extracts.
- `write_recode_report.py` writes the disagreement list.

**Calculate.**

- `01_load_and_validate.py` builds the connectivity index, the tier, and the rank.
- `03_reliability.py` writes the version 1.0 agreement and kappa.
- `04_descriptives_tests.py` writes medians, the sector test, the adopter tests, and the correlations.
- `05_figures.py` draws the five figures.
- `update_provenance_computed.py` appends rows to the file log.

## How the index is calculated

Banks have a maximum of 12 (C1, C5a, C5b, C7). Every other firm in this sample has a maximum of 18, because each has a decommissioning, restoration, or asset-retirement provision, so C4 applies. NA is left out of the maximum. The index is the sum of the applicable C scores, divided by that maximum, times 100. A1 is not in the index.

Tiers: 67–100 Connected, 34–66 Partial, 1–33 Boilerplate, 0 Silent. In the tables these are written Tier 1 Connected through Tier 4 Silent. Ties break on a higher C7, then more indicators scored 3, then a higher A1.

The version 1.1 location rule is in `config/codebook_v1.1.md`. C1 to C6 count only inside the audited financial statements, in the named note. C7 scores a link in either direction. A1 is only the independent auditor's report. `config/rubric_definition.json` is the frozen version 1.0 rubric. The five-firm agreement used that rubric. The pilot note inside the JSON, which says Airtel's C4 is not applicable, is stale. The evidence file is the later decision: C4 applies and scores 0.

## Score files

| File | What it is |
| --- | --- |
| `outputs/v11/evidence_v11.csv` | Published scores, quotes, and the page checked |
| `outputs/tables/table_master_firm_scores.csv` | One row per firm: index, tier, rank |
| `data/coded/evidence_log.csv` | Version 1.0 first score in `score`, and the five-firm second pass in `recode_score` |
| `data/coded/firm_profiles.csv` | Sector, adoption group, auditor, assets, and the count of climate risks named in the annual report |
| `data/coded/sources.csv` | Document titles and URLs |
| `data/provenance.csv` | Download dates and file hashes |

`score` and `recode_score` are kept so the version 1.0 agreement can be rerun. They are not the published index.

## What this pack does not contain

The annual-report PDFs and the page-marked extracts are not here. `data/coded/sources.csv` and `data/provenance.csv` record where each file came from and the hash. Copy `data/raw_pdfs/` and `data/extracted_text/` into this folder before running the download, extract, or keyword scripts.

`outputs/archive_v2/` is the index from before version 1.1. Zenith is 75.00 and Airtel is 11.11 in that folder. Do not cite it. The memo `outputs/archive_v2/stats_v2.json` still says kappa was not computed. Use `outputs/tables/table_reliability_summary.csv` and `outputs/archive_v2/RECODE_PASS2.md`.

## Limits a reader should keep

- Stanbic IBTC is labelled Voluntary and scores 0 on the NGX financial statements. The full integrated report was not in the file set.
- The second pass covered Zenith, MTN, Seplat, Dangote Cement, and GTCO only, under version 1.0. Exact agreement is 74.19 percent (23 of 31). The other nine firms were not recoded.
- Keyword counts are for the whole annual report. A financial-statements-only recount was not published.
- Market capitalisation is filled only for Dangote Cement and BUA Cement. No market-cap correlation was calculated.
- Airtel Africa reports in US dollars for the year to 31 March 2026. It is excluded from the asset correlation, which uses 13 firms.
- Seplat's independent auditor's report is not in the NGX extract, so A1 is 0.
- p-values are indicative at 14 firms. The rank-biserial in the tables is r = 1 − 2U / (n1 × n2). A negative figure means the first-named group ranks higher.
