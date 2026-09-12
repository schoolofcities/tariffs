# data prep for JSON -> input: QCEW, % visit change, population data; output: regressionData.js for frontend chart.
# outputs each metro w/ visit change, total jobs, population 2025, industry shares, industry totals.

from __future__ import annotations

import ast
import re
from pathlib import Path

import difflib
import json
import pandas as pd


def extract_primary_city(name: str) -> str:
    return re.split(r"[-,]", name)[0].strip().lower()

def print_metros_yoy():
    print()


def build_metro_mapping(visit_metros: list[str], qcew_metros: list[str]) -> tuple[dict[str, str], list[str]]:
    mapping: dict[str, str] = {}
    unmatched: list[str] = []

    lower_map = {m.lower(): m for m in qcew_metros}
    primary_map: dict[str, list[str]] = {}
    for m in qcew_metros:
        key = extract_primary_city(m)
        primary_map.setdefault(key, []).append(m)

    for vm in visit_metros:
        if vm in qcew_metros:
            mapping[vm] = vm
            continue
        if vm.lower() in lower_map:
            mapping[vm] = lower_map[vm.lower()]
            continue

        vm_primary = extract_primary_city(vm)
        vm_state = vm.split(",")[-1].strip().lower()
        candidates = [
            qm for qm in primary_map.get(vm_primary, [])
            if vm_state in qm.lower()
        ]
        if candidates:
            mapping[vm] = candidates[0]
            continue

        matches = difflib.get_close_matches(vm, qcew_metros, n=1, cutoff=0.75)
        if matches:
            mapping[vm] = matches[0]
        else:
            unmatched.append(vm)

    return mapping, unmatched


def suggest_matches(unmatched: list[str], qcew_metros: list[str], limit: int = 5) -> None:
    if not unmatched:
        return
    print("Closest QCEW metro suggestions (check manually):")
    for name in unmatched[:20]:
        suggestions = difflib.get_close_matches(name, qcew_metros, n=limit, cutoff=0.55)
        if suggestions:
            print(f"  {name} -> {suggestions}")
        else:
            print(f"  {name} -> no close match")


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


def metro_key(name: str) -> str:
    normalized = name.replace("\u2013", "-").replace("\u2014", "-")
    normalized = normalized.replace(" Micro Area", "").replace(" Metro Area", "").strip()
    normalized = normalized.lstrip(".")
    normalized = normalized.replace("Louisville, KY-IN", "Louisville/Jefferson County, KY-IN")
    city_part = normalized.split(",")[0].strip()
    city = re.split(r"[-/]", city_part)[0].strip().lower()
    match = re.search(r",\s*([A-Z]{2})", normalized)
    if match:
        state = match.group(1)
    else:
        state_match = re.search(r"\b([A-Z]{2})\b", normalized)
        state = state_match.group(1) if state_match else ""
    return f"{city}|{state}"

def load_population(paths: list[Path]) -> dict[str, int]:
    pop_map: dict[str, int] = {}
    for path in paths:
        if not path.exists():
            continue
        df = pd.read_excel(path, header=None, skiprows=6, usecols=[0, 7])
        df = df.rename(columns={0: "name", 7: "pop2025"}).dropna()
        df["pop2025"] = pd.to_numeric(
            df["pop2025"].astype(str).str.replace(",", "", regex=False),
            errors="coerce",
        )
        df = df.dropna(subset=["pop2025"])
        print(f"Loaded population rows from {path.name}: {len(df)}")
        for _, row in df.iterrows():
            key = metro_key(str(row["name"]))
            try:
                pop_val = int(float(row["pop2025"]))
            except Exception:
                continue
            if key and pop_val > 0:
                pop_map[key] = pop_val
    return pop_map


def load_msa_features(path: Path) -> dict[str, dict[str, float | None]]:
    """Load MSA features (distance to border, enplanements) from CSV.
    Returns dict mapping metro_name to {distToBorderKm, cy24Enplanements}.
    """
    features_map: dict[str, dict[str, float | None]] = {}
    if not path.exists():
        return features_map
    
    df = pd.read_csv(path)
    print(f"Loaded MSA features: {len(df)} rows")
    
    for _, row in df.iterrows():
        msa_name = str(row["MSA"]).strip()
        if not msa_name or msa_name == "nan":
            continue
        
        dist_km = pd.to_numeric(row["dist_to_border_km"], errors="coerce")
        enplanements = pd.to_numeric(row["CY24_Enplanements"], errors="coerce")
        
        features_map[msa_name] = {
            "distToBorderKm": float(dist_km) if pd.notna(dist_km) else None,
            "cy24Enplanements": int(enplanements) if pd.notna(enplanements) else None,
        }
    
    return features_map


def apply_manual_aliases(name: str) -> str:
    manual = {
        "Poughkeepsie, NY": "Poughkeepsie-Newburgh-Middletown, NY",
        "Sebastian, FL": "Sebastian-Vero Beach, FL",
        "Prescott Valley, AZ": "Prescott Valley-Prescott, AZ",
        "Torrington, CT": "Hartford-East Hartford-Middletown, CT",  # changed
        "Racine, WI": "Racine, WI",
        "Lebanon, NH": "Lebanon, NH-VT",
        "Hilo, HI": "Hilo, HI",
        "Muskegon, MI": "Muskegon, MI",
        "Dayton, OH": "Dayton, OH",
        "Omaha, NE": "Omaha-Council Bluffs, NE-IA",
        "Palm Bay-Melbourne-Titusville, FL": "Palm Bay-Melbourne-Titusville, FL",  # explicit passthrough
        "Port St. Lucie, FL": "Port St. Lucie, FL",  # explicit passthrough
    }
    return manual.get(name, name)

def main() -> None:
    repo = Path(__file__).resolve().parents[2]
    source_script = repo / "analysis" / "scripts" / "canada_visits_vs_jobsv2.py"
    qcew_path = repo / "analysis" / "outputs" / "qcew_msa_industry_2023_a.csv"

    pop_paths = [
        repo / "analysis" / "raw" / "cbsa-met-est2025-pop.xlsx",
        repo / "analysis" / "raw" / "cbsa-mic-est2025-pop.xlsx",
    ]

    out_js = repo / "src" / "routes" / "canada-us-visits-regression" / "assets" / "regressionData.js"
    msa_features_path = repo / "analysis" / "outputs" / "msa_features.csv"

    visit_changes, naics_labels = load_constants(source_script)
    df = pd.read_csv(qcew_path)

    codes = list(naics_labels.keys())
    df = df[df["industry_code"].isin(codes)].copy()

    total_jobs = df.groupby("metro_name", as_index=False)["jobs"].sum()
    total_jobs.rename(columns={"jobs": "total_jobs"}, inplace=True)

    industry_jobs = (
        df.groupby(["metro_name", "industry_code"], as_index=False)["jobs"].sum()
        .pivot(index="metro_name", columns="industry_code", values="jobs")
        .fillna(0)
        .reset_index()
    )

    industry_jobs = industry_jobs.merge(total_jobs, on="metro_name", how="left")

    for code in codes:
        if code not in industry_jobs.columns:
            industry_jobs[code] = 0

    raw_cols = {code: f"raw_{code}" for code in codes}
    industry_jobs_raw = industry_jobs[codes].copy().rename(columns=raw_cols)
    industry_jobs = pd.concat([industry_jobs, industry_jobs_raw], axis=1)

    industry_jobs[codes] = industry_jobs[codes].div(industry_jobs["total_jobs"].replace({0: pd.NA}), axis=0)

    visit_df = pd.DataFrame(list(visit_changes.items()), columns=["orig_metro_name", "visit_yoy_pct"])
    visit_df["alias_metro_name"] = visit_df["orig_metro_name"].map(apply_manual_aliases)
    qcew_metros = sorted(industry_jobs["metro_name"].unique())
    mapping, unmatched = build_metro_mapping(list(visit_df["alias_metro_name"]), qcew_metros)

    if unmatched:
        print("Unmatched metros:")
        for name in unmatched:
            print("-", name)
        suggest_matches(unmatched, qcew_metros)

    visit_df["metro_name"] = visit_df["alias_metro_name"].map(mapping)
    visit_df = visit_df.dropna(subset=["metro_name"])

    merged = industry_jobs.merge(visit_df, on="metro_name", how="left")

    pop_map = load_population(pop_paths)
    print(f"Population keys loaded: {len(pop_map)}")
    
    msa_features_map = load_msa_features(msa_features_path)
    print(f"MSA features loaded: {len(msa_features_map)}")

    print(f"Visit metros: {len(visit_df)}")
    print(f"Industry job rows: {len(industry_jobs)}")
    print(f"Merged rows: {len(merged)}")

    merged_keys = {metro_key(name) for name in merged["metro_name"].unique()}
    pop_keys = set(pop_map.keys())
    intersection = merged_keys & pop_keys
    print(f"Population key matches: {len(intersection)}")
    if not intersection and merged_keys and pop_keys:
        print("Sample merged keys:", sorted(list(merged_keys))[:10])
        print("Sample population keys:", sorted(list(pop_keys))[:10])

    records = []
    for _, row in merged.iterrows():
        key = metro_key(row["metro_name"])
        pop_val = pop_map.get(key)
        metro_name = str(row["metro_name"])
        msa_features = msa_features_map.get(metro_name, {})
        
        shares = {code: float(row[code]) if pd.notna(row[code]) else 0.0 for code in codes}
        totals = {code: int(row[f"raw_{code}"]) if pd.notna(row[f"raw_{code}"]) else 0 for code in codes}
        records.append({
            "metro": metro_name,
            "visitChange": float(row["visit_yoy_pct"]) if pd.notna(row["visit_yoy_pct"]) else None,
            "totalJobs": int(row["total_jobs"]),
            "population2025": int(pop_val) if pop_val is not None else None,
            "distToBorderKm": msa_features.get("distToBorderKm"),
            "cy24Enplanements": msa_features.get("cy24Enplanements"),
            "industryShares": shares,
            "industryTotals": totals,
        })

    have_population = sum(1 for r in records if r["population2025"] is not None)
    print(f"Records with population: {have_population} / {len(records)}")
    if have_population == 0 and records:
        sample_metros = records[:10]
        print("Sample metro keys:")
        for sample in sample_metros:
            print(sample["metro"], "->", metro_key(sample["metro"]))
        sample_pop_keys = list(pop_map.keys())[:10]
        print("Sample population keys:", sample_pop_keys)

    js_text = "export const regressionData = " + json.dumps(records, ensure_ascii=True, indent=2) + ";\n"
    out_js.write_text(js_text, encoding="utf-8")
    print(f"Wrote {out_js}")

    for probe in ["Dayton", "Omaha", "Muskegon", "Poughkeepsie", "Sebastian", "Racine", "Hilo", "Lebanon", "Prescott", "Tupelo"]:
        hits = [m for m in qcew_metros if probe.lower() in m.lower()]
        print(f"{probe}: {hits}")

    print("\n".join(sorted(qcew_metros)))

    all_metros_in_raw = df["metro_name"].unique()
    for probe in ["Dayton", "Omaha", "Muskegon", "Poughkeepsie", "Sebastian", "Racine", "Hilo", "Lebanon", "Prescott", "Tupelo"]:
        hits = [m for m in all_metros_in_raw if probe.lower() in m.lower()]
        print(f"{probe}: {hits}")


if __name__ == "__main__":
    main()
