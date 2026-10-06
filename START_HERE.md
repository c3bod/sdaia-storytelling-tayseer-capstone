# Open the project

Start with the [seven-slide PDF](deliverables/Tayseer_Executive_Story.pdf). It contains the completed investment story and needs no software setup.

## Open each deliverable

| Deliverable | How to open it | Purpose |
|---|---|---|
| [Presentation PDF](deliverables/Tayseer_Executive_Story.pdf) | Click the link and view it in the browser, or download it. | Read the finished seven-slide story. |
| [Editable PowerPoint](deliverables/Tayseer_Executive_Story_Final.pptx) | Open the link on GitHub, click **Download raw file**, then open the downloaded file in PowerPoint. | Present or edit the slides and their speaking notes. |
| [Tableau workbook](tableau/Tayseer_Investment_Dashboard.twbx) | Download the raw file and open it in Tableau Desktop or Tableau Public. Follow the [Tableau guide](docs/TABLEAU_GUIDE.md). | Inspect the interactive dashboard and four worksheets. Actual Tableau opening remains to be verified. |
| [Analysis notebook](analysis/capstone_analysis.ipynb) | Preview it on GitHub, or open it in Google Colab using **File → Open notebook → GitHub** and paste this repository URL. | Read or reproduce the calculations. |
| [Presentation script](docs/PRESENTATION_SCRIPT.md) | Read it directly on GitHub. | Rehearse the story and explain the charts. |
| [Questions and answers](docs/QA.md) | Read it directly on GitHub. | Prepare for questions about the evidence and recommendation. |

To download everything, open the [repository](https://github.com/c3bod/sdaia-storytelling-tayseer-capstone), click the green **Code** button, choose **Download ZIP**, and extract it. Keep the extracted folders together so data paths continue to work.

## Run the notebook

The saved notebook already contains executed results. To run it again in Colab, first download [the project CSV](data/tayseer_services_synthetic.csv), select **Runtime → Run all**, then upload that CSV when the notebook prompts you. Locally, keep the CSV in the project's `data` folder or beside the notebook.

For a local Python environment, install `requirements.txt`, then run `python analysis/analyze.py` and `python analysis/validate_delivery.py` from the extracted project folder.

## Requirements and completed work

The course requires a seven-slide investment story, a clear funding request within the first 30 seconds and at closing, a presentation of at most seven minutes, Tableau evidence, and a public GitHub repository with a README and tools information. The required Day 2 dashboard and instructor's submission form are not present in the supplied files.

Completed: the PDF and editable PowerPoint, checked source data and analysis, investment scenarios and budget calculations, reconstructed Tableau package, executed notebook, English speaking script, Q&A, methodology, validation report and public repository.

Before final course submission: verify the required Day 2 evidence or obtain acceptance of the reconstructed workbook; open and inspect the workbook in Tableau; rehearse the presentation; verify the required contributor configuration; and submit the repository URL through the instructor's Google Form.

See the [requirements checklist](docs/REQUIREMENTS_CHECKLIST.md) and [submission status](docs/SUBMISSION_READY.md) for the exact distinction between completed artifacts and outstanding course checks.
