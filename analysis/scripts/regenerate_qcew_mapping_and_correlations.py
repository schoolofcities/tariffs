import ast
import re
from pathlib import Path
import difflib
import json
import pandas as pd

repo = Path(__file__).resolve().parents[2]
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
if visit_changes is None:
    raise RuntimeError('VISIT_CHANGES not found in script')

visit_names = sorted(visit_changes.keys())

# paths
qcew_path = repo / 'analysis' / 'outputs' / 'qcew_msa_industry_2023_a.csv'
mapping_out = repo / 'analysis' / 'outputs' / 'qcew_msa_mapping.csv'
cor_out = repo / 'analysis' / 'outputs' / 'dominant_industry_correlations.csv'
ui_js_out = repo / 'src' / 'routes' / 'canada-us-visits' / 'assets' / 'industryCorrelations.js'

# load QCEW metro info
qcew = pd.read_csv(qcew_path)
if 'area_title' in qcew.columns:
    area_title_col = 'area_title'
elif 'area_title' in qcew.columns.str.lower():
    area_title_col = [c for c in qcew.columns if c.lower() == 'area_title'][0]
else:
    area_title_col = None

qcew_metros = qcew[['metro_name', 'area_code']].drop_duplicates()
if area_title_col:
    qcew_metros = qcew_metros.merge(qcew[[ 'metro_name', area_title_col ]].drop_duplicates(), on='metro_name', how='left')
    qcew_metros = qcew_metros.rename(columns={area_title_col: 'area_title'})
else:
    qcew_metros['area_title'] = ''

qcew_names = list(qcew_metros['metro_name'].unique())

# normalization helpers
_word_re = re.compile(r"\w+", re.UNICODE)

def tokens(name):
    return set(_word_re.findall(name.lower()))

def token_set_score(a, b):
    ta = tokens(a)
    tb = tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


# match each visit name to best qcew name
rows = []
for v in visit_names:
    best = None
    best_score = 0.0
    best_type = 'none'
    # exact
    for q in qcew_names:
        if v == q:
            best = q
            best_score = 1.0
            best_type = 'exact'
            break
    if best is None:
        # use difflib ratio and token set
        for q in qcew_names:
            r = difflib.SequenceMatcher(None, v.lower(), q.lower()).ratio()
            t = token_set_score(v, q)
            score = max(r, t)
            if score > best_score:
                best_score = score
                best = q
        if best_score >= 0.6:
            best_type = 'fuzzy'
        else:
            best_type = 'none'
            best = None
            best_score = 0.0

    if best is not None:
        row = {
            'metro_name': v,
            'area_code': qcew_metros.loc[qcew_metros['metro_name'] == best, 'area_code'].iloc[0],
            'area_title': best,
            'match_type': best_type,
            'match_score': round(float(best_score), 3),
        }
    else:
        row = {
            'metro_name': v,
            'area_code': '',
            'area_title': '',
            'match_type': 'none',
            'match_score': 0.0,
        }
    rows.append(row)

mapping_df = pd.DataFrame(rows)
mapping_df.to_csv(mapping_out, index=False)
print('Wrote mapping to', mapping_out)

# compute dominant industry correlations using the new mapping
valid_codes = ['11','21','22','23','31-33','42','44-45','48-49','51','52','53','54','55','56','61','62','71','72','81','99']
qcew2 = qcew[qcew['industry_code'].isin(valid_codes)].copy()
# dominant per qcew metro
qcew_dom = qcew2.sort_values('jobs', ascending=False).groupby('metro_name', as_index=False).first()[['metro_name', 'industry_code', 'jobs']]
qcew_dom = qcew_dom.rename(columns={'industry_code': 'dominant_code', 'jobs': 'dominant_jobs'})

# build visit df
visit_df = pd.DataFrame(list(visit_changes.items()), columns=['metro_name', 'visit_yoy_pct'])

# merge mapping -> qcew_dom via matched area_title
merged = mapping_df.merge(qcew_dom, left_on='area_title', right_on='metro_name', how='left', suffixes=('','_q'))
merged = merged.merge(visit_df, on='metro_name', how='left')

# compute per-industry correlations
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
    if n >= 2:
        corr = subset['visit_yoy_pct'].corr(subset['dominant_jobs'])
    else:
        corr = None
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

print('\nDone')
