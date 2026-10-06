# Independent review and correction report

Reviewed on 2026-10-06 by a separate grading subagent against the supplied capstone requirements, with an independent recalculation of the CSV and inspection of the slide images and native chart data.

**Provisional artifact-quality estimate: 86/100 before corrections; 91/100 after the substantive corrections.** This is an internal quality estimate, not an official SDAIA grade or a prediction of the assessed result. Live presence, delivery, Q&A performance and actual timing could not be scored from files. The final caption and layout refinements were checked after the subagent's second review.

## Findings and fixes

| Finding | Correction | Verification |
|---|---|---|
| High: pilots launched before the metric/baseline/cost were agreed | Funding and intervention now require approved metric, measured baseline, comparison design, verified shortlist, service plans and costs. Day 0 appoints the owner; launch occurs only when ready | Slides 1, 5 and 7, notes, both scripts, method, README and notebook aligned |
| Medium: weighted 66.12% reversed national target status but was not visible in the deck | Slide 2 explicitly says course adoption and shows the weighted alternative; Slide 4 states that weighting substitutes Al-Baha for Jazan | Final slide images and embedded text inspected |
| Medium: canonical PPTX/PDF/ZIP and GitHub were stale | The corrected canonical deck and PDF replace the previous presentation; ZIP and GitHub are synchronized to the same final package | Published content compared with local files, accounting for Git text line endings |
| Low: equal allocation displayed 4.44M × 9 as an exact 40M allocation | Slide 5 shows SAR 40M ÷ 9, about 4.44M each | Final table inspected |
| Small regression: chart-caption details were lost when adding sensitivity | Restored December 2025, synthetic-data disclosure, colour meanings and the statement that the priority proxy is not a conversion count | Final evidence slide inspected |
| Requirement gap found in the primary audit: Slide 4 originally had only a table | Replaced it with an annotated chart ranking all nine laggards, target-gap annotations and the near-tied third/fourth places | Three native charts and three tables in the seven-slide deck; actual Tableau-export requirement remains open |

## Confirmed evidence

The independent reviewer confirmed national arithmetic-mean adoption of 63.328346%, nine regions below 65%, top-three priority share of 42.614613%, weighted national adoption of 66.118639%, the priority ranking and budget totals. Northern Borders (446.2596675) and Al-Baha (445.6011875) differ by only 0.65848 priority units; the final narrative discloses this near tie.

`python analysis/validate_delivery.py` checks the raw source against the headline calculations and all four embedded chart series, at the deck's two-decimal reporting precision. It also checks the seven-slide count, three native charts/three tables, 40M envelope, 10M pilot sum, seven-page PDF, workbook source identity, recorded notebook execution and local delivery links. All checks passed for the corrected package. Every final PowerPoint slide and corresponding PDF page was visually inspected. Numerical checks do not constitute Tableau execution or a live rehearsal.

## Required steps still outside verified completion

| Remaining requirement | Why it is open | Next step |
|---|---|---|
| Day 2 Tableau evidence and annotated Tableau export | Original Day 2 dashboard was not supplied; the replacement workbook was built from CSV. Tableau is not installed here | Align with the original Day 2 workbook or obtain instructor acceptance of the replacement; open it in Tableau, check values/appearance and export the evidence chart |
| Tableau calculation and visual execution | Official XML schema and source-package checks passed, but those do not prove actual application behavior | Follow TABLEAU_GUIDE.md and record the actual application check |
| Seven-minute delivery, presence and Q&A | Scripts and speaker assignments are prepared; no actual group rehearsal was observed | Rehearse with a timer and the live dashboard |
| Teammate access and contributions | Invitations were issued; acceptance and team-authored contributions cannot be completed on others' behalf | Sanad and Hathal accept their invitations and review/contribute themselves |
| Google Form submission | Instructor's form URL was not supplied | Submit the public repository URL through that exact form |

The corrected artifact package is prepared and reviewed. Full course submission cannot be represented as completed while these requirements remain open.
