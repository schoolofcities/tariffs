// Shared basemap for all tariff maps: style, overlay sources and layers.
//
// Data layers are slotted in between these with `beforeId`, using the anchor
// ids exported below, so the draw order is defined in one place:
//
//   background / ocean
//   [data fills]          -> before ANCHORS.fills
//   land tint, lakes
//   [data outlines/hover] -> before ANCHORS.lines
//   admin boundaries, census divisions, province lines
//   [data circles]        -> before ANCHORS.circles
//   labels

import { base } from '$app/paths';

const WATER = '#E3F4FB';
const LABEL_FONT = ['Open Sans Regular'];

export const ANCHORS = {
	fills: 'land',
	lines: 'boundaries',
	circles: 'city_names_big'
};

export const INITIAL_VIEW = {
	center: [-95, 60],
	zoom: 3,
	minZoom: 1,
	maxZoom: 11.9,
	pitch: 5
};

// Below this zoom the map is drawn as a globe, above it as flat mercator.
export const GLOBE_MAX_ZOOM = 7;

export function baseStyle() {
	return {
		version: 8,
		glyphs: 'https://schoolofcities.github.io/fonts/fonts/{fontstack}/{range}.pbf',
		sources: {
			osm: {
				type: 'vector',
				tiles: ['https://vector.openstreetmap.org/shortbread_v1/{z}/{x}/{y}.mvt'],
				maxzoom: 14
			}
		},
		layers: [
			{ id: 'background', type: 'background', paint: { 'background-color': '#fbfbfb' } },
			{ id: 'ocean', type: 'fill', source: 'osm', 'source-layer': 'ocean', paint: { 'fill-color': WATER } }
		]
	};
}

const labelText = (size) => ({
	'text-field': ['get', 'name'],
	'text-font': LABEL_FONT,
	'text-size': ['interpolate', ['linear'], ['zoom'], 4, size[0], 10, size[1]],
	'text-anchor': 'center'
});

const labelPaint = (opacity = 0.8) => ({
	'text-color': '#333333',
	'text-halo-color': '#fff',
	'text-halo-width': 1.5,
	'text-opacity': opacity
});

const BIG_PLACE = ['any', ['==', ['get', 'kind'], 'city'], ['==', ['get', 'kind'], 'state_capital'], ['==', ['get', 'kind'], 'national capital']];
const LAKE_AREA_CUTOFF = 30000000;

/** Add overlay sources + layers on top of baseStyle(). Call once, in map.on('load'). */
export function addBasemapLayers(map, { censusDivisions = true } = {}) {
	const geo = (f) => `${base}/data/geo/${f}`;

	map.addSource('ne_lakes', { type: 'geojson', data: geo('ne_50m_lakes.geojson') });
	map.addSource('province_lines', { type: 'geojson', data: geo('province-state-lines.geojson') });
	map.addSource('province_points', { type: 'geojson', data: geo('province-points.geojson') });
	map.addSource('city_names', { type: 'geojson', data: geo('populated-places-canada.geojson') });
	if (censusDivisions) {
		map.addSource('census_divisions', { type: 'vector', url: `pmtiles://${base}/tiles/census-divisions.pmtiles` });
	}

	const layers = [
		{ id: 'land', type: 'fill', source: 'osm', 'source-layer': 'land', paint: { 'fill-color': 'black', 'fill-opacity': 0.02 } },
		{ id: 'ne_lakes', type: 'fill', source: 'ne_lakes', maxzoom: 5, paint: { 'fill-color': WATER } },
		{
			id: 'lakes_large', type: 'fill', source: 'osm', 'source-layer': 'water_polygons', minzoom: 5,
			filter: ['all', ['==', ['get', 'kind'], 'water'], ['>=', ['get', 'way_area'], LAKE_AREA_CUTOFF]],
			paint: { 'fill-color': WATER }
		},
		{
			id: 'lakes_small', type: 'fill', source: 'osm', 'source-layer': 'water_polygons', minzoom: 11,
			filter: ['all', ['==', ['get', 'kind'], 'water'], ['<', ['get', 'way_area'], LAKE_AREA_CUTOFF]],
			paint: { 'fill-color': WATER }
		},
		{ id: 'boundaries', type: 'line', source: 'osm', 'source-layer': 'boundaries', paint: { 'line-color': '#D0D1C9', 'line-width': 1 } },
		{ id: 'province_lines_case', type: 'line', source: 'province_lines', maxzoom: 6, paint: { 'line-color': '#ffffff', 'line-width': 3, 'line-opacity': 0.5 } },
		...(censusDivisions
			? [{ id: 'census_divisions', type: 'line', source: 'census_divisions', 'source-layer': 'censusdivisions', minzoom: 6, paint: { 'line-color': '#4d4d4d', 'line-width': 0.5 } }]
			: []),
		{ id: 'province_lines', type: 'line', source: 'province_lines', maxzoom: 6, paint: { 'line-color': '#D0D1C9', 'line-width': 1 } },
		{
			id: 'city_names_big', type: 'symbol', source: 'city_names', minzoom: 2, maxzoom: 6,
			filter: ['<', ['get', 'scalerank'], 5],
			layout: { ...labelText([10, 13]), 'symbol-sort-key': ['get', 'scalerank'] },
			paint: labelPaint()
		},
		{
			id: 'city_names_all', type: 'symbol', source: 'city_names', minzoom: 6, maxzoom: 8,
			layout: { ...labelText([10, 13]), 'symbol-sort-key': ['get', 'scalerank'] },
			paint: labelPaint()
		},
		{ id: 'place_labels_big', type: 'symbol', source: 'osm', 'source-layer': 'place_labels', minzoom: 8, filter: BIG_PLACE, layout: labelText([10, 13]), paint: labelPaint() },
		{ id: 'place_labels', type: 'symbol', source: 'osm', 'source-layer': 'place_labels', minzoom: 8, filter: ['!', BIG_PLACE], layout: labelText([9, 11]), paint: labelPaint(0.65) },
		{
			id: 'province_points', type: 'symbol', source: 'province_points', minzoom: 2, maxzoom: 6,
			layout: { ...labelText([14, 16]), 'text-font': ['Open Sans Italic'] },
			paint: labelPaint()
		}
	];

	for (const layer of layers) map.addLayer(layer);
}
