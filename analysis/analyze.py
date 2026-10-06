"""Reproduce the final presentation using the shared Tableau definition."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/tayseer_services_synthetic.csv'
OUT = ROOT / 'analysis'
df = pd.read_csv(SOURCE, parse_dates=['month'])
keys = ['month', 'region', 'service_category', 'channel']
assert df.shape == (24960, 12) and not df.isna().any().any()
assert not df.duplicated(keys).any()
assert [df[k].nunique() for k in keys] == [48, 13, 8, 5]
assert df.digital_adoption_pct.between(0, 100).all()
assert df.csat.between(1, 5).all()
assert (df.transactions > 0).all() and (df.unique_users > 0).all()
latest = df.month.max()
current = df[df.month == latest].copy()

def adoption_table(frame, dimension):
    """Use users as weights, without treating their sum as distinct people."""
    table = frame.assign(adoption_product=frame.digital_adoption_pct * frame.unique_users).groupby(dimension).agg(
        adoption_product=('adoption_product', 'sum'), user_weight=('unique_users', 'sum'),
        transactions=('transactions', 'sum')).reset_index()
    table['adoption_pct'] = table.adoption_product / table.user_weight
    return table.drop(columns='adoption_product')

trend = adoption_table(df, 'month')
trend['target_pct'] = 65.0
regional = adoption_table(current, 'region')
regional['gap_pp'] = np.maximum(65 - regional.adoption_pct, 0)
regional['target_status'] = np.where(regional.gap_pp > 0, 'Below Target', 'On/Above Target')
regional = regional.sort_values(['gap_pp', 'region'], ascending=[False, True]).reset_index(drop=True)
regional['priority_rank'] = np.where(regional.gap_pp > 0, np.arange(1, len(regional)+1), 0)
funded = regional[regional.gap_pp > 0].copy().reset_index(drop=True)
total_gap = float(funded.gap_pp.sum())
funded['gap_share_pct'] = funded.gap_pp / total_gap * 100
funded['ideal_allocation_sar_m'] = 40 * funded.gap_pp / total_gap
# Allocate 80 half-million units. Largest remainders keep the total exact.
ideal_units = funded.ideal_allocation_sar_m.to_numpy() / 0.5
units = np.floor(ideal_units).astype(int)
order = np.argsort(-(ideal_units - units), kind='stable')
for i in order[:80-int(units.sum())]:
    units[i] += 1
funded['allocation_sar_m'] = units * 0.5
funded['allocation_tier'] = ['Four widest gaps'] * 4 + ['Other four regions'] * 4
expected = {'Najran':13.5, 'Northern Borders':7.5, 'Al-Baha':7.5, 'Jazan':6.5,
            'Asir':2.0, 'Tabuk':1.5, 'Hail':1.0, 'Al-Jouf':0.5}
assert dict(zip(funded.region, funded.allocation_sar_m)) == expected
assert funded.allocation_sar_m.sum() == 40
regional['allocation_sar_m'] = regional.region.map(expected).fillna(0)
channels = adoption_table(current, 'channel')
services = adoption_table(current, 'service_category')
national = float(trend.adoption_pct.iloc[-1])
first = float(trend.adoption_pct.iloc[0])
summary = {
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'rows':len(df), 'columns':len(df.columns), 'start_month':df.month.min().strftime('%Y-%m'),
    'latest_month':latest.strftime('%Y-%m'), 'national_latest_pct':national,
    'national_first_pct':first, 'national_headroom_pp':national-65,
    'national_growth_pp':national-first, 'regions_below_target':len(funded), 'total_regions':13,
    'total_positive_gap_pp':total_gap, 'priority_regions':funded.head(4).region.tolist(),
    'priority_regions_gap_share_pct':float(funded.head(4).gap_pp.sum()/total_gap*100),
    'selected_regions':funded.region.tolist(), 'budget_sar_m':40,
    'four_widest_budget_sar_m':float(funded.head(4).allocation_sar_m.sum()),
    'other_four_budget_sar_m':float(funded.iloc[4:].allocation_sar_m.sum()),
    'rounding_unit_sar_m':0.5, 'target_pct':65,
    'metric_method':'SUM(digital_adoption_pct * unique_users) / SUM(unique_users), matching the shared Tableau workbook. A weighted index, not a directly measured digital-transaction share or distinct national user count.',
    'priority_method':'Rank positive gaps to 65% in descending order, in percentage points.',
    'allocation_method':'40M times regional gap / total positive gap; largest-remainder rounding to 0.5M units. All 40M goes to the eight regions.',
    'synthetic':True, 'missing_cells':int(df.isna().sum().sum()),
    'duplicate_keys':int(df.duplicated(keys).sum()),
    'selected_allocations':json.loads(funded.to_json(orient='records', double_precision=15)),
    'checkpoints':{'cost_validation_days':30, 'progress_review_months':6, 'timetable_is_proposed':True},
    'data_sources':{
        'csv':'https://drive.google.com/file/d/1T6pweFV4EjBxZ75gge775OOYMYx2aKX0/view',
        'dictionary':'https://drive.google.com/file/d/1htqVTYconACXDD28CACXOpz8VAyz8Xm5/view',
        'lab2':'https://drive.google.com/file/d/1_DAzbKnnIl4dn1JN2hffwhCueJOoqPOh/view',
        'tableau':'https://public.tableau.com/views/Dvis_17912834975050/TayseerDigitalAdoption'}
}
OUT.mkdir(exist_ok=True)
for name, table in [('national_trend',trend), ('regional_priorities',regional), ('budget_allocation',funded),
                    ('channel_evidence',channels), ('service_evidence',services), ('latest_month_evidence',current)]:
    table.to_csv(OUT/(name+'.csv'), index=False, date_format='%Y-%m-%d', lineterminator='\n')
(OUT/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'National: {national:.6f}%; below target: {len(funded)}/13; four-gap share: {summary["priority_regions_gap_share_pct"]:.6f}%')
print(funded[['region','adoption_pct','gap_pp','allocation_sar_m']].to_string(index=False))
