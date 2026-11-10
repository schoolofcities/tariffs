"""
Build the per-geography lookup files the exposure map reads.

    python3 -I scripts/build_exposure_data.py <old-tariffs-repo> [out-dir]

Inputs (from the analysis pipeline output, read-only):
    analysis/outputs/csv/choropleth.csv       ADA percents  (<code>_1/_2/_3, fractions)
    analysis/outputs/csv/centroids.csv        ADA counts    (<code>_B/_E/_C) + WKT point
    analysis/outputs/csv/choropleth_csd.csv   CSD percents
    analysis/outputs/csv/centroids_csd.csv    CSD counts + WKT point
    static/csv/csdnames.csv                   CSD names (CSDUID -> CSDNAME)

Output: <out-dir>/ada.json, <out-dir>/csd.json, columnar to keep them small:
    {
      "ids":   [guid, ...],
      "names": [name|null, ...],          # CSD only
      "lon":   [...], "lat": [...],       # centroid, for the count (circle) layer
      "cols":  { "Auto_1": [v|null, ...], "Auto_B": [...], ... }
    }

The map joins these to the (attribute-free) PMTiles polygons by GUID, so the
values shown in colours and in the tooltip always come from the same place.
"""

import csv
import json
import re
import sys
from pathlib import Path

PERCENT_SUFFIXES = ("_1", "_2", "_3")
COUNT_SUFFIXES = ("_B", "_E", "_C")
POINT_RE = re.compile(r"POINT\s*\(\s*(-?[\d.eE+-]+)\s+(-?[\d.eE+-]+)\s*\)")


def num(s, digits):
    s = (s or "").strip()
    if s == "" or s.lower() in ("nan", "none", "null"):
        return None
    v = float(s)
    if v != v:  # NaN
        return None
    return round(v, digits) if digits else int(round(v))


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build(id_field, pct_path, cnt_path, names=None):
    pct_rows = {r[id_field]: r for r in read_csv(pct_path)}
    cnt_rows = {r[id_field]: r for r in read_csv(cnt_path)}

    ids = sorted(set(pct_rows) | set(cnt_rows))
    sample_p = next(iter(pct_rows.values()))
    sample_c = next(iter(cnt_rows.values()))
    pct_cols = [c for c in sample_p if c.endswith(PERCENT_SUFFIXES)]
    cnt_cols = [c for c in sample_c if c.endswith(COUNT_SUFFIXES)]

    out = {"ids": ids, "lon": [], "lat": [], "cols": {c: [] for c in pct_cols + cnt_cols}}
    if names is not None:
        out["names"] = []

    missing_pt = 0
    for gid in ids:
        p = pct_rows.get(gid, {})
        c = cnt_rows.get(gid, {})
        m = POINT_RE.search(c.get("geometry", "") or "")
        if m:
            out["lon"].append(round(float(m.group(1)), 5))
            out["lat"].append(round(float(m.group(2)), 5))
        else:
            missing_pt += 1
            out["lon"].append(None)
            out["lat"].append(None)
        for col in pct_cols:
            out["cols"][col].append(num(p.get(col), 6))
        for col in cnt_cols:
            out["cols"][col].append(num(c.get(col), 0))
        if names is not None:
            out["names"].append(names.get(gid))

    nulls = {k: sum(v is None for v in vals) for k, vals in out["cols"].items()}
    print(
        f"  {len(ids)} areas, {len(pct_cols)} percent + {len(cnt_cols)} count columns, "
        f"{missing_pt} without centroid, max nulls in a column: {max(nulls.values())}"
    )
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("static/data/exposure")
    out_dir.mkdir(parents=True, exist_ok=True)
    csvs = src / "analysis/outputs/csv"

    # CSDDGUID = "2021A0005" + CSDUID
    csd_names = {
        "2021A0005" + r["CSDUID"]: r["CSDNAME"] for r in read_csv(src / "static/csv/csdnames.csv")
    }

    jobs = {
        "ada": ("ADADGUID", csvs / "choropleth.csv", csvs / "centroids.csv", None),
        "csd": ("CSDDGUID", csvs / "choropleth_csd.csv", csvs / "centroids_csd.csv", csd_names),
    }
    for key, (id_field, pct, cnt, names) in jobs.items():
        print(f"{key}:")
        data = build(id_field, pct, cnt, names)
        path = out_dir / f"{key}.json"
        path.write_text(json.dumps(data, separators=(",", ":")))
        print(f"  wrote {path} ({path.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
