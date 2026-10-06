# Data dictionary

Source: the supplied [synthetic training data dictionary](https://drive.google.com/open?id=1htqVTYconACXDD28CACXOpz8VAyz8Xm5). The accompanying CSV contains 24,960 records and 12 columns.

Each record represents one **month × region × service category × channel** combination. Coverage is January 2022 through December 2025: 48 months, 13 Saudi regions, eight service categories and five channels. The dimension grid is complete, with no missing values or duplicate dimension keys.

| Column | Meaning | Unit or interpretation |
|---|---|---|
| `month` | Reporting month. | Date representing a monthly period. |
| `region` | Saudi region. | One of 13 regions. |
| `service_category` | Type of service. | Category, such as licensing. |
| `channel` | Channel used to access the service. | Category, such as mobile app. |
| `transactions` | Recorded transactions for the combination. | Count. |
| `unique_users` | Unique users within the record's scope. | Count; users may overlap across records. |
| `digital_adoption_pct` | Supplied digital adoption measure. | Percentage on a 0–100 scale. |
| `csat` | Customer satisfaction score. | Score out of five. |
| `avg_completion_min` | Average service completion time. | Minutes. |
| `first_time_resolution_pct` | Cases resolved on the first attempt without follow-up. | Percentage on a 0–100 scale. |
| `cost_per_txn_sar` | Cost per transaction. | Saudi riyals per transaction. |
| `sla_breach_pct` | Cases exceeding the agreed service time. | Percentage on a 0–100 scale. |

## Interpretation rules

- All records are synthetic training data; findings do not describe verified real-world service performance.
- The course adoption index is the arithmetic mean of `digital_adoption_pct` in the selected period and geography. It is not a directly measured share of digital transactions.
- Differences between percentages are stated in **percentage points**. Moving from 60% to 65% is a five-point increase.
- Do not sum percentages. Do not sum `unique_users` across services or channels as a national count, because individuals may overlap.
- Transaction weighting is an explicitly disclosed sensitivity analysis. It changes both the national assessment and the regional shortlist.
- The priority index combines the positive target gap with transaction activity. It does not estimate converted transactions, causal impact or financial return.

See [methodology](../docs/METHODOLOGY.md) for formulas and [the executed notebook](../analysis/capstone_analysis.ipynb) for reproducible calculations.
