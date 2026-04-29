<script>
	export let filteredTrends = [];
	export let chartHeight = 50;
	export let metroLabelWidth = 180;

	const chartWidth = 560;

	function getRegionColor(regionName) {
		const regionColors = {
			Midwest: '#6FC7EA',
			Northeast: '#8DBF2E',
			Southwest: '#F1C500',
			Southeast: '#AB1368',
			Pacific: '#00AEB3',
			Canada: '#F3603E'
		};
		return regionColors[regionName] || '#999';
	}

	function getMetroDisplayName(metroName) {
		const metroNameAliases = {
			"Louisville, KY-IN": "Louisville/Jefferson County, KY-IN"
		};
		const normalized = metroName.replace(' Micro Area', '').trim();
		const aliased = metroNameAliases[normalized] || normalized;

		const stateMatch = aliased.match(/,\s*([A-Z]{2})/);
		const state = stateMatch ? stateMatch[1] : '';

		const cityPart = aliased.split(',')[0].trim();
		const shortCity = cityPart.split(/[-/]/)[0].trim().replace(/\s+/g, ' ');

		return state ? `${shortCity}, ${state}` : shortCity;
	}
</script>

<div class="charts-scroll-container">
	<div class="charts-inner">
		<!-- Header row -->
		<div class="chart-wrapper header-row">
			<div class="left">
				<span class="header-text">Metro Area</span>
			</div>
			<div class="arrow"></div>
			<div class="number">
				<span class="header-text">% Change</span>
			</div>
			<div class="bar-container">
				<svg height="45" width="100%" viewBox="0 0 {chartWidth} 45" preserveAspectRatio="none" class="chart">
					<text x={chartWidth / 4} y="15" class="textYear">2024 / 2025</text>
					<text x={chartWidth * 3/4} y="15" class="textYear">2025 / 2026</text>

					<line x1={chartWidth / 2} y1="0" x2={chartWidth / 2} y2="45" stroke="#555555" stroke-width="2"/>

					{#each [0, 1] as yearIndex}
						{#each [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3] as month, i}
							<text
								x={yearIndex * (chartWidth / 2) + i * (chartWidth / 24) + (chartWidth / 48)}
								y="35"
								class="textLabelSmall"
								style="text-anchor: middle;"
							>{month}</text>

							{#if !(yearIndex === 0 && i === 0)}
								<line
									x1={yearIndex * (chartWidth / 2) + i * (chartWidth / 24)}
									y1="40"
									x2={yearIndex * (chartWidth / 2) + i * (chartWidth / 24)}
									y2="45"
									stroke="#555555"
									stroke-width="1"
								/>
							{/if}
						{/each}
					{/each}

					<line x1="0" y1="45" x2={chartWidth} y2="45" stroke="#555555" stroke-width="1"/>
				</svg>
			</div>
		</div>

		{#each filteredTrends as metro, i}
			{@const label = getMetroDisplayName(metro.metro)}
			<div class="chart-wrapper" style="height: 53px;">
				<div class="left">
					<svg width={metroLabelWidth} height={chartHeight} class="region-bar">
						<line x1="5" y1="15" x2="5" y2="{chartHeight - 15}" stroke={getRegionColor(metro.region)} stroke-width="3"/>
						<text x="12" y="31" class="textCity">{i + 1}. {label}</text>
					</svg>
				</div>

				<div class="arrow">
					{#if metro.percentChange >= 0}
						<span class="arrow-icon up-arrow">▲</span>
					{:else}
						<span class="arrow-icon down-arrow">▼</span>
					{/if}
				</div>

				<div class="number">
					<span class="percent-main">
						{metro.percentChangeDisplay}
					</span>
				</div>

				<div class="bar-container">
					<svg height={chartHeight} width="100%" viewBox="0 0 {chartWidth} {chartHeight}" preserveAspectRatio="none" class="chart">
						<!-- Grid lines -->
						{#each [0, 1] as yearIndex}
							{#each [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] as tick}
								<line
									x1={yearIndex * (chartWidth / 2) + (tick * chartWidth / 2 / 12)}
									y1={5}
									x2={yearIndex * (chartWidth / 2) + (tick * chartWidth / 2 / 12)}
									y2={45}
									stroke="#333333"
									stroke-opacity="0.15"
									stroke-width="1"
								/>
							{/each}
							{#if yearIndex < 1}
								<line
									x1={(yearIndex + 1) * (chartWidth / 2)}
									y1={5}
									x2={(yearIndex + 1) * (chartWidth / 2)}
									y2={45}
									stroke="#555555"
									stroke-width="2"
								/>
							{/if}
						{/each}

						<!-- Baseline (Year 1 average) -->
						{#if metro.meanLine !== null}
							<line x1="0" y1={metro.meanLine} x2={chartWidth} y2={metro.meanLine} stroke="#D0D1C9" stroke-width="1" stroke-dasharray="4"/>
						{/if}

						<!-- LOESS regression line -->
						{#if metro.regressionLine}
							<path d={metro.regressionLine} stroke="#111" stroke-width="2" fill="none"/>
							{#if metro.startCircle}
								<circle cx={metro.startCircle.cx} cy={metro.startCircle.cy} r="2" fill="#111"/>
							{/if}
							{#if metro.endCircle}
								<circle cx={metro.endCircle.cx} cy={metro.endCircle.cy} r="2" fill="#111"/>
							{/if}
						{/if}
					</svg>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.charts-scroll-container {
		overflow-x: hidden;
		overflow-y: scroll;
		margin: 0 auto;
		max-width: 880px;
		max-height: 70vh;
		overscroll-behavior: contain;
		width: 100%;
		border-right: solid 4px var(--brandGray);
		border-bottom: solid 4px var(--brandGray);
	}

	.charts-inner {
		min-width: 0;
	}

	.chart-wrapper {
		display: flex;
		margin: 0 auto;
		padding-left: 5px;
		padding-right: 5px;
		margin-bottom: 0px;
		max-width: 880px;
		height: 53px;
		background-color: var(--brandWhite);
		border-bottom: solid 1px var(--brandGray);
	}

	.chart-wrapper.header-row {
		position: sticky;
		top: 0;
		z-index: 10;
		background-color: var(--brandWhite);
		border-bottom: solid 2px var(--brandGray);
		height: auto;
		min-height: 53px;
	}

	.header-text {
		font-family: OpenSansRegular, sans-serif;
		font-size: 14px;
		font-weight: normal;
		color: var(--brandGray90);
	}

	.left {
		width: 180px;
		min-width: 180px;
		display: flex;
		align-items: center;
	}

	.textCity {
		font-family: OpenSansRegular, sans-serif;
		font-size: 14px;
		font-weight: normal;
		text-anchor: start;
		fill: var(--brandBlack);
	}

	.textYear {
		font-family: OpenSansRegular, sans-serif;
		font-size: 14px;
		font-weight: normal;
		text-anchor: middle;
		fill: var(--brandBlack);
	}

	.arrow {
		margin: auto 0;
		margin-left: 6px;
		width: 32px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.arrow-icon {
		width: 30px;
		height: 30px;
	}

	.number {
		width: 68px;
		display: flex;
		align-items: center;
		justify-content: flex-start;
		padding-left: 4px;
	}

	.percent-main {
		font-family: OpenSansBold, sans-serif;
		font-size: 14px;
		font-weight: normal;
		color: var(--brandBlack);
		font-variant-numeric: tabular-nums;
	}

	.textLabelSmall {
		font-family: OpenSansRegular, sans-serif;
		font-size: 10px;
		font-weight: normal;
		font-variant-numeric: tabular-nums;
		fill: var(--brandBlack);
	}

	.bar-container {
		flex: 1;
		min-width: 0;
		display: flex;
		align-items: center;
		overflow: hidden;
	}

	.chart {
		display: block;
		margin-left: 6px;
		min-width: 0;
	}

	.arrow-icon {
		display: inline-flex;
		font-size: 22px;
		line-height: 1;
		font-family: OpenSansBold;
	}

	.up-arrow {
		color: #007FA3;
	}

	.down-arrow {
		color: #DC4633;
	}

	@media (max-width: 600px) {
		.textYear, .textLabelSmall {
			display: none;
		}
	}
</style>
