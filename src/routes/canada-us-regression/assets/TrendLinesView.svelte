<script>
	export let filteredTrends = [];
	export let chartHeight = 50;
	export let metroLabelWidth = 180;

	let chartWidth = 360;
	const eventColor = "#007FA3";

	let showTrump = false;
	let showCad = false;
	let showCarney = false;
	let showTariffs = false;
	let showTruckTariffs = false;

	function dateToX(
		dateString,
		periodStartString,
		periodEndString,
		offset = 0,
	) {
		const start = new Date(periodStartString).getTime();
		const end = new Date(periodEndString).getTime();
		const date = new Date(dateString).getTime();
		const progress = (date - start) / (end - start);
		return offset + progress * (chartWidth / 2);
	}
	const eventMarkers = [
		{
			key: "trump",
			x: dateToX("2024-11-29", "2024-04-01", "2025-03-31", 0),
		},
		{
			key: "cad",
			x: dateToX("2024-12-18", "2024-04-01", "2025-03-31", 0),
		},
		{
			key: "carney",
			x: dateToX("2025-03-14", "2024-04-01", "2025-03-31", 0),
		},
		{
			key: "tariffs",
			x: dateToX(
				"2025-05-03",
				"2025-04-01",
				"2026-03-31",
				chartWidth / 2,
			),
		},
		{
			key: "truckTariffs",
			x: dateToX(
				"2025-11-01",
				"2025-04-01",
				"2026-03-31",
				chartWidth / 2,
			),
		},
	];

	function getRegionColor(regionName) {
		const regionColors = {
			Midwest: "#6FC7EA",
			Northeast: "#8DBF2E",
			Southwest: "#F1C500",
			Southeast: "#AB1368",
			Pacific: "#00AEB3",
			Canada: "#F3603E",
		};
		return regionColors[regionName] || "#999";
	}

	function getMetroDisplayName(metroName) {
		const metroNameAliases = {
			"Louisville, KY-IN": "Louisville/Jefferson County, KY-IN",
		};
		const normalized = metroName.replace(" Micro Area", "").trim();
		const aliased = metroNameAliases[normalized] || normalized;

		const stateMatch = aliased.match(/,\s*([A-Z]{2})/);
		const state = stateMatch ? stateMatch[1] : "";

		const cityPart = aliased.split(",")[0].trim();
		const shortCity = cityPart.split(/[-/]/)[0].trim().replace(/\s+/g, " ");

		return state ? `${shortCity}, ${state}` : shortCity;
	}
</script>

<div class="event-legend">
	<div class="event-legend-row">
		<span class="event-legend-item">
			<svg width="30" height="10"
				><line
					x1="0"
					y1="5"
					x2="30"
					y2="5"
					stroke="#1E3765"
					stroke-width="2"
				/>
				<circle 
					cx="3" 
					cy="5" 
					r="3" 
					fill="#1E3765" 
				/>
				<circle
					cx="27"
					cy="5"
					r="3"
					fill="#DC4633"
				/>
			</svg
			>
			Visitation trend (rolling average)
		</span>
		<span class="event-legend-item">
			<svg width="20" height="10"
				><line
					x1="0"
					y1="5"
					x2="20"
					y2="5"
					stroke="#1E3765"
					stroke-opacity="0.75"
					stroke-width="1"
					stroke-dasharray="4"
				/></svg
			>
			Average visitation for Apr. 2024 – Mar. 2025
		</span>
	</div>
	<div class="event-btns">
		<button
			class="event-btn"
			class:active={showTrump}
			on:click={() => (showTrump = !showTrump)}
		>
			<svg width="12" height="9"
				><line
					x1="6"
					y1="0"
					x2="6"
					y2="9"
					stroke={eventColor}
					stroke-width="2"
					stroke-dasharray="3 1"
				/></svg
			>
			Nov. 29, 2024 — Trump mentions Canada as 51st state
		</button>
		<button
			class="event-btn"
			class:active={showCad}
			on:click={() => (showCad = !showCad)}
		>
			<svg width="12" height="9"
				><line
					x1="6"
					y1="0"
					x2="6"
					y2="9"
					stroke={eventColor}
					stroke-width="2"
					stroke-dasharray="3 1"
				/></svg
			>
			Dec. 18, 2024 — CAD/USD dropped below 0.70
		</button>
		<button
			class="event-btn"
			class:active={showCarney}
			on:click={() => (showCarney = !showCarney)}
		>
			<svg width="12" height="9"
				><line
					x1="6"
					y1="0"
					x2="6"
					y2="9"
					stroke={eventColor}
					stroke-width="2"
					stroke-dasharray="3 1"
				/></svg
			>
			Mar. 14, 2025 — Mark Carney takes office
		</button>
		<button
			class="event-btn"
			class:active={showTariffs}
			on:click={() => (showTariffs = !showTariffs)}
		>
			<svg width="12" height="9"
				><line
					x1="6"
					y1="0"
					x2="6"
					y2="9"
					stroke={eventColor}
					stroke-width="2"
					stroke-dasharray="3 1"
				/></svg
			>
			May 3, 2025 — 25% auto tariffs
		</button>
		<button
			class="event-btn"
			class:active={showTruckTariffs}
			on:click={() => (showTruckTariffs = !showTruckTariffs)}
		>
			<svg width="12" height="9"
				><line
					x1="6"
					y1="0"
					x2="6"
					y2="9"
					stroke={eventColor}
					stroke-width="2"
					stroke-dasharray="3 1"
				/></svg
			>
			Nov. 1, 2025 — 25% truck tariffs
		</button>
	</div>
</div>

<div class="charts-scroll-container">
	<div class="charts-inner">
		<!-- Header row -->
		<div class="chart-wrapper header-row">
			<div class="left">
				<span class="header-text">Metro area</span>
			</div>
			<div class="arrow"></div>
			<div class="number">
				<span class="header-text header-text-percent"
					>Year-over-year<br />% change</span
				>
			</div>
			<div class="bar-container">
				<svg
					height="45"
					width={chartWidth}
					viewBox="0 0 ${chartWidth} 45"
					preserveAspectRatio="xMinYMid meet"
					class="chart"
				>
					<text x={chartWidth / 4} y="15" class="textYear"
						>2024 / 2025</text
					>
					<text x={(chartWidth * 3) / 4} y="15" class="textYear"
						>2025 / 2026</text
					>

					<line
						x1={chartWidth / 2}
						y1="0"
						x2={chartWidth / 2}
						y2="45"
						stroke="var(--brandGray50)"
						stroke-width="2"
					/>

					{#each [0, 1] as yearIndex}
						{#each [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3] as month, i}
							<text
								x={yearIndex * (chartWidth / 2) +
									i * (chartWidth / 24) +
									chartWidth / 48}
								y="35"
								class="textLabelSmall"
								style="text-anchor: middle;">{month}</text
							>
							{#if !(yearIndex === 0 && i === 0)}
								<line
									x1={yearIndex * (chartWidth / 2) +
										i * (chartWidth / 24)}
									y1="40"
									x2={yearIndex * (chartWidth / 2) +
										i * (chartWidth / 24)}
									y2="45"
									stroke="#555555"
									stroke-width="1"
								/>
							{/if}
						{/each}
					{/each}

					<line
						x1="0"
						y1="45"
						x2={chartWidth}
						y2="45"
						stroke="#555555"
						stroke-width="1"
					/>
				</svg>
			</div>
		</div>

		{#each filteredTrends as metro, i}
			{@const label = getMetroDisplayName(metro.metro)}
			<div class="chart-wrapper" style="height: 53px;">
				<div class="left">
					<svg
						width={metroLabelWidth}
						height={chartHeight}
						class="region-bar"
					>
						<line
							x1="5"
							y1="15"
							x2="5"
							y2={chartHeight - 15}
							stroke={getRegionColor(metro.region)}
							stroke-width="3"
						/>
						<text x="12" y="31" class="textCity"
							>{i + 1}. {label}</text
						>
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
					<svg
						height={chartHeight}
						width={chartWidth}
						viewBox="0 0 {chartWidth} {chartHeight}"
						preserveAspectRatio="xMinYMid meet"
						class="chart"
					>
						<!-- Grid lines -->
						{#each [0, 1] as yearIndex}
							{#each [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] as tick}
								<line
									x1={yearIndex * (chartWidth / 2) +
										(tick * chartWidth) / 2 / 12}
									y1={5}
									x2={yearIndex * (chartWidth / 2) +
										(tick * chartWidth) / 2 / 12}
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
									stroke="var(--brandGray50)"
									stroke-width="2"
									stroke-opacity="0.65"
								/>
							{/if}
						{/each}

						<!-- Event markers -->
						{#each eventMarkers as event}
							{#if (event.key === "trump" && showTrump) || (event.key === "cad" && showCad) || (event.key === "carney" && showCarney) || (event.key === "tariffs" && showTariffs) || (event.key === "truckTariffs" && showTruckTariffs)}
								<line
									x1={event.x}
									y1={5}
									x2={event.x}
									y2={45}
									stroke={eventColor}
									stroke-width="2"
									stroke-dasharray="3 1"
								/>
							{/if}
						{/each}

						<!-- Baseline (Year 1 average) -->
						{#if metro.meanLine !== null}
							<line
								x1="0"
								y1={metro.meanLine}
								x2={chartWidth}
								y2={metro.meanLine}
								stroke="#1E3765"
								stroke-opacity="0.75"
								stroke-width="1"
								stroke-dasharray="4"
							/>
						{/if}

						<!-- LOESS regression line -->
						{#if metro.regressionLine}
							<path
								d={metro.regressionLine}
								stroke="#1E3765"
								stroke-width="2"
								fill="none"
							/>
							{#if metro.startCircle}
								<circle
									cx={metro.startCircle.cx}
									cy={metro.startCircle.cy}
									r="3"
									fill="#1E3765"
								/>
							{/if}
							{#if metro.endCircle}
								<circle
									cx={metro.endCircle.cx}
									cy={metro.endCircle.cy}
									r="3"
									fill="#DC4633"
								/>
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
		overflow-x: auto;
		overflow-y: scroll;
		margin: 0 auto;
		max-width: 680px;
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
		max-width: 680px;
		width: max-content;
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

	.header-text-percent {
		display: block;
		line-height: 1.05;
		transform: translateX(-28px);
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
		margin-left: 2px;
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
		width: 96px;
		display: flex;
		align-items: center;
		justify-content: flex-start;
		padding-left: 0;
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
		margin-left: 0;
		min-width: 0;
	}

	.arrow-icon {
		display: inline-flex;
		font-size: 22px;
		line-height: 1;
		font-family: OpenSansBold;
	}

	.up-arrow {
		color: #007fa3;
	}

	.down-arrow {
		color: #dc4633;
	}

	@media (max-width: 600px) {
		.textLabelSmall {
			font-size: 8px
		}
	}

	.event-legend {
		display: flex;
		flex-direction: column;
		gap: 10px;
		margin-bottom: 13px;
		max-width: 680px;
		margin-left: auto;
		margin-right: auto;
		padding: 0 5px;
	}

	.event-legend-row {
		display: flex;
		flex-wrap: wrap;
		gap: 14px;
		align-items: center;
	}

	.event-legend-item {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
	}

	.event-btns {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 4px;
	}

	.event-btns {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 4px;
	min-width: 0;
}

.event-btn {
	display: inline-flex;
	align-items: center;
	gap: 5px;
	font-family: OpenSans, sans-serif;
	font-size: 11px;
	text-align: left;
	color: var(--brandGray90);
	background: transparent;
	border: 1px solid var(--brandGray);
	border-radius: 4px;
	padding: 1px 5px;
	cursor: pointer;
	opacity: 0.4;
	transition:
		opacity 0.15s ease,
		border-color 0.15s ease;

	/* important */
	min-width: 0;
	max-width: 100%;
}

/* Mobile */
@media (max-width: 600px) {
	.event-btns {
		grid-template-columns: 1fr;
	}

	.event-btn {
		white-space: normal;
		font-size: 10px;
	}
}

.event-btn.active {
	opacity: 1;
	border-color: #007fa3;
}

.event-btn:hover {
	opacity: 0.85;
}


</style>
