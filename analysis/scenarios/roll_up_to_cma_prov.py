#!/usr/bin/env python3
"""
roll_up_to_cma_prov.py

Aggregate CSD-level tariff scenario job-loss estimates up to
Census Metropolitan Area (CMA) and Province/Territory (PR) level.

Rules enforced here:
  * Job counts are SUMMED across CSDs. Never averaged.
  * Percentages are computed AFTER aggregation:
        pct = (aggregated jobs / aggregated employment) * 100
  * Provinces are built from CSDs directly, NOT from CMAs.
    (CMAs like Ottawa-Gatineau straddle a provincial boundary, and most
     CSDs are not in any CMA, so province-from-CMA would be wrong twice.)

Usage
-----
  # see what it detected without writing anything
  python roll_up_to_cma_prov.py --csd input/all_scenarios_csd.csv --inspect

  # counts only: province from the DGUID, CMA from the StatCan correspondence file
  python roll_up_to_cma_prov.py \
      --csd input/all_scenarios_csd.csv \
      --cma-lookup input/2021_98260004.csv \
      --derive-province-from-dguid \
      --outdir output

  # full run: named CMAs, agglomerations dropped, rates from Census Profile
  python roll_up_to_cma_prov.py \
      --csd input/all_scenarios_csd.csv \
      --cma-lookup input/2021_98260004.csv \
      --derive-province-from-dguid \
      --cma-names input/cma_denominator.csv \
      --cma-level-filter "Census metropolitan area" \
      --cma-denominator input/cma_denominator.csv \
      --denominator-col EMP_TOTAL --denominator-kind employment \
      --outdir output

  # province rollup only, before you have a CSD->CMA crosswalk
  python roll_up_to_cma_prov.py --csd input/all_scenarios_csd.csv \
      --derive-province-from-dguid --skip-cma --outdir output

In PowerShell use a backtick, not a caret, for line continuation.

Outputs (in --outdir)
---------------------
  all_scenarios_cma.csv / .json
  all_scenarios_province.csv / .json
  rollup_breaks.json        quantile class breaks per metric, for map/chart colours
  rollup_report.txt         detection, sign handling, reconciliation, plausibility log

The JSON files are records-oriented and shaped for the Svelte charts:
GEO_LEVEL / GEO_UID / GEO_NAME / CSD_COUNT plus every metric column.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Column detection
# --------------------------------------------------------------------------

# Job-loss value fields, e.g. S1_DIR_Jobs, S2_INDIR_Jobs, S3_INDCD_Jobs
VALUE_REGEX = r"^S(?P<scenario>\d+)_(?P<effect>DIR|INDIR|INDCD)_Jobs$"

# Candidate columns, in priority order.
# DGUIDs are preferred over UIDs so output joins straight onto the centroid JSONs.
# The *_SDRIDUGD / *_RMRIDUGD spellings are the bilingual headers StatCan ships
# in the 98-26-0004 correspondence file.
CSD_ID_CANDIDATES = ["CSDDGUID", "CSDDGUID_SDRIDUGD", "CSDUID", "DGUID",
                     "CSD_UID", "ALT_GEO_CODE", "GEO_UID"]
CSD_NAME_CANDIDATES = ["CSDNAME", "CSD_NAME", "GEO_NAME", "CSD"]
CMA_ID_CANDIDATES = ["CMADGUID", "CMADGUID_RMRIDUGD", "CMAUID", "CMA_UID",
                     "CMAPDGUID_RMRPIDUGD", "CMAPUID", "CMAP"]
CMA_NAME_CANDIDATES = ["CMANAME", "CMA_NAME", "CMAPNAME", "GEO_NAME"]
PR_ID_CANDIDATES = ["PRUID", "PRDGUID", "PRDGUID_PRIDUGD", "PR_UID", "PROVUID"]
PR_NAME_CANDIDATES = ["PRNAME", "PR_NAME", "PROVINCE", "PROV_NAME"]
EMP_CANDIDATES = [
    "TOTAL_EMP", "EMP_TOTAL", "TOTAL_EMPLOYMENT", "EMPLOYMENT",
    "CHAR_EMP21", "EMP21", "TOT_EMP",
]
POP_CANDIDATES = ["CHAR_POP21", "POP21", "POPULATION", "TOTAL_POP"]

# Rows whose CMA field means "not part of any CMA". StatCan uses 999 / blank.
NON_CMA_TOKENS = {"", "999", "999.0", "0", "nan", "none", "n/a", "na", "-", "..", "..."}

# PRUID -> name. Stable since 1999 (Nunavut's creation).
PR_NAMES = {
    "10": "Newfoundland and Labrador", "11": "Prince Edward Island",
    "12": "Nova Scotia", "13": "New Brunswick", "24": "Quebec",
    "35": "Ontario", "46": "Manitoba", "47": "Saskatchewan",
    "48": "Alberta", "59": "British Columbia", "60": "Yukon",
    "61": "Northwest Territories", "62": "Nunavut",
}

EFFECT_ORDER = ["DIR", "INDIR", "INDCD"]
EFFECT_LABEL = {"DIR": "direct", "INDIR": "indirect", "INDCD": "induced"}


def pick(df: pd.DataFrame, candidates: list[str], what: str, required=False, override=None):
    """Return the first candidate column present in df (case-insensitive)."""
    if override:
        if override not in df.columns:
            sys.exit(f"ERROR: --{what} column '{override}' not found. Columns: {list(df.columns)}")
        return override
    lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    if required:
        sys.exit(
            f"ERROR: could not find a {what} column. Tried {candidates}.\n"
            f"       Columns present: {list(df.columns)}\n"
            f"       Pass it explicitly with the matching CLI flag."
        )
    return None


def find_value_cols(df: pd.DataFrame, regex: str) -> list[str]:
    pat = re.compile(regex)
    cols = [c for c in df.columns if pat.match(c)]
    if not cols:
        sys.exit(
            f"ERROR: no job-loss columns matched /{regex}/.\n"
            f"       Columns present: {list(df.columns)}\n"
            f"       Override with --value-regex or --value-cols."
        )
    return cols


def scenarios_from(value_cols: list[str], regex: str) -> dict[str, list[str]]:
    """Group matched columns by scenario number -> {'1': ['DIR','INDIR',...]}"""
    pat = re.compile(regex)
    out: dict[str, list[str]] = {}
    for c in value_cols:
        m = pat.match(c)
        if not m or "scenario" not in m.groupdict():
            continue
        s = m.group("scenario")
        out.setdefault(s, []).append(m.group("effect"))
    for s in out:
        out[s] = [e for e in EFFECT_ORDER if e in out[s]]
    return out


# --------------------------------------------------------------------------
# Load and prepare
# --------------------------------------------------------------------------

def derive_province_from_id(df: pd.DataFrame, id_col: str, log: list[str]) -> None:
    """
    A CSD DGUID looks like 2021A00053520005: vintage + type + schema(0005=CSD)
    + PRUID(35) + CDUID(20) + CSD(005). The province is the first two digits of
    the trailing 7-character standard geographic code, so no crosswalk is needed.
    CMA membership is NOT encoded and still requires a lookup.
    """
    code = normalize_key(df[id_col]).str[-7:]
    pruid = code.str[:2]
    bad = pruid[~pruid.isin(PR_NAMES)].dropna().unique()
    if len(bad):
        log.append(f"Province: {len(bad)} unrecognised province codes derived from {id_col}: "
                   f"{sorted(bad)[:10]} — check the id column is really a CSD DGUID/UID")
    df["PRUID"] = pruid
    df["PRNAME"] = pruid.map(PR_NAMES)
    counts = df["PRNAME"].value_counts()
    log.append(f"Province: derived PRUID from {id_col} ({len(counts)} provinces/territories, "
               f"{int(df['PRNAME'].isna().sum())} unresolved)")


def read_table(path: Path, usecols=None) -> pd.DataFrame:
    if not path.exists():
        sys.exit(f"ERROR: file not found: {path}")
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        return pd.read_excel(path, dtype=str, usecols=usecols)
    if path.suffix.lower() == ".json":
        return pd.read_json(path, dtype=str)
    return pd.read_csv(path, dtype=str, keep_default_na=True, usecols=usecols)


def peek_columns(path: Path) -> pd.DataFrame:
    """Header-only read, so we can choose columns before loading a large file."""
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        return pd.read_excel(path, dtype=str, nrows=0)
    if path.suffix.lower() == ".json":
        return pd.read_json(path, dtype=str).head(0)
    return pd.read_csv(path, dtype=str, nrows=0)


def to_numeric(df: pd.DataFrame, cols: list[str], log: list[str]) -> pd.DataFrame:
    """Coerce value columns to float, stripping commas/spaces. Log what breaks."""
    for c in cols:
        raw = df[c]
        cleaned = (
            raw.astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.strip()
            .replace({"": None, "nan": None, "-": None, "..": None, "x": None, "X": None,
                      "F": None, "f": None})  # StatCan suppression flags
        )
        num = pd.to_numeric(cleaned, errors="coerce")
        bad = int(num.isna().sum() - raw.isna().sum())
        if bad > 0:
            log.append(f"  {c}: {bad} non-numeric/suppressed values coerced to NaN (treated as 0 in sums)")
        neg, pos = int((num < 0).sum()), int((num > 0).sum())
        if neg and pos:
            log.append(f"  {c}: MIXED SIGNS ({neg} negative, {pos} positive) — sums will net "
                       f"gains against losses in this field")
        df[c] = num
    return df


def apply_sign(df: pd.DataFrame, cols: list[str], mode: str, log: list[str]) -> None:
    """
    Impact models often emit job losses as negative numbers. Bar lengths and
    'top ten hardest hit' rankings both want positive magnitudes, so flip once
    here rather than scattering Math.abs() through the chart code.
    """
    finite = df[cols].to_numpy(dtype="float64")
    has_neg = bool((finite < 0).any())
    has_pos = bool((finite > 0).any())
    if mode == "keep":
        log.append("  signs left as found (--sign keep)")
        return
    if mode == "abs" or (mode == "auto" and has_neg and not has_pos):
        df[cols] = df[cols].abs()
        log.append("  all job fields were <= 0 (losses); converted to positive magnitudes. "
                   "Every output number is now a job LOSS — label the charts accordingly.")
        return
    if has_neg and has_pos:
        log.append("  WARNING: job fields contain BOTH positive and negative values. "
                   "Left as-is; sums will net gains against losses. Decide deliberately "
                   "and rerun with --sign abs or --sign keep.")


def report_missing(df: pd.DataFrame, cols: list[str], id_col: str, log: list[str]) -> None:
    """Distinguish 'no estimate produced' from 'estimated as zero'."""
    all_na = df[cols].isna().all(axis=1)
    n = int(all_na.sum())
    if n:
        log.append(f"  {n:,} of {len(df):,} CSDs have NO estimate in any scenario field. "
                   f"They contribute 0 to every rollup, which is the right arithmetic but "
                   f"means '0 jobs lost' and 'not modelled' look identical downstream.")
    all_zero = (df[cols].fillna(0) == 0).all(axis=1) & ~all_na
    if int(all_zero.sum()):
        log.append(f"  {int(all_zero.sum()):,} CSDs are modelled at exactly zero in every field.")


def attach_names(agg: pd.DataFrame, names_path: Path | None, level_filter: str | None,
                 id_cands: list[str], log: list[str]) -> tuple[pd.DataFrame, int]:
    """Label aggregated units from an external file, optionally filtering by GEO_LEVEL."""
    if not names_path:
        return agg, 0
    head = peek_columns(names_path)
    nid = pick(head, list(id_cands) + ["DGUID", "GEO_UID"],
               "CMA id (in names file)", required=True)
    keep = [nid] + [c for c in ("GEO_NAME", "GEO_LEVEL") if c in head.columns]
    nm = read_table(names_path, usecols=keep).drop_duplicates(subset=[nid])
    nm[nid] = normalize_key(nm[nid])

    if level_filter:
        if "GEO_LEVEL" not in nm.columns:
            sys.exit("ERROR: --cma-level-filter given but the names file has no GEO_LEVEL column")
        before = len(nm)
        nm = nm[nm["GEO_LEVEL"].str.strip() == level_filter]
        log.append(f"CMA names: filtered {before} to {len(nm)} units where "
                   f"GEO_LEVEL == '{level_filter}'")

    out = agg.merge(nm, how="left", left_on="GEO_UID", right_on=nid, suffixes=("", "_nm"))
    dropped = 0
    named = out["GEO_NAME_nm"] if "GEO_NAME_nm" in out.columns else out.get("GEO_NAME")
    if named is not None:
        unmatched = out.loc[named.isna(), "GEO_UID"].tolist()
        dropped = len(unmatched)
        if unmatched:
            log.append(f"CMA names: {dropped} aggregated units had no name/level match and "
                       f"were dropped (census agglomerations and the Non-CMA bucket). "
                       f"CMA output is now a SUBSET of the national total by design.")
        out = out.loc[named.notna()].copy()
        out["GEO_NAME"] = named.loc[named.notna()].to_numpy()
    drop = [c for c in out.columns if c.endswith("_nm") or c == nid]
    return out.drop(columns=drop, errors="ignore").reset_index(drop=True), dropped


def attach_denominator(agg: pd.DataFrame, path: Path | None, col_override: str | None,
                       kind: str, job_cols: list[str], id_cands: list[str],
                       level: str, log: list[str],
                       id_override: str | None = None) -> tuple[pd.DataFrame, list[str]]:
    """
    Join a denominator that is already at the aggregated geography and derive
    rates from it. Numerator and denominator are both aggregate totals here, so
    this is still a ratio-of-sums, not a mean-of-ratios.

    kind="employment" -> {metric}_Pct   (jobs / employment * 100)
    kind="population" -> {metric}_Per1k (jobs / population * 1000). Population is
    NOT a share of employment; label charts accordingly.
    """
    if not path:
        return agg, []
    head = peek_columns(path)
    did = pick(head, list(id_cands) + ["DGUID", "GEO_UID"],
               f"{level} id (in denominator file)", required=True, override=id_override)
    dcol = col_override or pick(head, EMP_CANDIDATES + POP_CANDIDATES,
                                "denominator-col", required=True)
    dn = read_table(path, usecols=[did, dcol]).drop_duplicates(subset=[did])
    dn[did] = normalize_key(dn[did])
    dn[dcol] = pd.to_numeric(
        dn[dcol].astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce")

    out = agg.merge(dn, how="left", left_on="GEO_UID", right_on=did, suffixes=("", "_dn"))
    matched = int(out[dcol].notna().sum())
    log.append(f"{level} denominator: '{dcol}' from {path.name} matched {matched} of "
               f"{len(out)} units")
    if matched < len(out):
        missing = out.loc[out[dcol].isna(), "GEO_UID"].tolist()
        log.append(f"  no denominator for {len(missing)} units, rates left null: {missing[:8]}")

    denom = out[dcol].replace(0, np.nan)
    added = []
    for c in job_cols:
        stem = c.removesuffix("_Jobs")
        if kind == "employment":
            out[f"{stem}_Pct"] = (out[c] / denom * 100).round(3)
            added.append(f"{stem}_Pct")
        else:
            out[f"{stem}_Per1k"] = (out[c] / denom * 1000).round(3)
            added.append(f"{stem}_Per1k")
    if kind == "population":
        log.append("  rates are per 1,000 RESIDENTS, not a share of employment — "
                   "do not label these as '% of employment'")
    out = out.rename(columns={dcol: "DENOM"}).drop(
        columns=[c for c in out.columns if c.endswith("_dn") or c == did], errors="ignore")
    return out, added


def normalize_key(s: pd.Series) -> pd.Series:
    """Strip whitespace and any trailing '.0' from IDs read as strings."""
    return (
        s.astype(str).str.strip().str.replace(r"\.0$", "", regex=True).replace({"nan": None})
    )


def attach_lookup(csd: pd.DataFrame, csd_id: str, lookup_path: Path | None,
                  id_cands, name_cands, level: str, log: list[str]):
    """
    Return (csd_frame, id_col, name_col) for `level`, joining an external lookup
    if needed. Prefers columns already on the CSD table.
    """
    id_col = pick(csd, id_cands, f"{level} id")
    name_col = pick(csd, name_cands, f"{level} name")
    if id_col:
        if not lookup_path:
            log.append(f"{level}: using columns already on the CSD file ({id_col}"
                       + (f", {name_col})" if name_col else ")"))
            return csd, id_col, name_col
        log.append(f"{level}: CSD file has {id_col}, but --{level.lower()}-lookup was given; the lookup wins")

    if not lookup_path:
        sys.exit(
            f"ERROR: no {level} column on the CSD file and no lookup supplied.\n"
            f"       Tried {id_cands}. Pass --{level.lower()}-lookup with a CSD->{level} crosswalk."
        )

    head = peek_columns(lookup_path)
    lk_csd = pick(head, CSD_ID_CANDIDATES, "CSD id (in lookup)", required=True)
    lk_id = pick(head, id_cands, f"{level} id (in lookup)", required=True)
    lk_name = pick(head, name_cands, f"{level} name (in lookup)")

    keep = [lk_csd, lk_id] + ([lk_name] if lk_name and lk_name != lk_id else [])
    lk = read_table(lookup_path, usecols=keep)
    n_raw = len(lk)
    lk[lk_csd] = normalize_key(lk[lk_csd])
    lk[lk_id] = normalize_key(lk[lk_id])

    # Correspondence files are published at dissemination-block level, so most of
    # those rows are repeats. Collapsing them is only safe if the mapping agrees.
    pairs = lk.drop_duplicates(subset=[lk_csd, lk_id])
    conflicting = pairs.groupby(lk_csd, dropna=False).size()
    conflicting = conflicting[conflicting > 1]
    if len(conflicting):
        log.append(f"{level} lookup: {len(conflicting)} CSDs map to more than one {level} "
                   f"(e.g. {list(conflicting.index[:5])}). Kept the first; these CSDs are "
                   f"now MISASSIGNED and their jobs land in one {level} only. Split the "
                   f"CSD before aggregating if this is real.")
    lk = lk.drop_duplicates(subset=[lk_csd], keep="first")
    if n_raw != len(lk):
        log.append(f"{level} lookup: collapsed {n_raw:,} rows to {len(lk):,} unique CSDs"
                   + ("" if len(conflicting) else ", mapping consistent throughout"))

    before = len(csd)
    csd_key = "__csd_key__"
    csd[csd_key] = normalize_key(csd[csd_id])
    merged = csd.merge(lk, how="left", left_on=csd_key, right_on=lk_csd,
                       suffixes=("", f"_{level.lower()}lk"))
    assert len(merged) == before, "lookup join changed row count — duplicate keys remain"

    unmatched = int(merged[lk_id].isna().sum())
    if unmatched:
        log.append(f"{level} lookup: {unmatched} of {before} CSDs found no match and will "
                   f"land in the 'Unassigned' bucket")

    merged.drop(columns=[csd_key], inplace=True, errors="ignore")
    return merged, lk_id, lk_name


# --------------------------------------------------------------------------
# Aggregation
# --------------------------------------------------------------------------

def derive_totals(df: pd.DataFrame, scen: dict[str, list[str]], log: list[str]) -> list[str]:
    """Add S{n}_TOT_Jobs = DIR + INDIR + INDCD. Returns the new column names."""
    added = []
    for s, effects in sorted(scen.items(), key=lambda kv: int(kv[0])):
        parts = [f"S{s}_{e}_Jobs" for e in effects]
        col = f"S{s}_TOT_Jobs"
        df[col] = df[parts].fillna(0).sum(axis=1)
        added.append(col)
        if len(effects) < 3:
            log.append(f"  S{s}: only {', '.join(EFFECT_LABEL[e] for e in effects)} present; "
                       f"{col} is a partial total")
    return added


def aggregate(csd: pd.DataFrame, group_id: str, group_name: str | None,
              sum_cols: list[str], geo_level: str, unassigned_label: str,
              drop_unassigned: bool, log: list[str]) -> pd.DataFrame:
    """Group CSDs and SUM the value columns. No averaging anywhere."""
    df = csd.copy()
    key = normalize_key(df[group_id])
    is_unassigned = key.isna() | key.str.lower().isin(NON_CMA_TOKENS)

    n_un = int(is_unassigned.sum())
    if n_un:
        jc = [c for c in sum_cols if c.endswith("_Jobs")] or sum_cols
        jobs_un = float(df.loc[is_unassigned, jc].fillna(0).to_numpy().sum())
        log.append(f"{geo_level}: {n_un} CSDs are outside any {geo_level} "
                   f"({jobs_un:,.0f} jobs across all scenario/effect fields). "
                   + ("Dropped." if drop_unassigned
                      else f"Kept as '{unassigned_label}' so totals reconcile."))
    if drop_unassigned:
        df = df.loc[~is_unassigned].copy()
        key = key.loc[df.index]
    else:
        key = key.mask(is_unassigned, unassigned_label)

    df["__gid__"] = key
    if group_name and group_name in df.columns:
        names = df[group_name].astype(str).str.strip()
        names = names.mask(is_unassigned.reindex(df.index, fill_value=False), unassigned_label)
        df["__gname__"] = names
    else:
        df["__gname__"] = df["__gid__"]

    # Name per group: use the modal name, and flag disagreement.
    name_map = df.groupby("__gid__")["__gname__"].agg(
        lambda s: s.value_counts().idxmax() if len(s) else ""
    )
    conflicts = df.groupby("__gid__")["__gname__"].nunique()
    for gid, n in conflicts[conflicts > 1].items():
        log.append(f"{geo_level} {gid}: {n} different names in the source; used '{name_map[gid]}'")

    out = df.groupby("__gid__", dropna=False)[sum_cols].sum(min_count=1).reset_index()
    out.insert(0, "GEO_LEVEL", geo_level)
    out.insert(1, "GEO_UID", out["__gid__"])
    out.insert(2, "GEO_NAME", out["__gid__"].map(name_map))
    out["CSD_COUNT"] = df.groupby("__gid__").size().reindex(out["__gid__"]).to_numpy()
    out.drop(columns=["__gid__"], inplace=True)
    return out


def add_percentages(df: pd.DataFrame, job_cols: list[str], emp_col: str | None,
                    pop_col: str | None, log: list[str]) -> list[str]:
    """
    Percentages computed on the AGGREGATED numerator and denominator.
    This is the whole reason the script exists — do not move it upstream.
    """
    added = []
    if not emp_col or emp_col not in df.columns:
        if not any("no employment denominator" in line for line in log):
            log.append("  no employment denominator available — percentage fields skipped. "
                       "Add a CSD-level employment column and pass --employment-col to get "
                       "'% of employment' fields computed after aggregation.")
        return added
    denom = df[emp_col].replace(0, np.nan)
    for c in job_cols:
        pct = f"{c.removesuffix('_Jobs')}_Pct"
        df[pct] = (df[c] / denom * 100).round(3)
        added.append(pct)
    if pop_col and pop_col in df.columns:
        pdenom = df[pop_col].replace(0, np.nan)
        for c in job_cols:
            if c.endswith("_TOT_Jobs"):
                col = f"{c.removesuffix('_Jobs')}_PctPop"
                df[col] = (df[c] / pdenom * 100).round(3)
                added.append(col)
    return added


def quantile_breaks(df: pd.DataFrame, cols: list[str], n_classes=5) -> dict[str, list[float]]:
    """
    n_classes-1 upper bounds per metric, for the graduated colour ramps the
    Svelte charts expect (GRADUATED_COLORS has 5 entries -> 4 breakpoints).
    """
    out = {}
    qs = [i / n_classes for i in range(1, n_classes)]
    for c in cols:
        s = pd.to_numeric(df[c], errors="coerce").dropna()
        s = s[s > 0]
        if len(s) < n_classes:
            continue
        vals = [float(s.quantile(q)) for q in qs]
        # round sensibly: percentages to 1dp, counts to a readable magnitude
        if c.endswith(("_Pct", "_PctPop")):
            vals = [round(v, 1) for v in vals]
        else:
            vals = [float(int(round(v, -max(0, len(str(int(v))) - 2)))) if v >= 10 else round(v, 1)
                    for v in vals]
        out[c] = sorted(set(vals)) if len(set(vals)) == len(vals) else vals
    return out


# --------------------------------------------------------------------------
# Reconciliation
# --------------------------------------------------------------------------

def sanity_checks(csd: pd.DataFrame, prov: pd.DataFrame, scen: dict[str, list[str]],
                 job_cols: list[str], log: list[str]) -> None:
    """
    Arithmetic checks confirm the rollup is faithful to its input. These check
    whether the input itself looks right, which reconciliation cannot tell you.
    """
    log.append("\nPLAUSIBILITY CHECKS (on the source estimates, not the rollup)")
    flagged = False

    # Whole provinces at zero are almost always an upstream join failure.
    tot_cols = [c for c in job_cols if c.endswith("_TOT_Jobs")] or job_cols
    zero_pr = prov.loc[prov[tot_cols].fillna(0).sum(axis=1) == 0, "GEO_NAME"].tolist()
    if zero_pr:
        flagged = True
        log.append(f"  {len(zero_pr)} province(s) are exactly ZERO in every scenario: "
                   f"{zero_pr}. A whole province at zero usually means missing input data, "
                   f"not the absence of tariff exposure. Verify before publishing.")

    # Induced effects larger than direct is unusual for an I-O model.
    for sc, effects in sorted(scen.items(), key=lambda kv: int(kv[0])):
        if not {"DIR", "INDIR", "INDCD"} <= set(effects):
            continue
        d = abs(float(csd[f"S{sc}_DIR_Jobs"].fillna(0).sum()))
        ind = abs(float(csd[f"S{sc}_INDIR_Jobs"].fillna(0).sum()))
        icd = abs(float(csd[f"S{sc}_INDCD_Jobs"].fillna(0).sum()))
        if d > 0 and (ind > d or icd > d):
            flagged = True
            log.append(f"  S{sc}: indirect is {ind / d:.1f}x direct and induced is "
                       f"{icd / d:.1f}x direct. Input-output models normally give "
                       f"direct > indirect > induced, so check the columns are not "
                       f"transposed and that the multipliers are Type II as intended.")

    if not flagged:
        log.append("  no anomalies detected")


def reconcile(csd: pd.DataFrame, cma: pd.DataFrame, prov: pd.DataFrame,
              cols: list[str], cma_dropped: bool, log: list[str]) -> None:
    log.append("\nRECONCILIATION (CSD sum vs rollup sum)")
    pairs = [("Province", prov, True)]
    if cma is not None:
        pairs.append(("CMA", cma, not cma_dropped))
    for name, agg, expect_equal in pairs:
        bad = 0
        for c in cols:
            src = float(csd[c].fillna(0).sum())
            got = float(agg[c].fillna(0).sum())
            diff = got - src
            if expect_equal and abs(diff) > max(1e-6, abs(src) * 1e-9):
                bad += 1
                log.append(f"  MISMATCH {name} {c}: CSD={src:,.2f} rollup={got:,.2f} "
                           f"diff={diff:,.2f}")
        if expect_equal and bad:
            log.append(f"  {name}: {bad} of {len(cols)} fields FAILED to reconcile — "
                       f"do not use this output until resolved")
        elif expect_equal:
            log.append(f"  {name}: all {len(cols)} summed fields reconcile to the CSD totals")
        else:
            coverage = (agg[cols].fillna(0).to_numpy().sum()
                        / max(1e-9, csd[cols].fillna(0).to_numpy().sum()) * 100)
            log.append(f"  CMA: covers {coverage:.1f}% of national job effects "
                       f"(the rest is outside CMA boundaries — CMA totals are NOT national totals)")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--csd", required=True, type=Path, help="CSD-level scenario file (csv/xlsx)")
    p.add_argument("--cma-lookup", type=Path, help="CSD -> CMA crosswalk (only if CSD file lacks CMAUID)")
    p.add_argument("--prov-lookup", type=Path, help="CSD -> province crosswalk (only if CSD file lacks PRUID)")
    p.add_argument("--outdir", type=Path, default=Path("output"))
    p.add_argument("--csd-id-col", help="override CSD id column")
    p.add_argument("--employment-col", help="override total-employment denominator column")
    p.add_argument("--population-col", help="override population column")
    p.add_argument("--value-cols", nargs="+", help="explicit list of job-loss columns to sum")
    p.add_argument("--value-regex", default=VALUE_REGEX, help=f"default: {VALUE_REGEX}")
    p.add_argument("--sign", choices=["auto", "keep", "abs"], default="auto",
                   help="auto (default): if job fields are all <=0, convert to positive "
                        "magnitudes so charts read as losses; keep: leave signs as-is; "
                        "abs: always take absolute values")
    p.add_argument("--cma-denominator", type=Path,
                   help="CSV/JSON at CMA level with a CMA DGUID + a denominator column, "
                        "joined AFTER aggregation to derive rates")
    p.add_argument("--prov-denominator", type=Path,
                   help="same, at province level (join key must match GEO_UID, i.e. PRUID)")
    p.add_argument("--denominator-id-col",
                   help="join key in the denominator file(s), if not auto-detected")
    p.add_argument("--denominator-col",
                   help="column name in the denominator file(s)")
    p.add_argument("--denominator-kind", choices=["employment", "population"],
                   default="employment",
                   help="employment -> *_Pct fields; population -> *_Per1k fields")
    p.add_argument("--cma-names", type=Path,
                   help="CSV/JSON with a CMA DGUID + GEO_NAME (e.g. your existing "
                        "cma_tariffs_counts_centroidsv2.json) to label CMAs")
    p.add_argument("--cma-level-filter", default=None,
                   help="keep only rows whose GEO_LEVEL in --cma-names equals this, "
                        "e.g. \"Census metropolitan area\" to exclude census agglomerations")
    p.add_argument("--derive-province-from-dguid", action="store_true",
                   help="derive PRUID/PRNAME from the CSD DGUID/UID instead of a lookup")
    p.add_argument("--skip-cma", action="store_true",
                   help="produce the province rollup only (use when you have no CSD->CMA crosswalk yet)")
    p.add_argument("--drop-non-cma", action="store_true",
                   help="drop CSDs outside any CMA instead of bucketing them as 'Non-CMA'")
    p.add_argument("--no-totals", action="store_true",
                   help="do not derive S*_TOT_Jobs = DIR+INDIR+INDCD")
    p.add_argument("--inspect", action="store_true",
                   help="print detected schema and exit without writing")
    args = p.parse_args()

    log: list[str] = []
    csd = read_table(args.csd)
    log.append(f"Input: {args.csd}  ({len(csd):,} rows, {len(csd.columns)} columns)")

    csd_id = pick(csd, CSD_ID_CANDIDATES, "csd-id-col", required=True, override=args.csd_id_col)
    emp_col = pick(csd, EMP_CANDIDATES, "employment-col", override=args.employment_col)
    pop_col = pick(csd, POP_CANDIDATES, "population-col", override=args.population_col)
    value_cols = args.value_cols or find_value_cols(csd, args.value_regex)
    scen = scenarios_from(value_cols, args.value_regex)

    log.append(f"CSD id: {csd_id}")
    log.append(f"Employment denominator: {emp_col or 'NONE — percentages will be skipped'}")
    log.append(f"Population: {pop_col or 'none'}")
    log.append(f"Job-loss fields ({len(value_cols)}): {', '.join(value_cols)}")
    if scen:
        log.append("Scenarios detected: " + "; ".join(
            f"S{s} [{', '.join(EFFECT_LABEL[e] for e in eff)}]"
            for s, eff in sorted(scen.items(), key=lambda kv: int(kv[0]))))

    if args.inspect:
        print("\n".join(log))
        return

    dupe_csd = int(normalize_key(csd[csd_id]).duplicated().sum())
    if dupe_csd:
        log.append(f"WARNING: {dupe_csd} duplicate {csd_id} values in the CSD file. "
                   f"Duplicates inflate every rollup — de-duplicate before trusting output.")

    log.append("\nNUMERIC COERCION")
    numeric_cols = value_cols + [c for c in (emp_col, pop_col) if c]
    csd = to_numeric(csd, numeric_cols, log)

    log.append("\nSIGN AND MISSINGNESS")
    apply_sign(csd, value_cols, args.sign, log)
    report_missing(csd, value_cols, csd_id, log)

    log.append("\nDERIVED TOTALS")
    total_cols = [] if args.no_totals else derive_totals(csd, scen, log)
    log.append("  " + (", ".join(total_cols) if total_cols else "(skipped)"))

    sum_cols = value_cols + total_cols + [c for c in (emp_col, pop_col) if c]
    job_cols = value_cols + total_cols

    log.append("\nGEOGRAPHY")
    if args.derive_province_from_dguid:
        derive_province_from_id(csd, csd_id, log)

    cma = None
    cma_is_subset = args.drop_non_cma
    if args.skip_cma:
        log.append("CMA: skipped (--skip-cma)")
    else:
        csd, cma_id, cma_name = attach_lookup(csd, csd_id, args.cma_lookup,
                                              CMA_ID_CANDIDATES, CMA_NAME_CANDIDATES, "CMA", log)
        cma = aggregate(csd, cma_id, cma_name, sum_cols, "Census metropolitan area",
                        "Non-CMA", args.drop_non_cma, log)
        cma, n_dropped = attach_names(cma, args.cma_names, args.cma_level_filter,
                                      CMA_ID_CANDIDATES, log)
        cma_is_subset = args.drop_non_cma or n_dropped > 0

    csd, prov_id, prov_name = attach_lookup(csd, csd_id, args.prov_lookup,
                                            PR_ID_CANDIDATES, PR_NAME_CANDIDATES, "Province", log)
    prov = aggregate(csd, prov_id, prov_name, sum_cols, "Province/territory",
                     "Unassigned", False, log)

    log.append("\nPERCENTAGES (computed after aggregation)")
    pct_cma = add_percentages(cma, job_cols, emp_col, pop_col, log) if cma is not None else []
    pct_prov = add_percentages(prov, job_cols, emp_col, pop_col, log)

    if cma is not None:
        cma, extra = attach_denominator(cma, args.cma_denominator, args.denominator_col,
                                        args.denominator_kind, job_cols,
                                        CMA_ID_CANDIDATES, "CMA", log,
                                        args.denominator_id_col)
        pct_cma += extra
    prov, extra = attach_denominator(prov, args.prov_denominator, args.denominator_col,
                                     args.denominator_kind, job_cols,
                                     PR_ID_CANDIDATES, "Province", log,
                                     args.denominator_id_col)
    pct_prov += extra
    if pct_cma or pct_prov:
        log.append(f"  added {len(pct_cma)} percentage fields at each level")

    sanity_checks(csd, prov, scen, job_cols, log)
    reconcile(csd, cma, prov, job_cols, cma_is_subset, log)

    # Sort descending on the first scenario total so the files are chart-ready.
    rank_col = (total_cols or job_cols)[0]
    prov = prov.sort_values(rank_col, ascending=False).reset_index(drop=True)
    outputs = {"all_scenarios_province": prov}
    if cma is not None:
        cma = cma.sort_values(rank_col, ascending=False).reset_index(drop=True)
        outputs = {"all_scenarios_cma": cma, **outputs}

    args.outdir.mkdir(parents=True, exist_ok=True)
    for stem, df in outputs.items():
        df.to_csv(args.outdir / f"{stem}.csv", index=False)
        df.to_json(args.outdir / f"{stem}.json", orient="records", indent=1)

    breaks = {"province": quantile_breaks(prov, job_cols + pct_prov)}
    if cma is not None:
        breaks["cma"] = quantile_breaks(cma, job_cols + pct_cma)
    (args.outdir / "rollup_breaks.json").write_text(json.dumps(breaks, indent=1))

    log.append("\nOUTPUT")
    for stem, df in outputs.items():
        log.append(f"  {args.outdir / (stem + '.csv')}  ({len(df)} rows, {len(df.columns)} cols)")
        log.append(f"  {args.outdir / (stem + '.json')}")
    log.append(f"  {args.outdir / 'rollup_breaks.json'}")

    report = "\n".join(log)
    (args.outdir / "rollup_report.txt").write_text(report + "\n")
    print(report)
    print(f"\nReport written to {args.outdir / 'rollup_report.txt'}")


if __name__ == "__main__":
    main()
