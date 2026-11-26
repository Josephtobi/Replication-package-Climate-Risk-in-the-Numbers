# Paper C v2 changelog

25 November 2026. Statistics below were rerun from `scripts/01_load_and_validate.py`, `scripts/04_descriptives_tests.py`, and `scripts/05_figures.py`. They were not typed over the script output. The rubric was not changed.

## Score and label changes

| Item | Old | New | Reason |
| --- | --- | --- | --- |
| Airtel C4 | NA | 0 | Note 27 (extract p.213) records asset retirement obligations. The note gives no climate or transition reason. C4 therefore applies. |
| Airtel sector maximum | 15 | 18 | C4 is now scored. |
| Airtel raw score | 2 | 2 | A score of 0 does not add to the raw total. |
| Airtel CI | 13.33 | 11.11 | 2 / 18 × 100. Still Boilerplate. Rank stays 7 because C7 is 2. |
| Airtel tier | Boilerplate | Boilerplate | Unchanged. |
| Oando SR risks | 0 | 2 | Counted from the 2025 annual report that is in the file, not from the separate sustainability report. |
| Oando gap | 0 | 2 | Two named items, and no connectivity indicator at 2 or 3. |
| Oando CI | 11.11 | 11.11 | The financial-statement scores were not changed. |
| Zenith C7 | 3 | 3 | Score kept. The logged evidence was replaced. |
| Zenith CI and tier | 75.00, Connected | 75.00, Connected | Unchanged. |
| Tier counts | 1, 3, 8, 2 | 1, 3, 8, 2 | Connected, Partial, Boilerplate, Silent. Unchanged. |
| Stanbic adoption label | Voluntary | Voluntary | Not changed. See NOT FOUND. |
| Any C5b score | — | — | None changed. |

## Evidence that supports the changes

**Airtel C4.** Extract p.213, Note 27: "Asset retirement obligations. The amount of future cash outflows to meet the asset retirement obligations are subject to inherent uncertainties due to limited availability of information on the amount of cost to be incurred in future." Printed page number was not on that extract page. Flagged as PDF p. 213.

**MTN C4, for the comparison.** Note 4.8, extract p.102, printed pp. 202–203: property and equipment includes "the estimated amount required for the decommissioning, dismantling and restoration of network sites." No climate link. C4 stays 0 and the maximum stays 18.

**Oando SR risks.** The annual report says a comprehensive sustainability report for the year ended 31 December 2025 "is currently being finalised and will be published separately" (printed p.79). The 90-page page list was not used.

Two distinct items in the annual report:

1. Printed p.79: "The Company continues to assess climate-related risks within its risk management framework, including transition risks, regulatory developments, and evolving stakeholder expectations."
2. Printed p.86: flood management in Rivers, Delta and Imo "help mitigate the impacts of seasonal flooding on assets and host communities."

The phrase "physical risk" was not found. The financial statements still contain only the IASB examples paragraph, already scored C1 = 1 and C7 = 1. No C-score changed.

**Zenith C7.** The old evidence, extract p.173, printed p.171, is only a cross-reference. The quantified passage is the ΔECL table on printed p.93 (extract p.95): "The table below presents the ΔECL across various climate scenario and time horizons. The values represent the additional provisioning requirement above the baseline ECL driven by climate-related PD and LGD stress." C7 stays 3 on that passage. The table does not walk through every named risk. See Rubric questions.

**Seplat C1.** Confirmed in the NGX FY2025 financial results, not the integrated report. Printed p.62 (extract p.63): "The Group has carefully considered how the principles in the examples impact the disclosures in it's financial statements and conclude that the amendments do not have a material impact on the Group's financial statements." The source's "it's" is kept. Score unchanged at 1.

## Statistics that moved because Airtel and Oando changed

| Statistic | v1 | v2 |
| --- | --- | --- |
| Kruskal-Wallis H | 5.867 | 5.380 |
| Kruskal-Wallis p | 0.118 | 0.146 |
| Epsilon-squared | 0.451 | 0.414 |
| Telecoms median (min–max) | 23.33 (13.33–33.33) | 22.22 (11.11–33.33) |
| Panel A U, p, script r | 32.5, 0.106, −0.625 | 33.0, 0.076, −0.650 |
| Panel A other-firms IQR | 10.28 | 9.72 |
| Panel B U, p, script r | 37.0, 0.108, −0.542 | 37.5, 0.108, −0.562 |
| Panel B non-adopter IQR | 8.61 | 6.94 |
| Spearman, SR risks and CI | 0.417, p 0.138, n = 14 | 0.434, p 0.121, n = 14 |
| Spearman, CI and whole-report hits | 0.676, p 0.0079, n = 14 | 0.652, p 0.0115, n = 14 |
| Spearman, CI and ln(assets) | 0.533, p 0.0605, n = 13 | unchanged, n = 13 |

The script's rank-biserial is r = 1 − 2U / (n1 × n2). A negative figure means the first-named group ranks higher. The sign that is positive when that group ranks higher is Panel A 0.650 and Panel B 0.562. Panel B still counts Stanbic as an adopter.

Banking median 25.00, oil and gas median 11.11, and cement median 5.56 did not change. Cement still has no spread.

Figures 1 to 5 were redrawn from the rerun and copied to `outputs/v2/figures/`.

## C5b check

No score was changed. The table is `bank_c5b_check.csv`.

- Access, GTCO, UBA, and Stanbic have an oil-and-gas sector line. The line itself has no climate wording, so C5b stays 0.
- UBA's transition-risk sentence that names Oil and Gas is in the sustainability narrative (extract p.31), not on the note table.
- Fidelity's C5b = 2 is the ESG-risk sentence on extract p.107, not the project-finance row on extract p.105.
- Zenith's C5b = 2 is the high-carbon sentence on printed p.93. A separate oil-and-gas exposure line is on extract p.205.

## Rubric questions

1. Zenith C7. The level-3 wording asks why each named risk does or does not change the numbers. The ΔECL table quantifies climate scenarios against credit losses and does not cover each named risk. The score was kept at 3 because a reconciling passage with figures exists. If the stricter reading is preferred, C7 becomes 2, CI becomes 66.67, the tier becomes Partial, and the Connected count becomes 0.
2. Airtel asset retirement obligations were treated as the site-restoration provision that makes C4 applicable. The note does not say the provision is for masts or climate damage. If that provision is not the C4 item, C4 returns to NA, the maximum returns to 15, and CI returns to 13.33.

## NOT FOUND

- Stanbic's full FY2025 annual report was not saved from the investor-relations site, so the firm was not recoded and the Voluntary label was not changed. A third-party text preview was not used as a source.
- Seplat's auditor's report. The NGX file used for coding does not contain it. The OCR reading of printed pp. 162–166 of the integrated report was not confirmed from a file in this project. A1 stays 0, and the limitation is not resolved.
- Oando's separate 2025 sustainability report. The annual report says it is still being finalised.
- Market capitalisation from NGX price times shares outstanding, except the figures already printed in the Dangote and BUA reports (N10.20 trillion, and approximately N6.0 trillion). No market-cap correlation was calculated.
- A Central Bank of Nigeria closing rate on 31 March 2026. Airtel's assets stay in US dollars. The 14-firm asset correlation was not calculated.
- Printed page numbers for most evidence rows. Confirmed printed pages are Seplat C1 and C7 (62), Zenith C5a, C5b and C7 (93), Zenith's cross-reference (171), and the two Oando annual-report items (79 and 86). Other rows say "PDF p. N (printed number not confirmed)."
- Financial-statements-only keyword counts. A first cut treated contents pages, five-year summaries, and sentences inside the notes as the statement of financial position. Those counts were not saved, and the financial-statements-only Spearman was not calculated. The whole-report counts are unchanged. Their correlation with CI moved only because Airtel's CI moved.
- Reliability recode and kappa. Not started. The five-firm recode is due on or after 9 December 2026.
