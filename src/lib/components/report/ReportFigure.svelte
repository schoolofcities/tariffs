<!--
	Renders report figure `n` with the chart component for its type (see figures.js),
	using the data rows generated from the report's chart CSVs.
-->
<script>
	import ChartFrame from './ChartFrame.svelte';
	import RankedBars from './RankedBars.svelte';
	import StackedShares from './StackedShares.svelte';
	import RegionalStacks from './RegionalStacks.svelte';
	import ExportsTimeline from './ExportsTimeline.svelte';
	import IndustryHeatmap from './IndustryHeatmap.svelte';
	import { FIGURES } from './figures.js';
	import { RANKED } from './theme.js';

	let { n, rows, caption = '' } = $props();

	const spec = $derived(FIGURES[n]);
	const fmt2 = (v) => v.toFixed(2);
	const fmtInt = (v) => Math.round(v).toLocaleString('en-CA');

	// job-loss tables carry a "Canada" row: used as the reference line, not a bar
	const regions = $derived(rows.filter((r) => r.region !== 'Canada'));
	const canada = $derived(rows.find((r) => r.region === 'Canada'));
</script>

{#if spec}
	<ChartFrame title={caption}>
		{#snippet chart(width)}
			{#if spec.type === 'ranked'}
				<RankedBars {width} contextColour={RANKED.per1000} format={fmt2}
					rows={regions.map((r) => ({ label: r.region, value: r.jobs_lost_per_1000_pop }))}
					ref={canada ? { value: canada.jobs_lost_per_1000_pop, label: 'Canada' } : null} />
			{:else if spec.type === 'paired'}
				{@const side = width >= 640}
				{@const pw = side ? (width - 24) / 2 : width}
				<div class="paired" class:side>
					<RankedBars width={pw} contextColour={RANKED.total} format={fmtInt} heading="Total jobs lost" refSpace={!!canada}
						rows={regions.map((r) => ({ label: r.region, value: r.jobs_lost }))} />
					<RankedBars width={pw} contextColour={RANKED.per1000} format={fmt2} heading="Jobs lost per 1,000 residents"
						rows={regions.filter((r) => Number.isFinite(r.jobs_lost_per_1000_pop)).map((r) => ({ label: r.region, value: r.jobs_lost_per_1000_pop }))}
						ref={canada ? { value: canada.jobs_lost_per_1000_pop, label: 'Canada' } : null} />
				</div>
			{:else if spec.type === 'stacked'}
				<StackedShares {width}
					rows={rows.map((r) => ({ label: r.region, direct: r.pct_direct, indirect: r.pct_indirect, induced: r.pct_induced }))} />
			{:else if spec.type === 'grouped'}
				<RegionalStacks {width}
					rows={rows.map((r) => ({ label: r.region, direct: r.share_of_canada_direct_pct, indirect: r.share_of_canada_indirect_pct, induced: r.share_of_canada_induced_pct }))} />
			{:else if spec.type === 'timeline'}
				<ExportsTimeline {width} {rows} />
			{:else if spec.type === 'industry'}
				<IndustryHeatmap {rows} />
			{/if}
		{/snippet}
	</ChartFrame>
{/if}

<style>
	.paired {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.paired.side {
		flex-direction: row;
		gap: 24px;
	}
</style>
