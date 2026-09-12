import csv
import io
import requests

YEAR = 2025
QTR = 3
OWNERSHIP = "5"
AREA = "C1206"  # Atlanta-Sandy Springs-Roswell, GA MSA (Large metro to avoid suppression)

print(f"Fetching data for {AREA} in {YEAR} Q{QTR}...")
url = f"https://data.bls.gov/cew/data/api/{YEAR}/{QTR}/area/{AREA}.csv"
response = requests.get(url, timeout=30)
response.raise_for_status()

reader = csv.DictReader(io.StringIO(response.text))
data = list(reader)

print(f"Total rows fetched: {len(data)}")

# Filter to ownership 5
private_data = [row for row in data if row.get("own_code") == OWNERSHIP]
print(f"Total private ownership rows: {len(private_data)}")

# Filter to 6-digit industry codes
six_digit_data = [
    row for row in private_data
    if len(row.get("industry_code", "").strip()) == 6
]
print(f"Total 6-digit industry rows (private): {len(six_digit_data)}")

# Count non-zero wages
non_zero = [row for row in six_digit_data if int(row.get("total_qtrly_wages", 0)) > 0]
zero = [row for row in six_digit_data if int(row.get("total_qtrly_wages", 0)) == 0]

print(f"6-digit rows with >0 wages: {len(non_zero)}")
print(f"6-digit rows with 0 wages: {len(zero)}")

print("\n--- SAMPLE OF NON-ZERO WAGE ROWS ---")
for row in non_zero[:5]:
    print(f"Industry: {row['industry_code']}, Estabs: {row['qtrly_estabs']}, Wages: {row['total_qtrly_wages']}, Disclosure: {row['disclosure_code']}")

print("\n--- SAMPLE OF ZERO WAGE ROWS ---")
for row in zero[:5]:
    print(f"Industry: {row['industry_code']}, Estabs: {row['qtrly_estabs']}, Wages: {row['total_qtrly_wages']}, Disclosure: {row['disclosure_code']}")
