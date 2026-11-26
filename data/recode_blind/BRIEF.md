# Blind second coding brief

This brief is the version 1.0 instrument used for the five-firm pass on 25 November 2026. The pass was done by an AI agent. The published scores use codebook version 1.1, in `config/codebook_v1.1.md`. Rule 3 below, which allows sustainability text to score bank C5, is the version 1.0 rule and is not the published rule.

You are a second coder. Score five companies from the extracted annual reports and this brief only. Do not look up, infer, or reuse any earlier score.

## Files you may read

- This brief.
- `data/recode_blind/recode_pass2_template.csv`
- These extracts, and no other extract:
  - `data/extracted_text/06-zenith-ar-FY2025.txt` (Zenith Bank, banking)
  - `data/extracted_text/13-mtn-ar-FY2025.txt` (MTN Nigeria, telecoms)
  - `data/extracted_text/01-seplat-ar-FY2025.txt` (Seplat Energy, oil and gas)
  - `data/extracted_text/10-dangote-ar-FY2025.txt` (Dangote Cement, cement)
  - `data/extracted_text/07-gtco-ar-FY2025.txt` (GTCO, banking)

Page markers in those files look like `=== PAGE N ===`. That N is the extract page. If a printed page number is visible in a footer or header on the same page as the quote, record it too. If it is not visible, leave `printed_page` empty.

## Files you must not open

Opening any of these makes the pass invalid. Do not search them, do not grep the project for scores, and do not read a file whose name suggests results, a handoff, a memo, or a checkpoint.

- `data/coded/evidence_log.csv`
- `data/coded/firm_profiles.csv`
- `data/coded/sources.csv`
- anything under `outputs/`
- `gemini_handoff.md`
- `Paper-C-Cursor-Handoff-v1-to-v2.md`
- `outputs/verification_memo.md`
- `outputs/AUTHOR_CHECKPOINT.md`
- `outputs/v2/`
- `config/rubric_definition.json` (it contains a pilot note that states a result)

Do not open other firms' extracts. Do not open PDFs. Do not browse agent transcripts.

## Scale

| Score | Meaning |
| --- | --- |
| 0 | Absent: climate is not mentioned where the indicator looks |
| 1 | Boilerplate: a generic climate sentence, with nothing specific to the firm |
| 2 | Entity-specific and qualitative: names the firm's own assets, loans, sites, or assumptions, without numbers |
| 3 | Quantified or tested: states figures, ranges, dates, or a sensitivity linked to climate |

Use `NA` only when the indicator does not apply to that sector. For the five firms below, every requested indicator applies, so do not write NA. C4 applies to MTN, Seplat, and Dangote. If a site-restoration or decommissioning provision is recorded and the note has no climate link, C4 scores 0. It does not become NA.

## Indicators to score

Score only these rows.

Banks (Zenith firm_id 06, GTCO firm_id 07): C1, C5a, C5b, C7, A1.

MTN (13), Seplat (01), Dangote (10): C1, C2, C3, C4, C6, C7, A1.

| Code | Where it looks | Score 2 | Score 3 |
| --- | --- | --- | --- |
| C1 | Critical accounting judgements and estimates note | Names which of the firm's own estimates climate could affect | States the affected estimates with ranges or a risk of material adjustment |
| C2 | Impairment note | Says an oil price, demand, or carbon-cost path reflects transition, in words | Gives the price, carbon cost, or demand path used, and its source |
| C3 | Impairment or estimates note | Describes how a transition scenario would affect headroom | Quantifies the change that would cause impairment under a climate case |
| C4 | Provisions note for decommissioning or restoration | Links timing or closure risk to transition | States closure dates or cost changes under transition and their effect |
| C5a | Banks only. Climate inside expected credit losses | Explains how climate enters credit risk or staging | Shows climate overlays, adjusted inputs, or figures |
| C5b | Banks only. Oil and gas in credit risk | Names an oil-and-gas book and a climate or transition link, without a figure | Shows oil-and-gas exposure figures tied to climate |
| C6 | Useful lives and property, plant and equipment | Says useful lives were reviewed for transition or physical risk | States changed lives or carrying amounts of high-emission assets |
| C7 | Financial statements set against climate risks named in the same annual report | The financial statements mention the main climate risks named elsewhere in the report | They cross-refer and explain, with figures, why each named risk does or does not change the numbers |
| A1 | Independent auditor's report and key audit matters. Not part of the connectivity score | Climate is mentioned inside another key audit matter | Climate is its own key audit matter, or a stated focus of one |

## Rules

1. A disclosure counts only where the indicator looks. Climate words in the chairman's statement do not score C1.
2. A statement that climate has no material effect scores 1, unless the firm explains why for its own assets (2) or shows the test (3).
3. For banks, climate content in the credit-risk notes can score C5. So can sustainability disclosures inside the same annual report, when they address climate in credit risk or expected credit losses.
4. An oil-and-gas sector table with no climate or transition wording scores 0 on C5b. Concentration alone is not a climate link.
5. A recorded site-restoration, decommissioning, or asset-retirement provision makes C4 applicable. With no climate link, the score is 0.
6. Every score needs a verbatim quote of no more than 60 words, copied from the extract, and the extract page. If the score is 0 because you found no climate wording, quote the closest provision, judgement, or key-audit-matter sentence that shows where you looked, and say in the rationale that climate is absent there.
7. Do not invent a sentence, a page, or a figure. If the auditor's report is not in the extract, score A1 as 0 and say the report was not in the extract.
8. Do not compute a connectivity index. Do not rank the firms.

## Output

Write `data/coded/recode_pass2.csv` using the template columns, one row per firm-indicator listed above (31 rows). Use a comma-separated file with quoted fields. Scores are 0, 1, 2, or 3 only.

Columns: `firm_id`, `company`, `sector`, `indicator`, `score`, `doc_file`, `extract_page`, `printed_page`, `verbatim_quote`, `rationale`.

`doc_file` is the extract filename you used. `rationale` is one or two sentences on why the score is that level.
