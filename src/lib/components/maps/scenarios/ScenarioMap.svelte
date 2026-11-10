<!--
	Job impact scenarios map: controls + notes for MapPage.
	Values per selection are computed by `derive` in ./config.js.
-->
<script>
	import MapPage from '../MapPage.svelte';
	import ToggleGroup from '../ToggleGroup.svelte';
	import { GEO_OPTIONS } from '$lib/maps/geographies.js';
	import { syncUrlState } from '$lib/utils/urlState.svelte.js';
	import { root } from '$lib/site/paths.js';
	import {
		DEFAULTS, EFFECTS, GEOGRAPHIES, METRICS, SCENARIOS, MAP_UPDATED,
		derive, resolveSelection, formatValue, formatBreak
	} from './config.js';

	let sel = $state({ ...DEFAULTS, effects: [...DEFAULTS.effects] });
	syncUrlState(
		sel,
		{
			scenario: { values: SCENARIOS.map((s) => s.code) },
			effects: { values: EFFECTS.map((e) => e.value), multiple: true },
			metric: { values: METRICS.map((m) => m.value) },
			geo: { values: Object.keys(GEOGRAPHIES) }
		},
		DEFAULTS
	);

	const selection = $derived(resolveSelection(sel));
</script>

<MapPage
	title="Mapping job impact scenarios due to U.S. tariffs in Canada"
	geographies={GEOGRAPHIES}
	view={selection.view}
	{derive}
	format={formatValue(sel.metric)}
	description={selection.description}
	formatBreak={formatBreak(sel.metric)}
>
	{#snippet byline()}
		<p>
			By <a href="https://www.linkedin.com/in/yihoi-jung-0b95351b5/" target="_blank" rel="noopener">Yihoi Jung</a>,
			<a href="https://jamaps.github.io/" target="_blank" rel="noopener">Jeff Allen</a>,
			<a href="https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco" target="_blank" rel="noopener">Richard J. DiFrancesco</a>,
			<a href="https://www.linkedin.com/in/clara-turner-64764b29/" target="_blank" rel="noopener">Clara Turner</a>,
			<a href="https://discover.research.utoronto.ca/8035-tara-vinodrai" target="_blank" rel="noopener">Tara Vinodrai</a>, and <a href="https://schoolofcities.utoronto.ca/people/karen-chapple/" target="_blank" rel="noopener">Karen Chapple</a>.<br />
			<i>Last updated {MAP_UPDATED}.</i>
		</p>
	{/snippet}

	{#snippet controls()}
		<p class="summary">
			The following employment scenarios are based on output from a <strong>Multiregional Input-Output (MRIO) model</strong> of
			the Canadian economy as represented by thirteen provinces and territories. The MRIO model computes direct, indirect
			and induced effects for each tariff scenario by industry for each region of Canada; these effects are then extended to
			the local level. The scenarios are described more fully <a href="{root}/scenarios">here</a>.
		</p>

		<label class="control-label" for="scenario-select">Select a scenario:</label>
		<select id="scenario-select" bind:value={sel.scenario}>
			{#each SCENARIOS as s (s.code)}
				<option value={s.code}>{s.label}</option>
			{/each}
		</select>
		<p class="control-note">{@html selection.scenario.description}</p>

		<p class="control-label">Select effects (combine as many as you like):</p>
		<ToggleGroup label="Effects" options={EFFECTS} multiple bind:value={sel.effects} />
		<p class="control-note">
			{#each EFFECTS.filter((e) => sel.effects.includes(e.value)) as e, i (e.value)}
				{#if i > 0}<br />{/if}{e.text}
			{/each}
		</p>

		<p class="control-label">Choose how to display this indicator:</p>
		<ToggleGroup label="Display" options={METRICS} bind:value={sel.metric} />

		<p class="control-label">Choose geographic unit:</p>
		<ToggleGroup label="Geographic unit" options={GEO_OPTIONS} bind:value={sel.geo} />
	{/snippet}

	{#snippet notes()}
		<p>
			Direct effects are estimated based on counts of employment (place of work) using the Canadian Business Register
			(December 2022). Indirect and induced effects are modelled using a provincial multi-regional input-output model and
			applied to employment at the local level. Percentages are job losses as a share of total
			local employment; areas without an employment estimate are shown as no data.
		</p>
		<h2>Data sources</h2>
		<ul>
			<li>Canadian Business Registry (Statistics Canada)</li>
			<li>Canadian Chamber of Commerce</li>
			<li>Canadian Census of Population (Statistics Canada)</li>
			<li>Canadian International Merchandise Trade Web Application (Statistics Canada Catalogue No. 71-607-X2021004)</li>
			<li>Harmonized Tariff Schedule of the United States (United States International Trade Commission)</li>
			<li>Statistics Canada Input-Output Multipliers, Provincial and Territorial, Detail Level (Table 36-10-0113-01)</li>
		</ul>
	{/snippet}
</MapPage>
