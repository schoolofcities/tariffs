import csv
import difflib
import io
import logging
import re
import time
from pathlib import Path
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


YEAR = 2023
QTR = "a"
INDUSTRY_CODE_LENGTH = 6
OWNERSHIP_CODE = "5"  # Private ownership; detailed industries are not available for total.
FUZZY_THRESHOLD = 0.85
SECONDARY_THRESHOLD = 0.6
INPUT_METROS_CSV = Path("static/canada-us-visits/us_normalized_trips_daily.csv")
OUTPUT_DIR = Path("analysis/outputs")
OUTPUT_DATA_CSV = OUTPUT_DIR / f"qcew_msa_industry_{YEAR}_{QTR}_2digit.csv"
OUTPUT_UNMATCHED_CSV = OUTPUT_DIR / "qcew_msa_unmatched.csv"
OUTPUT_MAPPING_CSV = OUTPUT_DIR / "qcew_msa_mapping.csv"
AREA_TITLES_URLS = [
    "https://data.bls.gov/cew/doc/titles/area/area_titles.csv",
    "http://data.bls.gov/cew/doc/titles/area/area_titles.csv",
]
INDUSTRY_TITLES_URLS = [
    "https://data.bls.gov/cew/doc/titles/industry/industry_titles.csv",
    "http://data.bls.gov/cew/doc/titles/industry/industry_titles.csv",
]
QCEW_AREA_URL = "https://data.bls.gov/cew/data/api/{year}/{qtr}/area/{area}.csv"


def normalize_name(value: str) -> str:
    if not value:
        return ""
    text = value.upper()
    text = re.sub(r"\(.*?\)", " ", text)
    text = text.replace("METROPOLITAN STATISTICAL AREA", " ")
    text = text.replace("MICROPOLITAN STATISTICAL AREA", " ")
    text = text.replace("MICRO AREA", " ")
    text = text.replace("MICRO", " ")
    text = text.replace("METROPOLITAN DIVISION", " ")
    text = text.replace("METRO AREA", " ")
    text = text.replace("METRO", " ")
    text = text.replace("MSA", " ")
    text = text.replace("CBSA", " ")
    text = text.replace("CSA", " ")
    text = re.sub(r"[^A-Z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_name(value: str) -> list[str]:
    normalized = normalize_name(value)
    return [token for token in normalized.split(" ") if token]


def extract_states(value: str) -> set[str]:
    if not value:
        return set()
    match = re.search(r",\s*([A-Z]{2}(?:-[A-Z]{2})*)", value.upper())
    if not match:
        return set()
    return {state for state in match.group(1).split("-") if state}


def is_metro_area_title(title: str) -> bool:
    if not title:
        return False
    upper = title.upper()
    if "COMBINED STATISTICAL" in upper:
        return False
    return any(
        token in upper
        for token in (
            "MSA",
            "MICRO",
            "METROPOLITAN",
            "MICROPOLITAN",
            "METROPOLITAN DIVISION",
        )
    )


def download_csv(urls):
    last_error = None
    for url in urls:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            last_error = exc
    raise RuntimeError(f"Failed to download CSV from URLs: {urls}. Last error: {last_error}")


def load_area_titles():
    csv_text = download_csv(AREA_TITLES_URLS)
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = [row for row in reader]
    for row in rows:
        row["area_code"] = (row.get("area_code") or row.get("area_fips") or "").strip()
        row["area_title"] = row.get("area_title", "").strip()
        row["name_key"] = normalize_name(row["area_title"])
        row["name_tokens"] = tokenize_name(row["area_title"])
        row["state_set"] = extract_states(row["area_title"])
    return rows


def load_industry_titles():
    csv_text = download_csv(INDUSTRY_TITLES_URLS)
    reader = csv.DictReader(io.StringIO(csv_text))
    title_map = {}
    for row in reader:
        code = (row.get("industry_code") or "").strip()
        title = (row.get("industry_title") or "").strip()
        # Clean title by removing the code at the beginning if it matches
        if title.startswith(code + " "):
            title = title[len(code) + 1:].strip()
        title_map[code] = title
    return title_map


def load_metro_names():
    metros = set()
    with INPUT_METROS_CSV.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            name = (row.get("METRO") or "").strip()
            if name:
                metros.add(name)
    return sorted(metros)


def build_area_lookup(area_rows):
    keyed = {}
    for row in area_rows:
        if not is_metro_area_title(row.get("area_title", "")):
            continue
        if not row.get("area_code"):
            continue
        key = row.get("name_key")
        if not key:
            continue
        keyed.setdefault(key, []).append(row)

    lookup = {}
    for key, rows in keyed.items():
        rows_sorted = sorted(
            rows,
            key=lambda r: (
                "METROPOLITAN" not in r["area_title"].upper(),
                len(r["area_title"]),
            ),
        )
        lookup[key] = rows_sorted[0]
    return lookup


def similarity_score(metro_tokens, candidate_tokens):
    metro_set = set(metro_tokens)
    candidate_set = set(candidate_tokens)
    if not metro_set or not candidate_set:
        return 0.0
    intersection = metro_set & candidate_set
    union = metro_set | candidate_set
    jaccard = len(intersection) / len(union)
    seq = difflib.SequenceMatcher(
        None, " ".join(metro_tokens), " ".join(candidate_tokens)
    ).ratio()
    return (0.6 * jaccard) + (0.4 * seq)


def fuzzy_match(
    metro_key,
    metro_tokens,
    primary_token,
    metro_states,
    candidates,
    threshold,
    secondary_threshold,
):
    best_row = None
    best_score = 0.0
    for row in candidates:
        if metro_states and row.get("state_set"):
            if not (metro_states & row["state_set"]):
                continue
        score = similarity_score(metro_tokens, row.get("name_tokens", []))
        if score > best_score:
            best_score = score
            best_row = row
    if best_row and best_score >= threshold:
        return best_row, best_score
    if (
        best_row
        and primary_token
        and primary_token in set(best_row.get("name_tokens", []))
        and best_score >= secondary_threshold
    ):
        return best_row, best_score
    return None, best_score


def fetch_qcew_area_data(area_code):
    url = QCEW_AREA_URL.format(year=YEAR, qtr=QTR, area=area_code)
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    reader = csv.DictReader(io.StringIO(response.text))
    return list(reader)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    metro_names = load_metro_names()
    area_rows = load_area_titles()
    area_lookup = build_area_lookup(area_rows)
    industry_titles = load_industry_titles()
    metro_candidates = [row for row in area_rows if is_metro_area_title(row.get("area_title", ""))]

    matched = {}
    mapping_rows = []
    unmatched = []
    for metro in metro_names:
        key = normalize_name(metro)
        metro_tokens = tokenize_name(metro)
        primary_token = metro_tokens[0] if metro_tokens else ""
        metro_states = extract_states(metro)
        if key in area_lookup:
            matched_row = area_lookup[key]
            matched[metro] = matched_row
            mapping_rows.append(
                {
                    "metro_name": metro,
                    "area_code": matched_row["area_code"],
                    "area_title": matched_row["area_title"],
                    "match_type": "exact",
                    "match_score": "1.0",
                }
            )
        else:
            matched_row, match_score = fuzzy_match(
                key,
                metro_tokens,
                primary_token,
                metro_states,
                metro_candidates,
                threshold=FUZZY_THRESHOLD,
                secondary_threshold=SECONDARY_THRESHOLD,
            )
            if matched_row:
                matched[metro] = matched_row
                mapping_rows.append(
                    {
                        "metro_name": metro,
                        "area_code": matched_row["area_code"],
                        "area_title": matched_row["area_title"],
                        "match_type": "fuzzy",
                        "match_score": f"{match_score:.3f}",
                    }
                )
            else:
                unmatched.append(metro)

    with OUTPUT_MAPPING_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["metro_name", "area_code", "area_title", "match_type", "match_score"],
        )
        writer.writeheader()
        writer.writerows(mapping_rows)

    with OUTPUT_UNMATCHED_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metro_name"])
        for metro in unmatched:
            writer.writerow([metro])

    results = []
    total_matched = len(matched)
    logging.info(f"Starting fetch for {total_matched} matched MSAs...")
    
    for i, (metro, area) in enumerate(matched.items(), 1):
        area_code = area["area_code"]
        area_title = area["area_title"]
        logging.info(f"[{i}/{total_matched}] Fetching data for area {area_code} ({area_title})")
        
        try:
            rows = fetch_qcew_area_data(area_code)
            time.sleep(1.0)  # Pause to avoid rate limits
        except requests.RequestException as e:
            logging.error(f"Failed to fetch data for {area_code}: {e}")
            continue

        preview_count = 0
        for row in rows:
            if row.get("own_code") != OWNERSHIP_CODE:
                continue
            if str(row.get("agglvl_code")).strip() != "44":
                continue

            industry_code = (row.get("industry_code") or "").strip()

            record = {
                "area_code": area_code,
                "area_title": area_title,
                "metro_name": metro,
                "year": row.get("year"),
                "qtr": row.get("qtr"),
                "industry_code": industry_code,
                "industry_title": industry_titles.get(industry_code, ""),
                "jobs": row.get("month3_emplvl") or row.get("annual_avg_emplvl"),
            }
            results.append(record)
            
            if preview_count < 3:
                logging.info(f"  Preview: {record['industry_code']} - {record['industry_title']}: {record['jobs']} jobs")
                preview_count += 1

    fieldnames = [
        "area_code",
        "area_title",
        "metro_name",
        "year",
        "qtr",
        "industry_code",
        "industry_title",
        "jobs",
    ]
    with OUTPUT_DATA_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
