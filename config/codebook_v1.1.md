# Paper C Codebook, version 1.1

Climate Risk in the Numbers: financial statement connectivity of 14 NGX companies, FY2025.
Coder guidance for scoring, re-scoring and replication.

Version 1.0 was frozen on 25 November 2026 after the pilot on Seplat Energy and Access Holdings. Version 1.1 (25 November 2026) adds the location rule in Section 3. The change was made after the inter-rater pass on five firms showed that most disagreements came from where each indicator may look. The agreement statistics for that pass are reported against version 1.0. All 14 firms are then re-scored under version 1.1.

## 1. Documents

For each firm, use:

1. The audited financial statements for FY2025. These are in the annual report or the NGX financial statements filing. They include the independent auditor's report, the primary statements and the notes.
2. The sustainability report, or the sustainability section of the annual report.

Record the document title, URL, date accessed and file hash in `sample_and_sources.csv`. Give page references as printed page numbers where visible. Where they are not visible, write "PDF p. N".

## 2. Score levels

Score each applicable indicator 0 to 3. If an indicator does not apply, mark it NA. NA is excluded from the firm's maximum.

| Score | Label | Test |
|---|---|---|
| 0 | Absent | No climate content where the indicator looks |
| 1 | Boilerplate | Generic climate mention with nothing specific to the firm |
| 2 | Entity-specific | Names the firm's own assets, loans, sites or assumptions, without figures |
| 3 | Quantified or tested | Gives figures, ranges, dates or a sensitivity linked to climate |

Climate content means physical risk, transition risk, carbon pricing, emissions, energy transition or climate scenarios. A generic commodity price sentence is not climate content unless the text links it to transition or climate.

## 3. Location rule (new in version 1.1)

**C1 to C6 are scored only from inside the financial statements**, in the location named for each indicator below. Climate text anywhere else does not count toward C1 to C6, however specific it is. This covers the sustainability report, the strategic report, the chair's or CEO's statement and the risk report outside the notes.

**C7 scores the link between sustainability reporting and the financial statements, in either direction.** It may use text in either place, but it scores the link, not climate content as such.

**A1 is scored only from the independent auditor's report**, including the key audit matter descriptions and the audit responses to them.

## 4. Indicators

| Code | Indicator | Applies to | Where to look |
|---|---|---|---|
| C1 | Climate in critical judgements and estimates | All firms | The note on significant judgements, estimates and assumptions. Also the basis-of-preparation or new-pronouncements note, but only where it states a conclusion on how climate, or the IASB climate examples, affect the financial statements (see 5.4) |
| C2 | Climate in impairment key assumptions | Oil and gas, cement, telecoms | The impairment note, the goodwill or CGU note, and the impairment accounting policy |
| C3 | Climate in impairment sensitivity or headroom | Oil and gas, cement, telecoms | The sensitivity or headroom disclosure in the impairment note |
| C4 | Climate in decommissioning, restoration or asset retirement provisions | Firms carrying such a provision | The provisions note |
| C5a | Climate in expected credit losses | Banks | The credit risk, ECL and impairment notes (see 5.5) |
| C5b | Climate linked to oil and gas or high-carbon credit concentrations | Banks | The credit risk concentration tables and notes (see 5.5) |
| C6 | Climate in useful lives or PP&E carrying amounts | Oil and gas, cement, telecoms | The PP&E note and the useful-life policy or estimate |
| C7 | Link between sustainability reporting and financial statements | All firms | Either place (see levels below) |
| A1 | Climate in the auditor's report | All firms (excluded from the index) | The independent auditor's report only |

### C7 levels

| Score | Test |
|---|---|
| 0 | No link in either direction |
| 1 | A generic pointer or adoption statement, for example "the sustainability disclosures are in section X" or "the Group adopted IFRS S1 and S2". It names no climate risk |
| 2 | Names climate risks and points to specific notes or line items, without amounts |
| 3 | Maps named climate risks to specific notes or line items with amounts, or explains for named risks why there is no financial statement effect |

### A1 levels

| Score | Test |
|---|---|
| 0 | No climate mention in the auditor's report |
| 1 | Climate mentioned in passing inside another key audit matter or its audit response |
| 2 | Climate named as an assumption the auditor specifically tested, inside another key audit matter |
| 3 | A key audit matter whose subject is climate |

## 5. Decision rules

5.1 **C5b sector lines.** A bank note showing an oil and gas exposure line without climate wording scores 0 on C5b. The indicator rewards a climate link, not sector exposure alone.

5.2 **C4 applicability.** C4 applies wherever the firm carries a decommissioning, restoration or asset retirement provision, whether or not the note mentions climate. A provision note without a climate link scores 0. Without a provision, C4 is NA.

5.3 **No-material-effect statements.** A statement that climate has no material effect scores 1. It scores 2 if it explains why for the firm's own assets, and 3 if it shows the test.

5.4 **IASB examples statements.** A sentence in the notes concluding on the effect of the IASB's November 2025 climate examples on the financial statements counts toward C1 under 5.3. A sentence that only lists the examples as a new pronouncement, with no conclusion, scores 0.

5.5 **Banks: sustainability-section content.** C5a and C5b are scored only from the credit risk, ECL, impairment and concentration notes in the financial statements. Climate-in-credit content that sits only in the sustainability section, for example a climate stress table, does not count toward C5a or C5b. It is considered under C7 if it links named risks to the financial statements. (Version 1.0 allowed such content to count toward C5a and C5b.)

5.6 **Statements outside the notes.** A chair's or CEO's climate sentence, a sustainability narrative sentence and a risk-report sentence do not count toward C1 to C6.

5.7 **Evidence.** Every score above 0 needs a verbatim quote of 60 words or fewer, a page reference and a one-line rationale.

## 6. Index and tiers

Connectivity Index = sum of applicable C scores ÷ firm maximum × 100.

Tiers:

| Tier | Index range |
|---|---|
| Connected | 67 to 100 |
| Partial | 34 to 66 |
| Boilerplate | 1 to 33 |
| Silent | 0 |

Ties are broken by higher C7, then by more indicators at 3, then by higher A1. Firms still tied share a rank.

Gap = distinct climate risks named in sustainability reporting minus applicable C indicators scored 2 or 3.

## 7. Second coder protocol

The second coder works from the original documents and this codebook only. They do not see the first coder's scores, the evidence log or results tables, and do not discuss individual firms until scoring is complete.

Agreement is reported before reconciliation:

- exact agreement;
- agreement within one point;
- unweighted kappa;
- quadratic weighted kappa with a bootstrap 95% interval.

Each measure is reported overall, for C1 to C7, and for A1. Disagreements are then settled by both coders against the source, and the reason for each settled score is logged.
