# Tableau guide

Download [the packaged workbook](../tableau/Tayseer_Investment_Dashboard.twbx) and open it in Tableau Desktop or Tableau Public desktop app. It includes the original CSV.

| Worksheet | Evidence |
|---|---|
| Latest national weighted adoption | December 2025 national result, 66.21%. |
| National monthly adoption toward 65% | All 48 months and the 65% target. |
| Regional adoption December 2025 | All 13 weighted values, ascending, with target status and 65% reference. |
| Regional target gaps December 2025 | Eight positive gaps, descending, with the four widest distinguished. |

The latest-month, monthly and regional calculations use user weights. MIN displays each fixed result without summing repeated LOD values. All eight laggards, including Al-Baha, have Below Target status and a dark teal color mapping. Other regions use a pale color. Adoption axes span 0–100, gap axes span 0–5 points, and field captions state the units. The dashboard states all eight amounts and the 35M/5M split.

The [shared reference](https://public.tableau.com/views/Dvis_17912834975050/TayseerDigitalAdoption) uses the same definition and December snapshot. It is credited as supplied reference evidence, not as our authored dashboard.

The package, data identity, formulas and official Tableau 2026.1 XML schema pass checks. Actual opening and rendering in Tableau remain unverified here. For an unpackaged TWB requiring a source repair, select the included Data/tayseer_services_synthetic.csv.

For Q&A explain national success versus regional gaps, 87% as summed-gap share, the gap-based allocation rule and the need to validate local costs.

Rebuild with `python tableau/build_workbook.py`. [Methodology](METHODOLOGY.md).
