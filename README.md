# Tayseer Digital Adoption Investment Story

SDAIA Academy SDA-DSC-112 capstone in Data Visualization and Storytelling.

The project recommends how to allocate a hypothetical **SAR 40 million** to move lagging Tayseer regions toward the **65% digital-adoption target**, using the supplied synthetic course data.

## Open the completed work

- **[View the seven-slide PDF](deliverables/Tayseer_Executive_Story.pdf)** — view the presentation or download it if the browser preview is unavailable.
- **[Download the editable PowerPoint](deliverables/Tayseer_Executive_Story_Final.pptx)** — seven slides in simple English, with presenter notes on every slide.
- **[Download the Tableau workbook](tableau/Tayseer_Investment_Dashboard.twbx)** — open the packaged file in Tableau. [Verification guide](docs/TABLEAU_GUIDE.md).
- **[Open the analysis notebook](analysis/capstone_analysis.ipynb)** — inspect the calculations or run them in Colab/Jupyter.

Viewing the PDF and presenting the PowerPoint do not require Python. [Opening instructions](START_HERE.md).

In PowerPoint, use **Slide Show → Use Presenter View** with a separate audience display to see your notes while the audience sees only the slides. Read the **SAY** section; use **IF ASKED** for extra answers. The notes include the required questions, chart colors and the Al-Baha comparison.

## Project requirements

- Recommend an allocation of SAR 40M toward the 65% adoption target.
- Produce exactly seven slides: BLUF/Ask, Situation, Complication, Evidence, Options, Recommendation, and Ask + Next Step.
- Use one main message and a takeaway title on each slide.
- State a Big Idea combining point of view, stakes and action.
- State the ask within the first 30 seconds and repeat it at the close; keep the presentation within seven minutes.
- Use the Day 2 Tableau dashboard as the main evidence source, with live Tableau available for supporting evidence and Q&A.
- Publish the presentation in a public GitHub repository with a README describing the project, dashboard and tools, the required contributor configuration and a SDAIA GitHub link.
- Submit the public repository URL through the instructor's Google Form.

[Detailed requirements and completion status](docs/REQUIREMENTS_CHECKLIST.md).

## Completed work

- Prepared the seven-slide executive presentation in simple English, with speaking notes and answers inside each PowerPoint slide, and a matching PDF.
- Analyzed 24,960 records across 48 months, 13 regions, eight services and five channels; checked the complete grid, missing cells and duplicate dimension keys.
- Calculated the national trend, latest regional gaps and a gap × transaction-volume priority index.
- Compared three funding options and proposed a staged SAR 40M envelope: Najran 13M, Jazan 11M, Northern Borders 11M and a 5M evaluation reserve.
- Specified an initial 10M pilot authorization, conditional on approved metric, baseline, comparison design, verified shortlist, service plans and costs before any funding release or intervention. Hold 30M for review.
- Disclosed metric sensitivity, the near tie between Northern Borders and Al-Baha, and the limits of the conditional national scenario.
- Prepared a Tableau TWB/TWBX package with four worksheets, one dashboard and the original CSV; passed structural schema and source-package checks.
- Prepared and executed a reproducible notebook, English presentation script, Q&A notes, data dictionary, methodology and opening guide.
- Checked all four embedded chart series against source calculations, verified the package and budget totals, and visually inspected the final slides and PDF pages.
- Published the presentation and supporting files in this public repository.

## Findings and limitations

December 2025 adoption is **63.33%** under the course arithmetic-mean definition, with **nine of thirteen regions** below 65%. The proposed three regions represent **42.61%** of the laggards' gap × volume index. Northern Borders and Al-Baha are separated by only **0.66 index units**.

Transaction weighting gives a national index of **66.12%**, above target, and selects Al-Baha instead of Jazan. Agree the metric before releasing pilot funding; a changed definition requires reranking and reallocating. Neither index is a verified digital-transactions share.

If the three selected regions each reach 65% and other regions remain unchanged, the national course index reaches **64.45%**. This is conditional arithmetic, not an investment forecast. Funding amounts are proposed envelopes, not verified implementation costs. All observations are synthetic training data.

The original Day 2 dashboard was not supplied. The replacement was built from the course CSV and structurally validated, but it has **not been opened or executed in Tableau**. Day 2 evidence alignment, actual Tableau verification/export, timed rehearsal, final contributor verification and Google Form submission remain outstanding. The form URL was not supplied.

## Supporting documentation

- [English presentation script](docs/PRESENTATION_SCRIPT.md)
- [Q&A notes](docs/QA.md)
- [Methodology](docs/METHODOLOGY.md)
- [Data dictionary](data/DATA_DICTIONARY.md)
- [Verification record](docs/VALIDATION.md)
- [Independent review and corrections](docs/REVIEW_REPORT.md)
- [Submission requirements and status](docs/SUBMISSION_READY.md)

## Tools and reproduction

Tools: Python with pandas, numpy and lxml; Colab/Jupyter and Plotly; Tableau TWB/TWBX format; editable PowerPoint charts and tables; PDF export; Git and GitHub. Codex assisted the analysis, writing and artifact generation.

```text
python -m pip install -r requirements.txt
python analysis/analyze.py
python analysis/validate_delivery.py
```

The analysis produces evidence CSVs and summary JSON. Validation checks calculations, native chart data, presentation structure, budgets, the packaged source, notebook outputs and local documentation links. It does not execute Tableau or assess live delivery.

## Sources

- [SDAIA Academy on GitHub](https://github.com/SDAIAAcademy)
- [Supplied synthetic CSV](https://drive.google.com/file/d/1T6pweFV4EjBxZ75gge775OOYMYx2aKX0/view)
- [Supplied dictionary](https://drive.google.com/file/d/1htqVTYconACXDD28CACXOpz8VAyz8Xm5/view)
- [Supplied Lab 2 calculation reference](https://drive.google.com/file/d/1_DAzbKnnIl4dn1JN2hffwhCueJOoqPOh/view)
- [Official Tableau document schemas](https://github.com/tableau/tableau-document-schemas)

The academy link was located independently; use the exact instructor-specified course link if supplied separately. Original course files are preserved unchanged outside the published deliverables.
