<!--
	Job impact scenario rankings for CMAs or provinces: data + controls for
	RankedBarChart. Bars = selected metric (jobs or share of employment),
	box = share of employment.

	Data: static/data/scenarios/rollup_{cma,province}.json and rollup_breaks.json
	(from analysis/scenarios/roll_up_to_cma_prov.py). Fields: S{n}_{DIR|INDIR|INDCD|TOT}_{Jobs|Pct}.
-->
<script>
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import RankedBarChart from '../RankedBarChart.svelte';
	import ToggleGroup from '$lib/components/maps/ToggleGroup.svelte';
	import { GRADUATED_COLOURS } from '$lib/components/maps/exposure/config.js';
	import { SCENARIOS, EFFECTS, scenarioLabel } from '$lib/components/maps/scenarios/config.js';
	import { SCALES } from './config.js';

	const LEVELS = [
		{ value: 'cma', label: 'Census metropolitan areas' },
		{ value: 'province', label: 'Provinces and territories' }
	];
	// the ranking tool's own wording for each economic impact indicator (the map keeps EFFECTS' text)
	const IMPACT_TEXT = {
		TOT: 'Estimated potential job losses, including direct, indirect and induced effects.',
		DIR: 'Estimated potential job losses based on tariffs to the affected industry/industries.',
		INDIR: 'Estimated potential job losses based on impacts to the supply chains of the affected industry/industries.',
		INDCD: 'Estimated potential job losses based on reduced spending as a result of tariffs on the affected industry/industries.'
	};
	const CHART_EFFECTS = [{ value: 'TOT', label: 'All effects' }, ...EFFECTS].map((e) => ({ ...e, text: IMPACT_TEXT[e.value] }));
	const RANK_BY = [
		{ value: 'percent', label: 'Share of employment' },
		{ value: 'count', label: 'Total jobs' }
	];

	let scenario = $state('S1');
	let level = $state('cma');
	let effect = $state('TOT');
	let rankBy = $state('count');
	let scale = $state('linear');

	let data = $state.raw({ cma: [], province: [] });
	let breaks = $state.raw({});
	let loadError = $state('');

	const countKey = $derived(`${scenario}_${effect}_Jobs`);
	const pctKey = $derived(`${scenario}_${effect}_Pct`);
	const isPercent = $derived(rankBy === 'percent');

	const rows = $derived.by(() => {
		const key = isPercent ? pctKey : countKey;
		return data[level]
			.filter((d) => Number.isFinite(+d[key]))
			.sort((a, b) => b[key] - a[key])
			.map((d) => ({ id: d.GEO_UID, label: d.GEO_NAME, bar: +d[key], box: +d[pctKey] }));
	});

	// Box classes: precomputed by the rollup script, quintiles as a fallback.
	const boxBreaks = $derived.by(() => {
		const supplied = breaks?.[level]?.[pctKey];
		if (supplied?.length) return supplied;
		const vals = rows.map((d) => d.box).filter(Number.isFinite).sort((a, b) => a - b);
		if (vals.length < 5) return [];
		return [0.2, 0.4, 0.6, 0.8].map((q) => Math.round(vals[Math.floor(q * (vals.length - 1))] * 10) / 10);
	});

	// Axis is rescaled per selection: scenarios and levels differ by orders of magnitude.
	const ticks = $derived.by(() => {
		const max = rows.length ? niceCeiling(rows[0].bar) : 0;
		if (!max) return [0];
		const fractions = scale === 'linear' ? [0, 0.25, 0.5, 0.75, 1] : [0, 0.02, 0.1, 0.3, 0.6, 1];
		return fractions.map((f) => max * f);
	});

	function niceCeiling(v) {
		if (!(v > 0)) return 1;
		const mag = Math.pow(10, Math.floor(Math.log10(v)));
		return Math.ceil(v / mag) * mag;
	}

	const formatTick = (n) => {
		if (isPercent) return `${Math.round(n * 10) / 10}%`;
		return n >= 1000 ? `${Math.round(n / 100) / 10}K` : String(Math.round(n));
	};

	const description = $derived(
		`${scenarioLabel(scenario)}, ${CHART_EFFECTS.find((e) => e.value === effect)?.label.toLowerCase()}. ` +
			`Bars show the potential number of jobs lost${isPercent ? ' as a share of all jobs' : ''}; ` +
			'the coloured box shows the potential number of jobs lost as a share of all jobs.'
	);

	onMount(async () => {
		try {
			const [cma, province, b] = await Promise.all(
				['rollup_cma', 'rollup_province', 'rollup_breaks'].map((f) => fetch(`${base}/data/scenarios/${f}.json`).then((r) => r.json()))
			);
			data = { cma, province };
			breaks = b;
		} catch (err) {
			loadError = `Couldn't load chart data (${err.message}).`;
		}
	});
</script>

<RankedBarChart
	{rows}
	{ticks}
	{scale}
	{formatTick}
	formatBox={(n) => `${n.toFixed(1)}%`}
	{boxBreaks}
	colours={GRADUATED_COLOURS}
	formatBoxBreak={(b) => `${b}%`}
	{description}
	note="Note: Differences in the five scenarios and geographic scale (CMA vs. province) mean that data displays differ by orders of magnitude. Please pay attention to the scale when comparing."
	error={loadError}
	ariaLabel="Ranked bar chart of job losses"
>
	{#snippet controls()}
		<label class="control-label" for="scenario-rank-select">Select a tariff scenario:</label>
		<select id="scenario-rank-select" bind:value={scenario}>
			{#each SCENARIOS as s (s.code)}
				<option value={s.code}>{s.label}</option>
			{/each}
		</select>
		<p class="control-note">{@html SCENARIOS.find((s) => s.code === scenario)?.description}</p>

		<p class="control-label">Select a geographic level:</p>
		<ToggleGroup label="Geographic level" options={LEVELS} bind:value={level} />

		<p class="control-label">Select the economic impact indicator:</p>
		<ToggleGroup label="Effects" options={CHART_EFFECTS} bind:value={effect} />
		<p class="control-note">{CHART_EFFECTS.find((e) => e.value === effect)?.text}</p>

		<p class="control-label">Choose how to rank this indicator:</p>
		<ToggleGroup label="Rank by" options={RANK_BY} bind:value={rankBy} />

		<p class="control-label">Choose the scale you want to use:</p>
		<ToggleGroup label="Scale" options={SCALES} bind:value={scale} />
	{/snippet}
</RankedBarChart>
