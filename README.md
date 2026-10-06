# Tayseer digital adoption capstone

SDAIA Academy SDA-DSC-112. Synthetic training data, January 2022–December 2025.

**Decision: allocate SAR 40M to all eight regions below the 65% adoption target.** Give SAR 35M to the four widest gaps and SAR 5M to the other four. This repository follows the supplied final presentation and the measure in the [shared Tableau reference](https://public.tableau.com/views/Dvis_17912834975050/TayseerDigitalAdoption).

**Big Idea:** National adoption exceeds 65%, but eight regions still lag, so allocate SAR 40M across all eight while directing SAR 35M to the four widest gaps.

## Open the project

| File | How to use it |
|---|---|
| [PowerPoint presentation](deliverables/Tayseer_Executive_Story_Final.pptx) | Download and open in PowerPoint. Seven English slides with short Arabic presenter notes in Notes or Presenter View. |
| [Presentation PDF](deliverables/Tayseer_Executive_Story.pdf) | Read the seven slides directly. |
| [Short Arabic presenter notes](deliverables/Tayseer_Presenter_Notes_AR.pdf) | One page of speaking notes and answers for all seven slides. |
| [Tableau packaged workbook](tableau/Tayseer_Investment_Dashboard.twbx) | Download and open in Tableau Desktop or Tableau Public desktop app. Data are included. |
| [Executed analysis notebook](analysis/capstone_analysis.ipynb) | View the results on GitHub or download and open in Jupyter/Colab. |
| [Regional budget](analysis/budget_allocation.csv) | Open the eight proposed allocations. |

Use [START_HERE](START_HERE.md) for instructions and [requirements checklist](docs/REQUIREMENTS_CHECKLIST.md) for course coverage.

## Findings and recommendation

December 2025 national adoption is **66.21%**, compared with **54.14%** in January 2022. Eight of 13 regions remain below 65%. Najran, Northern Borders, Al-Baha and Jazan hold **86.96% of the combined positive regional gap**.

| Region | Adoption | Gap in percentage points | Proposed SAR M |
|---|---:|---:|---:|
| Najran | 60.86% | 4.14 | 13.5 |
| Northern Borders | 62.70% | 2.30 | 7.5 |
| Al-Baha | 62.78% | 2.22 | 7.5 |
| Jazan | 63.03% | 1.97 | 6.5 |
| Asir | 64.36% | 0.64 | 2.0 |
| Tabuk | 64.48% | 0.52 | 1.5 |
| Hail | 64.74% | 0.26 | 1.0 |
| Al-Jouf | 64.82% | 0.18 | 0.5 |
| **Total** | | | **40.0** |

Adoption = `SUM(digital_adoption_pct * unique_users) / SUM(unique_users)`. Rank regions by positive gap to 65%. Distribute SAR 40M in proportion to these gaps, then round to half a million using largest remainders. This yields exactly SAR 35M for the four widest gaps and SAR 5M for the others.

The figures are a user-weighted index. User counts may overlap across records, so the denominator is a weight rather than a deduplicated population. These data do not establish intervention costs or a guaranteed improvement.

At approval, appoint an implementation lead. Validate local costs and service plans within 30 days before spending. After six months, review adoption, spending and service quality. These dates are proposed checkpoints.

## Reproduce and check

Install Python 3.10 or later, then run from the repository folder:

```text
python -m pip install -r requirements.txt
python analysis/analyze.py
python tableau/build_workbook.py
python analysis/validate_delivery.py
```

The executed notebook independently calculates the same results from the raw CSV. [Methodology](docs/METHODOLOGY.md) explains the formula, rounding, source provenance and limits. [Validation](docs/VALIDATION.md) separates completed checks from live application and submission steps.

The shared Tableau reference belongs to the project supplied by the user. We verified its embedded CSV and weighted calculation. Our packaged workbook adds a monthly trend and gap view from the same source; the published reference itself shows the December snapshot.

Tools used: Python, pandas, NumPy, Plotly, PowerPoint and Tableau workbook XML. [SDAIA Academy on GitHub](https://github.com/SDAIAAcademy).
