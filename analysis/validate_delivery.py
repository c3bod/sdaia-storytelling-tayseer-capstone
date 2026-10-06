"""Independently verify source results and delivered capstone files."""
from pathlib import Path
from collections import defaultdict
import csv,hashlib,json,math,re,zipfile,io
import xml.etree.ElementTree as E
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
def readcsv(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def close(a,b,tol=1e-9):assert math.isclose(float(a),float(b),abs_tol=tol),(a,b)
source=ROOT/'data/tayseer_services_synthetic.csv'
summary=json.loads((ROOT/'analysis/summary.json').read_text(encoding='utf-8'))
rows=readcsv(source)
assert len(rows)==24960 and len(rows[0])==12
keys=['month','region','service_category','channel']
assert len({tuple(r[k] for k in keys) for r in rows})==len(rows)
assert all(all(v!='' for v in r.values()) for r in rows)
assert [len({r[k] for r in rows}) for k in keys]==[48,13,8,5]
digest=hashlib.sha256(source.read_bytes()).hexdigest()
assert digest==summary['source_sha256']=='1f8b72a24356f8aa07d983de21e069ed7c36e48a309b03be8a24c99789ab56c6'
def weighted(rs):
    return sum(float(r['digital_adoption_pct'])*int(r['unique_users']) for r in rs)/sum(int(r['unique_users']) for r in rs)
monthly=defaultdict(list)
for r in rows:monthly[r['month']].append(r)
latest=max(monthly);current=monthly[latest]
regions=defaultdict(list)
for r in current:regions[r['region']].append(r)
adoption={r:weighted(rs) for r,rs in regions.items()}
gap={r:max(65-v,0) for r,v in adoption.items()}
funded=sorted((r for r in regions if gap[r]>0),key=lambda r:(-gap[r],r))
assert funded==summary['selected_regions'] and len(funded)==summary['regions_below_target']==8
assert funded[:4]==summary['priority_regions']==['Najran','Northern Borders','Al-Baha','Jazan']
national=weighted(current);first=weighted(monthly[min(monthly)])
close(national,summary['national_latest_pct']);close(first,summary['national_first_pct'])
close(national-first,summary['national_growth_pp'])
close(national-65,summary['national_headroom_pp'])
share=100*sum(gap[r] for r in funded[:4])/sum(gap.values())
close(share,summary['priority_regions_gap_share_pct'])
ideal=[80*gap[r]/sum(gap.values()) for r in funded]
units=[math.floor(x) for x in ideal]
remaining=80-sum(units)
for i in sorted(range(8),key=lambda i:(-(ideal[i]-units[i]),i))[:remaining]:units[i]+=1
allocation={r:u*0.5 for r,u in zip(funded,units)}
assert list(allocation.values())==[13.5,7.5,7.5,6.5,2,1.5,1,0.5]
assert sum(allocation.values())==40
assert sum(allocation[r] for r in funded[:4])==35
assert sum(allocation[r] for r in funded[4:])==5
for r in summary['selected_allocations']:
    close(r['adoption_pct'],adoption[r['region']]);close(r['allocation_sar_m'],allocation[r['region']])
for r in readcsv(ROOT/'analysis/national_trend.csv'):close(r['adoption_pct'],weighted(monthly[r['month']]))
for r in readcsv(ROOT/'analysis/regional_priorities.csv'):
    close(r['adoption_pct'],adoption[r['region']]);close(r['gap_pp'],gap[r['region']])
    close(r['allocation_sar_m'],allocation.get(r['region'],0))
budget=readcsv(ROOT/'analysis/budget_allocation.csv')
assert [r['region'] for r in budget]==funded
for r in budget:close(r['allocation_sar_m'],allocation[r['region']])
for dimension,file in [('channel','channel_evidence.csv'),('service_category','service_evidence.csv')]:
    groups=defaultdict(list)
    for r in current:groups[r[dimension]].append(r)
    for r in readcsv(ROOT/'analysis'/file):close(r['adoption_pct'],weighted(groups[r[dimension]]))
assert readcsv(ROOT/'analysis/latest_month_evidence.csv')==current
print('Independent raw-source results, six evidence CSVs and 40M/35M/5M allocation: PASS')

with zipfile.ZipFile(ROOT/'tableau/Tayseer_Investment_Dashboard.twbx') as z:
    assert z.testzip() is None
    assert hashlib.sha256(z.read('Data/tayseer_services_synthetic.csv')).hexdigest()==digest
    workbook=E.fromstring(z.read('Tayseer_Investment_Dashboard.twb'))
    assert z.read('Tayseer_Investment_Dashboard.twb')==(ROOT/'tableau/Tayseer_Investment_Dashboard.twb').read_bytes()
    assert len(workbook.findall('./worksheets/worksheet'))==4 and len(workbook.findall('./dashboards/dashboard'))==1
    calcs={c.get('name'):c.find('calculation').get('formula') for c in workbook.findall('./datasources/datasource/column') if c.find('calculation') is not None}
    assert '* [unique_users]' in calcs['[Latest Adoption Product]']
    assert 'SUM([Latest Adoption Product])' in calcs['[National Latest Adoption]'] and 'SUM([Latest Users])' in calcs['[National Latest Adoption]']
    assert calcs['[Gap pp]']=='MAX(65 - [Regional Adoption], 0)'
    assert '[Priority Index]' not in calcs and '[Pilot Region]' not in calcs
    assert set(workbook.findall('.//computed-sort')[0].attrib)
    for region,amount in allocation.items():assert f'WHEN "{region}" THEN {amount}' in calcs['[Allocation SAR M]']
print('Tableau package, original data, weighted definitions and allocations: PASS')

ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(ROOT/'deliverables/Tayseer_Executive_Story_Final.pptx') as z:
    assert z.testzip() is None
    slides=sorted(n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n))
    charts=sorted(n for n in z.namelist() if re.fullmatch(r'ppt/charts/chart\d+\.xml',n))
    assert len(slides)==7 and len(charts)==3
    checked=0
    for name in charts:
        doc=E.fromstring(z.read(name))
        for series in doc.findall('.//c:ser',ns):
            cats=[v.text for v in series.findall('./c:cat/c:strRef/c:strCache/c:pt/c:v',ns)]
            values=[float(v.text) for v in series.findall('./c:val/c:numRef/c:numCache/c:pt/c:v',ns)]
            assert len(cats)==len(values)
            if len(values)==48:
                expected=[65]*48 if all(v==65 for v in values) else [weighted(monthly[m]) for m in sorted(monthly)]
                from datetime import date
                assert cats==[date(2022+i//12,i%12+1,1).strftime('%b %Y') for i in range(48)]
            elif len(values)==13:
                labels=[re.sub(r'\s+\d+(?:\.\d+)?%$','',c).strip() for c in cats]
                assert set(labels)==set(regions)
                expected=[adoption[r] for r in labels]
                # All eight below-target points use one color; all five others
                # use another. Validate each point's explicit native color.
                colors={}
                for point in series.findall('c:dPt',ns):
                    index=int(point.find('c:idx',ns).get('val'))
                    color=point.find('.//a:solidFill/a:srgbClr',ns)
                    if color is not None:colors[index]=color.get('val')
                assert len(colors)==13
                below={colors[i] for i,r in enumerate(labels) if gap[r]>0}
                above={colors[i] for i,r in enumerate(labels) if gap[r]==0}
                assert len(below)==len(above)==1 and below!=above
            else:
                assert len(values)==8 and cats==funded
                expected=[gap[r] for r in cats]
            assert all(abs(a-b)<=0.005001 for a,b in zip(values,expected)),name
            checked+=1
    assert checked==4
    tables=[t for n in slides for t in E.fromstring(z.read(n)).findall('.//a:tbl',ns)]
    assert len(tables)==1
    records=[]
    for row in tables[0].findall('a:tr',ns):
        records.append([''.join(t.text or '' for t in cell.findall('.//a:t',ns)) for cell in row.findall('a:tc',ns)])
    actual={}
    for record in records:
        if record[0] in allocation:
            actual[record[0]]=float(record[-1]);close(float(record[1]),gap[record[0]],0.050001)
    assert actual==allocation
    assert float(next(r[-1] for r in records if r[0]=='Four widest gaps'))==35
    assert float(next(r[-1] for r in records if r[0]=='Other four regions'))==5
    assert float(next(r[-1] for r in records if r[0]=='Total'))==40
    for i in range(1,8):
        note=E.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
        text=' '.join(t.text or '' for t in note.findall('.//a:t',ns))
        assert re.search(r'[\u0600-\u06FF]',text) and 'السؤال' in text
    for n in slides:
        text=' '.join(t.text or '' for t in E.fromstring(z.read(n)).findall('.//a:t',ns))
        assert not re.search(r'[\u0600-\u06FF]',text)
    types=E.fromstring(z.read('[Content_Types].xml'))
    assert all(not e.get('PartName') or e.get('PartName').lstrip('/') in z.namelist() for e in types)
    books=[n for n in z.namelist() if re.fullmatch(r'ppt/embeddings/.*\.xlsx',n)]
    assert len(books)==3
    for book in books:
        with zipfile.ZipFile(io.BytesIO(z.read(book))) as wb:
            assert wb.testzip() is None
            root=E.fromstring(wb.read('xl/worksheets/sheet1.xml'))
            assert not root.findall('.//s:f',ns),'Unexpected spreadsheet formula'
print('PowerPoint: four source-matched series, all laggards highlighted, exact budget table and Arabic notes: PASS')
pdf=PdfReader(ROOT/'deliverables/Tayseer_Executive_Story.pdf')
assert len(pdf.pages)==7 and all(float(p.mediabox.width)==960 and float(p.mediabox.height)==540 for p in pdf.pages)
notes=PdfReader(ROOT/'deliverables/Tayseer_Presenter_Notes_AR.pdf')
assert len(notes.pages)==1
print('Presentation PDF: seven landscape pages; Arabic notes PDF: one page: PASS')
nb=json.loads((ROOT/'analysis/capstone_analysis.ipynb').read_text(encoding='utf-8'))
codes=[c for c in nb['cells'] if c['cell_type']=='code']
assert len(codes)==7 and [c['execution_count'] for c in codes]==list(range(1,8))
assert not any(o['output_type']=='error' for c in codes for o in c['outputs'])
for path in [ROOT/'README.md',ROOT/'START_HERE.md',ROOT/'data/DATA_DICTIONARY.md',*list((ROOT/'docs').glob('*.md'))]:
    text=path.read_text(encoding='utf-8')
    for ref in re.findall(r'\]\(([^)]+)\)',text):
        if re.match(r'https?://',ref):continue
        assert (path.parent/ref.split('#')[0]).exists(),(path,ref)
    assert not re.search(r'63\.33|64\.45|nine laggards|day[- ]90|arithmetic.mean|gap x transactions|13M / 11M',text,re.I),path
print('Executed notebook, local document links and stale-baseline checks: PASS')
print('Live Tableau/PowerPoint execution, timed presentation and external course submission are separate checks.')
