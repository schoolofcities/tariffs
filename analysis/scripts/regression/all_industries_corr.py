from __future__ import annotations

import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd
import difflib
import re

try:
    from scipy.stats import pearsonr
except Exception:  # pragma: no cover
    pearsonr = None


def extract_primary_city(name: str) -> str:
    """Extract just the first city name for fallback matching."""
    # "Chicago-Naperville-Elgin, IL-IN-WI" → "chicago"
    return re.split(r"[-,]", name)[0].strip().lower()


def load_constants(source_script: Path) -> tuple[dict[str, float], dict[str, str]]:
    source = source_script.read_text(encoding="utf-8")
    module = ast.parse(source)

    visit_changes = None
    naics_labels = None

    for node in module.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue

        if target.id == "VISIT_CHANGES":
            visit_changes = ast.literal_eval(node.value)
        elif target.id == "NAICS_LABELS":
            naics_labels = ast.literal_eval(node.value)

    if visit_changes is None or naics_labels is None:
        raise RuntimeError("Could not find VISIT_CHANGES and NAICS_LABELS in source script")

    return visit_changes, naics_labels


def compute_all_industry_correlations(
    qcew_df: pd.DataFrame,
    visit_changes: dict[str, float],
    naics_labels: dict[str, str],
) -> pd.DataFrame:
    codes = list(naics_labels.keys())

    visit_df = pd.DataFrame(
        list(visit_changes.items()), columns=["orig_metro_name", "visit_yoy_pct"]
    )

    # Build metro name mapping once (visit names → QCEW names)
    qcew_metros = sorted(qcew_df["metro_name"].unique())
    mapping: dict[str, str] = {}
    unmatched: list[str] = []

    for vm in visit_df["orig_metro_name"]:
        if vm in qcew_metros:
            mapping[vm] = vm
            continue
        lower_map = {m.lower(): m for m in qcew_metros}
        if vm.lower() in lower_map:
            mapping[vm] = lower_map[vm.lower()]
            continue
        matches = difflib.get_close_matches(vm, qcew_metros, n=1, cutoff=0.75)
        if matches:
            mapping[vm] = matches[0]
        else:
            unmatched.append(vm)

    visit_df["metro_name"] = visit_df["orig_metro_name"].map(mapping)
    # Drop visit metros that couldn't be matched to any QCEW metro
    visit_df = visit_df.dropna(subset=["metro_name"])

    rows = []
    for code in codes:
        # Get only the metros that have jobs data for THIS industry
        industry_jobs = (
            qcew_df[qcew_df["industry_code"] == code]
            .groupby("metro_name", as_index=False)["jobs"]
            .sum()
        )

        # Join visit data with THIS industry's jobs — varies per industry
        subset = industry_jobs.merge(
            visit_df[["metro_name", "visit_yoy_pct"]],
            on="metro_name",
            how="inner",
        )

        n = len(subset)

        if n < 2:
            rows.append({
                "NAICS": code,
                "Industry": naics_labels.get(code, code),
                "Correlation": np.nan,
                "PValue": np.nan,
                "SampleSize": n,
                "DominantMetroCount": n,
            })
            continue

        x = subset["visit_yoy_pct"].to_numpy(dtype=float)
        y = subset["jobs"].to_numpy(dtype=float)

        if np.std(x) > 0 and np.std(y) > 0:
            corr = float(np.corrcoef(x, y)[0, 1])
            if pearsonr is not None:
                _, p_value = pearsonr(x, y)
                p_value = float(p_value)
            else:
                p_value = np.nan
        else:
            corr = np.nan
            p_value = np.nan

        rows.append({
            "NAICS": code,
            "Industry": naics_labels.get(code, code),
            "Correlation": corr,
            "PValue": p_value,
            "SampleSize": n,
            "DominantMetroCount": n,
        })

    return pd.DataFrame(rows).sort_values("Correlation", ascending=False, na_position="last")


def to_js_array(df: pd.DataFrame) -> str:
    lines: list[str] = []
    for _, row in df.iterrows():
        corr = "null" if pd.isna(row["Correlation"]) else f"{float(row['Correlation']):.6f}"
        pval = "null" if pd.isna(row["PValue"]) else f"{float(row['PValue']):.6f}"
        lines.append(
            "\t{ "
            f"code: '{row['NAICS']}', "
            f"industry: '{row['Industry']}', "
            f"correlation: {corr}, "
            f"pValue: {pval}, "
            f"sampleSize: {int(row['SampleSize'])}, "
            f"dominantMetroCount: {int(row['DominantMetroCount'])} "
            "}"
        )

    return "export const industryCorrelations = [\n" + ",\n".join(lines) + "\n];\n"


def main() -> None:
    repo = Path(__file__).resolve().parents[2]

    source_script = repo / "analysis" / "scripts" / "canada_visits_vs_jobsv2.py"
    qcew_path = repo / "analysis" / "outputs" / "qcew_msa_industry_2023_a.csv"

    out_csv = repo / "analysis" / "outputs" / "dominant_industry_correlations.csv"
    out_js_main = repo / "src" / "routes" / "canada-us-visits" / "assets" / "industryCorrelations.js"
    out_js_v2 = repo / "src" / "routes" / "canada-us-visits-regression" / "assets" / "industryCorrelations.js"

    visit_changes, naics_labels = load_constants(source_script)
    qcew_df = pd.read_csv(qcew_path)

    # Quick diagnostics: how many visit metros match QCEW metro_name values?
    qcew_metros = sorted(qcew_df["metro_name"].unique())
    v_metros = sorted(visit_changes.keys())
    exact_matches = [m for m in v_metros if m in qcew_metros]
    # case-insensitive and fuzzy matches
    import difflib as _dif
    mapped = {}
    unmatched = []
    lower_map = {m.lower(): m for m in qcew_metros}


    for vm in v_metros:
        if vm in qcew_metros:
            mapped[vm] = vm
            continue
        if vm.lower() in lower_map:
            mapped[vm] = lower_map[vm.lower()]
            continue
        matches = _dif.get_close_matches(vm, qcew_metros, n=1, cutoff=0.75)
        if matches:
            mapped[vm] = matches[0]
        else:
            unmatched.append(vm)

    print(f"Visit metros total: {len(v_metros)}")
    print(f"Unique metros in QCEW: {len(qcew_metros)}")
    print(f"Exact matches: {len(exact_matches)}")
    print(f"Mapped (incl. fuzzy): {len(mapped)}")
    print(f"Unmatched: {len(unmatched)}")
    if unmatched:
        print("Unmatched examples:")
        for m in unmatched[:20]:
            print(" -", m)

    corr_df = compute_all_industry_correlations(qcew_df, visit_changes, naics_labels)

    corr_df.to_csv(out_csv, index=False)
    js_text = to_js_array(corr_df)
    out_js_main.write_text(js_text, encoding="utf-8")
    out_js_v2.write_text(js_text, encoding="utf-8")

    print(f"Wrote correlation CSV: {out_csv}")
    print(f"Wrote industry correlations JS: {out_js_main}")
    print(f"Wrote industry correlations JS: {out_js_v2}")
    print(f"Per-industry sample size: {len(visit_changes)} metros")

    qcew_df = pd.read_csv(qcew_path)

    # How many unique industries does each metro have?
    coverage = qcew_df.groupby("metro_name")["industry_code"].nunique().sort_values()
    print(coverage.describe())
    print("\nMetros with ALL industries:")
    print((coverage == coverage.max()).sum())
    print("\nSample of low-coverage metros:")
    print(coverage.head(20))

    # Are there zero-job rows masking missing data?
    print(qcew_df[qcew_df["jobs"] == 0].shape[0], "zero-job rows")
    print(qcew_df[qcew_df["jobs"].isna()].shape[0], "null-job rows")

    # What does coverage look like for a sparse industry?
    print(qcew_df[qcew_df["industry_code"] == "21"]["metro_name"].nunique(), "metros for Mining")
    print(qcew_df[qcew_df["industry_code"] == "72"]["metro_name"].nunique(), "metros for Accommodation")


if __name__ == "__main__":
    main()
