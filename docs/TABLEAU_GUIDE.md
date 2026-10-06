# Tableau workbook guide

## Workbook status

The [packaged workbook](../tableau/Tayseer_Investment_Dashboard.twbx) was reconstructed from the supplied CSV. It contains four worksheets and one dashboard named **Tayseer investment decision**. The package includes its data, and its workbook XML passes the official Tableau 2026.1 schema with local namespace-import declarations.

Actual application opening, calculation execution and visual inspection in Tableau remain unverified. The course requests the Day 2 dashboard as the main evidence source; that original dashboard was not supplied. Confirm that requirement or obtain acceptance of this reconstruction before submission. The presentation's editable charts reproduce the data calculations; they are not screenshots exported from Tableau.

## Open and verify

1. Download `Tayseer_Investment_Dashboard.twbx` from GitHub using **Download raw file**.
2. Open it in Tableau Desktop or Tableau Public 2026.1, or a compatible newer version.
3. If the connection needs repair, point it to [the included CSV](../tableau/Data/tayseer_services_synthetic.csv).
4. Open **Tayseer investment decision** and inspect all four worksheets.
5. Confirm that `month` is a date, percentages use the supplied 0–100 scale, region names are readable and the reference target is 65. Avoid a percentage format that turns 65 into 6,500%.
6. Reconcile the displayed results against the table below. Check bars start at zero, labels do not clip and the monthly trend retains all 48 months.
7. If the instructor requires an actual Tableau export in the deck, export the verified view and annotate it while preserving the seven-slide story.

## Expected values

| Check | Expected result |
|---|---|
| Source size | 24,960 rows, 12 columns |
| Latest month | December 2025 |
| January 2022 national course index | 51.402423% |
| December 2025 national course index | 63.328346% |
| Regions below 65% in December | 9 of 13 |
| Najran adoption / transactions / priority | 58.88875% / 9,329 / 570.1185125 |
| Jazan adoption / transactions / priority | 60.66175% / 10,490 / 455.082425 |
| Northern Borders adoption / transactions / priority | 60.91225% / 10,917 / 446.2596675 |
| Al-Baha priority | 445.6011875 |
| Selected share of laggard priority index | 42.614613% |
| Transaction-weighted national sensitivity | 66.118639% |

The third/fourth difference is approximately 0.66 priority units. Transaction weighting changes the shortlist to Najran, Northern Borders and Al-Baha. Neither result is a causal estimate.

## Calculations and aggregation

The workbook uses the latest month from `{ FIXED : MAX([month]) }`. Latest-month adoption and transaction fields return their source values for that month and null otherwise.

- **Regional adoption:** fixed-region arithmetic mean of latest-month adoption.
- **Regional transactions:** fixed-region sum of latest-month transactions.
- **Target gap:** `MAX(65 - [Regional adoption], 0)`.
- **Priority index:** `[Target gap] / 100 * [Regional transactions]`.

The four worksheets show the national latest-month KPI, the complete monthly trend, regional adoption and regional priority. Adoption views average the relevant adoption field. The priority view uses the minimum of the fixed-region priority value, because that value repeats across underlying rows; summing it would inflate the result.

See [methodology](METHODOLOGY.md), [regional priorities](../analysis/regional_priorities.csv) and [the notebook](../analysis/capstone_analysis.ipynb) for independent reproduction. Record successful Tableau opening and reconcile these checks before relying on the workbook during the live presentation.
