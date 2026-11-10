"""
Build trail_ada_full.csv — raw, UNWEIGHTED employment by NAICS code, per ADA,
for the FULL economy (not just tariff-relevant NAICS).

This is a leaner version of the notebook's Step 5 (cell 17) + Step 6 (cells
19-21), but using ADA as the geographic unit instead of CSD.

- Skips HS-code / tariff-category / export-ratio-weighting entirely.
- Keeps EVERY NAICS code, no filtering.
- Aggregates DA-level employment to ADA via spatial join.

Output: trail_ada_full.csv (ADADGUID + one column per NAICS code, wide format)

WARNING: wide table (~900 NAICS columns) — run as a separate output.
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
import time

# ============================================================
# PATHS — verify these exist on your system
# ============================================================
SCRIPT_DIR = Path(__file__).parent

ESTAB_COUNTS = SCRIPT_DIR / '../input-data/large_size_data/Dec2022_Estabcounts_byDA.csv'
DA_SHAPEFILE = SCRIPT_DIR / '../input-data/large_size_data/lda_000b21a_e.shp'
ADA_SHAPEFILE = SCRIPT_DIR / '../input-data/large_size_data/lada000b21a_e.shp'  # <-- ADA shapefile D:\coding\SoC\tariffs\tariffs\analysis\input-data\large_size_data
OUTPUT_CSV = SCRIPT_DIR / '../intermediate/trail_ada_full.csv'

CHUNK_SIZE = 1_000_000

# Not strictly needed for ADA, but kept for consistency
PROVINCE_CODE = {
    10: 'NL', 11: 'PEI', 12: 'NS', 13: 'NB', 24: 'QC', 35: 'ON',
    46: 'MB', 47: 'SK', 48: 'AL', 59: 'BC', 60: 'YK', 61: 'NWT', 62: 'NU'
}


def build_da_to_ada_relation():
    """
    Spatial join: DA representative points -> ADA polygons.
    Returns DataFrame with columns: DA, ADADGUID
    """
    print("Building DA -> ADA spatial relation...")
    
    # Load DA shapefile
    da = gpd.read_file(DA_SHAPEFILE)
    da['DA'] = da['DAUID']
    da['DADGUID'] = da['DGUID']
    da = da[['DA', 'DADGUID', 'geometry']].copy()
    
    # Load ADA shapefile
    ada = gpd.read_file(ADA_SHAPEFILE)
    # Use DGUID as ADA identifier; adjust column name if needed
    ada['ADADGUID'] = ada['DGUID']  # or 'ADAUID' depending on your file
    ada = ada[['ADADGUID', 'geometry']].copy()
    
    # Ensure both are in the same CRS (e.g., EPSG:3347)
    da = da.to_crs('EPSG:3347')
    ada = ada.to_crs('EPSG:3347')
    
    # Use representative points for DAs to avoid boundary issues
    da_pts = da[['DA', 'DADGUID', 'geometry']].copy()
    da_pts['geometry'] = da_pts.geometry.representative_point()
    
    # Spatial join: find which ADA contains each DA point
    da_relation = gpd.sjoin(
        da_pts, ada[['ADADGUID', 'geometry']], how='left', predicate='within'
    ).drop(columns=['index_right', 'geometry'])
    
    # Clean DA column to integer
    da_relation['DA'] = pd.to_numeric(da_relation['DA'], errors='coerce').astype('Int64')
    
    match_rate = da_relation['ADADGUID'].notna().mean()
    print(f"  DA->ADA match rate: {match_rate:.3%}")
    return da_relation[['DA', 'ADADGUID']]


def process_establishment_counts():
    """
    Same chunked processing as notebook cell 17, but WITHOUT tariff weighting
    and WITHOUT restricting NAICS codes.
    """
    # Read column names to exclude "Without employees"
    all_cols = pd.read_csv(ESTAB_COUNTS, encoding='ISO-8859-1', nrows=1).columns
    cols_to_keep = [c for c in all_cols if c != 'Without employees']
    
    # Data types for size columns
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
        
        # Remove summary rows
        chunk = chunk[~chunk['NAICS'].isin(['Sub-total, classified', 'Unclassified', 'Total'])].copy()
        chunk['NAICS'] = chunk['NAICS'].astype(str).str[:6]
        
        # Estimate employees from size bins
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
        
        # Pivot DA x NAICS -> one column per NAICS
        per_naics = (
            chunk[['DisseminationAre', 'NAICS', 'Est_Employees']]
            .pivot_table(index='DisseminationAre', columns='NAICS', values='Est_Employees',
                         aggfunc='sum', fill_value=0)
            .reset_index()
        )
        per_naics_frames.append(per_naics)
        
        print(f"  Chunk {chunk_num} processed in {time.time() - t0:.2f} sec "
              f"({per_naics.shape[1] - 1} NAICS columns so far)")
    
    # Combine chunks and sum duplicates (should be none, but safe)
    per_naics_all = (
        pd.concat(per_naics_frames, ignore_index=True)
        .groupby('DisseminationAre', as_index=False).sum()
    )
    per_naics_all = per_naics_all.rename(columns={'DisseminationAre': 'DA'})
    
    print(f"\n✅ All chunks processed in {time.time() - total_start:.2f} sec")
    print(f"   Total NAICS columns: {per_naics_all.shape[1] - 1}")
    return per_naics_all


def aggregate_to_ada(per_naics_all, da_relation):
    """
    DA -> ADA aggregation: sum NAICS employment for all DAs in each ADA.
    """
    # Merge DA employment with ADA assignment
    per_naics_all['DA'] = pd.to_numeric(per_naics_all['DA'], errors='coerce').astype('Int64')
    merged = per_naics_all.merge(da_relation, on='DA', how='left')
    
    # Columns except DA
    naics_cols = [c for c in per_naics_all.columns if c != 'DA']
    for col in naics_cols:
        merged[col] = merged[col].fillna(0)
    
    # Aggregate by ADADGUID
    ada_full = merged.groupby('ADADGUID', as_index=False)[naics_cols].sum()
    return ada_full


if __name__ == '__main__':
    # Step 1: Build DA->ADA relation
    da_relation = build_da_to_ada_relation()
    
    # Step 2: Build DA-level NAICS employment (wide)
    per_naics_all = process_establishment_counts()
    
    # Step 3: Aggregate DA -> ADA
    print("\nAggregating DA -> ADA...")
    ada_full = aggregate_to_ada(per_naics_all, da_relation)
    
    # Step 4: Save
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    ada_full.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n✅ Saved {OUTPUT_CSV}")
    print(f"   {len(ada_full)} ADAs x {ada_full.shape[1] - 1} NAICS columns")