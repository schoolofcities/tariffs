<!--
	Ranked horizontal bar chart (presentational). Used by the exposure city
	rankings and the job impact scenario rankings.

	Each row: { id, label, bar, box }
	  bar  -> bar length (on a linear or power-0.2 scale over `ticks`)
	  box  -> value in the coloured box on the left, classed by `boxBreaks`
	Rows are drawn in the order given (sort them in the wrapper).

	Hovering (or tapping) a row shows a tooltip with the exact values: the area's name,
	`barName`: formatBar(bar) and `boxName`: formatBox(box).

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
		/** bar value for the hover tooltip: nearest 10 (values under 10 as is, so small
		    counts don't show as 0) */
		formatBar = (n) => (n >= 10 ? Math.round(n / 10) * 10 : Math.round(n)).toLocaleString('en-CA'),
		/** short names for the bar and box values in the tooltip, e.g. 'Total', 'Percent' */
		barName = '',
		boxName = '',
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
	/** hovered row + pointer position within the chart, for the tooltip */
	let hover = $state(null);
	let legendWidth = $state(0);

	const P = { axisTop: 34, axisStart: 60, barTop: 52, barGap: 24, endGap: 60, boxW: 50, boxH: 16, barW: 16 };
	const chartHeight = $derived(P.barGap * rows.length + 40);

	const xScale = $derived.by(() => {
		const range = [0, Math.max(0, chartWidth - P.axisStart - P.endGap)];
		const domain = [0, ticks.at(-1) || 1];
		return scale === 'linear' ? scaleLinear().domain(domain).range(range) : scalePow().exponent(0.2).domain(domain).range(range);
	});

	function track(e, row) {
		const box = e.currentTarget.ownerSVGElement.getBoundingClientRect();
		const x = e.clientX - box.left;
		const y = e.clientY - box.top;
		// open left near the right edge, and upwards near the bottom (the wrapper scrolls, so it would clip)
		hover = { row, x, y, flip: x > chartWidth * 0.6, up: y > chartHeight - 70 };
	}

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
			<svg height={chartHeight} width={chartWidth} role="img" aria-label={ariaLabel} onpointerleave={() => (hover = null)}>
				{#each ticks as g}
					<line class="grid" x1={P.axisStart + xScale(g)} y1={P.axisTop} x2={P.axisStart + xScale(g)} y2={chartHeight} />
					<text class="axis-label" x={P.axisStart + xScale(g)} y={P.axisTop - 4} text-anchor="middle">{formatTick(g)}</text>
				{/each}

				{#each rows as row, i (row.id)}
					{@const y = P.barTop + i * P.barGap}
					{@const fill = boxColour(row.box ?? 0)}
					<line class="bar" class:hovered={hover?.row.id === row.id} x1={P.axisStart + 1} y1={y} x2={P.axisStart + 1 + xScale(Math.max(0, row.bar ?? 0))} y2={y} stroke-width={P.barW} />
					<rect x="0" y={y - P.boxH / 2} width={P.boxW} height={P.boxH} {fill} stroke={fill} />
					<text class="box-label" x={P.boxW / 2} y={y + 4} text-anchor="middle">{formatBox(row.box ?? 0)}</text>
					<text class="bar-label" x={P.axisStart + 5} y={y + 5}>{row.label}</text>
					<!-- invisible hover area: the whole row -->
					<rect
						class="hit"
						x="0"
						y={y - P.barGap / 2}
						width={chartWidth}
						height={P.barGap}
						role="presentation"
						onpointermove={(e) => track(e, row)}
						onpointerdown={(e) => track(e, row)}
					/>
				{/each}
			</svg>
			{#if hover}
				<div class="tooltip" class:flip={hover.flip} class:up={hover.up} style="left: {hover.x}px; top: {hover.y}px;">
					<span class="tooltip-name">{hover.row.label}</span>
					<span>{barName ? `${barName}: ` : ''}<strong>{formatBar(hover.row.bar ?? 0)}</strong></span>
					{#if boxName}<span>{boxName}: <strong>{formatBox(hover.row.box ?? 0)}</strong></span>{/if}
				</div>
			{/if}
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
		position: relative; /* the tooltip is placed within it */
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

	.bar.hovered {
		stroke: var(--brandGray50);
	}

	.hit {
		fill: transparent;
		cursor: default;
	}

	/* hover tooltip: same look as the map tooltips; to the left of the pointer near the right edge */
	.tooltip {
		position: absolute;
		z-index: 3;
		pointer-events: none;
		transform: translate(12px, 12px);
		display: flex;
		flex-direction: column;
		gap: 1px;
		max-width: 240px;
		padding: 4px 8px;
		background-color: var(--brandGray80);
		color: var(--brandWhite);
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		line-height: 1.35;
		width: max-content; /* as wide as the text, up to max-width, then wraps */
	}

	.tooltip.flip {
		transform: translate(calc(-100% - 12px), 12px);
	}

	.tooltip.up {
		transform: translate(12px, calc(-100% - 12px));
	}

	.tooltip.flip.up {
		transform: translate(calc(-100% - 12px), calc(-100% - 12px));
	}

	/* area name underlined, values bold */
	.tooltip-name {
		margin-bottom: 3px;
		text-decoration: underline;
		text-underline-offset: 2px;
	}

	.tooltip strong {
		font-family: OpenSansBold, sans-serif;
		font-weight: normal;
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
