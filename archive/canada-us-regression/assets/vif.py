import os, re, json, sys
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SCRIPT_DIR, "regressionData_v2.js"), "r") as f:
    js = f.read()

json_str = re.sub(r"^export\s+const\s+\w+\s*=\s*", "", js.strip().rstrip(";"))
data = json.loads(json_str)
print(f"Loaded {len(data)} metros")

# ── Region mapping ────────────────────────────────────────────────────────────
stateToRegion = {
    "IL":"Midwest","IN":"Midwest","MI":"Midwest","OH":"Midwest","WI":"Midwest",
    "IA":"Midwest","KS":"Midwest","MN":"Midwest","MO":"Midwest","NE":"Midwest",
    "ND":"Midwest","SD":"Midwest","CT":"Northeast","ME":"Northeast","MA":"Northeast",
    "NH":"Northeast","RI":"Northeast","VT":"Northeast","NJ":"Northeast","NY":"Northeast",
    "PA":"Northeast","DE":"Northeast","MD":"Northeast","AZ":"Southwest","NM":"Southwest",
    "OK":"Southwest","TX":"Southwest","CO":"Southwest","NV":"Southwest","UT":"Southwest",
    "AL":"Southeast","AR":"Southeast","FL":"Southeast","GA":"Southeast","KY":"Southeast",
    "LA":"Southeast","MS":"Southeast","NC":"Southeast","SC":"Southeast","TN":"Southeast",
    "VA":"Southeast","WV":"Southeast","DC":"Southeast","AK":"Pacific","CA":"Pacific",
    "HI":"Pacific","OR":"Pacific","WA":"Pacific","ID":"Pacific","MT":"Pacific"
}

def get_region(metro):
    m = re.search(r",\s*([A-Z]{2})", metro)
    return stateToRegion.get(m.group(1)) if m else None

region_dummies = ["Northeast", "Southwest", "Southeast", "Pacific"]  # Midwest = baseline

# ── Build dataframe ───────────────────────────────────────────────────────────
rows = []
for d in data:
    if d.get("visitChange") is None:
        continue
    region = get_region(d["metro"])
    if not region or not d.get("population2025"):
        continue
    row = {
        "metro":             d["metro"],
        "visitChange":       d["visitChange"],
        "population_M":      d["population2025"] / 1_000_000,
        "distToBorderKm":    d.get("distToBorderKm") or np.nan,
        "log_enplanements":  np.log1p(d.get("cy24Enplanements") or 0),
    }
    for r in region_dummies:
        row[f"region_{r}"] = 1 if region == r else 0
    for k, v in d["industryShares"].items():
        row[f"ind_{k}"] = v
    rows.append(row)

df = pd.DataFrame(rows).dropna()
print(f"After filtering: {len(df)} metros\n")

# ── Full VIF ──────────────────────────────────────────────────────────────────
ind_cols = sorted([c for c in df.columns if c.startswith("ind_") and c != "ind_44-45"])
non_zero = [c for c in ind_cols if df[c].std() > 1e-6]
region_cols = [f"region_{r}" for r in region_dummies]

predictor_cols = ["population_M"] + region_cols + non_zero + ["distToBorderKm", "log_enplanements"]
X = df[predictor_cols]

print(f"Running VIF on {len(predictor_cols)} predictors, {len(X)} observations\n")

vif_df = pd.DataFrame({
    "feature": X.columns,
    "VIF":     [variance_inflation_factor(X.values.astype(float), i)
                for i in range(X.shape[1])]
}).sort_values("VIF", ascending=False).reset_index(drop=True)

naics_labels = {
    "11": "Agriculture", "21": "Mining/Oil & Gas", "22": "Utilities",
    "23": "Construction", "31-33": "Manufacturing", "42": "Wholesale Trade",
    "44-45": "Retail Trade", "48-49": "Transportation/Warehousing",
    "51": "Information", "52": "Finance & Insurance", "53": "Real Estate",
    "54": "Professional Services", "55": "Management", "56": "Admin/Support",
    "61": "Education", "62": "Health Care", "71": "Arts/Entertainment",
    "72": "Accommodation/Food", "81": "Other Services", "99": "Unclassified"
}

def relabel(feature):
    if feature.startswith("ind_"):
        code = feature.replace("ind_", "")
        return naics_labels.get(code, feature)
    return feature

vif_df["feature"] = vif_df["feature"].apply(relabel)

pd.set_option("display.max_rows", 60)
pd.set_option("display.float_format", "{:.2f}".format)
print(vif_df.to_string(index=False))
print(f"\nMedian VIF : {vif_df['VIF'].median():.2f}")
print(f"VIF > 10   : {(vif_df['VIF'] > 10).sum()} features")
print(f"VIF > 5    : {(vif_df['VIF'] > 5).sum()} features")
vif_df.to_csv(os.path.join(SCRIPT_DIR, "vif_results.csv"), index=False)

# ── Subset correlation matrix ─────────────────────────────────────────────────
print("\n── Pairwise correlations (subset) ──")
cols_of_interest = [
    "ind_44-45", "ind_62", "ind_72", "ind_31-33", "ind_23",
    "population_M", "distToBorderKm", "log_enplanements"
]
corr = df[cols_of_interest].corr().round(2)
print(corr.to_string())
corr.to_csv(os.path.join(SCRIPT_DIR, "correlation_matrix.csv"))
print("\nSaved vif_results.csv and correlation_matrix.csv")


# ── VIF: distToBorderKm vs region dummies ────────────────────────────────────
print("\n── VIF: distToBorderKm ~ regions ──")
cols_dist_region = ["distToBorderKm"] + region_cols
X_dist = df[cols_dist_region]
vif_dist = pd.DataFrame({
    "feature": X_dist.columns,
    "VIF":     [variance_inflation_factor(X_dist.values.astype(float), i)
                for i in range(X_dist.shape[1])]
}).sort_values("VIF", ascending=False)
print(vif_dist.to_string(index=False))

# ── What is distToBorderKm correlated with? ───────────────────────────────────
print("\nCorrelations with distToBorderKm")
corr_dist = df[predictor_cols].corr()["distToBorderKm"].drop("distToBorderKm").sort_values(key=abs, ascending=False).round(3)
corr_dist.index = [relabel(i) for i in corr_dist.index]
print(corr_dist.to_string())