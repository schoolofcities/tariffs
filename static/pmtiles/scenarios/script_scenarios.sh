#!/bin/bash
# This script runs tippecanoe and then pmtiles convert for each GeoJSON

set -e  # Stop on any error

for base in all_scenarios_csd all_scenarios_ada; do
    echo "Processing $base..."

    # 1. Generate .mbtiles with tippecanoe
    tippecanoe -Z 0 -z 11 \
        --output="${base}.mbtiles" \
        --detect-shared-borders \
        --drop-fraction-as-needed \
        --coalesce \
        --simplification=6 \
        --drop-densest-as-needed \
        "${base}.geojson" \
        --force

    # 2. Convert to .pmtiles
    pmtiles convert "${base}.mbtiles" "${base}.pmtiles"

    # (Optional) remove the .mbtiles to save space
    rm "${base}.mbtiles"
done

echo "All done!"