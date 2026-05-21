<script>
	export let data = [];
	export let mode = 'share';

	$: isShareMode = mode === 'share';
	$: chartRows = data.filter((item) => {
		if (!Number.isFinite(item.visitChange)) return false;
		if (isShareMode) return Number.isFinite(item.dominantShare);
		return Number.isFinite(item.totalJobs);
	});

	const colorSequence = [
		'rgb(127, 60, 141)',
		'rgb(17, 165, 121)',
		'rgb(57, 105, 172)',
		'rgb(242, 183, 1)',
		'rgb(231, 63, 116)',
		'rgb(128, 186, 90)',
		'rgb(230, 131, 16)',
		'rgb(0, 134, 149)',
		'rgb(207, 28, 144)',
		'rgb(225, 157, 168)'
	];

	let chartWidth = 0;
	const margin = { top: 46, right: 30, bottom: 64, left: 70 };
	let selectedPoint = null;
	let selectedIndustry = "all";

	$: chartHeight = Math.max(420, Math.round(chartWidth * 0.65));
	$: innerWidth = Math.max(1, chartWidth - margin.left - margin.right);
	$: innerHeight = Math.max(1, chartHeight - margin.top - margin.bottom);

	$: industries = [...new Set(chartRows.map((item) => item.dominantIndustry))].sort();
	$: colorMap = new Map(
		industries.map((industry, index) => [industry, colorSequence[index % colorSequence.length]])
	);
	$: filteredRows = selectedIndustry === "all"
		? chartRows
		: chartRows.filter((item) => item.dominantIndustry === selectedIndustry);

	$: xValues = filteredRows.map((item) => item.visitChange);
	$: yValues = filteredRows.map((item) => (isShareMode ? item.dominantShare : item.totalJobs));
	$: xMin = -100;
	$: xMax = 40;

	$: rawYMax = yValues.length ? Math.max(...yValues) : (isShareMode ? 0.15 : 100000);
	$: yMaxPercent = isShareMode ? Math.max(10, Math.ceil((rawYMax * 100) / 5) * 5) : 0;
	$: yMax = isShareMode ? yMaxPercent / 100 : 1_000_000;

	$: xScale = (value) => margin.left + ((value - xMin) / (xMax - xMin)) * innerWidth;
	$: yScale = (value) => margin.top + (1 - value / yMax) * innerHeight;

	function niceStep(range, tickCount = 5) {
		if (range <= 0) return 1;
		const rough = range / (tickCount - 1);
		const pow10 = 10 ** Math.floor(Math.log10(rough));
		const frac = rough / pow10;
		let niceFrac = 1;
		if (frac <= 1) niceFrac = 1;
		else if (frac <= 2) niceFrac = 2;
		else if (frac <= 5) niceFrac = 5;
		else niceFrac = 10;
		return niceFrac * pow10;
	}

	$: xTicks = [-100, -80, -60, -40, -20, 0, 20, 40];

	$: yTicks = (() => {
		if (isShareMode) {
			const step = yMaxPercent <= 20 ? 5 : 10;
			return Array.from(
				{ length: Math.floor(yMaxPercent / step) + 1 },
				(_, i) => (i * step) / 100
			);
		}
		return [0, 200_000, 400_000, 600_000, 800_000, 1_000_000];
	})();

	function linearRegression(xs, ys) {
		const n = xs.length;
		if (n < 2) return { slope: 0, intercept: 0 };
		const meanX = xs.reduce((sum, v) => sum + v, 0) / n;
		const meanY = ys.reduce((sum, v) => sum + v, 0) / n;
		let num = 0;
		let den = 0;
		for (let i = 0; i < n; i += 1) {
			const dx = xs[i] - meanX;
			num += dx * (ys[i] - meanY);
			den += dx * dx;
		}
		if (den < 1e-6) {
			return { slope: 0, intercept: meanY };
		}
		const slope = num / den;
		const intercept = meanY - slope * meanX;
		return { slope, intercept };
	}

	function lineToBounds(slope, intercept, bounds) {
		const { xMin: bxMin, xMax: bxMax, yMin: byMin, yMax: byMax } = bounds;
		const points = [];
		const yAtXMin = slope * bxMin + intercept;
		const yAtXMax = slope * bxMax + intercept;
		if (yAtXMin >= byMin && yAtXMin <= byMax) points.push({ x: bxMin, y: yAtXMin });
		if (yAtXMax >= byMin && yAtXMax <= byMax) points.push({ x: bxMax, y: yAtXMax });
		if (slope !== 0) {
			const xAtYMin = (byMin - intercept) / slope;
			const xAtYMax = (byMax - intercept) / slope;
			if (xAtYMin >= bxMin && xAtYMin <= bxMax) points.push({ x: xAtYMin, y: byMin });
			if (xAtYMax >= bxMin && xAtYMax <= bxMax) points.push({ x: xAtYMax, y: byMax });
		}
		if (points.length < 2) {
			return [
				{ x: bxMin, y: Math.max(byMin, Math.min(byMax, yAtXMin)) },
				{ x: bxMax, y: Math.max(byMin, Math.min(byMax, yAtXMax)) }
			];
		}
		return [points[0], points[1]];
	}

	$: trend = linearRegression(xValues, yValues);
	$: trendLine = lineToBounds(trend.slope, trend.intercept, {
		xMin,
		xMax,
		yMin: 0,
		yMax: yMax
	});

	function formatJobs(value) {
		if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
		if (value >= 1_000) return `${Math.round(value / 1_000)}k`;
		return `${Math.round(value)}`;
	}

	function tooltipX(value) {
		const base = xScale(value);
		const offset = base > chartWidth - 220 ? -200 : 12;
		return base + offset;
	}

	function tooltipY(value) {
		const base = yScale(value);
		const offset = base < 40 ? 6 : -70;
		return base + offset;
	}
</script>

<div class="correlation-panel">
	<div class="intro">
		<h3>{isShareMode ? 'Canadian visit change vs. dominant-industry job share' : 'Canadian visit change vs. total jobs by dominant industry'}</h3>
		<p>
			Each point is a metro. Color shows the dominant NAICS sector by 2023 jobs.
			The dotted line shows the overall trendline, and the vertical reference is 0% visit change.
		</p>
	</div>

	<div>
		<label class="filter-label" for="industry-filter">Filter by dominant industry:</label>
		<select id="industry-filter" bind:value={selectedIndustry}>
			<option value="all">All industries</option>
			{#each industries as industry}
				<option value={industry}>{industry}</option>
			{/each}
		</select>
	</div>

	<div class="chart-shell" bind:offsetWidth={chartWidth}>
	
		{#if chartRows.length === 0}
			<div class="loading-note">No visit/jobs sample available for this view.</div>
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
						{`${tick.toFixed(0)}%`}
					</text>
				{/each}

				{#each yTicks as tick}
					<line
						x1={margin.left}
						y1={yScale(tick)}
						x2={margin.left + innerWidth}
						y2={yScale(tick)}
						class="grid"
					/>
					<text
						x={margin.left - 10}
						y={yScale(tick) + 4}
						text-anchor="end"
						class="axis-label"
					>
						{isShareMode ? `${Math.round(tick * 100)}%` : formatJobs(tick)}
					</text>
				{/each}

				<line
					x1={xScale(0)}
					y1={margin.top}
					x2={xScale(0)}
					y2={margin.top + innerHeight}
					class="zero-line"
				/>

				<line
					x1={xScale(trendLine[0].x)}
					y1={yScale(trendLine[0].y)}
					x2={xScale(trendLine[1].x)}
					y2={yScale(trendLine[1].y)}
					class="trend-line"
				/>

				{#each filteredRows as row}
					<circle
						cx={xScale(row.visitChange)}
						cy={yScale(isShareMode ? row.dominantShare : row.totalJobs)}
						r="5"
						fill={colorMap.get(row.dominantIndustry) || '#999'}
						stroke="#000000"
						stroke-width="0.8"
						on:mouseenter={() => (selectedPoint = row)}
						on:mouseleave={() => (selectedPoint = null)}
					/>
				{/each}

				{#if selectedPoint}
					<foreignObject
						x={tooltipX(selectedPoint.visitChange)}
						y={tooltipY(isShareMode ? selectedPoint.dominantShare : selectedPoint.totalJobs)}
						width="220"
						height="120"
					>
						<div class="tooltip">
							<div class="tooltip-title">{selectedPoint.metro}</div>
							<div>Dominant industry: {selectedPoint.dominantIndustry}</div>
							{#if isShareMode}
								<div>Visit change: {selectedPoint.visitChange.toFixed(1)}%</div>
								<div>Job share: {(selectedPoint.dominantShare * 100).toFixed(1)}%</div>
							{:else}
								<div>Visit change: {selectedPoint.visitChange.toFixed(1)}%</div>
								<div>Total jobs: {formatJobs(selectedPoint.totalJobs)}</div>
							{/if}
						</div>
					</foreignObject>
				{/if}

				<text
					x={margin.left + innerWidth / 2}
					y={chartHeight - 8}
					text-anchor="middle"
					class="axis-title"
				>
					Canada to US Visits YoY % Change
				</text>
				<text
					x={margin.left + 40}
					y={margin.top - 18}
					text-anchor="middle"
					class="axis-title"
				>
					{isShareMode ? 'Dominant-industry' : 'Total jobs'}
				</text>
				<text
					x={margin.left + 40}
					y={margin.top}
					text-anchor="middle"
					class="axis-title"
				>
					{isShareMode ? 'share of jobs' : '(2023)'}
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
		max-width: 900px;
		margin: 0 auto;
		position: relative;
	}

	.chart {
		width: 100%;
		margin: 0 auto;
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

	.trend-line {
		stroke: rgba(30, 55, 101, 0.6);
		stroke-width: 1.5;
		stroke-dasharray: 5 4;
	}

	.axis-label {
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
		overflow: auto;
	}

	.tooltip-title {
		font-family: OpenSansBold, sans-serif;
		margin-bottom: 4px;
	}

	.intro p {
		margin-bottom: 0;
	}

	.filter-label {
		font-family: OpenSansBold, sans-serif;
		font-size: 14px;
		color: var(--brandGray90);
		margin-right: 8px;
	}

	#industry-filter {
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		padding: 4px 8px;
		border-radius: 5px;
		border: 1px solid rgba(30, 55, 101, 0.25);
		background-color: white;
	}

</style>
