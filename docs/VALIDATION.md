# Delivery checks

Checked on 2026-10-06.

- Source CSV: 24,960 × 12; complete 48 × 13 × 8 × 5 grid, no missing cells or duplicate dimension keys. SHA-256 recorded in `analysis/summary.json`.
- Independent notebook: seven executed calculation cells, no errors; national adoption, selected regions, score share, weighted sensitivity, conditional scenario and allocations reconciled with the analysis summary.
- Budget: 13 + 11 + 11 + 5 = 40M. Pilot amounts use largest remainders at 0.01M resolution: 3.72 + 3.14 + 3.14 = 10M.
- PowerPoint: seven slides, two native editable charts, four native tables; package and presentation font checks passed. The final exported PPTX was reimported and every slide rendered and visually inspected.
- PDF: seven 16:9 pages, generated from the reviewed final PowerPoint renders; exported pages rendered separately for inspection.
- Tableau package: four worksheets, one dashboard; packaged CSV matches the source SHA. Official Tableau 2026.1 XSD passed using local namespace-import declarations. No actual Tableau application opening, calculation execution or visual verification was performed.
- All local delivery links in README, start guide and documentation resolve.

These checks support the prepared artifacts; they do not establish investment effectiveness or successful live Tableau execution. Timed team rehearsal, Tableau opening verification and the instructor's Google Form submission remain outstanding.
