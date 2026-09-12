"""
export_analysis_data.py

Single script that exports all data needed for the R Markdown analysis.
Run from the repo root or any location — paths resolve relative to this file.

Outputs (written to analysis/outputs/):
  regression_data.csv      — one row per metro: visit change, industry shares,
                             population, distance to border, enplanements, region
  correlations.csv         — Pearson r of each industry job share vs visit change
  scatter_data.csv         — dominant industry per metro for scatter plot
"""

from __future__ import annotations

import ast
import math
import re
import difflib
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr


# ── Paths ─────────────────────────────────────────────────────────────────────

REPO          = Path(__file__).resolve().parents[2]
SCRIPT_PATH   = REPO / "analysis" / "scripts" / "canada_visits_vs_jobsv2.py"
QCEW_PATH     = REPO / "analysis" / "outputs" / "qcew_msa_industry_2023_a.csv"
POP_PATHS     = [
    REPO / "analysis" / "raw" / "cbsa-met-est2025-pop.xlsx",
    REPO / "analysis" / "raw" / "cbsa-mic-est2025-pop.xlsx",
]
MSA_FEATURES_PATH = REPO / "analysis" / "outputs" / "msa_features.csv"
OUT_DIR       = REPO / "analysis" / "outputs"


# ── Metro name helpers ────────────────────────────────────────────────────────

def extract_primary_city(name: str) -> str:
    return re.split(r"[-,]", name)[0].strip().lower()


MANUAL_ALIASES = {
    "Poughkeepsie, NY":                  "Poughkeepsie-Newburgh-Middletown, NY",
    "Sebastian, FL":                     "Sebastian-Vero Beach, FL",
    "Prescott Valley, AZ":               "Prescott Valley-Prescott, AZ",
    "Torrington, CT":                    "Hartford-East Hartford-Middletown, CT",
    "Lebanon, NH":                       "Lebanon, NH-VT",
    "Omaha, NE":                         "Omaha-Council Bluffs, NE-IA",
}

STATE_TO_REGION = {
    "IL": "Midwest", "IN": "Midwest", "MI": "Midwest", "OH": "Midwest", "WI": "Midwest",
    "IA": "Midwest", "KS": "Midwest", "MN": "Midwest", "MO": "Midwest", "NE": "Midwest",
    "ND": "Midwest", "SD": "Midwest",
    "CT": "Northeast", "ME": "Northeast", "MA": "Northeast", "NH": "Northeast",
    "RI": "Northeast", "VT": "Northeast", "NJ": "Northeast", "NY": "Northeast",
    "PA": "Northeast", "DE": "Northeast", "MD": "Northeast",
    "AZ": "Southwest", "NM": "Southwest", "OK": "Southwest", "TX": "Southwest",
    "CO": "Southwest", "NV": "Southwest", "UT": "Southwest",
    "AL": "Southeast", "AR": "Southeast", "FL": "Southeast", "GA": "Southeast",
    "KY": "Southeast", "LA": "Southeast", "MS": "Southeast", "NC": "Southeast",
    "SC": "Southeast", "TN": "Southeast", "VA": "Southeast", "WV": "Southeast",
    "DC": "Southeast",
    "AK": "Pacific", "CA": "Pacific", "HI": "Pacific", "OR": "Pacific",
    "WA": "Pacific", "ID": "Pacific", "MT": "Pacific",
}


def get_region(metro_name: str) -> str | None:
    m = re.search(r",\s*([A-Z]{2})", metro_name)
    if m:
        return STATE_TO_REGION.get(m.group(1))
    return None


def metro_key(name: str) -> str:
    """Stable key for population lookup: 'city|STATE'."""
    s = name.replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace(" Micro Area", "").replace(" Metro Area", "").strip().lstrip(".")
    s = s.replace("Louisville, KY-IN", "Louisville/Jefferson County, KY-IN")
    city = re.split(r"[-/]", s.split(",")[0].strip())[0].strip().lower()
    m = re.search(r",\s*([A-Z]{2})", s) or re.search(r"\b([A-Z]{2})\b", s)
    state = m.group(1) if m else ""
    return f"{city}|{state}"


def build_metro_mapping(
    visit_metros: list[str], qcew_metros: list[str]
) -> tuple[dict[str, str], list[str]]:
    mapping: dict[str, str] = {}
    unmatched: list[str] = []
    lower_map = {m.lower(): m for m in qcew_metros}
    primary_map: dict[str, list[str]] = {}
    for m in qcew_metros:
        primary_map.setdefault(extract_primary_city(m), []).append(m)

    for vm in visit_metros:
        if vm in qcew_metros:
            mapping[vm] = vm; continue
        if vm.lower() in lower_map:
            mapping[vm] = lower_map[vm.lower()]; continue
        vm_primary = extract_primary_city(vm)
        vm_state   = vm.split(",")[-1].strip().lower()
        candidates = [q for q in primary_map.get(vm_primary, []) if vm_state in q.lower()]
        if candidates:
            mapping[vm] = candidates[0]; continue
        close = difflib.get_close_matches(vm, qcew_metros, n=1, cutoff=0.75)
        if close:
            mapping[vm] = close[0]
        else:
            unmatched.append(vm)
    return mapping, unmatched


# ── Load source constants ─────────────────────────────────────────────────────

def load_constants(path: Path) -> tuple[dict[str, float], dict[str, str]]:
    src    = path.read_text(encoding="utf-8")
    module = ast.parse(src)
    visit_changes = naics_labels = None
    for node in module.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        t = node.targets[0]
        if not isinstance(t, ast.Name):
            continue
        if t.id == "VISIT_CHANGES":
            visit_changes = ast.literal_eval(node.value)
        elif t.id == "NAICS_LABELS":
            naics_labels  = ast.literal_eval(node.value)
    if visit_changes is None or naics_labels is None:
        raise RuntimeError("VISIT_CHANGES or NAICS_LABELS not found in source script")
    return visit_changes, naics_labels


# ── Load population ───────────────────────────────────────────────────────────

def load_population(paths: list[Path]) -> dict[str, int]:
    pop_map: dict[str, int] = {}
    for path in paths:
        if not path.exists():
            print(f"  [warn] population file not found: {path}")
            continue
        df = pd.read_excel(path, header=None, skiprows=6, usecols=[0, 7])
        df = df.rename(columns={0: "name", 7: "pop2025"}).dropna()
        df["pop2025"] = pd.to_numeric(
            df["pop2025"].astype(str).str.replace(",", "", regex=False), errors="coerce"
        )
        df = df.dropna(subset=["pop2025"])
        for _, row in df.iterrows():
            key = metro_key(str(row["name"]))
            try:
                val = int(float(row["pop2025"]))
            except Exception:
                continue
            if key and val > 0:
                pop_map[key] = val
        print(f"  Loaded {len(df)} population rows from {path.name}")
    return pop_map


# ── Load MSA features (border distance + enplanements) ───────────────────────

def load_msa_features(path: Path) -> dict[str, dict]:
    if not path.exists():
        print(f"  [warn] msa_features.csv not found: {path}")
        return {}
    df = pd.read_csv(path)
    out: dict[str, dict] = {}
    for _, row in df.iterrows():
        msa = str(row["MSA"]).strip()
        if not msa or msa == "nan":
            continue
        out[msa] = {
            "distToBorderKm":   float(row["dist_to_border_km"])   if pd.notna(row.get("dist_to_border_km"))   else None,
            "cy24Enplanements": float(row["CY24_Enplanements"])   if pd.notna(row.get("CY24_Enplanements"))   else None,
            "cy23Enplanements": float(row["CY23_Enplanements"])   if pd.notna(row.get("CY23_Enplanements"))   else None,
        }
    print(f"  Loaded MSA features for {len(out)} metros")
    return out


# ── Build base merged table ───────────────────────────────────────────────────

def build_base(
    visit_changes: dict[str, float],
    naics_labels:  dict[str, str],
    qcew_df:       pd.DataFrame,
    pop_map:       dict[str, int],
    msa_features:  dict[str, dict],
) -> pd.DataFrame:
    codes = list(naics_labels.keys())
    qcew  = qcew_df[qcew_df["industry_code"].isin(codes)].copy()

    total_jobs = qcew.groupby("metro_name", as_index=False)["jobs"].sum().rename(
        columns={"jobs": "total_jobs"}
    )

    # Industry jobs — wide (raw counts and shares)
    wide = (
        qcew.groupby(["metro_name", "industry_code"], as_index=False)["jobs"]
        .sum()
        .pivot(index="metro_name", columns="industry_code", values="jobs")
        .fillna(0)
        .reset_index()
    )
    wide = wide.merge(total_jobs, on="metro_name", how="left")
    for code in codes:
        if code not in wide.columns:
            wide[code] = 0.0

    # Store raw counts with prefix, then overwrite code columns with shares
    for code in codes:
        wide[f"raw_{code}"] = wide[code]
    wide[codes] = wide[codes].div(wide["total_jobs"].replace({0: pd.NA}), axis=0)

    # Visit changes — apply manual aliases then fuzzy-match to QCEW names
    visit_df = pd.DataFrame(
        list(visit_changes.items()), columns=["orig_metro", "visitChange"]
    )
    visit_df["alias"] = visit_df["orig_metro"].map(
        lambda n: MANUAL_ALIASES.get(n, n)
    )
    qcew_metros = sorted(wide["metro_name"].unique())
    mapping, unmatched = build_metro_mapping(list(visit_df["alias"]), qcew_metros)
    if unmatched:
        print(f"  [warn] {len(unmatched)} unmatched metros: {unmatched[:10]}")
    visit_df["metro_name"] = visit_df["alias"].map(mapping)
    visit_df = visit_df.dropna(subset=["metro_name"])

    merged = wide.merge(visit_df[["metro_name", "visitChange"]], on="metro_name", how="left")

    # Attach population, region, and MSA features
    merged["population2025"]   = merged["metro_name"].map(lambda n: pop_map.get(metro_key(n)))
    merged["region"]           = merged["metro_name"].map(get_region)
    merged["distToBorderKm"]   = merged["metro_name"].map(lambda n: msa_features.get(n, {}).get("distToBorderKm"))
    merged["cy24Enplanements"] = merged["metro_name"].map(lambda n: msa_features.get(n, {}).get("cy24Enplanements"))
    merged["cy23Enplanements"] = merged["metro_name"].map(lambda n: msa_features.get(n, {}).get("cy23Enplanements"))

    print(f"  Base table: {len(merged)} metros")
    print(f"    With visitChange:    {merged['visitChange'].notna().sum()}")
    print(f"    With population:     {merged['population2025'].notna().sum()}")
    print(f"    With distToBorder:   {merged['distToBorderKm'].notna().sum()}")
    print(f"    With enplanements:   {merged['cy24Enplanements'].notna().sum()}")

    return merged, codes


# ── Export 1: regression_data.csv ────────────────────────────────────────────

def export_regression(merged: pd.DataFrame, codes: list[str], out_dir: Path) -> None:
    share_cols = codes
    raw_cols   = [f"raw_{c}" for c in codes]
    keep = (
        ["metro_name", "visitChange", "total_jobs", "population2025",
         "region", "distToBorderKm", "cy24Enplanements", "cy23Enplanements"]
        + share_cols
        + raw_cols
    )
    df = merged[keep].copy()

    # Rename share columns to share_<code> (hyphens → underscores for R)
    rename = {c: f"share_{c.replace('-', '_')}" for c in share_cols}
    rename.update({f"raw_{c}": f"jobs_{c.replace('-', '_')}" for c in codes})
    df = df.rename(columns={"metro_name": "metro"} | rename)

    path = out_dir / "regression_data.csv"
    df.to_csv(path, index=False)
    print(f"  Wrote {path}  ({len(df)} rows, {len(df.columns)} cols)")


# ── Export 2: correlations.csv ────────────────────────────────────────────────

def export_correlations(
    merged: pd.DataFrame,
    codes: list[str],
    naics_labels: dict[str, str],
    qcew_df: pd.DataFrame,
    visit_changes: dict[str, float],
    out_dir: Path,
) -> None:
    """
    Re-compute correlations per-industry using variable sample sizes
    (only metros that have >0 jobs in that industry), matching all_industries_corr_v2.py.
    """
    # Rebuild visit_df with QCEW-matched names (same mapping used in build_base)
    visit_df = pd.DataFrame(
        list(visit_changes.items()), columns=["orig_metro", "visitChange"]
    )
    visit_df["alias"] = visit_df["orig_metro"].map(lambda n: MANUAL_ALIASES.get(n, n))
    qcew_metros = sorted(qcew_df["metro_name"].unique())
    mapping, _ = build_metro_mapping(list(visit_df["alias"]), qcew_metros)
    visit_df["metro_name"] = visit_df["alias"].map(mapping)
    visit_df = visit_df.dropna(subset=["metro_name"])

    total_jobs = (
        qcew_df.groupby("metro_name", as_index=False)["jobs"]
        .sum()
        .rename(columns={"jobs": "total_jobs"})
    )

    rows = []
    for code in codes:
        ind = (
            qcew_df[(qcew_df["industry_code"] == code) & (qcew_df["jobs"] > 0)]
            .groupby("metro_name", as_index=False)["jobs"]
            .sum()
        )
        sub = (
            ind
            .merge(visit_df[["metro_name", "visitChange"]], on="metro_name", how="inner")
            .merge(total_jobs, on="metro_name", how="left")
        )
        sub = sub[sub["total_jobs"] > 0].copy()
        sub["job_share"] = sub["jobs"] / sub["total_jobs"]
        n = len(sub)

        if n < 2:
            rows.append(dict(naics=code, industry=naics_labels.get(code, code),
                             correlation=np.nan, pValue=np.nan, sampleSize=n))
            continue

        x, y = sub["visitChange"].to_numpy(float), sub["job_share"].to_numpy(float)
        if np.std(x) > 0 and np.std(y) > 0:
            corr = float(np.corrcoef(x, y)[0, 1])
            pval = float(pearsonr(x, y)[1])
        else:
            corr = pval = np.nan

        rows.append(dict(naics=code, industry=naics_labels.get(code, code),
                         correlation=corr, pValue=pval, sampleSize=n))

    df = pd.DataFrame(rows).sort_values("correlation", ascending=False, na_position="last")
    path = out_dir / "correlations.csv"
    df.to_csv(path, index=False)
    print(f"  Wrote {path}  ({len(df)} rows)")


# ── Export 3: scatter_data.csv ────────────────────────────────────────────────

def export_scatter(
    merged: pd.DataFrame,
    codes: list[str],
    naics_labels: dict[str, str],
    out_dir: Path,
) -> None:
    """Dominant industry (by raw job count) per metro."""
    raw_cols = {code: f"raw_{code}" for code in codes}

    rows = []
    for _, row in merged.iterrows():
        if not pd.notna(row.get("visitChange")):
            continue
        job_counts = {code: row[f"raw_{code}"] for code in codes}
        dom_code   = max(job_counts, key=lambda c: job_counts[c])
        dom_jobs   = int(job_counts[dom_code])
        dom_share  = row[dom_code]   # already a share in merged
        rows.append({
            "metro":            row["metro_name"],
            "visitChange":      row["visitChange"],
            "totalJobs":        int(row["total_jobs"]),
            "dominantIndustry": naics_labels.get(dom_code, dom_code),
            "dominantCode":     dom_code,
            "dominantJobs":     dom_jobs,
            "dominantShare":    dom_share,
        })

    df = pd.DataFrame(rows).sort_values("dominantIndustry")
    path = out_dir / "scatter_data.csv"
    df.to_csv(path, index=False)
    print(f"  Wrote {path}  ({len(df)} rows)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading constants...")
    visit_changes, naics_labels = load_constants(SCRIPT_PATH)
    print(f"  {len(visit_changes)} visit metros, {len(naics_labels)} NAICS codes")

    print("Loading QCEW...")
    qcew_df = pd.read_csv(QCEW_PATH)
    print(f"  {len(qcew_df)} rows")

    print("Loading population...")
    pop_map = load_population(POP_PATHS)
    print(f"  {len(pop_map)} keys")

    print("Loading MSA features...")
    msa_features = load_msa_features(MSA_FEATURES_PATH)

    print("Building base table...")
    merged, codes = build_base(visit_changes, naics_labels, qcew_df, pop_map, msa_features)

    print("Exporting regression_data.csv...")
    export_regression(merged, codes, OUT_DIR)

    print("Exporting correlations.csv...")
    export_correlations(merged, codes, naics_labels, qcew_df, visit_changes, OUT_DIR)

    print("Exporting scatter_data.csv...")
    export_scatter(merged, codes, naics_labels, OUT_DIR)

    print("Done.")


if __name__ == "__main__":
    main()
