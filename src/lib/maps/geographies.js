// Polygon tiles shared by every area map. The tiles hold geometry + id only;
// each map supplies its own values in a lookup file (static/data/<map>/{ada,csd}.json),
// joined on the GUID. Exposure and scenario data use the same 2021 ADA/CSD ids,
// so they share these tiles.

import { base } from '$app/paths';

export const AREA_TILES = {
	ADA: {
		label: 'Aggregate dissemination areas',
		tiles: `${base}/tiles/exposure/ada.pmtiles`,
		sourceLayer: 'choropleth',
		idField: 'ADADGUID',
		linePaint: {
			'line-color': '#808080',
			'line-width': ['interpolate', ['linear'], ['zoom'], 3, 1, 16, 2],
			'line-opacity': 0.15
		}
	},
	CSD: {
		label: 'Census subdivisions (municipalities)',
		tiles: `${base}/tiles/exposure/csd.pmtiles`,
		sourceLayer: 'choropleth_csd',
		idField: 'CSDDGUID',
		linePaint: {
			'line-color': '#808080',
			'line-width': ['interpolate', ['linear'], ['zoom'], 4, 0, 17, 3],
			'line-opacity': 0.4
		}
	}
};

/** AREA_TILES plus a data URL per geography: withData({ ADA: url, CSD: url }) */
export function withData(urls) {
	return Object.fromEntries(Object.entries(AREA_TILES).map(([key, g]) => [key, { ...g, data: urls[key] }]));
}

/** Options for a geographic-unit ToggleGroup. */
export const GEO_OPTIONS = Object.entries(AREA_TILES).map(([value, g]) => ({ value, label: g.label }));
