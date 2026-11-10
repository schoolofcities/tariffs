"""
Build the per-geography lookup files the scenarios map reads.

    python3 -I scripts/build_scenario_data.py <old-tariffs-repo> [out-dir]

Inputs:
    <old>/analysis/outputs/csv/all_scenarios_{ada,csd}.csv   S{n}_{DIR,INDIR,INDCD}_Jobs (negative = losses)
    <old>/static/csv/{ada,csd}_total_emp.csv                 total employment (place of work), the % denominator
    static/data/exposure/{ada,csd}.json (this repo)           names + centroids for the same GUIDs

Output: <out-dir>/{ada,csd}.json, same columnar shape as the exposure files:
    { ids, names?, lon, lat, cols: { "S1_DIR_Jobs": [...], ..., "EMP": [...] } }

Job columns are stored as positive job losses. EMP is null where the area has
no employment figure (or zero), so a percentage can't be computed and the map
shows "no data" -- consistently in colour and tooltip.
"""

import csv
import json
import sys
from pathlib import Path

GEOS = {"ada": "ADADGUID", "csd": "CSDDGUID"}


def num(s):
    s = (s or "").strip()
    if s == "" or s.lower() in ("nan", "none", "null"):
        return None
    v = float(s)
    return None if v != v else v


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    old = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("static/data/scenarios")
    out_dir.mkdir(parents=True, exist_ok=True)

    for geo, id_field in GEOS.items():
        exposure = json.loads(Path(f"static/data/exposure/{geo}.json").read_text())
        idx = {gid: i for i, gid in enumerate(exposure["ids"])}

        with open(old / f"analysis/outputs/csv/all_scenarios_{geo}.csv", newline="") as f:
            rows = {r[id_field]: r for r in csv.DictReader(f)}
        with open(old / f"static/csv/{geo}_total_emp.csv", newline="") as f:
            reader = csv.DictReader(f)
            emp_col = [c for c in reader.fieldnames if c != id_field][0]
            emp = {r[id_field]: num(r[emp_col]) for r in reader}

        ids = sorted(rows)
        missing = [g for g in ids if g not in idx]
        if missing:
            sys.exit(f"{geo}: {len(missing)} ids not in exposure lookup (e.g. {missing[:3]})")

        job_cols = [c for c in next(iter(rows.values())) if c.endswith("_Jobs")]
        out = {"ids": ids, "lon": [], "lat": [], "cols": {c: [] for c in job_cols + ["EMP"]}}
        if "names" in exposure:
            out["names"] = []

        for gid in ids:
            i = idx[gid]
            out["lon"].append(exposure["lon"][i])
            out["lat"].append(exposure["lat"][i])
            if "names" in out:
                out["names"].append(exposure["names"][i])
            for c in job_cols:
                v = num(rows[gid][c])
                out["cols"][c].append(None if v is None else round(abs(v), 2))
            e = emp.get(gid)
            out["cols"]["EMP"].append(e if e and e > 0 else None)

        no_emp = sum(v is None for v in out["cols"]["EMP"])
        path = out_dir / f"{geo}.json"
        path.write_text(json.dumps(out, separators=(",", ":")))
        print(f"{geo}: {len(ids)} areas, {len(job_cols)} job columns, {no_emp} without employment -> {path} ({path.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
