import pandas as pd
from analysis.scripts.canada_visits_vs_jobsv2 import VISIT_CHANGES, NAICS_LABELS

# Load QCEW metros
qcew = pd.read_csv('analysis/outputs/qcew_msa_industry_2023_a.csv')
qcew_metros = set(qcew['metro_name'].unique())
visit_metros = set(VISIT_CHANGES.keys())

print(f'Visit list metros: {len(visit_metros)}')
print(f'QCEW job metros: {len(qcew_metros)}')
print(f'Metros in BOTH: {len(visit_metros & qcew_metros)}')
print(f'In visit list but NO QCEW data: {len(visit_metros - qcew_metros)}')
print(f'\nMissing metros:')
for m in sorted(visit_metros - qcew_metros):
    print(f'  - {m}')

# Now check for each industry, how many metros have data
print("\n" + "="*80)
print("INDUSTRY COVERAGE (out of ~125 matched metros)")
print("="*80)

visit_df = pd.DataFrame(list(VISIT_CHANGES.items()), columns=['metro_name', 'visit_yoy_pct'])
qcew_matched = qcew.merge(visit_df, on='metro_name', how='inner')

for code in sorted(NAICS_LABELS.keys()):
    count = len(qcew_matched[qcew_matched['industry_code'] == code])
    label = NAICS_LABELS[code]
    print(f"{code:5s} {label:30s} : {count:3d} metros")

print(f"\nTotal matched metros (any industry): {len(qcew_matched['metro_name'].unique())}")
