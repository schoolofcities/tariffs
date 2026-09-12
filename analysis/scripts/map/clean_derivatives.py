"""
Script to clean the tariff HS codes CSV file by removing derivative items 
when their first 6 digits already exist in non-derivative items.
"""

import pandas as pd

# Read the CSV file
input_file = 'tariff_hs_codes_derivatives_included_6_digit_rule.csv'
output_file = 'tariff_hs_codes_cleaned.csv'

df = pd.read_csv(input_file, dtype={'HS Code': str})

# Ensure HS Code is a string and pad with leading zeros if needed
df['HS Code'] = df['HS Code'].astype(str).str.strip()

# Extract the first 6 digits of each HS code
df['HS6'] = df['HS Code'].str[:6]

# Identify derivative and non-derivative items
df['is_derivative'] = df['Category'].str.contains(r'\(derivative\)', case=False, na=False)

# Get the set of 6-digit prefixes from non-derivative items
non_derivative_df = df[~df['is_derivative']]
non_derivative_hs6_set = set(non_derivative_df['HS6'].unique())

print(f"Total rows: {len(df)}")
print(f"Non-derivative items: {len(non_derivative_df)}")
print(f"Derivative items: {len(df[df['is_derivative']])}")
print(f"Unique 6-digit prefixes in non-derivatives: {len(non_derivative_hs6_set)}")

# Filter out derivative items where the first 6 digits exist in non-derivative items
def should_keep(row):
    if not row['is_derivative']:
        # Keep all non-derivative items
        return True
    else:
        # Keep derivative items only if their HS6 prefix is NOT in non-derivative set
        return row['HS6'] not in non_derivative_hs6_set

# Apply the filter
df['keep'] = df.apply(should_keep, axis=1)

# Count how many derivatives will be removed
derivatives_to_remove = df[(df['is_derivative']) & (~df['keep'])]
print(f"\nDerivative items to be removed (HS6 exists in non-derivatives): {len(derivatives_to_remove)}")

# Show some examples of what will be removed
if len(derivatives_to_remove) > 0:
    print("\nExamples of derivative items being removed:")
    print(derivatives_to_remove[['HS Code', 'Category', 'HS6']].head(10).to_string(index=False))

# Keep only the items that pass the filter
cleaned_df = df[df['keep']][['HS Code', 'Category']]

print(f"\nFinal row count: {len(cleaned_df)}")

# Save to new CSV
cleaned_df.to_csv(output_file, index=False)
print(f"\nCleaned data saved to: {output_file}")
