// U.S. region colours for the travel charts (swatches, trend lines). Pacific and Canada
// aren't brand colours.
import { BRAND } from '$lib/styles/brand.js';

export const REGION_COLOURS = {
	Midwest: BRAND.lightBlue,
	Northeast: BRAND.lightGreen,
	Southwest: BRAND.yellow,
	Southeast: BRAND.pink,
	Pacific: '#00AEB3',
	Canada: '#F3603E'
};

export const regionColour = (region) => REGION_COLOURS[region] || '#999';
