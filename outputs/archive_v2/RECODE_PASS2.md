# Second coding pass (version 1.0)

This memo records the five-firm pass. It is not the published index.

The pass was done by an AI agent in Cursor on 25 November 2026. It used the brief in `data/recode_blind/BRIEF.md` and codebook version 1.0. It was not done by a named person, and it is not the same-coder recode. Agreement below compares the version 1.0 first score with that pass. The published Connectivity Index is version 1.1.

The coder reported opening only the brief, the template, and the five named extracts. All 31 quotes were then checked against those extracts. Each quote is on the stated extract page and is within 60 words.

The first `score` column was not changed. The new scores sit in `recode_score`, dated 2026-11-25. The index, the figures, and `gemini_handoff.md` were not rerun.

## Agreement

From `scripts/03_reliability.py`, on the 31 paired rows (5 firms):

| Measure | Result |
| --- | --- |
| Exact agreement | 74.19% (23 of 31) |
| Within one point | 87.1% |
| Unweighted kappa | 0.494 |
| Quadratic weighted kappa | 0.663 |
| Bootstrap 95% interval for the weighted kappa | 0.279 to 0.879 |
| Meets the 80% target | No |

Split, because A1 is outside the index:

| Subset | Pairs | Exact agreement | Within one point | Unweighted kappa | Quadratic weighted kappa |
| --- | --- | --- | --- | --- | --- |
| Connectivity indicators | 26 | 73.08% | 88.46% | 0.519 | 0.706 |
| A1 only | 5 | 80% (4 of 5) | 80% | 0.000 | 0.000 |

The A1 kappa is 0 because four of the five pairs are 0 against 0. Agreement is high and the chance agreement is also high. The one A1 difference is Dangote Cement, 0 against 2.

Exact agreement is below 80%. The other nine firms were not coded. The frozen rubric was not edited.

## The eight differences

Quotes are in `outputs/archive_v2/recode_disagreements.csv`.

| Firm | Indicator | First | Second | What the two coders used |
| --- | --- | --- | --- | --- |
| Seplat Energy | C1 | 1 | 0 | First: the IASB examples sentence on extract p.63. Second: the estimates note on extract p.78, which does not mention climate. |
| Seplat Energy | C7 | 1 | 3 | First: the examples sentence on extract p.63. Second: a climate-section cross-reference on extract p.35 that ties an oil-price change to notes 9 and 18. |
| Zenith Bank | C1 | 1 | 0 | First: the first-time IFRS S1 and S2 sentence on extract p.173. Second: the judgements note on extract p.261, which does not mention climate. |
| Zenith Bank | C7 | 3 | 1 | First: the ΔECL table on extract p.95. Second: the IFRS S1 and S2 adoption sentence on extract p.173, read as a pointer rather than a reconciliation of each named risk. |
| Dangote Cement | C7 | 1 | 0 | First: a decarbonisation sentence in the sustainability material. Second: the financial-statement notes on extract p.149, which do not mention climate. |
| Dangote Cement | A1 | 0 | 2 | Second: the impairment key audit matter on extract p.118 names climate change inside the audit response. It is not a separate climate key audit matter. |
| MTN Nigeria | C1 | 2 | 0 | First: a sustainability sentence on how climate affects financial position. Second: the judgements note on extract p.109, which does not mention climate. |
| MTN Nigeria | C2 | 1 | 0 | First: a qualitative measurement-uncertainty sentence. Second: the goodwill impairment note on extract p.120, which has no climate path. |

Four of the eight gaps are two points: Seplat C7 (1 to 3), Zenith C7 (3 to 1), Dangote A1 (0 to 2), and MTN C1 (2 to 0).

The pattern is where the indicator is allowed to look. The second coder stayed inside the named note. The first coder sometimes used a climate sentence elsewhere in the same report.

Under version 1.0 the first C7 score stayed 3, so that index was 75.00. The second score was 1, and the first score was not replaced. Version 1.1 scores the same expected-credit-loss table as C7, and sets C5a and C5b to 0, because the table sits outside the notes. Zenith's published index is 25.00.

## What was left alone

- The other nine firms.
- The rubric.
- Every first score, including Dangote A1.
- The version 1.0 first scores. They remain in the `score` column of `data/coded/evidence_log.csv`.
