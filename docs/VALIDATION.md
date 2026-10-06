# Validation

The final baseline is the supplied seven-slide presentation and weighted adoption measure in the shared Tableau reference.

Completed checks:

- Unchanged source SHA-256, 24,960 × 12 data, full 48 × 13 × 8 × 5 grid, no missing cells or duplicate keys.
- Independent recomputation of 66.210761% latest national adoption, 54.142142% first month and eight below-target regions.
- Four widest gaps: 86.957753% of summed positive gaps.
- Eight exact allocations, 40M total, 35M first four, 5M other four and half-million rounding.
- Tableau package: identical source, four worksheets, one dashboard, weighted formulas, target-gap ranking. Official 2026.1 XML schema passes.
- PowerPoint: seven slides, three editable charts, four data series, three embedded spreadsheets and one native allocation table. All series match raw data to reporting precision.
- PowerPoint package, chart/workbook references, fonts and declared geometry pass native structural checks.
- Source file repairs: removed six stale content-type declarations, fixed invalid dash values, normalized single-level chart categories. Filled all 48 workbook month labels and displayed annual labels for readability. Numeric values and final budget story are preserved.
- Seven Arabic note bodies with English visible slide text.
- Seven landscape presentation PDF pages and one Arabic notes PDF page.
- Seven executed notebook code cells without recorded errors; independent results reconciled.
- Local Markdown links resolve.

Run `python analysis/validate_delivery.py`.

These checks establish source/file consistency. Actual Tableau or PowerPoint application execution, timed delivery, collaborator acceptance and Google Form submission require their corresponding external actions.
