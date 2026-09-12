import pandas as pd
import geopandas as gpd
import openpyxl
from pathlib import Path

# ============================================================
# PATHS -- must match scenario_allocation.py
# ============================================================
SCRIPT_DIR = Path(__file__).parent

MRIO_WORKBOOK = SCRIPT_DIR / '../raw/scenario summary - clsd MRIO - as of June 21 2026 - 2022 model.xlsx'
CONCORDANCE_WORKBOOK = SCRIPT_DIR / '../intermediate/NAICS 2022v1 to IOIC 2022 concordance.xlsx'
TRAIL_CSD_FULL_CSV = SCRIPT_DIR / '../intermediate/trail_csd_full.csv'
CSD_SHAPEFILE = SCRIPT_DIR / '../../data/census/lcsd000b21a_e/lcsd000b21a_e.shp'
OUTPUT_DIR = SCRIPT_DIR / '../outputs'

SCENARIOS = [1, 2, 3, 4, 5, 6]
EFFECTS = ['DIR', 'INDIR', 'INDCD']          # 3 effects, all treated identically
EFFECT_COLUMN_INDEX = {'DIR': 4, 'INDIR': 5, 'INDCD': 6}
OUTPUT_NAME = 'all_scenarios_csd'

SCENARIO_LABELS = {
    1: 'Household Consumption', 2: 'Aggregate Exports', 3: 'Agri-food & Seafood',
    4: 'Steel & Aluminum', 5: 'Softwood Lumber', 6: 'Autos & Parts',
}

MRIO_TO_NOTEBOOK_PROVINCE = {
    'NL': 'NL', 'PEI': 'PEI', 'NS': 'NS', 'NB': 'NB', 'QC': 'QC',
    'ON': 'ON', 'MB': 'MB', 'SK': 'SK', 'AB': 'AL', 'BC': 'BC',
    'YT': 'YK', 'NT': 'NWT', 'NU': 'NU'
}

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
# STEP 1: Extract provincial job loss for one (scenario, effect)
# Delta X - D Level and Jobs Multipliers D are the SAME for every scenario,
# so they're parsed once and passed in. Only the DIR_INDIR_INDCD_SC{n} sheet
# and which column (4/5/6) change.
# ============================================================
def parse_shared_sheets(wb):
    """Delta X - D Level (province+BS per row) and Jobs Multipliers D lookup.
    Identical across all scenarios -- parse once."""
    delta_x_rows = list(wb['Delta X - D Level'].iter_rows(min_row=4, values_only=True))
    delta_x_pb = []
    current_province = None
    for r in delta_x_rows:
        if r[0] is not None:
            current_province = r[0]
        delta_x_pb.append((current_province, r[3]))

    mult_rows = list(wb['Jobs Multipliers D'].iter_rows(min_row=2, values_only=True))

    print(mult_rows)

    multiplier_lookup = {}
    current_province = None
    for r in mult_rows:
        #print(r)
        if r[1] is not None:
            current_province = r[1]
        multiplier_lookup[(current_province, r[2])] = r[4]

    return delta_x_pb, multiplier_lookup


if __name__ == '__main__':
    print("Loading shared inputs once (workbook, employment, geometry)...")
    wb = openpyxl.load_workbook(MRIO_WORKBOOK, data_only=True)
    delta_x_pb, multiplier_lookup = parse_shared_sheets(wb)