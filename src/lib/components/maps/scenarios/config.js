// Job-loss scenarios (MRIO model): shared by the scenarios map, the rankings
// chart and the /scenarios overview page.

import { base } from '$app/paths';
import { root } from '$lib/site/paths.js';
import { withData } from '$lib/maps/geographies.js';
import { GRADUATED_COLOURS, GRADUATED_SIZES } from '$lib/components/maps/exposure/config.js';

/** All scenarios content (map, rankings, overview) was first published together. */
export const PUBLISHED = 'November 2026';

/**
 * Scenario codes match the S{n} prefixes in the data (there is no S2).
 * `report` is the scenario's number in the MRIO report (/scenarios/report), which numbers them 1–5.
 */
export const SCENARIOS = [
	{
		code: 'S1',
		report: 1,
		label: 'Household Consumption',
		description: `Overall household consumption expenditures in Canada decline by 1%. <a href="https://www.scotiabank.com/ca/en/about/economics/economics-publications/post.other-publications.insights-views.cusma-scenario-note--march-5--2026-.html" target="_blank">Scotiabank Economics</a> and the <a href="https://www.bankofcanada.ca/wp-content/uploads/2025/01/mpr-2025-01-29.pdf" target="_blank">Bank of Canada</a> have given their projections of consumption decline, ranging from 0.5% to 2% of GDP consumption in Canada due to the tariffs.`
	},
	{
		code: 'S3',
		report: 2,
		label: 'Agri-food & Seafood',
		description: `Agriculture, agri-food, and seafood exports to the U.S. decline. Although not as directly affected, analysis from <a href="https://www.agri-pulse.com/articles/23170-analysis-checking-in-on-us-canada-agricultural-trade" target="_blank">Agri-Pulse</a> and <a href="https://retail-insider.com/retail-insider/opinion/2025/08/canadas-agri-food-sector-hit-by-35-u-s-tariff-after-ottawa-stalls/" target="_blank">Retail Insider</a> show significant declines in this sector in terms of agri-food exports.`
	},
	{
		code: 'S4',
		report: 3,
		label: 'Steel & Aluminum',
		description: `Steel and aluminum manufacturing exports to the U.S. decline. The <a href="https://fao-on.org/en/report/impacts-of-us-tariffs/" target="_blank">Financial Accountability Office (FAO) of Ontario</a> reported a potential 137,900 job decrease in Ontario by 2029 under the April 2025 tariff scenario.`
	},
	{
		code: 'S5',
		report: 4,
		label: 'Softwood Lumber',
		description: `Softwood lumber exports to the U.S. decline. The softwood lumber tariffs have affected the industry drastically, leading to declining lumber production and exports as noted by a report from the <a href="https://www.rbc.com/en/economics/canadian-analysis/featured-analysis/insights/tracking-the-impact-of-u-s-tariffs-on-five-targeted-canadian-industries/" target="_blank">Royal Bank of Canada</a> and our <a href="${root}/exposure/lumber">softwood lumber post</a>.`
	},
	{
		code: 'S6',
		report: 5,
		label: 'Autos & Parts',
		description: 'Automobile and auto-parts exports to the U.S. decline. The FAO noted a potential 20% decrease in U.S. motor vehicles exports and a 30% decrease for motor parts by 2029.'
	}
];

export const scenarioLabel = (code) => SCENARIOS.find((s) => s.code === code)?.label ?? `Scenario ${code.slice(1)}`;

export const EFFECTS = [
	{ value: 'DIR', label: 'Direct', text: 'Direct job losses in the industries facing the tariff.' },
	{ value: 'INDIR', label: 'Indirect', text: 'Indirect job losses in supplier industries.' },
	{ value: 'INDCD', label: 'Induced', text: 'Induced job losses from reduced household spending.' }
];

export const effectLabel = (codes) => codes.map((c) => EFFECTS.find((e) => e.value === c)?.label ?? c).join(' + ');

// ------------------------------------------------------------------ map

export const GEOGRAPHIES = withData({
	ADA: `${base}/data/scenarios/ada.json`,
	CSD: `${base}/data/scenarios/csd.json`
});

export const METRICS = [
	{ value: 'percent', label: 'Percent' },
	{ value: 'count', label: 'Total' }
];

export const DEFAULTS = { scenario: 'S1', effects: ['DIR'], metric: 'percent', geo: 'CSD' };

// Percent = job losses as % of local employment (percent units, 1 = 1%).
const PERCENT_BREAKS = { default: [1, 3, 5, 7], S4: [0.1, 0.5, 1, 2] };
const COUNT_BREAKS = [5, 25, 500, 2000];

const EFFECT_ORDER = EFFECTS.map((e) => e.value);

/** Column key for a selection, e.g. "S1|DIR+INDIR|percent" (computed by derive()). */
export function columnKey({ scenario, effects, metric }) {
	const sorted = EFFECT_ORDER.filter((e) => effects.includes(e));
	return `${scenario}|${sorted.join('+')}|${metric}`;
}

/**
 * AreaMap `derive` hook: sums the selected effects' job losses per area and,
 * for percent, divides by total employment. Areas with no employment figure
 * get null (shown as "no data") rather than being divided by a placeholder.
 */
export function derive(data, column) {
	const [scenario, effectList, metric] = column.split('|');
	if (!effectList) return null;
	const parts = effectList.split('+').map((e) => data.cols[`${scenario}_${e}_Jobs`]);
	if (parts.some((p) => !p)) return null;
	const emp = data.cols.EMP;
	return data.ids.map((_, i) => {
		let total = null;
		for (const p of parts) if (p[i] != null) total = (total ?? 0) + p[i];
		if (metric !== 'percent' || total == null) return total;
		return emp[i] ? (total / emp[i]) * 100 : null;
	});
}

export function resolveSelection(sel) {
	const isPercent = sel.metric === 'percent';
	const effects = effectLabel(EFFECT_ORDER.filter((e) => sel.effects.includes(e)));
	const scenario = scenarioLabel(sel.scenario);
	return {
		scenario: SCENARIOS.find((s) => s.code === sel.scenario) ?? SCENARIOS[0],
		description: isPercent
			? `Estimated share of local employment lost (${effects}) under the ${scenario} scenario`
			: `Estimated jobs lost (${effects}) under the ${scenario} scenario`,
		view: {
			geo: sel.geo,
			mode: isPercent ? 'fill' : 'circle',
			column: columnKey(sel),
			breaks: isPercent ? (PERCENT_BREAKS[sel.scenario] ?? PERCENT_BREAKS.default) : COUNT_BREAKS,
			colours: GRADUATED_COLOURS,
			sizes: GRADUATED_SIZES
		}
	};
}

export const formatValue = (metric) => (v) => {
	if (v == null) return 'No data';
	return metric === 'percent' ? `${v.toFixed(1)}%` : `${Math.round(v).toLocaleString('en-CA')} jobs`;
};

export const formatBreak = (metric) => (b) => (metric === 'percent' ? `${b}%` : b.toLocaleString('en-CA'));
