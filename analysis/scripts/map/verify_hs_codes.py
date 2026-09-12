"""
Script to verify and flag HS codes in the tariff CSV file for manual review.
This script identifies codes that may need verification against official Federal Register sources.

Key Federal Register Sources:
- Proclamation 9980 (Derivatives): https://www.federalregister.gov/documents/2020/01/29/2020-01806/
- Proclamation 10895 (Aluminum 2025): https://www.federalregister.gov/documents/2025/03/05/2025-03596/
- Proclamation 10896 (Steel 2025): https://www.federalregister.gov/documents/2025/06/16/2025-11067/
- Additional Derivatives (Aug 2025): https://www.federalregister.gov/documents/2025/08/19/2025-15819/
"""

import pandas as pd
import re

# Read the cleaned CSV file
input_file = 'tariff_hs_codes_cleaned.csv'
output_file = 'hs_codes_flagged_for_verification.csv'

df = pd.read_csv(input_file, dtype={'HS Code': str})
df['HS Code'] = df['HS Code'].astype(str).str.strip()

# Define expected chapter ranges for each category based on HTSUS structure
EXPECTED_CHAPTERS = {
    'Steel': {
        'base_chapters': ['72', '73'],  # Chapter 72-73: Iron and Steel
        'derivative_allowed_chapters': [
            '72', '73',  # Steel products
            '82',  # Tools (some steel derivatives)
            '83',  # Misc articles of base metal
            '84',  # Machinery (steel components)
            '85',  # Electrical equipment
            '86',  # Railway equipment
            '87',  # Vehicles
            '94',  # Furniture (steel)
            '95',  # Toys/sports (steel)
        ],
        'questionable_chapters': ['21', '22', '27', '28', '29', '30', '32', '33', '34', '35', '38', '39']
    },
    'Aluminum': {
        'base_chapters': ['76'],  # Chapter 76: Aluminum
        'derivative_allowed_chapters': [
            '76',  # Aluminum products
            '83',  # Misc articles
            '84',  # Machinery
            '85',  # Electrical equipment
            '87',  # Vehicles
            '94',  # Furniture
            '95',  # Sports equipment
            '96',  # Misc manufactured
        ],
        'questionable_chapters': ['04', '21', '22', '27', '28', '29', '30', '32', '33', '34', '35', '37', '38', '66']
    },
    'Copper': {
        'base_chapters': ['74'],  # Chapter 74: Copper
        'derivative_allowed_chapters': ['74', '85'],  # Copper and electrical wiring
        'questionable_chapters': []
    },
    'Auto': {
        'base_chapters': ['87'],  # Chapter 87: Vehicles
        'allowed_chapters': ['40', '70', '83', '84', '85', '87', '90', '94', '97'],
        'questionable_chapters': []
    },
    'Lumber': {
        'base_chapters': ['44'],  # Chapter 44: Wood
        'allowed_chapters': ['44', '94'],
        'questionable_chapters': []
    },
    'Energy Mineral': {
        'base_chapters': ['25', '26', '27', '28', '71', '72', '75', '76', '78', '79', '80', '81', '85'],
        'questionable_chapters': []
    },
    'MHDV': {
        'base_chapters': ['87'],
        'questionable_chapters': []
    }
}

# Flags for verification
flags = []

def get_chapter(hs_code):
    """Extract the 2-digit chapter from HS code."""
    return hs_code[:2] if len(hs_code) >= 2 else None

def get_base_category(category):
    """Extract base category without (derivative) or (old)/(new) suffixes."""
    match = re.match(r'^([A-Za-z\s]+)', category)
    return match.group(1).strip() if match else category

def check_code(row):
    """Check a single HS code and return any flags."""
    hs_code = str(row['HS Code'])
    category = row['Category']
    base_category = get_base_category(category)
    chapter = get_chapter(hs_code)
    is_derivative = 'derivative' in category.lower()
    
    issues = []
    
    # Flag 1: Invalid HS code length (should be 6-10 digits typically)
    if len(hs_code) < 6:
        issues.append(f"SHORT_HS_CODE: Only {len(hs_code)} digits")
    elif len(hs_code) > 10:
        issues.append(f"LONG_HS_CODE: {len(hs_code)} digits")
    
    # Flag 2: Non-numeric characters
    if not hs_code.isdigit():
        issues.append("NON_NUMERIC: Contains non-digit characters")
    
    # Flag 3: Check chapter alignment with category
    if base_category in EXPECTED_CHAPTERS:
        config = EXPECTED_CHAPTERS[base_category]
        
        if is_derivative:
            # For derivatives, check if chapter is questionable
            if 'questionable_chapters' in config and chapter in config['questionable_chapters']:
                issues.append(f"QUESTIONABLE_DERIVATIVE_CHAPTER: Ch.{chapter} unusual for {base_category} derivative")
            
            # Check if derivative is in non-standard chapter
            if 'derivative_allowed_chapters' in config:
                if chapter not in config['derivative_allowed_chapters']:
                    issues.append(f"UNEXPECTED_DERIVATIVE_CHAPTER: Ch.{chapter} not typical for {base_category}")
        else:
            # For base items, check if chapter matches expected
            if 'base_chapters' in config:
                if chapter not in config['base_chapters'] and 'allowed_chapters' not in config:
                    pass  # Many base items span multiple chapters
                elif 'allowed_chapters' in config and chapter not in config['allowed_chapters']:
                    issues.append(f"UNEXPECTED_BASE_CHAPTER: Ch.{chapter} not typical for {base_category}")
    
    # Flag 4: Specific questionable patterns
    # Food/beverage codes as metal derivatives
    if is_derivative and chapter in ['21', '22']:  # Food/beverages
        issues.append("FOOD_BEVERAGE_AS_DERIVATIVE: Unusual - verify this is correct")
    
    # Cosmetics/personal care as derivatives
    if is_derivative and chapter in ['33']:
        issues.append("COSMETICS_AS_DERIVATIVE: Ch.33 (cosmetics) as metal derivative - verify")
    
    # Organic chemicals as derivatives
    if is_derivative and chapter in ['29']:
        issues.append("ORGANIC_CHEMICALS_AS_DERIVATIVE: Ch.29 unusual for metal derivative")
    
    # Pharmaceuticals as derivatives
    if is_derivative and chapter == '30':
        issues.append("PHARMA_AS_DERIVATIVE: Ch.30 (pharma) as metal derivative - verify")
    
    # Flag 5: Check for potential duplicates (same code, different categories)
    # This will be handled separately
    
    return '; '.join(issues) if issues else None

# Apply verification
df['Verification_Flags'] = df.apply(check_code, axis=1)

# Check for duplicates (same HS code appearing multiple times)
duplicate_codes = df[df.duplicated(subset=['HS Code'], keep=False)]['HS Code'].unique()
df['Is_Duplicate'] = df['HS Code'].isin(duplicate_codes)
df.loc[df['Is_Duplicate'], 'Verification_Flags'] = df.loc[df['Is_Duplicate'], 'Verification_Flags'].fillna('') + '; DUPLICATE_HS_CODE'

# Clean up flags
df['Verification_Flags'] = df['Verification_Flags'].str.strip('; ')
df['Verification_Flags'] = df['Verification_Flags'].replace('', None)

# Summary statistics
print("=" * 70)
print("HS CODE VERIFICATION SUMMARY")
print("=" * 70)

total_codes = len(df)
flagged_codes = df['Verification_Flags'].notna().sum()
clean_codes = total_codes - flagged_codes

print(f"\nTotal HS Codes: {total_codes}")
print(f"Clean (no flags): {clean_codes} ({100*clean_codes/total_codes:.1f}%)")
print(f"Flagged for review: {flagged_codes} ({100*flagged_codes/total_codes:.1f}%)")

# Breakdown by flag type
print("\n" + "-" * 70)
print("FLAG BREAKDOWN:")
print("-" * 70)

all_flags = df['Verification_Flags'].dropna().str.split('; ').explode()
flag_counts = all_flags.value_counts()
for flag, count in flag_counts.items():
    if flag:
        print(f"  {flag}: {count}")

# Breakdown by category
print("\n" + "-" * 70)
print("FLAGGED CODES BY CATEGORY:")
print("-" * 70)

flagged_df = df[df['Verification_Flags'].notna()]
category_counts = flagged_df['Category'].value_counts()
for cat, count in category_counts.head(15).items():
    print(f"  {cat}: {count}")

# Show duplicate HS codes
duplicates_df = df[df['Is_Duplicate']][['HS Code', 'Category']].drop_duplicates()
if len(duplicates_df) > 0:
    print("\n" + "-" * 70)
    print(f"DUPLICATE HS CODES ({len(duplicate_codes)} unique codes):")
    print("-" * 70)
    for code in duplicate_codes[:20]:
        cats = df[df['HS Code'] == code]['Category'].tolist()
        print(f"  {code}: {', '.join(cats)}")
    if len(duplicate_codes) > 20:
        print(f"  ... and {len(duplicate_codes) - 20} more")

# Show examples of questionable derivative codes
print("\n" + "-" * 70)
print("EXAMPLES OF QUESTIONABLE DERIVATIVE CODES:")
print("-" * 70)

questionable = df[df['Verification_Flags'].str.contains('QUESTIONABLE|FOOD|COSMETICS|PHARMA|ORGANIC', na=False)]
for _, row in questionable.head(20).iterrows():
    print(f"  {row['HS Code']} - {row['Category']}")
    print(f"    Flags: {row['Verification_Flags']}")

# Save flagged results
df_flagged = df[['HS Code', 'Category', 'Verification_Flags', 'Is_Duplicate']]
df_flagged.to_csv(output_file, index=False)
print(f"\n{'=' * 70}")
print(f"Results saved to: {output_file}")
print("=" * 70)

# Also save just the items that need review
review_df = df[df['Verification_Flags'].notna()][['HS Code', 'Category', 'Verification_Flags']]
review_df.to_csv('hs_codes_needs_review.csv', index=False)
print(f"Items needing review saved to: hs_codes_needs_review.csv")
