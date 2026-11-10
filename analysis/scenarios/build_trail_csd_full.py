"""
Build trail_csd_full.csv — raw, UNWEIGHTED employment by NAICS code, per CSD,
for the FULL economy (not just tariff-relevant NAICS).

This is a leaner version of the notebook's Step 5 (cell 17) + Step 6 (cells
19-21): it skips the entire HS-code / tariff-category / export-ratio-weighting
apparatus (concordance, weight_naics, category masks) since none of that is
needed here -- we want RAW industry employment, unweighted, for every NAICS
code, so it can be used as an allocation weight denominator later.

The one filter this REMOVES relative to the original notebook: cell 17's
`is_total = s.isin(total_naics)` line, which restricted the per-NAICS pivot
to only tariff-relevant NAICS codes. Here, every NAICS code in the raw file
gets its own column.

Output: trail_csd_full.csv (CSDDGUID + one column per NAICS code, wide format)

WARNING: this produces a much wider table (~900 NAICS columns vs ~38) and
will take longer to run per chunk than the original tariff-filtered pipeline.
Run this as a SEPARATE output, don't overwrite trail_csd.csv -- your existing
tariff-exposure map depends on that file as-is.
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
import time

# ============================================================
# PATHS -- adjust if these don't match your actual folder structure
# (verify with e.g. print(ESTAB_COUNTS.resolve()) if anything fails to load)
# ============================================================
SCRIPT_DIR = Path(__file__).parent

ESTAB_COUNTS = SCRIPT_DIR / '../input-data/large_size_data/Dec2022_Estabcounts_byDA.csv'
DA_SHAPEFILE = SCRIPT_DIR / '../input-data/large_size_data/lda_000b21a_e.shp'
CSD_SHAPEFILE = SCRIPT_DIR / '../../data/census/lcsd000b21a_e/lcsd000b21a_e.shp'
OUTPUT_CSV = SCRIPT_DIR / '../intermediate/trail_csd_full.csv'

CHUNK_SIZE = 1_000_000

PROVINCE_CODE = {
    10: 'NL', 11: 'PEI', 12: 'NS', 13: 'NB', 24: 'QC', 35: 'ON',
    46: 'MB', 47: 'SK', 48: 'AL', 59: 'BC', 60: 'YK', 61: 'NWT', 62: 'NU'
}


def build_da_to_csd_relation():
    """Same spatial-join approach as the notebook's cells 19-20."""
    print("Building DA -> CSD spatial relation...")
    da = gpd.read_file(DA_SHAPEFILE)
    da['DA'] = da['DAUID']
    da['DADGUID'] = da['DGUID']
    da = da[['DA', 'DADGUID', 'geometry']].copy()

    csd = gpd.read_file(CSD_SHAPEFILE)
    csdc = csd.copy()
    csdc['CSDDGUID'] = csdc['DGUID']
    csdc = csdc[['CSDDGUID', 'geometry']].copy()

    da = da.to_crs('EPSG:3347')
    csdc = csdc.to_crs('EPSG:3347')

    da_pts = da[['DA', 'DADGUID', 'geometry']].copy()
    da_pts['geometry'] = da_pts.geometry.representative_point()

    da_relation = gpd.sjoin(
        da_pts, csdc[['CSDDGUID', 'geometry']], how='left', predicate='within'
    ).drop(columns=['index_right', 'geometry'])

    da_relation['DA'] = pd.to_numeric(da_relation['DA'], errors='coerce').astype('Int64')

    match_rate = da_relation['CSDDGUID'].notna().mean()
    print(f"  DA->CSD match rate: {match_rate:.3%}")
    return da_relation[['DA', 'CSDDGUID']]


def process_establishment_counts():
    """Same chunked processing as notebook cell 17, but WITHOUT the tariff
    category weighting and WITHOUT restricting the per-NAICS pivot to
    tariff-relevant codes only."""
    all_cols = pd.read_csv(ESTAB_COUNTS, encoding='ISO-8859-1', nrows=1).columns
    cols_to_keep = [c for c in all_cols if c != 'Without employees']

    dtype_hint = {
        '1-4': 'Int64', '5-9': 'Int64', '10-19': 'Int64', '20-49': 'Int64',
        '50-99': 'Int64', '100-199': 'Int64', '200-499': 'Int64', '500 +': 'Int64',
        'Total, with employees': 'Int64',
    }

    per_naics_frames = []
    total_start = time.time()
    chunk_num = 0

    for chunk in pd.read_csv(
        ESTAB_COUNTS, encoding='ISO-8859-1', chunksize=CHUNK_SIZE,
        usecols=cols_to_keep, dtype=dtype_hint,
    ):
        t0 = time.time()
        chunk_num += 1

        chunk = chunk[~chunk['NAICS'].isin(['Sub-total, classified', 'Unclassified', 'Total'])].copy()
        chunk['NAICS'] = chunk['NAICS'].astype(str).str[:6]

        chunk['Est_Employees'] = (
            chunk['1-4'].fillna(0) * 3 +
            chunk['5-9'].fillna(0) * 7 +
            chunk['10-19'].fillna(0) * 15 +
            chunk['20-49'].fillna(0) * 35 +
            chunk['50-99'].fillna(0) * 75 +
            chunk['100-199'].fillna(0) * 150 +
            chunk['200-499'].fillna(0) * 350 +
            chunk['500 +'].fillna(0) * 550
        )

        # NO category masks, NO tariff weighting, NO is_total filter --
        # every NAICS code gets pivoted into its own column.
        per_naics = (
            chunk[['DisseminationAre', 'NAICS', 'Est_Employees']]
            .pivot_table(index='DisseminationAre', columns='NAICS', values='Est_Employees',
                         aggfunc='sum', fill_value=0)
            .reset_index()
        )
        per_naics_frames.append(per_naics)

        print(f"  Chunk {chunk_num} processed in {time.time() - t0:.2f} sec "
              f"({per_naics.shape[1] - 1} NAICS columns so far)")

    per_naics_all = (
        pd.concat(per_naics_frames, ignore_index=True)
        .groupby('DisseminationAre', as_index=False).sum()
    )
    per_naics_all = per_naics_all.rename(columns={'DisseminationAre': 'DA'})

    print(f"\n✅ All chunks processed in {time.time() - total_start:.2f} sec")
    print(f"   Total NAICS columns: {per_naics_all.shape[1] - 1}")
    return per_naics_all


def aggregate_to_csd(per_naics_all, da_relation):
    """DA -> CSD aggregation, same method as notebook cell 21, but for the
    full NAICS column set instead of just tariff-relevant ones."""
    per_naics_all['DA'] = pd.to_numeric(per_naics_all['DA'], errors='coerce').astype('Int64')

    merged = per_naics_all.merge(da_relation, on='DA', how='left')
    naics_cols = [c for c in per_naics_all.columns if c != 'DA']

    for col in naics_cols:
        merged[col] = merged[col].fillna(0)

    csd_full = merged.groupby('CSDDGUID', as_index=False)[naics_cols].sum()
    return csd_full


if __name__ == '__main__':
    da_relation = build_da_to_csd_relation()
    per_naics_all = process_establishment_counts()

    print("\nAggregating DA -> CSD...")
    csd_full = aggregate_to_csd(per_naics_all, da_relation)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    csd_full.to_csv(OUTPUT_CSV, index=False)

    print(f"\n✅ Saved {OUTPUT_CSV}")
    print(f"   {len(csd_full)} CSDs x {csd_full.shape[1] - 1} NAICS columns")
