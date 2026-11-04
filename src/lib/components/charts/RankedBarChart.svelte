<!--
	Ranked horizontal bar chart (presentational). Used by the exposure city
	rankings and the job-loss scenario rankings.

	Each row: { id, label, bar, box }
	  bar  -> bar length (on a linear or power-0.2 scale over `ticks`)
	  box  -> value in the coloured box on the left, classed by `boxBreaks`
	Rows are drawn in the order given (sort them in the wrapper).

	Wrappers pass their controls as the `controls` snippet; the shared control
	styles below (.control-label, select) apply to it.
-->
<script>
	import { scaleLinear, scalePow } from 'd3';

	let {
		controls,
		rows = [],
		/** gridline values; the last one is the axis maximum */
		ticks = [0],
		scale = 'linear',
		formatTick = (n) => String(n),
		formatBox = (n) => String(n),
		/** 4 class breaks for the box colour (box <= break[i] -> colours[i]) */
		boxBreaks = [],
		colours,
		formatBoxBreak = (b) => String(b),
		/** text above the legend */
		description = '',
		note = '',
		error = '',
		ariaLabel = 'Ranked bar chart'
	} = $props();

	let chartWidth = $state(0);
	let legendWidth = $state(0);

	const P = { axisTop: 34, axisStart: 60, barTop: 52, barGap: 24, endGap: 60, boxW: 50, boxH: 16, barW: 16 };
	const chartHeight = $derived(P.barGap * rows.length + 40);

	const xScale = $derived.by(() => {
		const range = [0, Math.max(0, chartWidth - P.axisStart - P.endGap)];
		const domain = [0, ticks.at(-1) || 1];
		return scale === 'linear' ? scaleLinear().domain(domain).range(range) : scalePow().exponent(0.2).domain(domain).range(range);
	});

	function boxColour(v) {
		if (!boxBreaks.length) return colours[0];
		for (let i = 0; i < boxBreaks.length; i++) if (v <= boxBreaks[i]) return colours[i];
		return colours[boxBreaks.length] ?? colours.at(-1);
	}
</script>

<div class="ranked-chart">
	{#if controls}{@render controls()}{/if}

	<div class="legend">
		<p class="control-label">{description}</p>
		<div bind:offsetWidth={legendWidth}>
			{#if legendWidth && boxBreaks.length}
				{@const w = legendWidth / 7.1}
				<svg width="100%" height="28" role="img" aria-label="Legend">
					{#each colours as colour, i}
						<rect x={i * w} y="0" width={w} height="12" fill={colour} stroke="white" />
					{/each}
					{#each boxBreaks as b, i}
						<text x={(i + 1) * w} y="26" text-anchor="middle">{formatBoxBreak(b)}</text>
					{/each}
				</svg>
			{/if}
		</div>
	</div>

	{#if error}
		<p class="error">{error}</p>
	{/if}

	<div class="chart-wrapper" bind:offsetWidth={chartWidth}>
		{#if chartWidth && rows.length}
			<svg height={chartHeight} width={chartWidth} role="img" aria-label={ariaLabel}>
				{#each ticks as g}
					<line class="grid" x1={P.axisStart + xScale(g)} y1={P.axisTop} x2={P.axisStart + xScale(g)} y2={chartHeight} />
					<text class="axis-label" x={P.axisStart + xScale(g)} y={P.axisTop - 4} text-anchor="middle">{formatTick(g)}</text>
				{/each}

				{#each rows as row, i (row.id)}
					{@const y = P.barTop + i * P.barGap}
					{@const fill = boxColour(row.box ?? 0)}
					<line class="bar" x1={P.axisStart + 1} y1={y} x2={P.axisStart + 1 + xScale(Math.max(0, row.bar ?? 0))} y2={y} stroke-width={P.barW} />
					<rect x="0" y={y - P.boxH / 2} width={P.boxW} height={P.boxH} {fill} stroke={fill} />
					<text class="box-label" x={P.boxW / 2} y={y + 4} text-anchor="middle">{formatBox(row.box ?? 0)}</text>
					<text class="bar-label" x={P.axisStart + 5} y={y + 5}>{row.label}</text>
				{/each}
			</svg>
		{/if}
		{#if note}<p class="note">{note}</p>{/if}
	</div>
</div>

<style>
	.ranked-chart > :global(.control-label:first-child) {
		margin-top: 0;
	}

	.ranked-chart :global(.control-label) {
		display: block;
		margin: 16px 0 8px;
		padding: 0;
		font-family: SourceSerif, serif;
		font-size: 16px;
		line-height: 22px;
		color: var(--brandGray90);
	}

	.ranked-chart :global(select) {
		width: 100%;
		padding: 8px 10px;
		border: 1px solid var(--brandGray);
		border-radius: 5px;
		background: var(--brandWhite);
		font-family: TradeGothicBold, sans-serif;
		font-size: 16px;
		color: var(--brandGray90);
		cursor: pointer;
	}

	.ranked-chart :global(select:hover),
	.ranked-chart :global(select:focus) {
		border-color: var(--brandMedBlue);
	}

	.ranked-chart :global(.control-note) {
		margin: 8px 0 0;
		padding: 4px 10px;
		border-left: 3px solid var(--brandLightBlue);
		background-color: #f7f9fb;
		font-size: 13px;
		line-height: 18px;
	}

	.legend {
		margin-top: 20px;
		padding-top: 5px;
		border-top: 1px solid var(--brandGray);
	}

	.legend text {
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		fill: var(--brandBlack);
	}

	.chart-wrapper {
		width: 100%;
		min-width: 250px;
		overflow-x: auto;
	}

	.chart-wrapper svg {
		display: block;
		margin: 10px 0;
	}

	.grid {
		stroke: var(--brandGray);
		stroke-width: 0.5px;
	}

	.axis-label {
		fill: var(--brandBlack);
		font-size: 12px;
		font-family: OpenSans, sans-serif;
	}

	.bar {
		stroke: var(--brandGray);
	}

	.box-label {
		fill: white;
		font-size: 12px;
		font-family: OpenSansBold, sans-serif;
	}

	.bar-label {
		fill: var(--brandGray70);
		font-size: 14px;
		font-family: OpenSans, sans-serif;
	}

	.note {
		font-size: 16px;
		line-height: 22px;
	}

	.error {
		color: var(--brandRed);
	}
</style>
