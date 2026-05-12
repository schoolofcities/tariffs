from pathlib import Path
import pandas as pd
import ast

repo = Path(__file__).resolve().parents[2]
map_path = repo / 'analysis' / 'outputs' / 'qcew_msa_mapping.csv'
qcew_path = repo / 'analysis' / 'outputs' / 'qcew_msa_industry_2023_a.csv'
cor_out = repo / 'analysis' / 'outputs' / 'dominant_industry_correlations.csv'
ui_js_out = repo / 'src' / 'routes' / 'canada-us-visits' / 'assets' / 'industryCorrelations.js'
script_path = repo / 'analysis' / 'scripts' / 'canada_visits_vs_jobsv2.py'

# load VISIT_CHANGES from script
module = ast.parse((script_path).read_text(encoding='utf-8'))
visit_changes = None
for node in module.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'VISIT_CHANGES':
                visit_changes = ast.literal_eval(node.value)
                break
    if visit_changes is not None:
        break
if visit_changes is None:
    raise RuntimeError('VISIT_CHANGES not found')
visit_df = pd.DataFrame(list(visit_changes.items()), columns=['metro_name', 'visit_yoy_pct'])

# load mapping and qcew
mapping = pd.read_csv(map_path)
qcew = pd.read_csv(qcew_path)

valid_codes = ['11','21','22','23','31-33','42','44-45','48-49','51','52','53','54','55','56','61','62','71','72','81','99']
qcew2 = qcew[qcew['industry_code'].isin(valid_codes)].copy()
qcew_dom = qcew2.sort_values('jobs', ascending=False).groupby('metro_name', as_index=False).first()[['metro_name', 'industry_code', 'jobs']]
qcew_dom = qcew_dom.rename(columns={'industry_code': 'dominant_code', 'jobs': 'dominant_jobs'})

# merge mapping -> qcew_dom via area_title
merged = mapping.merge(qcew_dom, left_on='area_title', right_on='metro_name', how='left', suffixes=('','_q'))
merged = merged.merge(visit_df, on='metro_name', how='left')

# compute per-industry r and p
labels = {
    '11':'Agriculture', '21':'Mining/Oil & Gas', '22':'Utilities', '23':'Construction',
    '31-33':'Manufacturing', '42':'Wholesale Trade', '44-45':'Retail Trade', '48-49':'Transportation/Warehousing',
    '51':'Information', '52':'Finance & Insurance', '53':'Real Estate', '54':'Professional Services',
    '55':'Management', '56':'Admin/Support', '61':'Education', '62':'Health Care', '71':'Arts/Entertainment',
    '72':'Accommodation/Food', '81':'Other Services', '99':'Unclassified'
}

rows = []
# try import scipy for p-values
try:
    from scipy.stats import pearsonr
    have_scipy = True
except Exception:
    have_scipy = False

for code in valid_codes:
    subset = merged[merged['dominant_code'] == code].copy()
    n = len(subset)
    r = None
    p = None
    if n >= 2:
        try:
            r = subset['visit_yoy_pct'].corr(subset['dominant_jobs'])
        except Exception:
            r = None
    if have_scipy and n >= 2 and subset['visit_yoy_pct'].notna().sum() > 1 and subset['dominant_jobs'].notna().sum() > 1:
        try:
            # scipy.pearsonr requires at least 2 non-NA
            xx = subset['visit_yoy_pct'].astype(float)
            yy = subset['dominant_jobs'].astype(float)
            if len(xx.dropna()) >= 2 and len(yy.dropna()) >= 2:
                r_scipy, p_scipy = pearsonr(xx.dropna(), yy.dropna())
                p = float(p_scipy)
                # prefer r from scipy (more numerically stable)
                r = float(r_scipy)
        except Exception:
            p = None
    rows.append({'NAICS': code, 'Industry': labels[code], 'Correlation': r, 'PValue': p, 'SampleSize': n, 'DominantMetroCount': n})

res_df = pd.DataFrame(rows).sort_values('Correlation', ascending=False, na_position='last')
res_df.to_csv(cor_out, index=False)
print('Wrote correlations to', cor_out)

# write UI module (only include fields; UI will exclude N<4)
js_rows = []
for _, r in res_df.iterrows():
    corr = r['Correlation']
    corr_val = 'null' if pd.isna(corr) else f"{float(corr):.6f}"
    p = r['PValue']
    p_val = 'null' if pd.isna(p) else f"{float(p):.6f}"
    js_rows.append(f"\t{{ code: '{r['NAICS']}', industry: '{r['Industry']}', correlation: {corr_val}, pValue: {p_val}, sampleSize: {int(r['SampleSize'])}, dominantMetroCount: {int(r['DominantMetroCount'])} }}")

js_text = 'export const industryCorrelations = [\n' + ',\n'.join(js_rows) + '\n];\n'
ui_js_out.write_text(js_text, encoding='utf-8')
print('Wrote UI JS to', ui_js_out)

print('\nDone — note: p-values computed only if scipy available; otherwise pValue=null')
