"""
ADA version: Combine all 5 (1, 3, 4, 5, 6) scenarios × 3 effects into ONE GeoJSON for ADAs.

Same logic as CSD version, but using:
    - ADA shapefile: data/census/ada000a21a_e/ada000a21a_e.shp
    - ADA employment: trail_ada_full.csv
    - GeoID column: ADADGUID
    - Output prefix: all_scenarios_ada

All values negative = job losses. Field names match S{n}_{EFFECT}_Jobs.
"""

import pandas as pd
import geopandas as gpd
import openpyxl
from pathlib import Path

# ============================================================
# PATHS -- adapt for ADA
# ============================================================
SCRIPT_DIR = Path(__file__).parent

MRIO_WORKBOOK = SCRIPT_DIR / '../raw/scenario summary - clsd MRIO - as of August 27 2026 - 2022 model.xlsx'
CONCORDANCE_WORKBOOK = SCRIPT_DIR / '../intermediate/NAICS 2022v1 to IOIC 2022 concordance.xlsx'
TRAIL_ADA_FULL_CSV = SCRIPT_DIR / '../intermediate/trail_ada_full.csv'      # <-- ADA employment
ADA_SHAPEFILE = SCRIPT_DIR / '../input-data/large_size_data/lada000b21a_e.shp'  # <-- ADA shapefile
OUTPUT_DIR = SCRIPT_DIR / '../outputs'

SCENARIOS = [1, 3, 4, 5, 6]
EFFECTS = ['DIR', 'INDIR', 'INDCD']
EFFECT_COLUMN_INDEX = {'DIR': 4, 'INDIR': 5, 'INDCD': 6}
OUTPUT_NAME = 'all_scenarios_ada'   # <-- changed prefix

SCENARIO_LABELS = {
    1: 'Household Consumption', 3: 'Agri-food & Seafood',
    4: 'Steel & Aluminum', 5: 'Softwood Lumber', 6: 'Autos & Parts',
}

MRIO_TO_NOTEBOOK_PROVINCE = {
    'NL': 'NL', 'PEI': 'PEI', 'NS': 'NS', 'NB': 'NB', 'QC': 'QC',
    'ON': 'ON', 'MB': 'MB', 'SK': 'SK', 'AB': 'AL', 'BC': 'BC',
    'YT': 'YK', 'NT': 'NWT', 'NU': 'NU'
}

# ADA province codes (same as CSD, first two digits of ADAUID)
PROVINCE_CODE = {
    10: 'NL', 11: 'PEI', 12: 'NS', 13: 'NB', 24: 'QC', 35: 'ON',
    46: 'MB', 47: 'SK', 48: 'AL', 59: 'BC', 60: 'YK', 61: 'NWT', 62: 'NU'
}


def load_bs_to_naics(concordance_path):
    wb = openpyxl.load_workbook(concordance_path)
    ws = wb['English']
    rows = list(ws.iter_rows(min_row=3, values_only=True))
    lookup = {}
    for r in rows:
        naics, naics_title, bs_code, bs_title = r[0], r[1], r[2], r[3]
        if bs_code is None or naics is None:
            continue
        lookup.setdefault(bs_code, []).append(str(naics))
    return lookup


BS_TO_NAICS = load_bs_to_naics(CONCORDANCE_WORKBOOK)


# ============================================================
# Shared extraction (identical to CSD version)
# ============================================================
def parse_shared_sheets(wb):
    delta_x_rows = list(wb['Delta X - D Level'].iter_rows(min_row=4, values_only=True))
    delta_x_pb = []
    current_province = None
    for r in delta_x_rows:
        if r[0] is not None:
            current_province = r[0]
        delta_x_pb.append((current_province, r[3]))

    mult_rows = list(wb['Jobs Multipliers D'].iter_rows(min_row=2, values_only=True))
    multiplier_lookup = {}
    current_province = None
    for r in mult_rows:
        if r[1] is not None:
            current_province = r[1]
        multiplier_lookup[(current_province, r[2])] = r[4]

    return delta_x_pb, multiplier_lookup


def split_into_blocks(province_list, payload_list):
    blocks = []
    for i, prov in enumerate(province_list):
        if prov in (None, 'Canada', 'CAN'):
            continue
        item = payload_list[i]
        if blocks and blocks[-1][0] == prov:
            blocks[-1][1].append(item)
        else:
            blocks.append((prov, [item]))
    return blocks


def extract_provincial_effect_jobs(wb, delta_x_pb, multiplier_lookup, scenario_num, effect):
    dir_sheet_name = f'DIR_INDIR_INDCD_DFD{scenario_num}'
    effect_col = EFFECT_COLUMN_INDEX[effect]

    effect_rows = list(wb[dir_sheet_name].iter_rows(min_row=2, values_only=True))
    effect_province = []
    effect_values = []
    current_province = None
    for r in effect_rows:
        if r[1] is not None:
            current_province = r[1]
        effect_province.append(current_province)
        effect_values.append(r[effect_col])

    delta_x_blocks = split_into_blocks([p for p, _ in delta_x_pb], [bs for _, bs in delta_x_pb])
    effect_blocks = split_into_blocks(effect_province, effect_values)

    delta_x_by_prov = dict(delta_x_blocks)
    effect_by_prov = dict(effect_blocks)

    mismatches = {
        prov: (len(delta_x_by_prov[prov]), len(effect_by_prov.get(prov, [])))
        for prov in delta_x_by_prov
        if len(delta_x_by_prov[prov]) != len(effect_by_prov.get(prov, []))
    }
    if mismatches:
        print(f"⚠️  [SC{scenario_num} {effect}] Per-province block size mismatch: {mismatches}")
        print("    Truncating to shorter length -- verify if unexpected.")

    records = []
    for prov, bs_codes in delta_x_blocks:
        effect_vals_for_prov = effect_by_prov.get(prov, [])
        n = min(len(bs_codes), len(effect_vals_for_prov))
        for bs_code, dollars in zip(bs_codes[:n], effect_vals_for_prov[:n]):
            mult = multiplier_lookup.get((prov, bs_code))
            if mult is None:
                continue
            jobs = (dollars or 0) / 1_000_000 * mult
            records.append({'Province': prov, 'BS_Code': bs_code, 'Jobs': jobs})

    return pd.DataFrame(records)


def get_relevant_bs_codes(df, threshold=1e-6):
    nonzero = df[df['Jobs'].abs() > threshold]
    return sorted(nonzero['BS_Code'].unique())


# ============================================================
# ADA employment loader (instead of CSD)
# ============================================================
def load_ada_employment_full(trail_ada_path):
    """Load ADA employment CSV. Expects columns: ADADGUID, then NAICS columns."""
    df = pd.read_csv(trail_ada_path, dtype={'ADADGUID': str})
    # Derive province from ADAUID (first two digits)
    #df['ADAUID'] = df['ADADGUID'].str[-7:]   # adjust if format differs
    df['PRUID'] = df['ADADGUID'].str[9:11].astype(int)
    df['Province'] = df['PRUID'].map(PROVINCE_CODE) 
    return df


def select_naics_columns(full_df, bs_codes):
    needed_naics = sorted(set(n for bs in bs_codes for n in BS_TO_NAICS.get(bs, [])))
    available_naics = [c for c in needed_naics if c in full_df.columns]
    return full_df[['ADADGUID', 'Province'] + available_naics]


# ============================================================
# Allocation (uses GEOID column = ADADGUID)
# ============================================================
def allocate_to_ada(ada_employment_df, provincial_effect_jobs_df, bs_codes, output_col):
    result = ada_employment_df[['ADADGUID', 'Province']].copy()
    result[output_col] = 0.0

    jobs_df = provincial_effect_jobs_df.copy()
    jobs_df['Province'] = jobs_df['Province'].map(MRIO_TO_NOTEBOOK_PROVINCE)

    skipped_no_concordance = []
    for bs_code in bs_codes:
        naics_cols = BS_TO_NAICS.get(bs_code)
        if not naics_cols:
            skipped_no_concordance.append(bs_code)
            continue

        available_cols = [c for c in naics_cols if c in ada_employment_df.columns]
        if not available_cols:
            continue

        ada_bs_employment = ada_employment_df[available_cols].sum(axis=1)
        prov_bs_totals = ada_bs_employment.groupby(ada_employment_df['Province']).sum().to_dict()

        weight = ada_employment_df['Province'].map(
            lambda p, totals=prov_bs_totals: totals.get(p, 0)
        )
        weight = ada_bs_employment / weight.replace(0, pd.NA)
        weight = weight.fillna(0.0)

        prov_loss_for_bs = jobs_df[jobs_df['BS_Code'] == bs_code].set_index('Province')['Jobs'].to_dict()
        provincial_loss = ada_employment_df['Province'].map(prov_loss_for_bs).fillna(0.0)

        result[output_col] += weight * provincial_loss

    return result[['ADADGUID', output_col]], skipped_no_concordance


# ============================================================
# Geometry: ADA shapefile
# ============================================================
def load_clean_ada_geometry(ada_shapefile_path):
    ada = gpd.read_file(ada_shapefile_path)
    ada['ADADGUID'] = ada['DGUID']   # or 'ADAUID'? adjust as needed
    ada = ada[['ADADGUID', 'geometry']].copy()

    ada = ada[ada.geometry.notna() & ~ada.geometry.is_empty].copy()
    invalid = ~ada.geometry.is_valid
    if invalid.any():
        print(f"   Repairing {invalid.sum()} invalid ADA geometries via buffer(0)...")
        ada.loc[invalid, 'geometry'] = ada.loc[invalid, 'geometry'].buffer(0)
        ada = ada[~ada.geometry.is_empty].copy()
    return ada


def save_combined(clean_ada, all_columns_df, output_name):
    merged = clean_ada.merge(all_columns_df, on='ADADGUID', how='left')
    merged = gpd.GeoDataFrame(merged, geometry='geometry', crs=clean_ada.crs)
    merged = merged.to_crs('EPSG:4326')

    geojson_path = OUTPUT_DIR / 'geojson' / f'{output_name}.geojson'
    csv_path = OUTPUT_DIR / 'csv' / f'{output_name}.csv'
    centroid_path = OUTPUT_DIR / 'geojson' / f'{output_name}_centroids.geojson'
    geojson_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    merged.to_file(geojson_path, driver='GeoJSON')
    merged.drop(columns='geometry').to_csv(csv_path, index=False)

    centroids = merged.to_crs('EPSG:3347').copy()
    centroids['geometry'] = centroids.geometry.representative_point()
    centroids = centroids.to_crs('EPSG:4326')
    centroids.to_file(centroid_path, driver='GeoJSON')

    print(f"\n✅ Saved {geojson_path}")
    print(f"✅ Saved {csv_path}")
    print(f"✅ Saved {centroid_path}")


# ============================================================
# MAIN: Generate ADA outputs
# ============================================================
if __name__ == '__main__':
    print("Loading shared inputs (workbook, ADA employment, ADA geometry)...")
    wb = openpyxl.load_workbook(MRIO_WORKBOOK, data_only=True)
    delta_x_pb, multiplier_lookup = parse_shared_sheets(wb)
    full_employment = load_ada_employment_full(TRAIL_ADA_FULL_CSV)
    clean_ada = load_clean_ada_geometry(ADA_SHAPEFILE)

    combined = full_employment[['ADADGUID']].drop_duplicates().reset_index(drop=True)

    all_skipped = set()
    summary = []

    for n in SCENARIOS:
        label = SCENARIO_LABELS.get(n, '')
        print(f"\n{'='*60}\n=== Scenario {n}: {label} ===\n{'='*60}")

        for effect in EFFECTS:
            output_col = f'S{n}_{effect}_Jobs'
            print(f"  [{output_col}] extracting + allocating...")

            provincial_jobs = extract_provincial_effect_jobs(
                wb, delta_x_pb, multiplier_lookup, n, effect
            )
            bs_codes = get_relevant_bs_codes(provincial_jobs)
            ada_employment = select_naics_columns(full_employment, bs_codes)

            col_df, skipped = allocate_to_ada(
                ada_employment, provincial_jobs, bs_codes, output_col
            )
            all_skipped.update(skipped)

            allocated = col_df[output_col].sum()
            extracted = provincial_jobs['Jobs'].sum()
            print(f"      {len(bs_codes)} BS codes | "
                  f"allocated {allocated:,.0f} vs extracted {extracted:,.0f}")

            combined = combined.merge(col_df, on='ADADGUID', how='left')
            summary.append((output_col, extracted, allocated, len(bs_codes)))

    combined = combined.fillna(0.0)

    print(f"\n{'='*60}\nSaving combined ADA output ({len(SCENARIOS)*len(EFFECTS)} columns)...\n{'='*60}")
    save_combined(clean_ada, combined, OUTPUT_NAME)

    print(f"\n{'='*60}\nSUMMARY — ADA 18 columns\n{'='*60}")
    print(f"{'Column':<18} {'Extracted':>14} {'Allocated':>14} {'BS codes':>9}")
    for col, extracted, allocated, ncodes in summary:
        print(f"{col:<18} {extracted:>14,.0f} {allocated:>14,.0f} {ncodes:>9}")
    if all_skipped:
        print(f"\n{len(all_skipped)} BS codes had no concordance across all "
              f"scenarios/effects (sample: {sorted(all_skipped)[:8]}).")
    print("\nNote: DIR/INDIR/INDCD magnitudes differ across scenarios; "
          "tune map breaks per scenario and effect-combination.")