from __future__ import annotations

import ast
import re
from pathlib import Path

import difflib
import numpy as np
import pandas as pd

try:
    from scipy.stats import pearsonr
except Exception:  # pragma: no cover
    pearsonr = None


def extract_primary_city(name: str) -> str:
    """Extract just the first city name for fallback matching.
    "Chicago-Naperville-Elgin, IL-IN-WI" → "chicago"
    """
    return re.split(r"[-,]", name)[0].strip().lower()


def build_metro_mapping(visit_metros: list[str], qcew_metros: list[str]) -> tuple[dict[str, str], list[str]]:
    """Map visit metro names to QCEW metro names using exact, case-insensitive,
    primary-city+state, and fuzzy matching — in that order."""
    mapping: dict[str, str] = {}
    unmatched: list[str] = []

    lower_map = {m.lower(): m for m in qcew_metros}
    primary_map: dict[str, list[str]] = {}
    for m in qcew_metros:
        key = extract_primary_city(m)
        primary_map.setdefault(key, []).append(m)

    for vm in visit_metros:
        # 1. Exact match
        if vm in qcew_metros:
            mapping[vm] = vm
            continue

        # 2. Case-insensitive exact match
        if vm.lower() in lower_map:
            mapping[vm] = lower_map[vm.lower()]
            continue

        # 3. Primary city + state match
        #    e.g. "Chicago, IL" → primary="chicago", state="il"
        #    matches "Chicago-Naperville-Elgin, IL-IN-WI" because primary="chicago" and "il" is in the name
        vm_primary = extract_primary_city(vm)
        vm_state = vm.split(",")[-1].strip().lower()  # "il" from "Chicago, IL"

        candidates = [
            qm for qm in primary_map.get(vm_primary, [])
            if vm_state in qm.lower()
        ]
        if candidates:
            mapping[vm] = candidates[0]
            continue

        # 4. Fuzzy match fallback
        matches = difflib.get_close_matches(vm, qcew_metros, n=1, cutoff=0.75)
        if matches:
            mapping[vm] = matches[0]
        else:
            unmatched.append(vm)

    return mapping, unmatched


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

    qcew_metros = sorted(qcew_df["metro_name"].unique())
    mapping, unmatched = build_metro_mapping(list(visit_df["orig_metro_name"]), qcew_metros)

    print(f"  Matched: {len(mapping)} / {len(visit_df)}  |  Unmatched: {len(unmatched)}")
    if unmatched:
        print("  Unmatched examples:", unmatched[:10])

    visit_df["metro_name"] = visit_df["orig_metro_name"].map(mapping)
    visit_df = visit_df.dropna(subset=["metro_name"])

    rows = []
    for code in codes:
        # Only keep metros with real (>0) employment in this industry
        industry_jobs = (
            qcew_df[(qcew_df["industry_code"] == code) & (qcew_df["jobs"] > 0)]
            .groupby("metro_name", as_index=False)["jobs"]
            .sum()
        )

        # Per-industry join — sample size varies by industry
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
            })
            continue

        x = subset["visit_yoy_pct"].to_numpy(dtype=float)
        y = subset["jobs"].to_numpy(dtype=float)

        if np.std(x) > 0 and np.std(y) > 0:
            corr = float(np.corrcoef(x, y)[0, 1])
            p_value = float(pearsonr(x, y)[1]) if pearsonr is not None else np.nan
        else:
            corr = np.nan
            p_value = np.nan

        rows.append({
            "NAICS": code,
            "Industry": naics_labels.get(code, code),
            "Correlation": corr,
            "PValue": p_value,
            "SampleSize": n,
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
            f"sampleSize: {int(row['SampleSize'])} "
            "}"
        )
    return "export const industryCorrelations = [\n" + ",\n".join(lines) + "\n];\n"


def main() -> None:
    repo = Path(__file__).resolve().parents[2]

    source_script = repo / "analysis" / "scripts" / "canada_visits_vs_jobsv2.py"
    qcew_path     = repo / "analysis" / "outputs" / "qcew_msa_industry_2023_a.csv"
    out_csv       = repo / "analysis" / "outputs" / "dominant_industry_correlations.csv"
    out_js_main   = repo / "src" / "routes" / "canada-us-visits"    / "assets" / "industryCorrelations.js"
    out_js_v2     = repo / "src" / "routes" / "canada-us-visits-v2" / "assets" / "industryCorrelations.js"

    visit_changes, naics_labels = load_constants(source_script)
    qcew_df = pd.read_csv(qcew_path)

    corr_df = compute_all_industry_correlations(qcew_df, visit_changes, naics_labels)

    print("\nSample size range across industries:")
    print(corr_df[["Industry", "SampleSize", "Correlation"]].to_string(index=False))

    corr_df.to_csv(out_csv, index=False)
    js_text = to_js_array(corr_df)
    out_js_main.write_text(js_text, encoding="utf-8")
    out_js_v2.write_text(js_text, encoding="utf-8")

    print(f"\nWrote CSV:  {out_csv}")
    print(f"Wrote JS:   {out_js_main}")
    print(f"Wrote JS:   {out_js_v2}")


if __name__ == "__main__":
    main()
