# Methodology

Synthetic course CSV: 24,960 rows, 12 columns, 48 months, 13 regions, eight services and five channels. Each row is month × region × service × channel. Coverage: January 2022–December 2025.

The supplied final presentation is the story baseline. The [shared Tableau reference](https://public.tableau.com/views/Dvis_17912834975050/TayseerDigitalAdoption) belongs to the user-supplied project. Its embedded CSV is byte-identical to our source, and its two worksheets filter December 2025. Our monthly trend is additionally computed from the full CSV using the same weighted definition.

## Formula and results

`adoption (%) = SUM(digital_adoption_pct * unique_users) / SUM(unique_users)`

Percentages already use a 0–100 scale. Tableau's division by 100 before weighting and multiplication by 100 afterward is equivalent.

For December regions, `gap_pp = MAX(65 - adoption, 0)`. Rank positive gaps descending, with region name as a deterministic tie-breaker. Transaction activity does not set this ranking.

National adoption: 66.210761%, versus 54.142142% in January 2022. Growth: 12.068619 points. Headroom: 1.210761 points. Eight of 13 regions are below 65%.

Najran, Northern Borders, Al-Baha and Jazan have the four widest gaps. Their combined gaps divided by all eight positive gaps equal 86.957753%, displayed as 87%. This is a share of summed gaps, not people or transactions.

## Budget

Compute `40 * gap / total positive gap` million SAR per laggard. Divide ideals by 0.5, floor the unit counts, then distribute remaining units to the largest fractional remainders. Ties retain gap order. Exactly 80 half-million units are allocated.

| Region | SAR M |
|---|---:|
| Najran | 13.5 |
| Northern Borders | 7.5 |
| Al-Baha | 7.5 |
| Jazan | 6.5 |
| Asir | 2 |
| Tabuk | 1.5 |
| Hail | 1 |
| Al-Jouf | 0.5 |
| Total | 40 |

First four: 35M. Other four: 5M. Alternatives are 5M per laggard or 10M per region in the four widest gaps.

## Limits and follow-up

The metric is a user-weighted index, not an independently observed digital-transaction share. Users may overlap across services and channels; summed weights are not a deduplicated population. Synthetic observations do not establish intervention costs, causes, financial return or a numeric investment effect.

Approve the full regional allocation and appoint a lead. Validate local service plans and costs within 30 days before spending. Review adoption, spending and service quality after six months. These dates are proposed.

Source SHA-256: `1f8b72a24356f8aa07d983de21e069ed7c36e48a309b03be8a24c99789ab56c6`.

[Analysis](../analysis/analyze.py), [independent notebook](../analysis/capstone_analysis.ipynb), [validation](VALIDATION.md).
