# Evidence and decision method

## Scope and sources

SDAIA Academy SDA-DSC-112 capstone. The decision is where to direct a hypothetical SAR 40 million to move lagging Tayseer regions toward 65% digital adoption. All observations are synthetic training data. The supplied CSV contains 24,960 monthly region × service × channel records, January 2022–December 2025. The full 48 × 13 × 8 × 5 grid is present. There are no missing cells or duplicate dimension keys. These checks establish structural completeness, not real-world validity.

## Main metric follows the course labs

Regional adoption = arithmetic mean of `digital_adoption_pct` across the 40 service × channel records in a region and month. National adoption = arithmetic mean of the 520 records for that month. Each region has the same number of records, so the national value is also the mean of the 13 regional values. These are course indices. They must not be described as digital transactions divided by total transactions. Do not sum percentage values. Report gaps and changes in percentage points, not relative percentages.

All current-status comparisons and priority rankings use December 2025. The trend uses the full 48 months; no full-period regional average is compared with a latest-month figure.

## Priority criterion

Priority index = `max(65 - regional adoption, 0) / 100 × latest-month transactions`.

The index combines the adoption shortfall with observed activity. It is a decision proxy; it is not a count of transactions that would convert to digital. Regions already at target receive zero in this gap-focused ranking. The index does not estimate marginal investment returns or establish root causes. It is selected for the capstone decision and is not a rule mandated by the course.

The top three are Najran, Jazan and Northern Borders. Together they represent 42.61% of the gap × volume index across the nine lagging regions. This is not 42.61% of users or transactions.

## Metric sensitivity affects the decision

As a sensitivity check, weight the supplied adoption percentages by transaction volume within each region. Then recalculate the same ranking. The resulting top three are Najran, Northern Borders and Al-Baha. The method changes both the overall national index and the third region selected. Weighting is an alternative definition of the index; neither index is a directly observed national digital-transaction share. The presentation uses the supplied lab definition consistently and discloses that Al-Baha replaces Jazan in the alternative ranking. The pilot must confirm the agreed metric and actual service-level demand before further releases. If the decision maker adopts the weighted definition, rerank and reallocate rather than keeping the current allocation.

## Allocation and alternatives

The weighted national December index is 66.118639%, above 65%, versus 63.328346% for the course arithmetic-mean index. National target status therefore reverses under the alternative definition. This reinforces the requirement to agree the metric before using the target gap for funding decisions.

Three options are compared: equal allocation across nine lagging regions; concentration of the full SAR 40 million in the current top three; or staged funding of those three with an evaluation reserve. The recommendation is the staged option: Najran SAR 13M, Jazan SAR 11M, Northern Borders SAR 11M and SAR 5M retained for cross-region measurement and subsequent reassessment. The regional SAR 35M envelope is proportional to the three priority scores, rounded to whole millions using largest remainders. This is a proposed envelope, not an implementation cost estimate. It is not derived from regional population sizes or verified project quotations.

Approve SAR 40M, initially release only SAR 10M for pilots across the three regions (approximately 3.72M, 3.14M, 3.14M), and hold SAR 30M. The SAR 25M remaining regional envelope and SAR 5M evaluation reserve are conditional on validated plans and the day-90 review. The exact procurement amounts depend on quotations and intervention design.

Candidate interventions include assisted digital onboarding and testing friction in high-volume services. These are hypotheses to test, not causes proven by this dataset. Evaluate service-level adoption and user feedback with a suitable comparison; descriptive correlations alone do not prove impact.

## Expected effect and limits

The intended effect is higher adoption in the funded regions while maintaining customer satisfaction and service performance. No causal investment-response model is supplied, so there is no defensible forecast that SAR 40M buys a specified adoption increase.

The deck includes a conditional scenario: if the three selected regional indices each reach 65% and all other regions remain unchanged, the national course index rises from 63.33% to 64.45%. It remains 0.55 percentage points below 65%. This is arithmetic, not a forecast or promise; a further wave would still be required. The scenario follows the course's equally weighted regional definition and must be recalculated if that definition changes.

Day-90 continuation criteria are proposed management thresholds: at least +2 percentage points relative to the verified baseline in each pilot region, no deterioration in the matched service/customer satisfaction and SLA measures, a defensible comparison indicating improvement, and an accepted implementation cost. These are pilot goals, not model predictions. Changes in composition and seasonality must be checked.

## Reproduction

Run `python analysis/analyze.py` with pandas and numpy. It writes summary JSON and evidence CSVs. `analysis/capstone_analysis.ipynb` presents the same method for Colab/Jupyter. The Tableau workbook uses the same source CSV, date and arithmetic-mean definition. `docs/TABLEAU_GUIDE.md` describes how to inspect the workbook and verify the evidence in Tableau.
