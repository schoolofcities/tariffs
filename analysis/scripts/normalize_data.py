import pandas as pd
import numpy as np
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = ANALYSIS_DIR.parent

# Load data
trips = pd.read_csv(ANALYSIS_DIR / 'raw' / 'ca_us_stops_geohash_trips_daily_v4.csv')
norm = pd.read_csv(ANALYSIS_DIR / 'raw' / 'daily_can_total_papa.csv')

# Filter out Canadian metros
can_provs = ['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL', 'YT', 'NT', 'NU']
is_can = trips['METRO'].apply(lambda x: any(f", {p}" in str(x) for p in can_provs))
us_trips = trips[~is_can].copy()

# Group by METRO and DATE and sum UNIQUESTOPS
us_trips['UNIQUESTOPS'] = pd.to_numeric(us_trips['UNIQUESTOPS'], errors='coerce').fillna(0)
agg_trips = us_trips.groupby(['METRO', 'DATE'])['UNIQUESTOPS'].sum().reset_index()

# Merge with norm data
norm['SNAPSHOT_EVENT_DATE'] = norm['SNAPSHOT_EVENT_DATE'].astype(str)
agg_trips['DATE'] = agg_trips['DATE'].astype(str)

merged = pd.merge(agg_trips, norm[['SNAPSHOT_EVENT_DATE', 'UNIQUE_CANADIAN_DEVICES']], 
                  left_on='DATE', right_on='SNAPSHOT_EVENT_DATE', how='inner')

# Normalize
merged['normalized'] = merged['UNIQUESTOPS'] / merged['UNIQUE_CANADIAN_DEVICES']

# We only need the date in the dateNum format, since parseDate expects YYYYMMDD string from number
# Let's filter date range in python as well? The frontend:
# const startDate = new Date("2024-03-13");
# const endDate = new Date("2026-03-13");

# The frontend outputs: metro, dateNum, stops, normalized
# We want to remove stops and just output normalized
final_df = merged[['METRO', 'DATE', 'normalized']]
output_path = PROJECT_ROOT / 'static' / 'canada-us-visits' / 'us_normalized_trips_daily_v4.csv'
output_path.parent.mkdir(parents=True, exist_ok=True)
final_df.to_csv(output_path, index=False)