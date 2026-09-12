#!/usr/bin/env python3
"""
run_rollup.py

One command for the whole rollup. Run from the repo root:

    python analysis/scripts/run_rollup.py

Steps:
  1. Read the two Census Profile files, pull the characteristics we need,
     and write cma_denominator.csv / prov_denominator.csv.
  2. Call roll_up_to_cma_prov.py with the right flags.

Adjust the PATHS block below if your directory layout differs. Nothing else
in here should need editing.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

# --------------------------------------------------------------------------
# PATHS - edit these if your layout differs
# --------------------------------------------------------------------------
CENSUS_DIR = Path("data/census")
CENSUS_CMA = CENSUS_DIR / "98-401-X2021002_English_CSV_data.csv"   # CMA/CA profile
CENSUS_PROV = CENSUS_DIR / "98-401-X2021001_English_CSV_data.csv"  # province profile

SCRIPT_DIR = Path("analysis/scripts")
INPUT_DIR = SCRIPT_DIR / "input"
OUTPUT_DIR = SCRIPT_DIR / "output"
ROLLUP = SCRIPT_DIR / "roll_up_to_cma_prov.py"

CSD_FILE = INPUT_DIR / "all_scenarios_csd.csv"
CMA_LOOKUP = INPUT_DIR / "2021_98260004.csv"

# --------------------------------------------------------------------------
# Census Profile characteristics (IDs confirmed from the 2021 metadata files)
# --------------------------------------------------------------------------
CHARACTERISTICS = {
    1: "CHAR_POP21",    # Population, 2021
    2223: "LF_BASE15",  # Total - Population aged 15 years and over by labour force status
    2225: "EMP_TOTAL",  # Employed
}

# Which column becomes the denominator, and how the rates are labelled.
# "employment" -> S*_Pct fields.  "population" -> S*_Per1k fields.
DENOMINATOR_COL = "EMP_TOTAL"
DENOMINATOR_KIND = "employment"

CMA_LEVEL = "Census metropolitan area"
PROV_DGUID_PREFIX = "2021A0002"  # province/territory schema; excludes Canada


def fail(msg: str) -> None:
    sys.exit(f"\nERROR: {msg}\n")


def load_profile(path: Path, label: str) -> pd.DataFrame:
    """Read a Census Profile data file and pivot the characteristics we need."""
    if not path.exists():
        fail(f"{label} profile not found at {path}\n"
             f"       Fix the PATHS block at the top of this script.")

    print(f"[{label}] reading {path.name}")
    cols = ["DGUID", "GEO_LEVEL", "GEO_NAME", "CHARACTERISTIC_ID", "C1_COUNT_TOTAL"]
    df = pd.read_csv(path, encoding="latin", usecols=cols, low_memory=False)
    df = df[df.CHARACTERISTIC_ID.isin(CHARACTERISTICS)]
    if df.empty:
        fail(f"{label}: none of the characteristic IDs {list(CHARACTERISTICS)} are in "
             f"this file. Check the IDs against its _meta.txt.")

    df["CHAR_COL"] = df.CHARACTERISTIC_ID.map(CHARACTERISTICS)

    # Suppression flags (x, F, .., ...) become NaN rather than a bogus denominator.
    df["C1_COUNT_TOTAL"] = pd.to_numeric(
        df.C1_COUNT_TOTAL.astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce")

    wide = df.pivot_table(index=["DGUID", "GEO_LEVEL", "GEO_NAME"],
                          columns="CHAR_COL", values="C1_COUNT_TOTAL",
                          aggfunc="first").reset_index()
    wide.columns.name = None

    missing = [c for c in CHARACTERISTICS.values() if c not in wide.columns]
    if missing:
        fail(f"{label}: characteristics missing after pivot: {missing}")
    return wide


def build_cma_denominator(wide: pd.DataFrame) -> Path:
    levels = sorted(wide.GEO_LEVEL.dropna().unique())
    if CMA_LEVEL not in levels:
        fail(f"CMA: no rows with GEO_LEVEL == '{CMA_LEVEL}'.\n"
             f"       Levels present: {levels}\n"
             f"       Set CMA_LEVEL at the top of this script to the exact string.")

    den = wide[wide.GEO_LEVEL == CMA_LEVEL].copy()
    n_sup = int(den[DENOMINATOR_COL].isna().sum())
    print(f"[CMA] {len(den)} census metropolitan areas"
          + (f", {n_sup} with a suppressed {DENOMINATOR_COL} (rates left null)" if n_sup else ""))

    out = INPUT_DIR / "cma_denominator.csv"
    den[["DGUID", "GEO_NAME", "GEO_LEVEL"] + list(CHARACTERISTICS.values())].to_csv(
        out, index=False)
    return out


def build_prov_denominator(wide: pd.DataFrame) -> Path:
    """
    Province rollup keys on a bare PRUID ('35'), but the profile ships DGUIDs
    ('2021A000235'). Slicing the last two characters of Canada's DGUID
    ('2021A000011124') yields '24' - Quebec's code - so Canada must be excluded
    by schema BEFORE the key is derived, or it silently overwrites Quebec.
    """
    den = wide[wide.DGUID.astype(str).str.startswith(PROV_DGUID_PREFIX)].copy()
    if len(den) != 13:
        fail(f"Province: expected 13 provinces/territories, got {len(den)}.\n"
             f"       DGUIDs matched: {den.DGUID.tolist()}\n"
             f"       Check PROV_DGUID_PREFIX.")

    den["PRUID"] = den.DGUID.astype(str).str[-2:]
    if den.PRUID.duplicated().any():
        fail(f"Province: duplicate PRUIDs derived: "
             f"{den.loc[den.PRUID.duplicated(keep=False), ['DGUID', 'GEO_NAME']].to_dict('records')}")

    n_sup = int(den[DENOMINATOR_COL].isna().sum())
    print(f"[Province] 13 provinces/territories"
          + (f", {n_sup} with a suppressed {DENOMINATOR_COL} (rates left null)" if n_sup else ""))

    out = INPUT_DIR / "prov_denominator.csv"
    den[["PRUID", "DGUID", "GEO_NAME"] + list(CHARACTERISTICS.values())].to_csv(
        out, index=False)
    return out


def main() -> None:
    for p, what in [(CSD_FILE, "CSD scenario file"), (CMA_LOOKUP, "CMA correspondence file"),
                    (ROLLUP, "rollup script")]:
        if not p.exists():
            fail(f"{what} not found at {p}")

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("STEP 1  building denominators from Census Profile")
    print("=" * 70)
    cma_den = build_cma_denominator(load_profile(CENSUS_CMA, "CMA"))
    prov_den = build_prov_denominator(load_profile(CENSUS_PROV, "Province"))
    print(f"\nwrote {cma_den}\nwrote {prov_den}")

    cmd = [
        sys.executable, str(ROLLUP),
        "--csd", str(CSD_FILE),
        "--cma-lookup", str(CMA_LOOKUP),
        "--derive-province-from-dguid",
        "--cma-names", str(cma_den),
        "--cma-level-filter", CMA_LEVEL,
        "--cma-denominator", str(cma_den),
        "--prov-denominator", str(prov_den),
        "--denominator-col", DENOMINATOR_COL,
        "--denominator-kind", DENOMINATOR_KIND,
        "--outdir", str(OUTPUT_DIR),
    ]

    print("\n" + "=" * 70)
    print("STEP 2  running the rollup")
    print("=" * 70)
    result = subprocess.run(cmd)
    if result.returncode != 0:
        fail(f"rollup exited with code {result.returncode}")

    print("\n" + "=" * 70)
    print("Check the report for these lines before trusting the rates:")
    print("  'CMA denominator: ... matched N of N'")
    print("  'Province denominator: ... matched 13 of 13'")
    print("  the PLAUSIBILITY CHECKS block")
    print(f"\nReport: {OUTPUT_DIR / 'rollup_report.txt'}")
    print("=" * 70)


if __name__ == "__main__":
    main()
