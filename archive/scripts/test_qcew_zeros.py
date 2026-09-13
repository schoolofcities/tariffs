import csv
import io
import requests

url = "https://data.bls.gov/cew/data/api/2025/3/area/C1206.csv"
response = requests.get(url)
data = list(csv.DictReader(io.StringIO(response.text)))

non_zero = [r for r in data if int(r.get("total_qtrly_wages", 0)) > 0]
print(f"Total rows: {len(data)}")
print(f"Total non-zero wages rows: {len(non_zero)}")

for r in non_zero[:5]:
    print(r["own_code"], r["industry_code"], r["total_qtrly_wages"])

for r in [r for r in data if r.get("disclosure_code") == "-"][:5]:
    print("Zero Data Example ->", r["own_code"], r["industry_code"], r["total_qtrly_wages"], "(Suppressed)")
