"""Author a packaged Tableau workbook from the supplied synthetic source."""
from pathlib import Path
from lxml import etree as E
import json,uuid,zipfile,copy,shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tableau'
DATA=OUT/'Data'
DATA.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'data/tayseer_services_synthetic.csv',DATA/'tayseer_services_synthetic.csv')
def add(parent,tag,text=None,**attrs):
 e=E.SubElement(parent,tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
 if text is not None:e.text=text
 return e
def uid(parent):add(parent,'simple-id',uuid='{'+str(uuid.uuid4()).upper()+'}')
W=E.Element('workbook',{'original-version':'26.1','source-build':'0.0.0 (0000.0.0.0)','source-platform':'win','version':'26.1'},nsmap={'user':'http://www.tableausoftware.com/xml/user'})
add(add(W,'document-format-change-manifest'),'ManifestByVersion')
prefs=add(W,'preferences');add(prefs,'preference',name='ui.encoding.shelf.height',value='24')
sources=add(W,'datasources')
ds=add(sources,'datasource',name='tayseer',caption='Tayseer synthetic training data',inline='true',version='26.1')
conn=add(ds,'connection',**{'class':'textscan','directory':'Data','filename':'tayseer_services_synthetic.csv','password':'','server':''})
rel=add(conn,'relation',name='tayseer_services_synthetic',table='[tayseer_services_synthetic.csv]',type='table')
rc=add(rel,'columns',header='yes',separator=',',locale='en_US')
fields=[('month','date','dimension','ordinal'),('region','string','dimension','nominal'),('service_category','string','dimension','nominal'),('channel','string','dimension','nominal'),('transactions','integer','measure','quantitative'),('unique_users','integer','measure','quantitative'),('digital_adoption_pct','real','measure','quantitative'),('csat','real','measure','quantitative'),('avg_completion_min','real','measure','quantitative'),('first_time_resolution_pct','real','measure','quantitative'),('cost_per_txn_sar','real','measure','quantitative'),('sla_breach_pct','real','measure','quantitative')]
for ordinal,(name,dtype,role,kind) in enumerate(fields):add(rc,'column',name=name,datatype=dtype,ordinal=ordinal)
add(ds,'aliases',enabled='yes')
for name,dtype,role,kind in fields:add(ds,'column',name='['+name+']',datatype=dtype,role=role,type=kind)
calcs={
 'Latest Month':('date','dimension','ordinal','{ FIXED : MAX([month]) }'),
 'Latest Adoption':('real','measure','quantitative','IF [month] = [Latest Month] THEN [digital_adoption_pct] END'),
 'Latest Transactions':('integer','measure','quantitative','IF [month] = [Latest Month] THEN [transactions] END'),
 'Regional Adoption':('real','measure','quantitative','{ FIXED [region] : AVG([Latest Adoption]) }'),
 'Regional Transactions':('integer','measure','quantitative','{ FIXED [region] : SUM([Latest Transactions]) }'),
 'Gap pp':('real','measure','quantitative','MAX(65 - [Regional Adoption], 0)'),
 'Priority Index':('real','measure','quantitative','[Gap pp] / 100 * [Regional Transactions]'),
 'Target':('real','measure','quantitative','65'),
 'Pilot Region':('string','dimension','nominal','IF [region] = "Najran" OR [region] = "Jazan" OR [region] = "Northern Borders" THEN "Pilot" ELSE "Other" END'),
}
for name,(dtype,role,kind,formula) in calcs.items():
 c=add(ds,'column',name='['+name+']',datatype=dtype,role=role,type=kind)
 add(c,'calculation',**{'class':'tableau','formula':formula})
worksheets=add(W,'worksheets')
def q(field,agg='avg',kind='qk'):return f'[tayseer].[{agg}:{field}:{kind}]'
def instance(deps,field,agg='avg',kind='qk'):
 add(deps,'column-instance',column=f'[{field}]',derivation={'avg':'Avg','min':'Min','sum':'Sum','none':'None'}[agg],name=f'[{agg}:{field}:{kind}]',pivot='key',type={'qk':'quantitative','nk':'nominal','ok':'ordinal'}[kind])
def sheet(name,value,agg='avg',dimension=None,mark='Bar',ref=False,sort=False,kpi=False):
 sh=add(worksheets,'worksheet',name=name)
 table=add(sh,'table');view=add(table,'view');ss=add(view,'datasources');add(ss,'datasource',name='tayseer',caption='Tayseer synthetic training data')
 deps=add(view,'datasource-dependencies',datasource='tayseer')
 for c in ds.findall('column'):deps.append(copy.deepcopy(c))
 instance(deps,value,agg)
 if dimension:instance(deps,dimension,'none','nk' if dimension=='region' else 'qk')
 if dimension=='region':instance(deps,'Pilot Region','none','nk')
 if ref:instance(deps,'Target','min')
 if dimension=='region':add(view,'computed-sort',column=q('region','none','nk'),direction='DESC' if value=='Priority Index' else 'ASC',using=q(value,agg))
 add(view,'aggregation',value='true')
 add(table,'style')
 pane=add(add(table,'panes'),'pane');add(add(pane,'view'),'breakdown',value='auto');add(pane,'mark',**{'class':mark})
 enc=add(pane,'encodings')
 add(enc,'text',column=q(value,agg))
 if dimension=='region':add(enc,'color',column=q('Pilot Region','none','nk'))
 if ref:add(pane,'reference-line',id='ref65',axis_column=q(value,agg),value_column=q('Target','min'),scope='per-table',label_type='custom',label='65% target',z_order='1',formula='constant',value='65',enable_instant_analytics='true')
 style=add(pane,'style');rule=add(style,'style-rule',element='mark');add(rule,'format',attr='mark-labels-show',value='true');add(rule,'format',attr='mark-labels-cull',value='true');add(rule,'format',attr='color',value='#087D82')
 if kpi:
  add(table,'rows');add(table,'cols')
 elif dimension=='region':
  add(table,'rows',q('region','none','nk'));add(table,'cols',q(value,agg))
 else:
  add(table,'rows',q(value,agg));add(table,'cols',q(dimension,'none','qk'))
 uid(sh)
 return sh
sheet('Latest national course index', 'Latest Adoption',kpi=True,mark='Text')
sheet('National monthly adoption toward 65%', 'digital_adoption_pct',dimension='month',mark='Line',ref=True)
sheet('Regional adoption December 2025', 'Latest Adoption',dimension='region',ref=True)
sheet('Gap and volume priority December 2025', 'Priority Index',agg='min',dimension='region')
dash=add(add(W,'dashboards'),'dashboard',name='Tayseer investment decision')
add(dash,'style')
add(dash,'size',maxheight='900',maxwidth='1400',minheight='900',minwidth='1400')
zones=add(dash,'zones',is_pixels='true')
def zone(i,x,y,w,h,name=None,title=True):
 z=add(zones,'zone',id=i,x=x,y=y,w=w,h=h,**({'name':name,'show-title':'true' if title else 'false'} if name else {'type-v2':'text'}))
 return z
def txtzone(i,x,y,w,h,text,size=14):
 z=zone(i,x,y,w,h);run=add(add(z,'formatted-text'),'run',text,fontname='Arial',fontsize=size,bold='true');return z
txtzone(1,20,10,1360,60,'Tayseer: phased SAR 40M investment toward 65% adoption',22)
zone(2,20,90,300,180,'Latest national course index')
zone(3,340,90,1040,260,'National monthly adoption toward 65%')
zone(4,20,365,680,455,'Regional adoption December 2025')
zone(5,720,365,660,350,'Gap and volume priority December 2025')
txtzone(6,720,730,660,90,'Proposed SAR M: Najran 13; Jazan 11; Northern Borders 11; reserve 5. Release only 10M initially; review at day 90.',14)
txtzone(7,20,835,1360,55,'Synthetic training data. Arithmetic-mean course index. Priority = gap x transactions (proxy). Transaction weighting selects Al-Baha instead of Jazan. Agree the metric before scaling.',12)
uid(dash)
add(W,'thumbnails')
add(add(W,'explain-data',enabled_for_viewer='false',extreme_values_enabled_for_all='false'),'explanation-types')
path=OUT/'Tayseer_Investment_Dashboard.twb'
E.ElementTree(W).write(str(path),encoding='utf-8',xml_declaration=True,pretty_print=True)
schema_file=ROOT/'.private/build/tableau.xsd'
if schema_file.exists():
 schema_tree=E.parse(str(schema_file))
 # The official file imports namespaces without locations. Supply extension
 # declarations locally; the source workbook has no user extension attributes.
 for imp in schema_tree.findall('{http://www.w3.org/2001/XMLSchema}import'):
  file='user.xsd' if imp.get('namespace')=='http://www.tableausoftware.com/xml/user' else 'xml.xsd'
  imp.set('schemaLocation',(schema_file.parent/file).as_uri())
 schema=E.XMLSchema(schema_tree)
 valid=schema.validate(E.parse(str(path)))
 report={'xsd_valid':valid,'schema':'Tableau official 2026.1 XSD with local declarations for its unlocated user and xml imports','semantic_open_in_tableau_verified':False,'errors':[str(e) for e in schema.error_log]}
 (ROOT/'.private/tableau_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps(report,indent=2))
 if not valid:raise SystemExit(1)
with zipfile.ZipFile(OUT/'Tayseer_Investment_Dashboard.twbx','w',zipfile.ZIP_DEFLATED) as z:
 z.write(path,path.name);z.write(DATA/'tayseer_services_synthetic.csv','Data/tayseer_services_synthetic.csv')
print('Packaged workbook created with the original CSV.')
