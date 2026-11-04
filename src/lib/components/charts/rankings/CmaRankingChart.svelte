<!--
	City (CMA) rankings by potential direct exposure: data + controls for
	RankedBarChart. Bars = counts (sorted by the selected metric), box = percent.
-->
<script>
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import RankedBarChart from '../RankedBarChart.svelte';
	import ToggleGroup from '$lib/components/maps/ToggleGroup.svelte';
	import { TARIFFS, INDICATORS, GRADUATED_COLOURS } from '$lib/components/maps/exposure/config.js';
	import { SCALES, BREAKS_PCT, AXIS_LINEAR, AXIS_POWER } from './config.js';

	const RANK_BY = [
		{ value: 'percent', label: 'Percent' },
		{ value: 'count', label: 'Total' }
	];

	let tariff = $state('ScenAfter');
	let indicator = $state('home');
	let rankBy = $state('count');
	let scale = $state('linear');

	let data = $state.raw([]);
	let loadError = $state('');

	const t = $derived(TARIFFS.find((x) => x.code === tariff) ?? TARIFFS[0]);
	const ind = $derived(INDICATORS.find((x) => x.value === indicator) ?? INDICATORS[0]);
	const keyPct = $derived(t.code + ind.percent);
	const keyCount = $derived(t.code + ind.count);

	const rows = $derived.by(() => {
		const sortKey = rankBy === 'percent' ? keyPct : keyCount;
		return data
			.filter((r) => r[sortKey] != null)
			.sort((a, b) => b[sortKey] - a[sortKey])
			.map((r) => ({ id: r.CMADGUID, label: r.GEO_NAME, bar: r[keyCount], box: r[keyPct] }));
	});

	const ticks = $derived([0, ...((scale === 'linear' ? AXIS_LINEAR : AXIS_POWER)[keyCount] ?? [])]);

	onMount(async () => {
		try {
			const [pcts, counts] = await Promise.all(
				['cma_percents', 'cma_counts'].map((f) => fetch(`${base}/data/exposure/${f}.json`).then((r) => r.json()))
			);
			const isCma = (r) => r.GEO_LEVEL === 'Census metropolitan area';
			// counts file: keep only the count columns so they don't overwrite the percent row
			const countCols = (r) => Object.fromEntries(Object.entries(r).filter(([k]) => /_(B|E|C)$/.test(k)));
			const countsById = new Map(counts.filter(isCma).map((r) => [r.CMADGUID, countCols(r)]));
			data = pcts.filter((r) => isCma(r) && countsById.has(r.CMADGUID)).map((r) => ({ ...r, ...countsById.get(r.CMADGUID) }));
		} catch (err) {
			loadError = `Couldn't load chart data (${err.message}).`;
		}
	});
</script>

<RankedBarChart
	{rows}
	{ticks}
	{scale}
	formatTick={(n) => (n >= 1000 ? `${n / 1000}K` : String(n))}
	formatBox={(n) => `${n.toFixed(1)}%`}
	boxBreaks={BREAKS_PCT[keyPct] ?? []}
	colours={GRADUATED_COLOURS}
	formatBoxBreak={(b) => `${b}%`}
	description={`Estimated % and number of ${ind.who} directly exposed to ${t.subject}`}
	note="Note: Due to the methods used to match tariffed goods to industry codes, selections are not additive. Pay attention to the scale when interpreting the chart."
	error={loadError}
	ariaLabel="Ranked bar chart of metropolitan areas"
>
	{#snippet controls()}
		<label class="control-label" for="cma-tariff">Select the good/product subject to U.S. tariffs:</label>
		<select id="cma-tariff" bind:value={tariff}>
			{#each TARIFFS as option (option.code)}
				<option value={option.code}>{option.label}</option>
			{/each}
		</select>

		<p class="control-label">Select an indicator:</p>
		<ToggleGroup label="Indicator" options={INDICATORS} bind:value={indicator} />

		<p class="control-label">Choose how to rank this indicator:</p>
		<ToggleGroup label="Rank by" options={RANK_BY} bind:value={rankBy} />

		<p class="control-label">Choose the scale you want to use:</p>
		<ToggleGroup label="Scale" options={SCALES} bind:value={scale} />
	{/snippet}
</RankedBarChart>
