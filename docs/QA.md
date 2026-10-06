# Questions and answers

## Why prioritize three regions?

Under the course arithmetic-mean definition, Najran, Jazan and Northern Borders have the highest combination of target gap and December transaction activity. Together they represent 42.61% of the priority index across the nine lagging regions. That is an index share, not a user or transaction share.

## Why select Jazan when Al-Baha has lower adoption?

The rule considers activity as well as the adoption gap. A lower adoption percentage alone does not determine the ranking. The [regional priority table](../analysis/regional_priorities.csv) shows the inputs and resulting scores.

## Is third place a reliable separation?

No. Northern Borders scores 446.26 and Al-Baha 445.60, a difference of approximately 0.66 index units. Treat the third-place choice as sensitive and verify service demand and the metric before funding.

## Does 63.33% mean that 63.33% of transactions were digital?

No. It is the arithmetic mean of the supplied `digital_adoption_pct` values for December 2025, following the course calculation. A directly measured digital-transaction share would require suitable numerator and denominator counts.

## Why use an arithmetic mean?

It follows the course labs and keeps the main story consistent. The analysis also discloses transaction weighting as a sensitivity check. The operational metric must be agreed before any pilot release.

## What changes under transaction weighting?

The national December index becomes 66.12%, above the 65% target. The top-three shortlist becomes Najran, Northern Borders and Al-Baha. This material change is disclosed in the deck and notebook; it prevents treating the shortlist as independent of the metric.

## Does SAR 40M guarantee reaching 65% nationally?

No. There is no observed investment-response model. If the three selected regions reach 65% and all other regions remain unchanged, the national course index reaches approximately 64.45%. This is conditional arithmetic, not a forecast.

## How were SAR 13M, 11M, 11M and 5M calculated?

SAR 35M is distributed in proportion to the three priority scores, then rounded to whole millions using largest remainders. SAR 5M is reserved for evaluation and reassessment. The total is SAR 40M. These are proposed envelopes, not verified local costs.

## How is the initial SAR 10M distributed?

In proportion to the regional envelopes, rounded using largest remainders at SAR 0.01M resolution: Najran 3.72M, Jazan 3.14M and Northern Borders 3.14M. The amounts total exactly 10M. Release requires prior approval of the metric, baseline, comparison design, service plans and costs.

## Is the two-point goal at day 90 a prediction?

No. It is a proposed management goal. Day 90 is counted from envelope approval; actual pilot exposure must be reported, and the review extended if that exposure is insufficient.

## Can satisfaction, time or SLA data prove the cause of low adoption?

No. Descriptive associations can guide investigation but do not establish causation. Use service-level diagnosis and a credible comparison design before making an effectiveness claim.

## Can unique users be summed across the dataset?

No. Individuals may appear across services or channels. Summing those values would risk counting the same person more than once.

## Why not give equal funding to all nine lagging regions?

Equal funding offers broad coverage, approximately SAR 4.44M per region, but ignores differences in gap and activity. It remains a policy option; the proposed staged approach makes its assumptions and uncertainties explicit.

## What if pilot evidence is weak?

Pause further releases, reassess the metric and shortlist, diagnose the service barriers and revise the plan. Do not claim a return that the data do not establish.

## Are these real government performance records?

No. The course file is synthetic training data. The recommendation demonstrates analytical storytelling and decision design; it is not a verified real-world funding case.

## What remains before course submission?

Verify the required Day 2 Tableau evidence or acceptance of the reconstruction, open and inspect the workbook in Tableau, rehearse within seven minutes, verify the required contributor configuration and submit through the instructor's Google Form. See [submission status](SUBMISSION_READY.md).
