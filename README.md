# Tayseer Digital Adoption Investment Story

## ابدأ هنا — أين الشغل الفعلي وكيف أفتحه؟

النتيجة الأساسية للمشروع **عرض تقديمي من سبع شرائح**، ومعه ملف Tableau والتحليل الذي يدعم الأرقام. ابدأ بالعرض:

1. **[افتح العرض كـ PDF](deliverables/Tayseer_Executive_Story.pdf)** — لمشاهدة الشرائح. إذا لم تظهر المعاينة، نزّل الملف وافتحه في المتصفح أو قارئ PDF.
2. **[نزّل العرض القابل للتعديل PowerPoint](deliverables/Tayseer_Executive_Story_Final.pptx)** — افتح رابط الملف، نزّله، ثم افتحه في PowerPoint. استخدمه أثناء التقديم ولتعديل الشرائح.
3. **[اقرأ نص الإلقاء العربي](docs/PRESENTATION_SCRIPT_AR.md)** — ماذا يقول كل عضو عند كل شريحة، مع توزيع الوقت.
4. **[نزّل ملف Tableau](tableau/Tayseer_Investment_Dashboard.twbx)** — يفتح داخل Tableau، والبيانات موجودة داخله. [دليل فتحه والتحقق من القيم](docs/TABLEAU_GUIDE.md). فتحه داخل البرنامج ما زال يحتاج التحقق.

مشاهدة العرض والتقديم به لا تتطلب تشغيل Python. استخدم ملفات التحليل عندما تريد إعادة حساب الأرقام أو مراجعة كيفية الوصول إلى التوصية.

| المجلد | محتواه | كيف تستخدمه؟ |
|---|---|---|
| `deliverables` | العرض النهائي بصيغتي PDF وPowerPoint | افتح PDF للمشاهدة، وPowerPoint للتقديم والتعديل |
| `docs` | نص الإلقاء، الأسئلة، المنهجية ودليل التسليم | اقرأ الملفات مباشرة داخل GitHub |
| `tableau` | الداشبورد وبياناته المرفقة | نزّل ملف TWBX وافتحه في Tableau |
| `analysis` | دفتر التحليل والحسابات ونتائجها | شغّل دفتر IPYNB في Colab أو Jupyter عند الحاجة لإعادة الحساب |
| `data` | البيانات الأصلية وقاموس الحقول | المصدر الذي اعتمدنا عليه في التحليل |

لشرح تنزيل الحزمة كاملة وفتح كل نوع ملف، اقرأ [دليل البداية بالعربية](START_HERE_AR.md).

---

SDAIA Academy SDA-DSC-112 capstone in Data Visualization and Storytelling.

**Decision:** approve a hypothetical SAR 40 million envelope to move lagging Tayseer regions toward 65% digital adoption. Release SAR 10M for initial pilots in Najran, Jazan and Northern Borders; hold SAR 30M subject to a day-90 review.

The project interprets the supplied synthetic Tayseer data, compares funding options and presents one seven-slide executive narrative. December 2025 national course adoption is **63.33%**; **9 of 13** regions are below target. The recommended envelope is **Najran 13M, Jazan 11M, Northern Borders 11M, evaluation reserve 5M**. These are proposed allocations, not quoted implementation costs or proven returns.

## Main deliverables

**Release prerequisite:** agree the metric, measured baseline, comparison design, verified shortlist, service plans and costs before any pilot funding or intervention. Name an owner on approval Day 0; launch within 30 days only when ready. Day 90 is counted from envelope approval; report actual exposure and extend evaluation if insufficient.

- [Seven-slide presentation](deliverables/Tayseer_Executive_Story_Final.pptx)
- [Presentation PDF](deliverables/Tayseer_Executive_Story.pdf)
- [Packaged Tableau workbook](tableau/Tayseer_Investment_Dashboard.twbx)
- [Arabic speaking script and handoffs](docs/PRESENTATION_SCRIPT_AR.md)
- [English speaking script](docs/PRESENTATION_SCRIPT_EN.md)
- [Q&A preparation in Arabic](docs/QA_AR.md)
- [Reproducible analysis notebook](analysis/capstone_analysis.ipynb)
- [Method and limitations](docs/METHODOLOGY.md)
- [Tableau opening and verification guide](docs/TABLEAU_GUIDE.md)
- [Requirements traceability and remaining submission steps](docs/REQUIREMENTS_CHECKLIST.md)
- [Independent review, provisional grading and corrections](docs/REVIEW_REPORT.md)

## Dashboard

`tableau/Tayseer_Investment_Dashboard.twbx` packages the original CSV with a Tableau 2026.1 workbook. It contains the latest national KPI, the 48-month national trend with a 65% reference, latest regional adoption with a target reference, and the gap × activity priority ranking. The dashboard also states the proposed allocation and metric sensitivity.

The source grid contains 24,960 records: 48 months × 13 regions × 8 services × 5 channels. Structural checks found no missing cells or duplicate dimension keys. The main metric is the arithmetic mean of `digital_adoption_pct`, matching the supplied labs. It is a course index, not a directly observed digital-transactions share. Priority combines the positive target gap with December transaction volume.

**Material uncertainty:** transaction weighting gives a national index of **66.12%**, above 65%, and selects Al-Baha instead of Jazan in the top three. Target status and the third priority therefore depend on the metric definition. The recommendation requires the decision maker to agree the metric before later releases. No investment-response model is supplied. If the three selected regions each reach 65% and other regions stay unchanged, the national course index reaches only **64.45%**. This is a conditional scenario, not an investment forecast.

**Tableau validation status:** the workbook passes the official Tableau 2026.1 structural XSD, with local declarations for its unlocated namespace imports. The package contains the original CSV and valid relative file paths. Tableau is not installed in the authoring environment, so opening, visual behavior and calculation execution in Tableau have **not** been verified. Open the workbook using the guide and compare its values with the provided evidence before treating it as final Tableau evidence. XSD validation does not guarantee semantic compatibility.

## Team and presentation

| Team member | GitHub | Speaking role | Time |
|---|---|---|---|
| Abdulelah | [@c3bod](https://github.com/c3bod) | Slides 1–2: opening and national situation | 0:00–1:15 |
| Sanad | [@SanadAlkhamali](https://github.com/SanadAlkhamali) | Slides 3–4: regional gap and evidence | 1:15–4:00 |
| Hathal | [@1Hathall](https://github.com/1Hathall) | Slides 5–7: options, recommendation and close | 4:00–7:00 |

These are speaking assignments, not claims about independently completed analytical contributions. All members should rehearse together. State the ask within 30 seconds, repeat it at the close and keep the total presentation within 7 minutes. Use the live Tableau dashboard for supporting evidence and Q&A; the seven slides remain the main presentation.

## Tools and reproduction

Tools used: Python (pandas, numpy and lxml) for analysis and workbook authoring; Jupyter/Colab notebook; Tableau TWB/TWBX format; editable PowerPoint tables and charts; PDF export; Git and GitHub. Codex assisted analysis, writing and artifact generation. The team must review the reasoning and deliver the presentation in its own words.

```text
python -m pip install -r requirements.txt
python analysis/analyze.py
python analysis/validate_delivery.py
```

The analysis writes the evidence CSVs and `analysis/summary.json`. Open the notebook for the calculations and interactive chart inspection. The Tableau builder requires the official XSD and namespace declarations when performing its optional structural validation; the packaged workbook is already supplied.

## Sources and academy link

- [SDAIA Academy on GitHub](https://github.com/SDAIAAcademy)
- [Supplied synthetic CSV](https://drive.google.com/file/d/1T6pweFV4EjBxZ75gge775OOYMYx2aKX0/view)
- [Supplied data dictionary](https://drive.google.com/file/d/1htqVTYconACXDD28CACXOpz8VAyz8Xm5/view)
- [Supplied Lab 2 calculation reference](https://drive.google.com/file/d/1_DAzbKnnIl4dn1JN2hffwhCueJOoqPOh/view)
- [Tableau official document schemas](https://github.com/tableau/tableau-document-schemas)
- [Tableau packaged workbook documentation](https://help.tableau.com/current/pro/desktop/en-us/save_savework_packagedworkbooks.htm)

The academy GitHub organization was located independently. If the instructor specified a different SDAIA repository link, use that exact course link. The original course materials remain unchanged; they are not represented as team-authored content.

## Submission

The evidence slide now ranks all nine lagging regions and annotates target gaps. Northern Borders and Al-Baha differ by only 0.66 priority-index units; this is a near tie, so third-place funding remains provisional pending verified demand and the agreed metric.

Public repository: [c3bod/sdaia-storytelling-tayseer-capstone](https://github.com/c3bod/sdaia-storytelling-tayseer-capstone). [Submission details and final team handoff](docs/SUBMISSION_READY.md).

Write-access invitations were issued on 2026-10-06. The final access check confirms `SanadAlkhamali` has write access; `1Hathall` still has a pending invitation. Access and invitations do not imply completed analytical contributions.

Copy this public repository URL into the instructor's Google Form. The form URL has not been supplied, so form submission remains outstanding. Collaborator invitations must be accepted by teammates before access is active. Tableau opening/visual verification and a timed team rehearsal remain necessary before final submission.
