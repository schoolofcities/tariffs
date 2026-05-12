import ast
import json
from pathlib import Path

import pandas as pd

root = Path(r"D:\coding\SoC\tariffs\tariffs")
script_path = root / "analysis" / "scripts" / "canada_visits_vs_jobsv2.py"
qcew_path = root / "analysis" / "outputs" / "qcew_msa_industry_2023_a.csv"
output_path = root / "src" / "routes" / "canada-us-visits-v2" / "assets" / "visitJobsScatterData.js"

source = script_path.read_text(encoding="utf-8")
module = ast.parse(source)
visit_changes = None
naics_labels = None
for node in module.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name == "VISIT_CHANGES":
            visit_changes = ast.literal_eval(node.value)
        if name == "NAICS_LABELS":
            naics_labels = ast.literal_eval(node.value)

if visit_changes is None or naics_labels is None:
    raise SystemExit("Missing VISIT_CHANGES or NAICS_LABELS in script")

df23 = pd.read_csv(qcew_path)
valid_codes = list(naics_labels.keys())
df23 = df23[df23["industry_code"].isin(valid_codes)].copy()

dominant = (
    df23.sort_values("jobs", ascending=False)
    .groupby("metro_name", as_index=False)
    .first()[["metro_name", "industry_code", "jobs"]]
    .rename(columns={"industry_code": "dominant_code", "jobs": "dominant_jobs"})
)

total = df23.groupby("metro_name")["jobs"].sum().reset_index()
total.rename(columns={"jobs": "total_jobs_2023"}, inplace=True)

summary = total.merge(dominant, on="metro_name")
visit_df = pd.DataFrame(list(visit_changes.items()), columns=["metro_name", "visit_yoy_pct"])
merged = summary.merge(visit_df, on="metro_name", how="inner")
merged["dominant_industry"] = merged["dominant_code"].map(naics_labels)

records = []
for _, row in merged.iterrows():
    records.append({
        "metro": row["metro_name"],
        "visitChange": float(row["visit_yoy_pct"]),
        "totalJobs": int(row["total_jobs_2023"]),
        "dominantIndustry": row["dominant_industry"],
        "dominantJobs": int(row["dominant_jobs"]),
        "dominantCode": row["dominant_code"],
    })

records.sort(key=lambda x: x["dominantIndustry"] or "")

js = "export const visitJobsScatterData = " + json.dumps(records, ensure_ascii=True, indent=2) + ";\n"
output_path.write_text(js, encoding="utf-8")
print(f"Wrote {output_path}")
