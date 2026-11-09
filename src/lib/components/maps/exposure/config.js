// Configuration for the direct-exposure map (/exposure/map).
//
// Column names in the lookup files are <tariff code><suffix>:
//   percent (fractions, 0.05 = 5%):  _1 businesses, _2 employees (work), _3 employees (home)
//   count:                            _B businesses, _E employees (work), _C employees (home)
import { BRAND } from '$lib/styles/brand.js';

import { base } from '$app/paths';
import { withData } from '$lib/maps/geographies.js';

export const UPDATED = 'September 2026';
export const TARIFFS_AS_OF = 'September 2026';

export const GRADUATED_COLOURS = [BRAND.yellow, '#fb921f', '#f3603e', '#d73256', BRAND.pink];
export const GRADUATED_SIZES = [5, 9, 15, 24, 34];

export const GEOGRAPHIES = withData({
	ADA: `${base}/data/exposure/ada.json`,
	CSD: `${base}/data/exposure/csd.json`
});

export const INDICATORS = [
	{ value: 'business', label: 'Businesses', who: 'businesses', percent: '_1', count: '_B' },
	{ value: 'work', label: 'Employees (place of work)', who: 'employees (by work location)', percent: '_2', count: '_E' },
	{ value: 'home', label: 'Employees (home)', who: 'employees (by primary residence)', percent: '_3', count: '_C' }
];

export const METRICS = [
	{ value: 'percent', label: 'Percent' },
	{ value: 'count', label: 'Total' }
];

// Dropdown order = array order. `breaks` keyed by column suffix.
// NOTE: several of these breaks are provisional (Dairy/Alcohol/Motor, ScenBefore/
// ScenAfter, S338_*) and should be recalibrated after the next pipeline run.
export const TARIFFS = [
	{
		code: 'ScenAfter',
		label: 'All goods subject to tariffs (after Sep 29, 2026)',
		subject: 'all tariffs in effect after September 29, 2026',
		note: 'Includes all tariffs in effect as of September 29, 2026, which include the Section 338 tariffs on dairy, alcohol, motor vehicles, and additionally non-CUSMA-compliant goods.',
		breaks: { _1: [0.05, 0.1, 0.2, 0.3], _2: [0.04, 0.1, 0.2, 0.4], _3: [0.05, 0.1, 0.2, 0.5], _B: [10, 50, 100, 200], _E: [500, 1000, 2500, 5000], _C: [400, 700, 1000, 1500] }
	},
	{
		code: 'ScenBefore',
		label: 'All goods subject to tariffs (prior to Sep 29, 2026)',
		subject: 'all tariffs in effect prior to September 29, 2026',
		note: 'Reflects tariffs in effect prior to the introduction of any Section 338 tariffs.',
		breaks: { _1: [0.05, 0.1, 0.2, 0.3], _2: [0.05, 0.1, 0.2, 0.4], _3: [0.05, 0.1, 0.2, 0.5], _B: [10, 50, 100, 200], _E: [500, 1000, 2500, 5000], _C: [400, 700, 1000, 1500] }
	},
	{
		code: 'S338_Tot',
		label: 'Section 338 – Total',
		subject: 'Section 338 tariffs (goods tariffed and excluded combined)',
		note: 'Reflects all goods that are tariffed or excluded under Section 338.',
		breaks: { _1: [0.01, 0.04, 0.08, 0.2], _2: [0.01, 0.04, 0.08, 0.2], _3: [0.01, 0.04, 0.08, 0.2], _B: [10, 50, 100, 200], _E: [200, 500, 1000, 2000], _C: [200, 500, 1000, 2000] }
	},
	{
		code: 'S338_Tar',
		label: 'Section 338 – Tariffed',
		subject: 'goods subject to Section 338 tariffs',
		note: 'Goods tariffed under Section 338.',
		breaks: { _1: [0.01, 0.04, 0.08, 0.2], _2: [0.01, 0.04, 0.08, 0.2], _3: [0.01, 0.04, 0.08, 0.2], _B: [10, 50, 100, 200], _E: [200, 500, 1000, 2000], _C: [200, 500, 1000, 2000] }
	},
	{
		code: 'S338_Exc',
		label: 'Section 338 – Excluded',
		subject: 'goods excluded from Section 338 tariffs',
		note: 'Goods that are banned from import to the U.S. from Canada under Section 338.',
		breaks: { _1: [0.002, 0.005, 0.01, 0.02], _2: [0.002, 0.005, 0.01, 0.02], _3: [0.002, 0.005, 0.01, 0.02], _B: [1, 2, 5, 10], _E: [10, 50, 100, 250], _C: [10, 50, 100, 250] }
	},
	{
		code: 'Dairy',
		label: 'Section 338 – Dairy',
		subject: "U.S. Administration's Dairy Tariffs on Canada",
		note: 'Dairy goods covered by Section 338, including both tariffed and excluded goods.',
		breaks: { _1: [0.01, 0.02, 0.03, 0.04], _2: [0.01, 0.02, 0.03, 0.04], _3: [0.01, 0.02, 0.03, 0.04], _B: [2, 5, 10, 20], _E: [25, 100, 250, 500], _C: [25, 100, 200, 500] }
	},
	{
		code: 'Alcohol',
		label: 'Section 338 – Alcohol',
		subject: "U.S. Administration's Alcohol Tariffs on Canada",
		note: 'Alcohol goods covered by Section 338, including both tariffed and excluded goods.',
		breaks: { _1: [0.01, 0.02, 0.03, 0.04], _2: [0.01, 0.02, 0.03, 0.04], _3: [0.01, 0.02, 0.03, 0.04], _B: [2, 5, 10, 20], _E: [25, 100, 250, 500], _C: [25, 100, 200, 500] }
	},
	{
		code: 'Motor',
		label: 'Section 338 – Motor vehicles',
		subject: "U.S. Administration's Motor Vehicle Tariffs on Canada",
		note: 'Motor vehicle goods covered by Section 338, including both tariffed and excluded goods.',
		breaks: { _1: [0.01, 0.04, 0.08, 0.2], _2: [0.01, 0.04, 0.08, 0.2], _3: [0.01, 0.04, 0.08, 0.2], _B: [10, 50, 100, 200], _E: [200, 500, 1000, 2000], _C: [200, 500, 1000, 2000] }
	},
	{
		code: 'Auto',
		label: 'Automobiles',
		subject: "U.S. Administration's Automobile Tariffs on Canada",
		breaks: { _1: [0.01, 0.02, 0.03, 0.06], _2: [0.01, 0.04, 0.08, 0.2], _3: [0.01, 0.02, 0.05, 0.2], _B: [5, 10, 20, 50], _E: [200, 500, 1000, 2000], _C: [50, 100, 250, 500] }
	},
	{
		code: 'Alum',
		label: 'Aluminum',
		subject: "U.S. Administration's Aluminum Tariffs on Canada",
		breaks: { _1: [0.01, 0.02, 0.03, 0.05], _2: [0.01, 0.05, 0.1, 0.2], _3: [0.01, 0.03, 0.07, 0.2], _B: [5, 10, 20, 50], _E: [200, 500, 1000, 2000], _C: [50, 100, 250, 500] }
	},
	{
		code: 'Steel',
		label: 'Steel',
		subject: "U.S. Administration's Steel Tariffs on Canada",
		breaks: { _1: [0.01, 0.02, 0.03, 0.07], _2: [0.01, 0.05, 0.1, 0.3], _3: [0.01, 0.05, 0.1, 0.25], _B: [5, 10, 20, 50], _E: [200, 500, 1000, 2000], _C: [50, 100, 250, 500] }
	},
	{
		code: 'Cop',
		label: 'Copper',
		subject: "U.S. Administration's Copper Tariffs on Canada",
		breaks: { _1: [0.01, 0.02, 0.03, 0.04], _2: [0.01, 0.02, 0.04, 0.08], _3: [0.01, 0.02, 0.03, 0.04], _B: [2, 5, 10, 20], _E: [200, 500, 1000, 2000], _C: [10, 25, 50, 100] }
	},
	{
		code: 'LumOld',
		label: 'Lumber (before Oct 14)',
		subject: "U.S. Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
		breaks: { _1: [0.01, 0.02, 0.07, 0.15], _2: [0.01, 0.05, 0.1, 0.2], _3: [0.01, 0.03, 0.08, 0.2], _B: [2, 5, 10, 20], _E: [25, 100, 250, 500], _C: [25, 100, 200, 500] }
	},
	{
		code: 'LumNew',
		label: 'Lumber (after Oct 14)',
		subject: "U.S. Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
		breaks: { _1: [0.01, 0.02, 0.07, 0.15], _2: [0.01, 0.05, 0.1, 0.2], _3: [0.01, 0.03, 0.08, 0.2], _B: [2, 5, 10, 20], _E: [25, 100, 250, 500], _C: [25, 100, 200, 500] }
	},
	{
		code: 'MHDV',
		label: 'Trucks (Medium & Heavy Duty Vehicles)',
		subject: "U.S. Administration's Medium Heavy Duty Vehicles Tariffs on Canada",
		breaks: { _1: [0.01, 0.02, 0.03, 0.04], _2: [0.01, 0.02, 0.03, 0.04], _3: [0.01, 0.02, 0.03, 0.04], _B: [2, 5, 10, 20], _E: [50, 100, 250, 500], _C: [25, 100, 200, 500] }
	},
	{
		code: 'Ene',
		label: 'Energy and natural resources',
		subject: "U.S. Administration's Energy and natural resources tariffs on Canada",
		breaks: { _1: [0.01, 0.02, 0.03, 0.08], _2: [0.01, 0.05, 0.1, 0.2], _3: [0.01, 0.03, 0.08, 0.2], _B: [5, 10, 20, 50], _E: [50, 100, 250, 1000], _C: [25, 100, 200, 500] }
	},
	{
		code: 'CUSMA',
		label: 'Non-CUSMA-Compliant',
		subject: "U.S. Administration's non-CUSMA Compliant Tariffs on Canada",
		breaks: { _1: [0.05, 0.1, 0.2, 0.3], _2: [0.05, 0.1, 0.2, 0.4], _3: [0.05, 0.1, 0.2, 0.5], _B: [10, 50, 100, 200], _E: [500, 1000, 2500, 5000], _C: [400, 700, 1000, 1500] }
	}
];

export const DEFAULTS = { tariff: 'ScenAfter', indicator: 'business', metric: 'percent', geo: 'ADA' };

/** Resolve the UI selection to everything the map + legend need. */
export function resolveSelection({ tariff, indicator, metric, geo }) {
	const t = TARIFFS.find((x) => x.code === tariff) ?? TARIFFS[0];
	const ind = INDICATORS.find((x) => x.value === indicator) ?? INDICATORS[0];
	const isPercent = metric === 'percent';
	const suffix = isPercent ? ind.percent : ind.count;
	const lead = isPercent ? `Estimated % of ${ind.who}` : `Estimated count of ${ind.who}`;
	return {
		tariff: t,
		description: `${lead} directly exposed to ${t.subject}`,
		view: {
			geo,
			mode: isPercent ? 'fill' : 'circle',
			column: `${t.code}${suffix}`,
			breaks: t.breaks[suffix],
			colours: GRADUATED_COLOURS,
			sizes: GRADUATED_SIZES
		}
	};
}

export const formatPercent = (v) => `${(Math.abs(v) * 100).toFixed(1)}%`;
export const formatCount = (v) => Math.round(v).toLocaleString('en-CA');

/** Legend break label: percent breaks as whole/decimal %, counts as integers. */
export const formatBreak = (metric) => (b) =>
	metric === 'percent' ? `${+(b * 100).toFixed(1)}%` : b.toLocaleString('en-CA');
