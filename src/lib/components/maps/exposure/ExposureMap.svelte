<!--
	Direct-exposure map: controls + notes for MapPage.

	Selection state is one object (tariff, indicator, metric, geo), mirrored to
	the URL so any view can be shared, e.g.
	/exposure/map?tariff=Steel&indicator=work&metric=count&geo=CSD
-->
<script>
	import MapPage from '../MapPage.svelte';
	import ToggleGroup from '../ToggleGroup.svelte';
	import { GEO_OPTIONS } from '$lib/maps/geographies.js';
	import { syncUrlState } from '$lib/utils/urlState.svelte.js';
	import {
		DEFAULTS, GEOGRAPHIES, INDICATORS, METRICS, TARIFFS, TARIFFS_AS_OF, UPDATED,
		resolveSelection, formatPercent, formatCount, formatBreak
	} from './config.js';

	let sel = $state({ ...DEFAULTS });
	syncUrlState(
		sel,
		{
			tariff: { values: TARIFFS.map((t) => t.code) },
			indicator: { values: INDICATORS.map((i) => i.value) },
			metric: { values: METRICS.map((m) => m.value) },
			geo: { values: Object.keys(GEOGRAPHIES) }
		},
		DEFAULTS
	);

	const selection = $derived(resolveSelection(sel));
	const format = (v) => (v == null ? 'No data' : sel.metric === 'percent' ? formatPercent(v) : formatCount(v));
</script>

<MapPage
	title="Mapping potential direct exposure of U.S. tariffs in Canada"
	geographies={GEOGRAPHIES}
	view={selection.view}
	{format}
	description={selection.description + (sel.metric === 'count' ? ` (as of ${TARIFFS_AS_OF})` : '')}
	formatBreak={formatBreak(sel.metric)}
>
	{#snippet byline()}
		<p>
			By <a href="https://mkbs-mkbs2000.github.io/Personal-Portfolio/" target="_blank" rel="noopener">Muhammad Khalis Bin Samion</a>,
			<a href="https://jamaps.github.io/" target="_blank" rel="noopener">Jeff Allen</a>,
			<a href="https://www.linkedin.com/in/yihoi-jung-0b95351b5/" target="_blank" rel="noopener">Yihoi Jung</a>,
			<a href="https://discover.research.utoronto.ca/8035-tara-vinodrai" target="_blank" rel="noopener">Tara Vinodrai</a>, and <a href="https://schoolofcities.utoronto.ca/people/karen-chapple/" target="_blank" rel="noopener">Karen Chapple</a>.<br />
			<i>First published October 2025. Updated {UPDATED}.</i>
		</p>
	{/snippet}

	{#snippet controls()}
		<label class="control-label" for="tariff-select">Select the good/product subject to U.S. tariffs:</label>
		<select id="tariff-select" bind:value={sel.tariff}>
			{#each TARIFFS as t (t.code)}
				<option value={t.code}>{t.label}</option>
			{/each}
		</select>
		{#if selection.tariff.note}
			<p class="control-note">{selection.tariff.note}</p>
		{/if}

		<p class="control-label">Select an indicator:</p>
		<ToggleGroup label="Indicator" options={INDICATORS} bind:value={sel.indicator} />

		<p class="control-label">Choose how to display this indicator:</p>
		<ToggleGroup label="Display" options={METRICS} bind:value={sel.metric} />

		<p class="control-label">Choose geographic unit:</p>
		<ToggleGroup label="Geographic unit" options={GEO_OPTIONS} bind:value={sel.geo} />
	{/snippet}

	{#snippet notes()}
		<p>
			Note: Due to the methods used to match tariffed goods to industry codes, selections are not additive. Pay
			attention to the scale when interpreting maps.
		</p>
		<h2>Data sources</h2>
		<p>All layers on this map are based on tariffs as of {TARIFFS_AS_OF}.</p>
		<p>Layers on this map were created by combining data from the following sources:</p>
		<ul>
			<li>Canadian Business Registry (Statistics Canada)</li>
			<li>Canadian Chamber of Commerce</li>
			<li>Canadian Census of Population (Statistics Canada)</li>
			<li>Canadian International Merchandise Trade Web Application (Statistics Canada Catalogue No. 71-607-X2021004)</li>
			<li>Cargo Systems Messaging Service (United States Customs and Border Protection)</li>
			<li>Harmonized Tariff Schedule of the United States (United States International Trade Commission)</li>
			<li>International Trade and Development Division (Statistics Canada)</li>
			<li>U.S. Department of Commerce</li>
			<li>U.S. Census Bureau</li>
		</ul>
		<p>
			For detailed data descriptions, download links, and processing steps, please read our
			<a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file" target="_blank" rel="noopener">data and methodology page</a>.
		</p>
	{/snippet}
</MapPage>
