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
 'Latest Adoption Product':('real','measure','quantitative','IF [month] = [Latest Month] THEN [digital_adoption_pct] * [unique_users] END'),
 'Latest Users':('integer','measure','quantitative','IF [month] = [Latest Month] THEN [unique_users] END'),
 'National Latest Adoption':('real','measure','quantitative','{ FIXED : SUM([Latest Adoption Product]) } / { FIXED : SUM([Latest Users]) }'),
 'Monthly Adoption':('real','measure','quantitative','{ FIXED [month] : SUM([digital_adoption_pct] * [unique_users]) } / { FIXED [month] : SUM([unique_users]) }'),
 'Regional Adoption':('real','measure','quantitative','{ FIXED [region] : SUM([Latest Adoption Product]) } / { FIXED [region] : SUM([Latest Users]) }'),
 'Gap pp':('real','measure','quantitative','MAX(65 - [Regional Adoption], 0)'),
 'Target':('real','measure','quantitative','65'),
 'Target Status':('string','dimension','nominal','IF [Regional Adoption] < 65 THEN "Below Target" ELSE "On/Above Target" END'),
 'Funding Priority':('string','dimension','nominal','IF [region] = "Najran" OR [region] = "Northern Borders" OR [region] = "Al-Baha" OR [region] = "Jazan" THEN "Four widest gaps" ELSE "Other regions" END'),
}
summary=json.loads((ROOT/'analysis/summary.json').read_text(encoding='utf-8'))
allocation='CASE [region] '+ ' '.join('WHEN "'+r['region']+'" THEN '+str(r['allocation_sar_m']) for r in summary['selected_allocations'])+' ELSE 0 END'
calcs['Allocation SAR M']=('real','measure','quantitative',allocation)
for name,(dtype,role,kind,formula) in calcs.items():
 c=add(ds,'column',name='['+name+']',datatype=dtype,role=role,type=kind)
 if name in ('National Latest Adoption','Monthly Adoption','Regional Adoption'):
  c.set('caption',name+' (%)')
 elif name=='Gap pp':c.set('caption','Gap (percentage points)')
 add(c,'calculation',**{'class':'tableau','formula':formula})
worksheets=add(W,'worksheets')
def q(field,agg='avg',kind='qk'):return f'[tayseer].[{agg}:{field}:{kind}]'
def instance(deps,field,agg='avg',kind='qk'):
 add(deps,'column-instance',column=f'[{field}]',derivation={'avg':'Avg','min':'Min','sum':'Sum','none':'None'}[agg],name=f'[{agg}:{field}:{kind}]',pivot='key',type={'qk':'quantitative','nk':'nominal','ok':'ordinal'}[kind])
def sheet(name,value,agg='min',dimension=None,mark='Bar',ref=False,sort=False,kpi=False,color='Target Status',laggards=False):
 sh=add(worksheets,'worksheet',name=name)
 table=add(sh,'table');view=add(table,'view');ss=add(view,'datasources');add(ss,'datasource',name='tayseer',caption='Tayseer synthetic training data')
 deps=add(view,'datasource-dependencies',datasource='tayseer')
 for c in ds.findall('column'):deps.append(copy.deepcopy(c))
 instance(deps,value,agg)
 if dimension:instance(deps,dimension,'none','nk' if dimension=='region' else 'qk')
 if dimension=='region':
  instance(deps,color,'none','nk')
  if laggards:
   if color!='Target Status':instance(deps,'Target Status','none','nk')
   filt=add(view,'filter',**{'class':'categorical','column':q('Target Status','none','nk')})
   add(filt,'groupfilter',function='member',level=q('Target Status','none','nk'),member='"Below Target"')
 if ref:instance(deps,'Target','min')
 if dimension=='region':add(view,'computed-sort',column=q('region','none','nk'),direction='DESC' if value=='Gap pp' else 'ASC',using=q(value,agg))
 add(view,'aggregation',value='true')
 table_style=add(table,'style')
 if not kpi:
  axis_rule=add(table_style,'style-rule',element='axis')
  add(axis_rule,'encoding',attr='space',**{'class':'0','field':q(value,agg),'field-type':'quantitative','max':'5' if value=='Gap pp' else '100','min':'0','range-type':'fixed','type':'space'})
 pane=add(add(table,'panes'),'pane');add(add(pane,'view'),'breakdown',value='auto');add(pane,'mark',**{'class':mark})
 enc=add(pane,'encodings')
 add(enc,'text',column=q(value,agg))
 if dimension=='region':add(enc,'color',column=q(color,'none','nk'))
 if ref:add(pane,'reference-line',id='ref65',axis_column=q(value,agg),value_column=q('Target','min'),scope='per-table',label_type='custom',label='65% target',z_order='1',formula='constant',value='65',enable_instant_analytics='true')
 style=add(pane,'style');rule=add(style,'style-rule',element='mark');add(rule,'format',attr='mark-labels-show',value='true');add(rule,'format',attr='mark-labels-cull',value='true');add(rule,'format',attr='color',value='#087D82')
 if dimension=='region':
  mapping=add(rule,'encoding',attr='color',field=q(color,'none','nk'),type='palette')
  color_pairs=[('Below Target','#087E87'),('On/Above Target','#D8E6E7')] if color=='Target Status' else [('Four widest gaps','#087E87'),('Other regions','#D8E6E7')]
  for label,hex_color in color_pairs:add(add(mapping,'map',to=hex_color),'bucket','"'+label+'"')
 if kpi:
  add(table,'rows');add(table,'cols')
 elif dimension=='region':
  add(table,'rows',q('region','none','nk'));add(table,'cols',q(value,agg))
 else:
  add(table,'rows',q(value,agg));add(table,'cols',q(dimension,'none','qk'))
 uid(sh)
 return sh
sheet('Latest national weighted adoption', 'National Latest Adoption',kpi=True,mark='Text')
sheet('National monthly adoption toward 65%', 'Monthly Adoption',dimension='month',mark='Line',ref=True)
sheet('Regional adoption December 2025', 'Regional Adoption',dimension='region',ref=True)
sheet('Regional target gaps December 2025', 'Gap pp',dimension='region',color='Funding Priority',laggards=True)
dash=add(add(W,'dashboards'),'dashboard',name='Tayseer investment decision')
add(dash,'style')
add(dash,'size',maxheight='900',maxwidth='1400',minheight='900',minwidth='1400')
zones=add(dash,'zones',is_pixels='true')
def zone(i,x,y,w,h,name=None,title=True):
 z=add(zones,'zone',id=i,x=x,y=y,w=w,h=h,**({'name':name,'show-title':'true' if title else 'false'} if name else {'type-v2':'text'}))
 return z
def txtzone(i,x,y,w,h,text,size=14):
 z=zone(i,x,y,w,h);run=add(add(z,'formatted-text'),'run',text,fontname='Arial',fontsize=size,bold='true');return z
txtzone(1,20,10,1360,60,'Tayseer: SAR 40M for the eight regions below 65%',22)
zone(2,20,90,300,180,'Latest national weighted adoption')
zone(3,340,90,1040,260,'National monthly adoption toward 65%')
zone(4,20,365,680,455,'Regional adoption December 2025')
zone(5,720,365,660,350,'Regional target gaps December 2025')
txtzone(6,720,730,660,90,'SAR M: Najran 13.5; Northern Borders 7.5; Al-Baha 7.5; Jazan 6.5; Asir 2; Tabuk 1.5; Hail 1; Al-Jouf 0.5.',14)
txtzone(7,20,835,1360,55,'Synthetic data. User-weighted adoption. Four widest gaps: 87% of combined gap and SAR 35M. Other four: SAR 5M. Validate costs within 30 days; review after six months.',12)
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
