from pathlib import Path
import pandas as pd

repo = Path(__file__).resolve().parents[2]
map_path = repo / 'analysis' / 'outputs' / 'qcew_msa_mapping.csv'
qcew_path = repo / 'analysis' / 'outputs' / 'qcew_msa_industry_2023_a.csv'
cor_out = repo / 'analysis' / 'outputs' / 'dominant_industry_correlations.csv'
ui_js_out = repo / 'src' / 'routes' / 'canada-us-visits' / 'assets' / 'industryCorrelations.js'

manual = {
    'Albany, NY': ('C1058', 'Albany-Schenectady-Troy, NY'),
    'Athens, GA': ('C1202', 'Athens-Clarke County, GA'),
    'Augusta, GA': ('C1226', 'Augusta-Richmond County, GA-SC'),
    'Bremerton, WA': ('C1474', 'Bremerton-Silverdale-Port Orchard, WA'),
    'Daphne, AL': ('C1930', 'Daphne-Fairhope-Foley, AL'),
    'Davenport, IA': ('C1934', 'Davenport-Moline-Rock Island, IA-IL'),
    'Hilo, HI': ('C4652', 'Urban Honolulu, HI'),
    'Houston, TX': ('C2642', 'Houston-The Woodlands-Sugar Land, TX'),
    'Miami, FL': ('C3310', 'Miami-Fort Lauderdale-Pompano Beach, FL'),
    'Minneapolis, MN': ('C3346', 'Minneapolis-St. Paul-Bloomington, MN-WI'),
    'Myrtle Beach, SC': ('C3482', 'Myrtle Beach-Conway-North Myrtle Beach, SC-NC'),
    'New York, NY': ('C3562', 'New York-Newark-Jersey City, NY-NJ-PA'),
    'Omaha, NE': ('C3070', 'Lincoln, NE'),
    'Philadelphia, PA': ('C3798', 'Philadelphia-Camden-Wilmington, PA-NJ-DE-MD'),
    'Poughkeepsie, NY': ('C4038', 'Rochester, NY'),
    'Seattle, WA': ('C4266', 'Seattle-Tacoma-Bellevue, WA'),
    'Sebastian, FL': ('C3610', 'Ocala, FL'),
}

mapping = pd.read_csv(map_path)
for metro, (code, title) in manual.items():
    idx = mapping['metro_name'] == metro
    if idx.any():
        mapping.loc[idx, 'area_code'] = code
        mapping.loc[idx, 'area_title'] = title
        mapping.loc[idx, 'match_type'] = 'manual'
        mapping.loc[idx, 'match_score'] = 1.0
    else:
        # append if missing
        mapping = mapping.append({'metro_name': metro, 'area_code': code, 'area_title': title, 'match_type': 'manual', 'match_score': 1.0}, ignore_index=True)

mapping.to_csv(map_path, index=False)
print('Applied manual mappings and saved', map_path)

# recompute correlations using updated mapping
qcew = pd.read_csv(qcew_path)
valid_codes = ['11','21','22','23','31-33','42','44-45','48-49','51','52','53','54','55','56','61','62','71','72','81','99']
qcew2 = qcew[qcew['industry_code'].isin(valid_codes)].copy()
qcew_dom = qcew2.sort_values('jobs', ascending=False).groupby('metro_name', as_index=False).first()[['metro_name', 'industry_code', 'jobs']]
qcew_dom = qcew_dom.rename(columns={'industry_code': 'dominant_code', 'jobs': 'dominant_jobs'})

# load visit changes from script
import ast
script_path = repo / 'analysis' / 'scripts' / 'canada_visits_vs_jobsv2.py'
module = ast.parse(script_path.read_text(encoding='utf-8'))
visit_changes = None
for node in module.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'VISIT_CHANGES':
                visit_changes = ast.literal_eval(node.value)
                break
    if visit_changes is not None:
        break
visit_df = pd.DataFrame(list(visit_changes.items()), columns=['metro_name', 'visit_yoy_pct'])

merged = mapping.merge(qcew_dom, left_on='area_title', right_on='metro_name', how='left', suffixes=('','_q'))
merged = merged.merge(visit_df, on='metro_name', how='left')

labels = {
    '11':'Agriculture', '21':'Mining/Oil & Gas', '22':'Utilities', '23':'Construction',
    '31-33':'Manufacturing', '42':'Wholesale Trade', '44-45':'Retail Trade', '48-49':'Transportation/Warehousing',
    '51':'Information', '52':'Finance & Insurance', '53':'Real Estate', '54':'Professional Services',
    '55':'Management', '56':'Admin/Support', '61':'Education', '62':'Health Care', '71':'Arts/Entertainment',
    '72':'Accommodation/Food', '81':'Other Services', '99':'Unclassified'
}
rows = []
for code in valid_codes:
    subset = merged[merged['dominant_code'] == code].copy()
    n = len(subset)
    corr = subset['visit_yoy_pct'].corr(subset['dominant_jobs']) if n >= 2 else None
    rows.append({'NAICS': code, 'Industry': labels[code], 'Correlation': corr, 'SampleSize': n, 'DominantMetroCount': n})

res_df = pd.DataFrame(rows).sort_values('Correlation', ascending=False, na_position='last')
res_df.to_csv(cor_out, index=False)
print('Wrote correlations to', cor_out)

# write UI module
js_rows = []
for _, r in res_df.iterrows():
    corr = r['Correlation']
    corr_val = 'null' if pd.isna(corr) else f"{float(corr):.6f}"
    js_rows.append(f"\t{{ code: '{r['NAICS']}', industry: '{r['Industry']}', correlation: {corr_val}, sampleSize: {int(r['SampleSize'])}, dominantMetroCount: {int(r['DominantMetroCount'])} }}")

js_text = 'export const industryCorrelations = [\n' + ',\n'.join(js_rows) + '\n];\n'
ui_js_out.write_text(js_text, encoding='utf-8')
print('Wrote UI JS to', ui_js_out)
