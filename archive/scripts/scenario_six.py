"""
Scenario 6 (Auto & Parts) — Direct effect job-loss allocation, CSD level.

Pipeline:
1. Extract provincial Direct job-loss (in JOBS, not dollars) for Scenario 6
   from the MRIO workbook, by row-position-joining three sheets that share
   identical (Province x BS_Code) row ordering:
     - 'Delta X - D Level'      -> gives us (Province, BS_Code) per row
     - 'DIR_INDIR_INDCD_SC6'    -> gives us DIR ($) per row
     - 'Jobs Multipliers D'     -> gives us jobs-per-$1M multiplier per row
   Direct_Jobs = DIR($) / 1,000,000 * multiplier

2. Sum Direct_Jobs by province. (Non-shocked BS codes have DIR=0, so this
   naturally isolates the ~9 auto/parts codes without needing to filter --
   but we filter anyway below for an explicit sanity check.)

3. Load CSD-level raw employment by NAICS from trail_csd.csv (business_grouped
   output -- UNSMOOTHED, i.e. NOT the 15km-accessibility-adjusted `jobs` table
   used elsewhere in the pipeline for the home-employment estimate. We want
   raw place-of-work counts here, so business_grouped/trail_csd.csv is the
   correct source, not trail5_csd.csv/jobs.)

4. Tag each CSD with its province (via CSDDGUID -> CSDUID -> PRUID prefix,
   same method the notebook already uses in Step 6/cell 17).

5. Allocate: CSD_direct_jobs = provincial_direct_jobs[province] *
   (CSD employment across the 9 NAICS codes / provincial employment across
   those same 9 codes).

6. Merge onto CSD geometry and save as GeoJSON, matching the notebook's own
   output convention (EPSG:4326, driver='GeoJSON').

ADJUST THE PATH CONSTANTS BELOW to match your actual folder structure.
"""

import pandas as pd
import geopandas as gpd
import openpyxl
from pathlib import Path

# ============================================================
# PATHS -- resolved relative to this script's own location, not the
# working directory you happen to run it from (fixes FileNotFoundError
# when running via `python analysis/scripts/scenario_six.py` from elsewhere).
# ============================================================
SCRIPT_DIR = Path(__file__).parent

MRIO_WORKBOOK = SCRIPT_DIR / '../raw/scenario summary - clsd MRIO - as of June 21 2026 - 2022 model.xlsx'
CONCORDANCE_WORKBOOK = SCRIPT_DIR / '../intermediate/NAICS 2022v1 to IOIC 2022 concordance.xlsx'
TRAIL_CSD_CSV = SCRIPT_DIR / '../intermediate/trail_csd.csv'
CSD_SHAPEFILE = SCRIPT_DIR / '../../data/census/lcsd000b21a_e/lcsd000b21a_e.shp'
OUTPUT_GEOJSON = SCRIPT_DIR / '../outputs/geojson/scenario6_direct_csd.geojson'
OUTPUT_CSV = SCRIPT_DIR / '../outputs/csv/scenario6_direct_csd.csv'


def load_bs_to_naics(concordance_path):
    """Build a real BS_Code -> [NAICS codes] lookup from the official
    StatCan NAICS<->IOIC concordance, instead of a hardcoded list."""
    wb = openpyxl.load_workbook(concordance_path)
    ws = wb['English']
    rows = list(ws.iter_rows(min_row=3, values_only=True))  # skip 2 header rows

    lookup = {}
    for r in rows:
        naics, naics_title, bs_code, bs_title = r[0], r[1], r[2], r[3]
        if bs_code is None or naics is None:
            continue
        lookup.setdefault(bs_code, []).append(str(naics))
    return lookup


BS_TO_NAICS = load_bs_to_naics(CONCORDANCE_WORKBOOK)
SCENARIO6_BS_CODES = ['BS336110', 'BS336300']
SCENARIO6_NAICS_CODES = [n for bs in SCENARIO6_BS_CODES for n in BS_TO_NAICS.get(bs, [])]

print(f"✅ Looked up NAICS codes from concordance: {SCENARIO6_NAICS_CODES}")
for bs in SCENARIO6_BS_CODES:
    if bs not in BS_TO_NAICS:
        print(f"⚠️  WARNING: {bs} not found in concordance file -- check the BS code is correct.")

# Province label translation: MRIO workbook uses AB/YT/NT,
# your notebook's province_code dict uses AL/YK/NWT for the same provinces.
MRIO_TO_NOTEBOOK_PROVINCE = {
    'NL': 'NL', 'PEI': 'PEI', 'NS': 'NS', 'NB': 'NB', 'QC': 'QC',
    'ON': 'ON', 'MB': 'MB', 'SK': 'SK', 'AB': 'AL', 'BC': 'BC',
    'YT': 'YK', 'NT': 'NWT', 'NU': 'NU'
}

# Same PRUID -> province-abbreviation dict already used in your notebook (cell 17)
PROVINCE_CODE = {
    10: 'NL', 11: 'PEI', 12: 'NS', 13: 'NB', 24: 'QC', 35: 'ON',
    46: 'MB', 47: 'SK', 48: 'AL', 59: 'BC', 60: 'YK', 61: 'NWT', 62: 'NU'
}


# ============================================================
# STEP 1: Extract provincial Direct job-loss for Scenario 6
# ============================================================
def extract_scenario6_provincial_direct_jobs(workbook_path):
    wb = openpyxl.load_workbook(workbook_path, data_only=True)

    # ---- Delta X - D Level: (Province, BS_Code) per row, forward-filled ----
    delta_x_rows = list(wb['Delta X - D Level'].iter_rows(min_row=4, values_only=True))
    delta_x_pb = []
    current_province = None
    for r in delta_x_rows:
        if r[0] is not None:
            current_province = r[0]
        delta_x_pb.append((current_province, r[3]))

    # ---- DIR_INDIR_INDCD_SC6: has its OWN Province column (r[1]), forward-filled ----
    dir_rows = list(wb['DIR_INDIR_INDCD_SC6'].iter_rows(min_row=2, values_only=True))
    dir_province = []
    dir_values = []
    current_province = None
    for r in dir_rows:
        if r[1] is not None:
            current_province = r[1]
        dir_province.append(current_province)
        dir_values.append(r[4])  # column index 4 = 'DIR'

    # ---- Jobs Multipliers D: has its OWN (Province, BS_Code) columns -- build a
    # real keyed lookup instead of relying on row position for this sheet at all. ----
    mult_rows = list(wb['Jobs Multipliers D'].iter_rows(min_row=2, values_only=True))
    multiplier_lookup = {}
    current_province = None
    for r in mult_rows:
        if r[1] is not None:
            current_province = r[1]
        multiplier_lookup[(current_province, r[2])] = r[4]  # (Province, BS Code) -> multiplier

    # ---- Split Delta X and DIR into per-province blocks, by order of appearance ----
    def split_into_blocks(province_list, payload_list=None):
        blocks = []  # list of (province, [payload...]) in order encountered
        for i, prov in enumerate(province_list):
            if prov in (None, 'Canada'):
                continue
            item = payload_list[i] if payload_list is not None else None
            if blocks and blocks[-1][0] == prov:
                blocks[-1][1].append(item)
            else:
                blocks.append((prov, [item]))
        return blocks

    delta_x_blocks = split_into_blocks([p for p, _ in delta_x_pb], [bs for _, bs in delta_x_pb])
    dir_blocks = split_into_blocks(dir_province, dir_values)

    # ---- Validate block sizes match per province before trusting any alignment ----
    delta_x_by_prov = {prov: bs_codes for prov, bs_codes in delta_x_blocks}
    dir_by_prov = {prov: vals for prov, vals in dir_blocks}

    mismatches = {}
    for prov in delta_x_by_prov:
        dx_len = len(delta_x_by_prov[prov])
        dir_len = len(dir_by_prov.get(prov, []))
        if dx_len != dir_len:
            mismatches[prov] = (dx_len, dir_len)

    if mismatches:
        print(f"⚠️  Per-province block size mismatch between 'Delta X - D Level' and "
              f"'DIR_INDIR_INDCD_SC6': {mismatches}")
        print("    Truncating each mismatched province's block to the shorter length. "
              "If any of these gaps look large/unexpected, stop and inspect that province "
              "manually in Excel before trusting the output.")

    records = []
    for prov, bs_codes in delta_x_blocks:
        dir_vals_for_prov = dir_by_prov.get(prov, [])
        n = min(len(bs_codes), len(dir_vals_for_prov))
        for bs_code, dir_dollars in zip(bs_codes[:n], dir_vals_for_prov[:n]):
            mult = multiplier_lookup.get((prov, bs_code))
            if mult is None:
                print(f"⚠️  No multiplier found for ({prov}, {bs_code}) -- skipping this row.")
                continue
            direct_jobs = (dir_dollars or 0) / 1_000_000 * mult
            records.append({'Province': prov, 'BS_Code': bs_code, 'Direct_Jobs': direct_jobs})

    df = pd.DataFrame(records)

    # Sanity check: confirm only the expected BS codes carry a nonzero contribution
    nonzero = df[df['Direct_Jobs'].abs() > 1e-6]
    unexpected = set(nonzero['BS_Code'].unique()) - set(SCENARIO6_BS_CODES)
    if unexpected:
        print(f"⚠️  WARNING: unexpected BS codes with nonzero Direct_Jobs under Scenario 6: {unexpected}")
        print("    (Sheet1's text description may not match the applied shock -- verify before trusting output.)")
    else:
        print(f"✅ Confirmed: only {SCENARIO6_BS_CODES} carry nonzero direct jobs, as expected.")

    provincial_totals = df.groupby('Province')['Direct_Jobs'].sum().to_dict()
    print(provincial_totals)
    print(f"   National total: {sum(provincial_totals.values()):,.1f} jobs\n")

    # Return per-(Province, BS_Code) rows, NOT pre-summed -- each shocked
    # industry needs its own weight downstream (see allocate_to_csd), since
    # BS336110 and BS336300 have different geographic footprints and
    # collapsing them into one provincial number before allocating would
    # implicitly assume they're distributed identically across CSDs.
    return df[df['BS_Code'].isin(SCENARIO6_BS_CODES)][['Province', 'BS_Code', 'Direct_Jobs']]


# ============================================================
# STEP 2: Load CSD-level raw employment, tag with province
# ============================================================
def load_csd_employment(trail_csd_path):
    df = pd.read_csv(trail_csd_path, dtype={'CSDDGUID': str})

    missing = [c for c in SCENARIO6_NAICS_CODES if c not in df.columns]
    if missing:
        raise ValueError(
            f"NAICS columns {missing} not found in {trail_csd_path}. "
            "These should already exist since they're part of the 'Auto' tariff "
            "category -- check the file path or whether the column names got "
            "cast differently (e.g. as floats) when the CSV was written."
        )

    # Province tag: CSDDGUID -> last 7 chars = CSDUID -> first 2 digits = PRUID
    df['CSDUID'] = df['CSDDGUID'].str[-7:]
    df['PRUID'] = df['CSDUID'].str[:2].astype(int)
    df['Province'] = df['PRUID'].map(PROVINCE_CODE)

    # Keep individual NAICS columns (not pre-summed) -- each BS code needs
    # its own subset summed separately in allocate_to_csd.
    return df[['CSDDGUID', 'Province'] + SCENARIO6_NAICS_CODES]


# ============================================================
# STEP 3: Allocate provincial job loss down to CSD, PER BS CODE, then sum
# ============================================================
def allocate_to_csd(csd_employment_df, provincial_direct_jobs_df):
    result = csd_employment_df[['CSDDGUID', 'Province']].copy()
    result['S6_Direct_Jobs'] = 0.0

    # Translate the extraction's province labels (MRIO workbook) to the
    # notebook's own province labels (AB->AL, YT->YK, NT->NWT)
    jobs_df = provincial_direct_jobs_df.copy()
    jobs_df['Province'] = jobs_df['Province'].map(MRIO_TO_NOTEBOOK_PROVINCE)

    for bs_code in SCENARIO6_BS_CODES:
        naics_cols = BS_TO_NAICS[bs_code]

        # This BS code's own employment footprint -- NOT blended with the
        # other shocked BS code's NAICS columns.
        csd_bs_employment = csd_employment_df[naics_cols].sum(axis=1)
        prov_bs_totals = csd_bs_employment.groupby(csd_employment_df['Province']).sum().to_dict()

        weight = csd_employment_df['Province'].map(
            lambda p, totals=prov_bs_totals: totals.get(p, 0)
        )
        weight = csd_bs_employment / weight.replace(0, pd.NA)
        weight = weight.fillna(0.0)

        # This BS code's own provincial job-loss number
        prov_loss_for_bs = jobs_df[jobs_df['BS_Code'] == bs_code].set_index('Province')['Direct_Jobs'].to_dict()
        provincial_loss = csd_employment_df['Province'].map(prov_loss_for_bs).fillna(0.0)

        contribution = weight * provincial_loss
        result[f'S6_Direct_Jobs_{bs_code}'] = contribution
        result['S6_Direct_Jobs'] += contribution

        # Sanity check: weights should sum to ~1 within each province for
        # THIS bs code specifically (zero is expected for provinces with
        # no employment in this industry).
        weight_sums = weight.groupby(csd_employment_df['Province']).sum()
        off = weight_sums[((weight_sums - 1).abs() > 1e-6) & (weight_sums != 0)]
        if len(off) > 0:
            print(f"⚠️  WARNING: {bs_code} weights don't sum to 1 in provinces: {off.to_dict()}")

    return result


# ============================================================
# STEP 4: Merge onto CSD geometry, save GeoJSON + CSV
# ============================================================
def save_outputs(result_df, csd_shapefile_path):
    csd = gpd.read_file(csd_shapefile_path)
    csd['CSDDGUID'] = csd['DGUID']
    csd = csd[['CSDDGUID', 'geometry']].copy()

    merged = csd.merge(result_df, on='CSDDGUID', how='left')
    merged = merged.to_crs('EPSG:4326')

    OUTPUT_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    merged.to_file(OUTPUT_GEOJSON, driver='GeoJSON')
    merged.drop(columns='geometry').to_csv(OUTPUT_CSV, index=False)

    print(f"✅ Saved {OUTPUT_GEOJSON}")
    print(f"✅ Saved {OUTPUT_CSV}")
    print(f"   Total CSDs: {len(merged)}")
    print(f"   Total estimated S6 Direct job loss (should ≈ provincial sum): "
          f"{merged['S6_Direct_Jobs'].sum():,.1f}")


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("STEP 1: Extracting provincial Direct job loss for Scenario 6, per BS code...")
    provincial_direct_jobs_df = extract_scenario6_provincial_direct_jobs(MRIO_WORKBOOK)

    print("STEP 2: Loading CSD-level raw auto employment (individual NAICS columns)...")
    csd_employment = load_csd_employment(TRAIL_CSD_CSV)
    print(f"   Loaded {len(csd_employment)} CSDs\n")

    print("STEP 3: Allocating provincial job loss to CSDs, per BS code, then summing...")
    result = allocate_to_csd(csd_employment, provincial_direct_jobs_df)
    print(result.sort_values('S6_Direct_Jobs', ascending=False).head(10))
    print()

    print("STEP 4: Saving outputs...")
    save_outputs(result, CSD_SHAPEFILE)