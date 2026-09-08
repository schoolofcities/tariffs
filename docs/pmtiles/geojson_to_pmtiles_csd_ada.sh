#!/bin/bash
# Build pmtiles for choropleth + centroid layers, ADA and CSD versions

set -e

build() {
    local dir="$1" base="$2"
    shift 2
    echo "Processing $dir/$base..."
    tippecanoe "$@" --output="$dir/${base}.mbtiles" --force "$dir/${base}.geojson"
    pmtiles convert "$dir/${base}.mbtiles" "$dir/${base}.pmtiles"
    rm "$dir/${base}.mbtiles"
}

CHORO_OPTS=(-Z 0 -z 11 --detect-shared-borders --drop-fraction-as-needed \
            --coalesce --simplification=6 --drop-densest-as-needed)
CENTROID_OPTS=(-Z 0 -z 12 --drop-rate=0)

build ada_all/v2 choropleth     "${CHORO_OPTS[@]}"
build ada_all/v2 centroids      "${CENTROID_OPTS[@]}"
build csd_all/v2 choropleth_csd "${CHORO_OPTS[@]}"
build csd_all/v2 centroids_csd  "${CENTROID_OPTS[@]}"

echo "All done!"