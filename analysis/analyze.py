"""Reproduce the capstone evidence from the supplied synthetic CSV."""
from pathlib import Path
import json, hashlib
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/tayseer_services_synthetic.csv'
OUT = ROOT / 'analysis'
df = pd.read_csv(SOURCE, parse_dates=['month'])
keys = ['month', 'region', 'service_category', 'channel']
assert df.shape == (24960, 12)
assert not df.isna().any().any()
assert not df.duplicated(keys).any()
assert len(df) == 48 * 13 * 8 * 5
assert df['digital_adoption_pct'].between(0, 100).all()
assert df['csat'].between(1, 5).all()
assert (df['transactions'] > 0).all()
latest = df['month'].max()
current = df[df['month'] == latest].copy()
trend = df.groupby('month').agg(adoption_pct=('digital_adoption_pct', 'mean'), transactions=('transactions', 'sum')).reset_index()
trend['target_pct'] = 65.0
weighted = df.assign(product=df.digital_adoption_pct * df.transactions).groupby('month').agg(product=('product','sum'),transactions=('transactions','sum'))
trend['transaction_weighted_adoption_pct'] = weighted['product'].to_numpy() / weighted['transactions'].to_numpy()
regional = current.groupby('region').agg(adoption_pct=('digital_adoption_pct','mean'),transactions=('transactions','sum'),csat=('csat','mean'),completion_min=('avg_completion_min','mean'),sla_breach_pct=('sla_breach_pct','mean')).reset_index()
regional['gap_pp'] = np.maximum(65 - regional.adoption_pct, 0)
# This is an index for ranking, not a count of non-digital transactions.
regional['priority_index'] = regional.gap_pp / 100 * regional.transactions
wr = current.assign(product=current.digital_adoption_pct * current.transactions).groupby('region').agg(product=('product','sum'),transactions=('transactions','sum'))
regional['weighted_adoption_pct'] = regional.region.map(wr['product'] / wr['transactions'])
regional['weighted_priority_index'] = np.maximum(65 - regional.weighted_adoption_pct,0)/100*regional.transactions
regional = regional.sort_values('priority_index',ascending=False).reset_index(drop=True)
regional['priority_rank'] = range(1,14)
top = regional.head(3).copy()
shares = top.priority_index / top.priority_index.sum()
ideal = shares.to_numpy() * 35
alloc = np.floor(ideal).astype(int)
for i in np.argsort(-(ideal - alloc))[:35-int(alloc.sum())]: alloc[i]+=1
top['allocation_sar_m'] = alloc
pilot_ideal = top.allocation_sar_m.to_numpy() / 35 * 1000
pilot_units = np.floor(pilot_ideal).astype(int)
for i in np.argsort(-(pilot_ideal - pilot_units))[:1000-int(pilot_units.sum())]: pilot_units[i]+=1
top['pilot_sar_m'] = pilot_units / 100
assert round(top.pilot_sar_m.sum(),2) == 10
top['score_share_of_laggards_pct'] = top.priority_index / regional.priority_index.sum() * 100
top['later_regional_release_sar_m'] = top.allocation_sar_m - top.pilot_sar_m
weighted_top = regional.sort_values('weighted_priority_index',ascending=False).head(3).region.tolist()
channels = current.groupby('channel').agg(transactions=('transactions','sum'),adoption_pct=('digital_adoption_pct','mean'),completion_min=('avg_completion_min','mean'),csat=('csat','mean')).reset_index()
services = current.groupby('service_category').agg(transactions=('transactions','sum'),completion_min=('avg_completion_min','mean'),csat=('csat','mean')).reset_index()
summary = {
 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'rows':len(df),'columns':len(df.columns),'start_month':df.month.min().strftime('%Y-%m'),'latest_month':latest.strftime('%Y-%m'),
 'national_latest_pct':float(current.digital_adoption_pct.mean()),'national_first_pct':float(trend.adoption_pct.iloc[0]),
 'national_gap_pp':float(65-current.digital_adoption_pct.mean()),'national_growth_pp':float(trend.adoption_pct.iloc[-1]-trend.adoption_pct.iloc[0]),
 'regions_below_target':int((regional.adoption_pct<65).sum()),'total_regions':13,
 'national_transaction_weighted_latest_pct':float(trend.transaction_weighted_adoption_pct.iloc[-1]),
 'selected_regions':top.region.tolist(),'selected_priority_index_share_pct':float(top.priority_index.sum()/regional.priority_index.sum()*100),
 'selected_transaction_share_of_laggards_pct':float(top.transactions.sum()/regional[regional.gap_pp>0].transactions.sum()*100),
 'weighted_sensitivity_top3':weighted_top,'weighted_top3_same':set(weighted_top)==set(top.region),
 'budget_sar_m':40,'regional_budget_sar_m':35,'reserve_sar_m':5,'initial_pilot_sar_m':10,'held_sar_m':30,
 'target_pct':65,'national_if_selected_reach_65_pct':float(current.digital_adoption_pct.mean()+top.gap_pp.sum()/13),
 'metric_method':'Arithmetic mean of digital_adoption_pct, matching supplied labs. This is a course index, not digital transactions / total transactions.',
 'priority_method':'max(65 - arithmetic mean adoption, 0) / 100 * latest-month transactions. Proxy index; not a missing-conversion count.',
 'synthetic':True,'missing_cells':int(df.isna().sum().sum()),'duplicate_keys':int(df.duplicated(keys).sum()),
 'selected_allocations':json.loads(top.to_json(orient='records')),
 'data_sources':{'csv':'https://drive.google.com/file/d/1T6pweFV4EjBxZ75gge775OOYMYx2aKX0/view','dictionary':'https://drive.google.com/file/d/1htqVTYconACXDD28CACXOpz8VAyz8Xm5/view','lab2':'https://drive.google.com/file/d/1_DAzbKnnIl4dn1JN2hffwhCueJOoqPOh/view'}
}
OUT.mkdir(exist_ok=True)
trend.to_csv(OUT/'national_trend.csv',index=False,date_format='%Y-%m-%d')
regional.to_csv(OUT/'regional_priorities.csv',index=False)
top.to_csv(OUT/'budget_allocation.csv',index=False)
channels.to_csv(OUT/'channel_evidence.csv',index=False)
services.to_csv(OUT/'service_evidence.csv',index=False)
current.to_csv(OUT/'latest_month_evidence.csv',index=False,date_format='%Y-%m-%d')
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['national_latest_pct','regions_below_target','selected_regions','selected_priority_index_share_pct','weighted_sensitivity_top3','weighted_top3_same']},ensure_ascii=False))
print(top[['region','adoption_pct','gap_pp','transactions','priority_index','allocation_sar_m']].to_string(index=False))
