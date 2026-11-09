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
import { BRAND } from '$lib/styles/brand.js';

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
	'text-color': BRAND.gray80,
	'text-halo-color': '#fff',
	'text-halo-width': 1.5,
	'text-opacity': opacity
});

const BIG_KINDS = ['city', 'state_capital', 'national capital', 'capital'];
const BIG_PLACE = ['in', ['get', 'kind'], ['literal', BIG_KINDS]];
const LAKE_AREA_CUTOFF = 30000000;

// OSM's place_labels repeat many cities and towns 2-3 times a few km apart (the place
// point plus points from the municipal boundary), with identical attributes, so a style
// filter can't drop them. Instead these kinds are read from the loaded tiles, reduced to
// one point per name, and drawn from a GeoJSON source. Which copy is kept doesn't matter.
const DEDUP_KINDS = [...BIG_KINDS, 'town'];
const DEDUP_MINZOOM = 8;
const SAME_PLACE_DEG = 0.3; // same name within ~30 km = same place

function dedupedPlaces(map) {
	const raw = map.querySourceFeatures('osm', {
		sourceLayer: 'place_labels',
		filter: ['in', ['get', 'kind'], ['literal', DEDUP_KINDS]]
	});
	// Stable order, so the same tiles always give the same pick. Ties on population go to the
	// copy with more tags (more translated names), which is usually the place's centre point.
	const pts = raw
		.map((f) => ({
			name: f.properties.name,
			kind: f.properties.kind,
			pop: f.properties.population ?? 0,
			tags: Object.keys(f.properties).length,
			xy: f.geometry.coordinates
		}))
		.filter((p) => p.name && Array.isArray(p.xy) && typeof p.xy[0] === 'number')
		.sort((a, b) => b.pop - a.pop || b.tags - a.tags || a.xy[0] - b.xy[0] || a.xy[1] - b.xy[1]);

	/** @type {Map<string, number[][]>} */
	const kept = new Map();
	const features = [];
	for (const p of pts) {
		const prev = kept.get(p.name) ?? [];
		if (prev.some(([x, y]) => Math.abs(x - p.xy[0]) < SAME_PLACE_DEG && Math.abs(y - p.xy[1]) < SAME_PLACE_DEG)) continue;
		prev.push(p.xy);
		kept.set(p.name, prev);
		features.push({ type: 'Feature', geometry: { type: 'Point', coordinates: p.xy }, properties: { name: p.name, kind: p.kind } });
	}
	return features;
}

/** Keep the 'place_labels_dedup' source in step with the loaded OSM tiles. */
function syncDedupedPlaces(map) {
	let lastKey = '';
	let queued = false;
	const update = () => {
		queued = false;
		if (map.getZoom() < DEDUP_MINZOOM) return;
		const features = dedupedPlaces(map);
		const key = features.map((f) => f.properties.name + f.geometry.coordinates.join()).sort().join('|');
		if (key === lastKey) return; // unchanged: skip setData so labels don't flicker
		lastKey = key;
		map.getSource('place_labels_dedup')?.setData({ type: 'FeatureCollection', features });
	};
	const schedule = () => {
		if (queued) return;
		queued = true;
		requestAnimationFrame(update);
	};
	map.on('moveend', schedule);
	map.on('sourcedata', (e) => {
		if (e.sourceId === 'osm' && e.isSourceLoaded) schedule();
	});
}

/** Add overlay sources + layers on top of baseStyle(). Call once, in map.on('load'). */
export function addBasemapLayers(map, { censusDivisions = true } = {}) {
	const geo = (f) => `${base}/data/geo/${f}`;

	map.addSource('ne_lakes', { type: 'geojson', data: geo('ne_50m_lakes.geojson') });
	map.addSource('province_lines', { type: 'geojson', data: geo('province-state-lines.geojson') });
	map.addSource('province_points', { type: 'geojson', data: geo('province-points.geojson') });
	map.addSource('city_names', { type: 'geojson', data: geo('populated-places-canada.geojson') });
	map.addSource('place_labels_dedup', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
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
		{ id: 'boundaries', type: 'line', source: 'osm', 'source-layer': 'boundaries', paint: { 'line-color': BRAND.gray, 'line-width': 1 } },
		{ id: 'province_lines_case', type: 'line', source: 'province_lines', maxzoom: 6, paint: { 'line-color': '#ffffff', 'line-width': 3, 'line-opacity': 0.5 } },
		...(censusDivisions
			? [{ id: 'census_divisions', type: 'line', source: 'census_divisions', 'source-layer': 'censusdivisions', minzoom: 6, paint: { 'line-color': BRAND.gray70, 'line-width': 0.5 } }]
			: []),
		{ id: 'province_lines', type: 'line', source: 'province_lines', maxzoom: 6, paint: { 'line-color': BRAND.gray, 'line-width': 1 } },
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
		// cities + towns: deduplicated copy (see syncDedupedPlaces); everything smaller straight from OSM
		{ id: 'place_labels_big', type: 'symbol', source: 'place_labels_dedup', minzoom: DEDUP_MINZOOM, filter: BIG_PLACE, layout: labelText([10, 13]), paint: labelPaint() },
		{ id: 'place_labels_town', type: 'symbol', source: 'place_labels_dedup', minzoom: DEDUP_MINZOOM, filter: ['!', BIG_PLACE], layout: labelText([9, 11]), paint: labelPaint(0.65) },
		{
			id: 'place_labels', type: 'symbol', source: 'osm', 'source-layer': 'place_labels', minzoom: DEDUP_MINZOOM,
			filter: ['!', ['in', ['get', 'kind'], ['literal', DEDUP_KINDS]]],
			layout: labelText([9, 11]), paint: labelPaint(0.65)
		},
		{
			id: 'province_points', type: 'symbol', source: 'province_points', minzoom: 2, maxzoom: 6,
			layout: { ...labelText([14, 16]), 'text-font': ['Open Sans Italic'] },
			paint: labelPaint()
		}
	];

	for (const layer of layers) map.addLayer(layer);
	syncDedupedPlaces(map);
}
