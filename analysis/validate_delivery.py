"""Check source calculations, embedded chart values and delivery packages.

Run from any directory: python analysis/validate_delivery.py
These checks do not execute Tableau or measure the team's live delivery.
"""
from pathlib import Path
from collections import defaultdict
from statistics import mean
import csv, hashlib, json, math, re, zipfile
import xml.etree.ElementTree as E
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'data/tayseer_services_synthetic.csv'
summary=json.loads((ROOT/'analysis/summary.json').read_text(encoding='utf-8'))
rows=list(csv.DictReader(source.open(encoding='utf-8',newline='')))
assert len(rows)==24960 and len(rows[0])==12
keys=['month','region','service_category','channel']
assert len({tuple(r[k] for k in keys) for r in rows})==len(rows)
assert all(all(v!='' for v in r.values()) for r in rows)
assert [len({r[k] for r in rows}) for k in keys]==[48,13,8,5]
assert hashlib.sha256(source.read_bytes()).hexdigest()==summary['source_sha256']
monthly=defaultdict(list)
for r in rows: monthly[r['month']].append(r)
latest=max(monthly)
current=monthly[latest]
regions=defaultdict(list)
for r in current: regions[r['region']].append(r)
adoption={k:mean(float(r['digital_adoption_pct']) for r in rs) for k,rs in regions.items()}
activity={k:sum(int(r['transactions']) for r in rs) for k,rs in regions.items()}
priority={k:max(65-adoption[k],0)/100*activity[k] for k in regions}
selected=sorted(priority,key=priority.get,reverse=True)[:3]
national=mean(float(r['digital_adoption_pct']) for r in current)
assert math.isclose(national,summary['national_latest_pct'],abs_tol=1e-10)
assert selected==summary['selected_regions']
assert sum(v<65 for v in adoption.values())==summary['regions_below_target']==9
share=sum(priority[k] for k in selected)/sum(priority.values())*100
assert math.isclose(share,summary['selected_priority_index_share_pct'],abs_tol=1e-10)
scenario=national+sum(65-adoption[k] for k in selected)/13
assert math.isclose(scenario,summary['national_if_selected_reach_65_pct'],abs_tol=1e-10)
assert math.isclose(priority['Northern Borders']-priority['Al-Baha'],0.65848,abs_tol=1e-9)
alloc=summary['selected_allocations']
assert sum(r['allocation_sar_m'] for r in alloc)+summary['reserve_sar_m']==40
assert round(sum(r['pilot_sar_m'] for r in alloc),2)==10
print('Source, national/regional indices, priority near tie, scenario and 40M/10M totals: PASS')

with zipfile.ZipFile(ROOT/'tableau/Tayseer_Investment_Dashboard.twbx') as z:
    assert z.testzip() is None
    assert hashlib.sha256(z.read('Data/tayseer_services_synthetic.csv')).hexdigest()==summary['source_sha256']
    workbook=E.fromstring(z.read('Tayseer_Investment_Dashboard.twb'))
    assert len(workbook.findall('./worksheets/worksheet'))==4
    assert len(workbook.findall('./dashboards/dashboard'))==1
print('Tableau package and source identity: PASS (actual Tableau execution unverified)')

ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(ROOT/'deliverables/Tayseer_Executive_Story_Final.pptx') as z:
    assert z.testzip() is None
    slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
    assert len(slides)==7
    charts=[n for n in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)]
    assert len(charts)==3
    checked=0
    for name in charts:
        doc=E.fromstring(z.read(name))
        for series in doc.findall('.//c:ser',ns):
            cats=[v.text for v in series.findall('./c:cat/c:strRef/c:strCache/c:pt/c:v',ns)]
            values=[float(v.text) for v in series.findall('./c:val/c:numRef/c:numCache/c:pt/c:v',ns)]
            assert len(cats)==len(values)
            if len(cats)==48:
                if all(v==65 for v in values): expected=[65]*48
                else: expected=[mean(float(r['digital_adoption_pct']) for r in monthly[k]) for k in sorted(monthly)]
                assert cats==[k[:7] for k in sorted(monthly)]
            elif len(cats)==13:
                assert set(cats)==set(regions)
                expected=[adoption[k] for k in cats]
            else:
                assert len(cats)==9 and set(cats)=={k for k,v in priority.items() if v>0}
                expected=[priority[k] for k in cats]
            assert all(abs(a-b)<=0.005001 for a,b in zip(values,expected)),name
            checked+=1
    assert checked==4
    assert sum(len(E.fromstring(z.read(n)).findall('.//a:tbl',ns)) for n in slides)==3
print('PPTX: seven slides; three charts / three tables; all four chart series match raw data to reporting precision: PASS')

pdf=PdfReader(ROOT/'deliverables/Tayseer_Executive_Story.pdf')
assert len(pdf.pages)==7
assert all(float(p.mediabox.width)==960 and float(p.mediabox.height)==540 for p in pdf.pages)
print('PDF page count and landscape dimensions: PASS')
nb=json.loads((ROOT/'analysis/capstone_analysis.ipynb').read_text(encoding='utf-8'))
codes=[c for c in nb['cells'] if c['cell_type']=='code']
assert len(codes)==7 and all(c['execution_count'] for c in codes)
assert not any(o['output_type']=='error' for c in codes for o in c['outputs'])
print('Notebook: seven executed cells without recorded errors: PASS')
for path in [ROOT/'README.md',ROOT/'START_HERE.md',*list((ROOT/'docs').glob('*.md'))]:
    for ref in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        if re.match(r'https?://',ref): continue
        assert (path.parent/ref.split('#')[0]).exists(),(str(path),ref)
print('Local Markdown delivery links: PASS')
print('Manual gates remain: original Day 2 evidence alignment, actual Tableau opening/export, timed rehearsal, invitation acceptance and Google Form submission.')
