#!/bin/bash
# Build pmtiles for choropleth + centroid layers, ADA and CSD versions

set -e

build() {
    local base="$1"
    shift
    echo "Processing $base..."
    tippecanoe "$@" --output="${base}.mbtiles" --force "${base}.geojson"
    pmtiles convert "${base}.mbtiles" "${base}.pmtiles"
    rm "${base}.mbtiles"
}

CHORO_OPTS=(-Z 0 -z 11 --detect-shared-borders --drop-fraction-as-needed \
            --coalesce --simplification=6 --drop-densest-as-needed --maximum-tile-bytes=2000000)
CENTROID_OPTS=(-Z 0 -z 12 --drop-rate=0 --maximum-tile-bytes=2000000)

build choropleth     "${CHORO_OPTS[@]}"
build centroids      "${CENTROID_OPTS[@]}"
build choropleth_csd "${CHORO_OPTS[@]}"
build centroids_csd  "${CENTROID_OPTS[@]}"

echo "All done!"