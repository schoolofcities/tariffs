// MapLibre paint expressions shared by the area maps.
//
// `breaks` are 4 class breaks -> 5 classes, `colours` has 5 entries.
import { BRAND } from '$lib/styles/brand.js';

export const NO_DATA_COLOUR = BRAND.gray;
export const TRANSPARENT = 'rgba(0,0,0,0)';

/** Value source for fills: feature-state set from the lookup (null = no data). */
export const stateValue = (column) => ['feature-state', column];

/** Value source for circles: the `v` property of our own GeoJSON points. */
export const propValue = () => ['get', 'v'];

const isNumber = (expr) => ['==', ['typeof', expr], 'number'];

/**
 * Choropleth fill: grey when there is no value, otherwise a 5-class step.
 * Mirrors classIndex() below, which the legend and tooltip use.
 */
export function fillColour(valueExpr, breaks, colours) {
	return [
		'case',
		isNumber(valueExpr),
		['step', valueExpr, colours[0], breaks[0], colours[1], breaks[1], colours[2], breaks[2], colours[3], breaks[3], colours[4]],
		NO_DATA_COLOUR
	];
}

/** Circle colour: transparent for missing/zero, otherwise classed by `> break`. */
export function circleColour(valueExpr, breaks, colours) {
	return [
		'case',
		['!', isNumber(valueExpr)], TRANSPARENT,
		['<=', valueExpr, 0], TRANSPARENT,
		['>', valueExpr, breaks[3]], colours[4],
		['>', valueExpr, breaks[2]], colours[3],
		['>', valueExpr, breaks[1]], colours[2],
		['>', valueExpr, breaks[0]], colours[1],
		colours[0]
	];
}

/**
 * Circle radius. Zoomed out (< z8) only the two largest classes are drawn at
 * full size, to keep the national view readable; from z8 every class shows.
 */
export function circleRadius(valueExpr, breaks, sizes) {
	const v = ['coalesce', valueExpr, 0];
	const topTwo = ['case', ['>', v, breaks[3]], sizes[4], ['>', v, breaks[2]], sizes[3], 0.5];
	const all = [
		'case',
		['>', v, breaks[3]], sizes[4],
		['>', v, breaks[2]], sizes[3],
		['>', v, breaks[1]], sizes[2],
		['>', v, breaks[0]], sizes[1],
		sizes[0]
	];
	return ['interpolate', ['linear'], ['zoom'], 3, topTwo, 7.9999, topTwo, 8, all];
}
