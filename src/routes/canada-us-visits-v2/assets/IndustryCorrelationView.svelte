<script>
	export let correlations = [];
	export let metricLabel = 'job share';

	const minSampleSize = 4;
	$: chartRows = correlations.filter(
		(item) => Number.isFinite(item.correlation) && item.sampleSize >= minSampleSize
	);

	let chartWidth = 0;
	const margin = { top: 20, right: 24, bottom: 40, left: 180 };
	const barHeight = 22;
	const barGap = 8;

	let selectedRow = null;

	$: sortedRows = [...chartRows].sort((a, b) => a.correlation - b.correlation);
	$: innerHeight = sortedRows.length > 0 ? sortedRows.length * (barHeight + barGap) - barGap : 0;
	$: chartHeight = Math.max(260, innerHeight + margin.top + margin.bottom);
	$: innerWidth = Math.max(1, chartWidth - margin.left - margin.right);

	$: xValues = sortedRows.map((row) => row.correlation);
	$: rawMin = xValues.length > 0 ? Math.min(...xValues) : -0.2;
	$: rawMax = xValues.length > 0 ? Math.max(...xValues) : 0.2;
	$: paddedMin = Math.min(rawMin, 0) - 0.05;
	$: paddedMax = Math.max(rawMax, 0) + 0.05;
	$: xMin = paddedMin === paddedMax ? paddedMin - 0.1 : paddedMin;
	$: xMax = paddedMin === paddedMax ? paddedMax + 0.1 : paddedMax;

	const tickCount = 5;
	$: xTicks = Array.from({ length: tickCount }, (_, i) => xMin + (i * (xMax - xMin)) / (tickCount - 1));

	$: xScale = (value) => margin.left + ((value - xMin) / (xMax - xMin)) * innerWidth;
	$: yScale = (index) => margin.top + index * (barHeight + barGap);

	const formatCorrelation = (value) => value.toFixed(2);

	function tooltipX(value) {
		const base = xScale(value);
		const offset = base > chartWidth - 220 ? -200 : 12;
		return base + offset;
	}

	function tooltipY(index) {
		const base = yScale(index);
		const offset = base < margin.top + 40 ? 6 : -70;
		return base + offset;
	}
</script>

<div class="correlation-panel">
	<div class="intro">
		<h3>Industry job correlations with Canadian visit percent change</h3>
		<p>
			Each bar shows the correlation between percent visit change and an industry's {metricLabel}. Sample size is shown in the hover.
		</p>
	</div>

	<div class="chart-shell" bind:offsetWidth={chartWidth}>
		{#if sortedRows.length === 0}
			<div class="loading-note">No dominant-industry sample available for this view.</div>
		{:else}
			<svg class="chart" width={chartWidth} height={chartHeight}>
				{#each xTicks as tick}
					<line
						x1={xScale(tick)}
						y1={margin.top}
						x2={xScale(tick)}
						y2={margin.top + innerHeight}
						class="grid"
					/>
					<text
						x={xScale(tick)}
						y={chartHeight - 20}
						text-anchor="middle"
						class="axis-label"
					>
						{formatCorrelation(tick)}
					</text>
				{/each}

				<line
					x1={xScale(0)}
					y1={margin.top}
					x2={xScale(0)}
					y2={margin.top + innerHeight}
					class="zero-line"
				/>

				{#each sortedRows as row, index}
					{#if row}
						<text
							x={xMin}
							y={yScale(index) + barHeight * 0.75}
							text-anchor="start"
							class="axis-label"
						>
							{row.industry}
						</text>

						<rect
							x={xScale(Math.min(0, row.correlation))}
							y={yScale(index)}
							width={Math.max(2, Math.abs(xScale(row.correlation) - xScale(0)))}
							height={barHeight}
							fill={row.correlation >= 0 ? '#007FA3' : '#DC4633'}
							rx="3"
							on:mouseenter={() => (selectedRow = { row, index })}
							on:mouseleave={() => (selectedRow = null)}
						/>

						<text
							x={xScale(row.correlation) + (row.correlation >= 0 ? 6 : -6)}
							y={yScale(index) + barHeight * 0.75}
							text-anchor={row.correlation >= 0 ? 'start' : 'end'}
							class="value-label"
						>
							{formatCorrelation(row.correlation)}
						</text>
					{/if}
				{/each}

				{#if selectedRow}
					<foreignObject
						x={tooltipX(selectedRow.row.correlation)}
						y={tooltipY(selectedRow.index)}
						width="190"
						height="80"
					>
						<div class="tooltip">
							<div class="tooltip-title">{selectedRow.row.industry}</div>
							<div>NAICS {selectedRow.row.code}</div>
							<div>Sample size: {selectedRow.row.sampleSize}</div>
							{#if selectedRow.row.pValue && Number.isFinite(selectedRow.row.pValue)}
								<div>p = {selectedRow.row.pValue.toFixed(4)}</div>
							{/if}
						</div>
					</foreignObject>
				{/if}

				<text
					x={margin.left + innerWidth / 2}
					y={chartHeight}
					text-anchor="middle"
					class="axis-title"
				>
					Correlation: visit decline vs. {metricLabel}
				</text>
			</svg>
		{/if}
	</div>
</div>

<style>
	.correlation-panel {
		max-width: 680px;
		margin: 0 auto;
		padding-top: 10px;
	}

	.intro {
		max-width: 680px;
		margin: 0 auto 20px auto;
	}

	.chart-shell {
		max-width: 680px;
		margin: 0 auto;
		position: relative;
	}

	.chart {
		width: 100%;
	}

	.loading-note {
		padding: 20px 0;
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: OpenSans, sans-serif;
		color: var(--brandGray90);
	}

	.grid {
		stroke: rgba(30, 55, 101, 0.12);
		stroke-width: 1;
	}

	.zero-line {
		stroke: rgba(30, 55, 101, 0.35);
		stroke-width: 1;
		stroke-dasharray: 4 3;
	}

	.axis-label {
		fill: var(--brandGray90);
		font-size: 12px;
		font-family: OpenSans, sans-serif;
	}

	.value-label {
		fill: var(--brandGray90);
		font-size: 12px;
		font-family: OpenSans, sans-serif;
	}

	.axis-title {
		fill: var(--brandGray90);
		font-size: 13px;
		font-family: OpenSansBold, sans-serif;
	}

	.tooltip {
		background: rgba(255, 255, 255, 0.95);
		border: 1px solid rgba(30, 55, 101, 0.2);
		border-radius: 6px;
		padding: 8px 10px;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray90);
	}

	.tooltip-title {
		font-family: OpenSansBold, sans-serif;
		margin-bottom: 4px;
	}

	.intro p {
		margin-bottom: 0;
	}

</style>
