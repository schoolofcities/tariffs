# Scatterplot - input: QCEW, jobs %
# output: scatterplot w/ dominant industry

"""
canada_visits_vs_jobs.py
========================
Merges QCEW 2023 MSA-level industry employment data with
Canada-to-US visit YoY % change data, then plots an interactive
Plotly scatter where:
  - X axis  : Canada-US visit YoY % change (from the pasted list)
  - Y axis  : YoY % change in total jobs (placeholder — see NOTE below)
  - Color   : Dominant NAICS sector (highest number of jobs)
  - Hover   : Metro name, dominant industry, jobs, visit % change

NOTE ON YoY JOBS:
  The uploaded file contains only 2023 annual data (no prior year).
  To compute a true YoY jobs % change you need a matching 2022 file.
  This script shows TWO modes:
    1. If you supply a 2022 CSV with the same schema, it computes real YoY.
    2. Otherwise it falls back to plotting 2023 total jobs on the Y-axis
       (still useful for showing the employment scale alongside visit decline).
  Drop a 2022 file at the path in JOBS_2022_PATH to enable mode 1.

Usage:
  pip install pandas plotly
  python canada_visits_vs_jobs.py
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── CONFIGURATION ────────────────────────────────────────────────────────────

from pathlib import Path
JOBS_2023_PATH = Path(__file__).parent / "qcew_msa_industry_2023_a.csv"
JOBS_2022_PATH = None  # e.g. "qcew_msa_industry_2022_a.csv" — set to enable YoY

OUTPUT_HTML = "canada_visits_vs_jobs.html"

# ── CANADA-US VISIT YoY % CHANGE (pasted data) ───────────────────────────────

VISIT_CHANGES = {
    "Myrtle Beach, SC": -65.4,
    "Yuma, AZ": -62.3,
    "Panama City, FL": -60.3,
    "Brownsville, TX": -58.5,
    "Orlando, FL": -58.2,
    "Cape Coral, FL": -58.2,
    "Miami, FL": -58.1,
    "Naples, FL": -57.4,
    "San Francisco, CA": -56.9,
    "North Port, FL": -56.3,
    "Palm Bay, FL": -55.9,
    "Providence, RI": -55.6,
    "New York, NY": -55.5,
    "Las Vegas, NV": -55.5,
    "Flint, MI": -55.3,
    "Deltona, FL": -55.1,
    "Albany, NY": -54.9,
    "Port St. Lucie, FL": -54.6,
    "Barnstable Town, MA": -54.4,
    "Ann Arbor, MI": -53.9,
    "Anchorage, AK": -53.5,
    "Urban Honolulu, HI": -53.3,
    "Grand Rapids, MI": -53.2,
    "Tampa, FL": -53.2,
    "San Diego, CA": -53.0,
    "Atlantic City, NJ": -52.8,
    "Hilton Head Island, SC": -52.6,
    "McAllen, TX": -52.6,
    "Sebastian, FL": -52.5,
    "Santa Maria, CA": -52.3,
    "Los Angeles, CA": -52.0,
    "Boston, MA": -52.0,
    "Hagerstown, MD": -52.0,
    "Bridgeport, CT": -51.9,
    "Saginaw, MI": -51.8,
    "Houston, TX": -51.7,
    "Rochester, NY": -51.6,
    "Syracuse, NY": -51.2,
    "Milwaukee, WI": -51.2,
    "Lebanon, NH": -51.0,
    "Muskegon, MI": -51.0,
    "Colorado Springs, CO": -51.0,
    "Nashville, TN": -50.8,
    "Buffalo, NY": -50.7,
    "Trenton, NJ": -50.7,
    "Austin, TX": -50.7,
    "Punta Gorda, FL": -50.5,
    "Philadelphia, PA": -50.4,
    "Manchester, NH": -50.3,
    "Utica, NY": -50.2,
    "Lakeland, FL": -49.8,
    "Monroe, LA": -49.6,
    "New Haven, CT": -49.6,
    "Dallas, TX": -49.6,
    "Tucson, AZ": -49.4,
    "Poughkeepsie, NY": -49.3,
    "San Jose, CA": -49.2,
    "Portland, ME": -49.0,
    "Indianapolis, IN": -48.8,
    "Oxnard, CA": -48.7,
    "Chicago, IL": -48.6,
    "Jacksonville, FL": -48.6,
    "Lansing, MI": -48.6,
    "Charleston, SC": -48.5,
    "Sacramento, CA": -48.4,
    "Memphis, TN": -48.4,
    "Riverside, CA": -48.3,
    "Binghamton, NY": -48.2,
    "Boulder, CO": -48.2,
    "Hilo, HI": -48.1,
    "Salisbury, MD": -48.1,
    "Reno, NV": -48.1,
    "Burlington, VT": -48.0,
    "Kahului, HI": -47.9,
    "Modesto, CA": -47.7,
    "Laredo, TX": -47.7,
    "Seattle, WA": -47.6,
    "Phoenix, AZ": -46.9,
    "Fresno, CA": -46.8,
    "Crestview, FL": -46.8,
    "Allentown, PA": -46.8,
    "Toledo, OH": -46.5,
    "Ocala, FL": -46.4,
    "Norwich, CT": -46.4,
    "St. George, UT": -46.3,
    "Omaha, NE": -46.2,
    "Champaign, IL": -46.1,
    "Baton Rouge, LA": -46.1,
    "Durham, NC": -45.9,
    "Dayton, OH": -45.9,
    "Evansville, IN": -45.8,
    "Bremerton, WA": -45.8,
    "Provo, UT": -45.4,
    "Columbus, OH": -45.4,
    "Little Rock, AR": -45.3,
    "Atlanta, GA": -45.2,
    "Denver, CO": -45.2,
    "Fayetteville, AR": -45.0,
    "Rochester, MN": -45.0,
    "Worcester, MA": -45.0,
    "Kansas City, MO": -45.0,
    "Daphne, AL": -44.9,
    "Washington, DC": -44.9,
    "Lancaster, PA": -44.8,
    "Jackson, MI": -44.7,
    "Lexington, KY": -44.7,
    "Hartford, CT": -44.7,
    "Oklahoma City, OK": -44.6,
    "Kalamazoo, MI": -44.5,
    "Wilmington, NC": -44.4,
    "Pittsburgh, PA": -44.3,
    "Olympia, WA": -44.2,
    "Greensboro, NC": -44.2,
    "Duluth, MN": -44.2,
    "Lake Havasu City, AZ": -44.2,
    "Raleigh, NC": -44.0,
    "Louisville, KY": -43.9,
    "Bloomington, IN": -43.9,
    "Akron, OH": -43.7,
    "Wichita, KS": -43.7,
    "Eau Claire, WI": -43.6,
    "Minneapolis, MN": -43.4,
    "Spokane, WA": -43.4,
    "Madison, WI": -43.2,
    "Fargo, ND": -43.1,
    "Green Bay, WI": -43.1,
    "Vallejo, CA": -43.1,
    "Tulsa, OK": -42.8,
    "Boise City, ID": -42.7,
    "El Centro, CA": -42.7,
    "Greenville, SC": -42.6,
    "Scranton, PA": -42.6,
    "Lafayette, LA": -42.5,
    "Canton, OH": -42.3,
    "Fayetteville, NC": -42.3,
    "New Orleans, LA": -42.3,
    "Winston, NC": -42.1,
    "San Antonio, TX": -42.0,
    "San Luis Obispo, CA": -42.0,
    "Janesville, WI": -41.9,
    "Charlotte, NC": -41.9,
    "Fort Collins, CO": -41.8,
    "Reading, PA": -41.7,
    "Virginia Beach, VA": -41.6,
    "Kingston, NY": -41.6,
    "Bakersfield, CA": -41.6,
    "Springfield, MO": -41.5,
    "East Stroudsburg, PA": -41.4,
    "Harrisburg, PA": -41.4,
    "Detroit, MI": -41.4,
    "Sioux Falls, SD": -41.3,
    "Des Moines, IA": -41.3,
    "York, PA": -41.2,
    "Huntington, WV": -41.2,
    "Lafayette, IN": -41.2,
    "Chattanooga, TN": -41.2,
    "Roanoke, VA": -41.1,
    "Redding, CA": -41.1,
    "Knoxville, TN": -41.0,
    "Kingsport, TN": -40.9,
    "Savannah, GA": -40.9,
    "Warner Robins, GA": -40.7,
    "Asheville, NC": -40.7,
    "Visalia, CA": -40.5,
    "Stockton, CA": -40.5,
    "Columbia, SC": -40.4,
    "Gainesville, GA": -39.8,
    "Mobile, AL": -39.8,
    "Coeur d'Alene, ID": -39.7,
    "Erie, PA": -39.7,
    "Macon, GA": -39.4,
    "Salinas, CA": -39.2,
    "St. Louis, MO": -39.1,
    "Salt Lake City, UT": -38.9,
    "Kennewick, WA": -38.9,
    "Baltimore, MD": -38.9,
    "Waco, TX": -38.9,
    "Santa Cruz, CA": -38.8,
    "Cincinnati, OH": -38.4,
    "Elkhart, IN": -38.2,
    "Ogden, UT": -38.2,
    "El Paso, TX": -38.2,
    "Yakima, WA": -38.1,
    "Charleston, WV": -38.1,
    "Appleton, WI": -38.1,
    "Bowling Green, KY": -37.7,
    "Montgomery, AL": -37.6,
    "Tallahassee, FL": -37.6,
    "Amarillo, TX": -37.6,
    "Corpus Christi, TX": -37.6,
    "Florence, SC": -37.5,
    "Youngstown, OH": -37.4,
    "Fort Wayne, IN": -37.3,
    "Cedar Rapids, IA": -37.3,
    "Gulfport, MS": -37.2,
    "Clarksville, TN": -37.0,
    "Tuscaloosa, AL": -36.9,
    "Rockford, IL": -36.8,
    "Killeen, TX": -36.7,
    "Columbia, MO": -36.7,
    "College Station, TX": -35.9,
    "Bloomington, IL": -35.9,
    "Terre Haute, IN": -35.8,
    "State College, PA": -35.5,
    "Charlottesville, VA": -35.3,
    "Lake Charles, LA": -35.1,
    "Torrington, CT": -35.1,
    "South Bend, IN": -35.1,
    "Birmingham, AL": -34.9,
    "Oshkosh, WI": -34.8,
    "Shreveport, LA": -34.6,
    "St. Cloud, MN": -34.6,
    "Prescott Valley, AZ": -33.9,
    "Spartanburg, SC": -33.8,
    "Fort Smith, AR": -33.5,
    "Wausau, WI": -33.1,
    "Idaho Falls, ID": -33.0,
    "Augusta, GA": -32.9,
    "Lubbock, TX": -32.8,
    "Topeka, KS": -32.6,
    "Lynchburg, VA": -32.3,
    "Midland, TX": -32.3,
    "Peoria, IL": -32.2,
    "Davenport, IA": -32.1,
    "Odessa, TX": -31.7,
    "Richmond, VA": -31.7,
    "Joplin, MO": -31.5,
    "Johnson City, TN": -31.4,
    "Athens, GA": -31.4,
    "Blacksburg, VA": -31.3,
    "Auburn, AL": -31.0,
    "Springfield, MA": -31.0,
    "Hickory, NC": -30.7,
    "Bellingham, WA": -30.5,
    "Longview, TX": -30.2,
    "Pueblo, CO": -30.1,
    "Las Cruces, NM": -29.9,
    "Greeley, CO": -29.9,
    "Abilene, TX": -29.8,
    "Yuba City, CA": -29.7,
    "Greenville, NC": -29.5,
    "Jacksonville, NC": -29.3,
    "Waterloo, IA": -29.2,
    "Merced, CA": -28.5,
    "Racine, WI": -27.7,
    "Huntsville, AL": -27.2,
    "Dover, DE": -27.1,
    "Jackson, MS": -26.7,
    "Billings, MT": -26.4,
    "Santa Rosa, CA": -26.3,
    "Springfield, IL": -25.0,
    "Lincoln, NE": -24.4,
    "Hattiesburg, MS": -24.3,
    "Beaumont, TX": -24.3,
    "Jackson, TN": -23.9,
    "Houma, LA": -23.8,
    "Tupelo, MS": -20.0,
    "Chico, CA": -19.9,
    "Tyler, TX": -19.5,
    "Iowa City, IA": -18.3,
    "Burlington, NC": -17.2,
    "Columbus, GA": -14.0,
    "Pensacola, FL": -12.1,
    "Albuquerque, NM": -5.9,
    "Gainesville, FL": 31.0,
    "Cleveland, OH": 35.5,
}

# ── NAICS labels (short) ─────────────────────────────────────────────────────

NAICS_LABELS = {
    "11":    "Agriculture",
    "21":    "Mining/Oil & Gas",
    "22":    "Utilities",
    "23":    "Construction",
    "31-33": "Manufacturing",
    "42":    "Wholesale Trade",
    "44-45": "Retail Trade",
    "48-49": "Transportation/Warehousing",
    "51":    "Information",
    "52":    "Finance & Insurance",
    "53":    "Real Estate",
    "54":    "Professional Services",
    "55":    "Management",
    "56":    "Admin/Support",
    "61":    "Education",
    "62":    "Health Care",
    "71":    "Arts/Entertainment",
    "72":    "Accommodation/Food",
    "81":    "Other Services",
    "99":    "Unclassified",
}

# ── LOAD & PROCESS DATA ───────────────────────────────────────────────────────

df23 = pd.read_csv(JOBS_2023_PATH)

# Keep only 2-digit NAICS (no totals / sub-sectors if present)
valid_codes = list(NAICS_LABELS.keys())
df23 = df23[df23["industry_code"].isin(valid_codes)].copy()

# Dominant industry per metro = sector with most jobs in 2023
dominant = (
    df23.sort_values("jobs", ascending=False)
    .groupby("metro_name", as_index=False)
    .first()[["metro_name", "industry_code", "jobs"]]
    .rename(columns={"industry_code": "dominant_code", "jobs": "dominant_jobs"})
)

# Total jobs per metro
total_jobs = df23.groupby("metro_name")["jobs"].sum().reset_index()
total_jobs.rename(columns={"jobs": "total_jobs_2023"}, inplace=True)

# YoY jobs % change
if JOBS_2022_PATH:
    df22 = pd.read_csv(JOBS_2022_PATH)
    df22 = df22[df22["industry_code"].isin(valid_codes)]
    total_22 = df22.groupby("metro_name")["jobs"].sum().reset_index()
    total_22.rename(columns={"jobs": "total_jobs_2022"}, inplace=True)
    total_jobs = total_jobs.merge(total_22, on="metro_name", how="left")
    total_jobs["jobs_yoy_pct"] = (
        (total_jobs["total_jobs_2023"] - total_jobs["total_jobs_2022"])
        / total_jobs["total_jobs_2022"] * 100
    )
    y_col   = "jobs_yoy_pct"
    y_label = "YoY % Change in Total Jobs (2022→2023)"
else:
    y_col   = "total_jobs_2023"
    y_label = "Total Jobs 2023 (log scale)"

# Merge everything
summary = total_jobs.merge(dominant, on="metro_name")

# Add visit change
visit_df = pd.DataFrame(
    list(VISIT_CHANGES.items()), columns=["metro_name", "visit_yoy_pct"]
)
merged = summary.merge(visit_df, on="metro_name", how="inner")

# Human-readable dominant industry label
merged["dominant_industry"] = merged["dominant_code"].map(NAICS_LABELS)

# Axis definitions:
#   X = Canada-US visitor YoY % change
#   Y = Total jobs 2023 (swap to jobs_yoy_pct if you add a 2022 file)
x_col   = "visit_yoy_pct"
x_label = "Canada to US Visits YoY % Change"
y_col   = "total_jobs_2023"
y_label = "Total Jobs (2023)"

print(f"Matched {len(merged)} metros out of {len(visit_df)} in visit list")
print(merged[["metro_name", "dominant_industry", y_col, x_col]].head(10).to_string(index=False))

# ── PER-INDUSTRY CORRELATION ANALYSIS ─────────────────────────────────────────

print("\n" + "="*80)
print("CORRELATION ANALYSIS BY INDUSTRY")
print("="*80)
print("(Positive = jobs rise with visit decline; Negative = jobs fall with visit decline)\n")

# Merge 2023 jobs by industry+metro with visit data
df23_with_visits = df23.merge(visit_df, on="metro_name", how="inner")

# Calculate correlation for each NAICS code
corr_results = []
for naics_code in sorted(df23_with_visits["industry_code"].unique()):
    industry_data = df23_with_visits[df23_with_visits["industry_code"] == naics_code]
    
    if len(industry_data) >= 3:  # need min 3 points for meaningful correlation
        corr = industry_data["visit_yoy_pct"].corr(industry_data["jobs"])
        count = len(industry_data)
        avg_jobs = industry_data["jobs"].mean()
        label = NAICS_LABELS.get(naics_code, "Unknown")
        
        corr_results.append({
            "NAICS": naics_code,
            "Industry": label,
            "Correlation": corr,
            "N_Metros": count,
            "Avg_Jobs": avg_jobs,
        })

corr_df = pd.DataFrame(corr_results).sort_values("Correlation", ascending=False)

# Display table
print(corr_df[["NAICS", "Industry", "Correlation", "N_Metros"]].to_string(index=False))

print("\n" + "-"*80)
print("INTERPRETATION:")
print("  • Positive correlation: More job loss in metros with bigger visit declines")
print("  • Negative correlation: More job gain despite visit declines (resilient)")
print("  • ~0: No clear relationship between visit decline and job changes")
print("-"*80)

# ── PLOT ─────────────────────────────────────────────────────────────────────

# Consistent color per NAICS sector
all_industries = sorted(merged["dominant_industry"].unique())

fig = px.scatter(
    merged,
    x=x_col,
    y=y_col,
    color="dominant_industry",
    hover_name="metro_name",
    hover_data={
        x_col: ":.1f",
        y_col: ":,",
        "dominant_industry": True,
        "dominant_jobs": ":,",
    },
    labels={
        x_col: x_label,
        y_col: y_label,
        "dominant_industry": "Dominant Industry",
        "dominant_jobs": "Dominant-sector Jobs",
    },
    title="Canadian to U.S. visit decline vs. total jobs by metro's most dominant industry",
    #log_y=True,   # log scale so large metros don't dwarf small ones
    size_max=14,
    template="plotly_dark",
    color_discrete_sequence=px.colors.qualitative.Bold,
    category_orders={"dominant_industry": all_industries},
)

# Reference line at x=0
fig.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.3)", line_width=1)

fig.update_traces(
    marker=dict(size=9, opacity=0.85, line=dict(width=0.5, color="rgba(255,255,255,0.4)")),
    selector=dict(mode="markers"),
)

fig.update_layout(
    width=1200,
    height=700,
    legend_title_text="Dominant NAICS Sector",
    legend=dict(
        orientation="v",
        x=1.01,
        y=1,
        font=dict(size=11),
    ),
    xaxis=dict(
        title=x_label,
        ticksuffix="%",
        zeroline=True,
        zerolinecolor="rgba(255,255,255,0.2)",
    ),
    yaxis=dict(
        title=y_label,
        #type="log",
        tickformat="~s",  # 100K, 250K, 1M etc, no clustering
        rangemode="tozero",  # forces 0 to show
    ),
    margin=dict(r=200),
    font=dict(family="Inter, sans-serif"),
)

# Trendline
x = merged[x_col].values
y = merged[y_col].values
m, b = np.polyfit(x, y, 1)
x_line = np.linspace(x.min(), x.max(), 100)
y_line = m * x_line + b

fig.add_trace(go.Scatter(
    x=x_line,
    y=y_line,
    mode="lines",
    name="Trendline",
    line=dict(color="white", width=1.5, dash="dash"),
    showlegend=True,
))

fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")
print(f"\nSaved → {OUTPUT_HTML}")

# ── INDUSTRY CORRELATION BAR CHART ───────────────────────────────────────────

fig_corr = px.bar(
    corr_df.sort_values("Correlation"),
    x="Correlation",
    y="Industry",
    orientation="h",
    labels={
        "Correlation": "Correlation: Visit YoY % ↔ Jobs",
        "Industry": "",
    },
    title="Correlation: Cross-border Visit Decline ↔ Industry Employment",
    color="Correlation",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=0,
    hover_data={"NAICS": True, "N_Metros": True, "Avg_Jobs": ":,.0f"},
    template="plotly_dark",
)

fig_corr.update_xaxes(zeroline=True, zerolinecolor="rgba(255,255,255,0.3)")
fig_corr.update_layout(
    width=900,
    height=600,
    margin=dict(l=150),
    font=dict(family="Inter, sans-serif"),
)

corr_html = "industry_correlations.html"
fig_corr.write_html(corr_html, include_plotlyjs="cdn")
print(f"Saved → {corr_html}")

fig.show()
fig_corr.show()
