<!-- <Password/> -->

<script>
	import '../../assets/global-styles.css';
	import Logo from '$lib/LogoTop.svelte';
	import Footer from '$lib/Footer.svelte';
	import AuthorDate from '$lib/AuthorDate.svelte';
	import TitleStandard from '$lib/TitleStandard.svelte';
	import Password from '$lib/Password.svelte';
	import bigMetroPopulation2025 from '$lib/data/big-metro-keys-2025.json';
	import TrendLinesView from './assets/TrendLinesView.svelte';
	import MapView from './assets/MapView.svelte';
	import IndustryScatterView from './assets/IndustryScatterView.svelte';
	import IndustryCorrelationSimple from './assets/IndustryCorrelationSimple.svelte';
	import RegressionView from './assets/RegressionView.svelte';
	import { industryCorrelations } from './assets/industryCorrelations.js';
	import { visitJobsScatterData } from './assets/visitJobsScatterData.js';
	import { onMount } from 'svelte';
	import { csvParse } from 'd3-dsv';
	import { scaleLinear, line } from "d3";
	import { regressionLoess } from "d3-regression";
	import { mean, sum, max as d3Max, min as d3Min } from 'd3-array';

	const regionOptions = ['Midwest', 'Northeast', 'Southwest', 'Southeast', 'Pacific'];
	let selectedRegions = [...regionOptions];

	const regionColors = {
		Midwest: '#6FC7EA',
		Northeast: '#8DBF2E',
		Southwest: '#F1C500',
		Southeast: '#AB1368',
		Pacific: '#00AEB3',
		Canada: '#F3603E'
	};

	const negativeColor = '#DC4633';
	const negativeMidColor = '#F1C500';
	const neutralColor = '#FFFFFF';
	const positiveColor = '#007FA3';

	function hexToRgb(hex) {
		const clean = hex.replace('#', '');
		const bigint = parseInt(clean, 16);
		return {
			r: (bigint >> 16) & 255,
			g: (bigint >> 8) & 255,
			b: bigint & 255
		};
	}

	function interpolateHex(fromHex, toHex, t) {
		const from = hexToRgb(fromHex);
		const to = hexToRgb(toHex);
		const r = Math.round(from.r + (to.r - from.r) * t);
		const g = Math.round(from.g + (to.g - from.g) * t);
		const b = Math.round(from.b + (to.b - from.b) * t);
		return `rgb(${r}, ${g}, ${b})`;
	}

	function getDivergingColor(value) {
		const clamped = Math.max(-70, Math.min(70, value));
		if (clamped < -15) {
			const t = (clamped + 70) / 55;
			return interpolateHex(negativeColor, negativeMidColor, t);
		}
		if (clamped < 0) {
			const t = (clamped + 15) / 15;
			return interpolateHex(negativeMidColor, neutralColor, t);
		}
		const t = clamped / 70;
		return interpolateHex(neutralColor, positiveColor, t);
	}

	// Get region color
	function getRegionColor(regionName) {
		return regionColors[regionName] || '#999';
	}

	// Configuration
	let selection = {
		year1: 2024,
		year2: 2025,
		year3: 2026,
		period1Start: "2024-04-01",
		period1End: "2025-03-31",
		period2Start: "2025-04-01",
		period2End: "2026-03-31",
		update_date: "2026-04-08"
	}

	// State variables
	let processedData = [];
	let metros = [];
	let loadedDateMin = null;
	let loadedDateMax = null;
	let isLoading = true;
	let dataLoaded = false;
	let searchQuery = "";
	let showBigMetros = true;
	let showSmallMetros = true;
	let selectedDataset = 'us_normalized_trips_daily.csv'
	// View toggle: "map", "rankings", or "trends"
	let viewMode = "trends";
	let correlationViewMode = "correlations-simple";
	let correlationMetric = "share";

	$: correlationData = industryCorrelations;
	$: scatterData = visitJobsScatterData;
	$: metricLabel = "job share";


	// Metro to region mapping (US states to regions)
	const stateToRegion = {
		// Midwest
		'IL': 'Midwest', 'IN': 'Midwest', 'MI': 'Midwest', 'OH': 'Midwest', 'WI': 'Midwest',
		'IA': 'Midwest', 'KS': 'Midwest', 'MN': 'Midwest', 'MO': 'Midwest', 'NE': 'Midwest',
		'ND': 'Midwest', 'SD': 'Midwest',
		// Northeast
		'CT': 'Northeast', 'ME': 'Northeast', 'MA': 'Northeast', 'NH': 'Northeast', 'RI': 'Northeast',
		'VT': 'Northeast', 'NJ': 'Northeast', 'NY': 'Northeast', 'PA': 'Northeast',
		'DE': 'Northeast', 'MD': 'Northeast',
		// Southwest
		'AZ': 'Southwest', 'NM': 'Southwest', 'OK': 'Southwest', 'TX': 'Southwest',
		'CO': 'Southwest', 'NV': 'Southwest', 'UT': 'Southwest',
		// Southeast
		'AL': 'Southeast', 'AR': 'Southeast', 'FL': 'Southeast', 'GA': 'Southeast', 'KY': 'Southeast',
		'LA': 'Southeast', 'MS': 'Southeast', 'NC': 'Southeast', 'SC': 'Southeast', 'TN': 'Southeast',
		'VA': 'Southeast', 'WV': 'Southeast', 'DC': 'Southeast',
		// Pacific
		'AK': 'Pacific', 'CA': 'Pacific', 'HI': 'Pacific', 'OR': 'Pacific', 'WA': 'Pacific', 'ID': 'Pacific', 'MT': 'Pacific'
	};

	function getMetroRegion(metroName) {
		// Extract state codes from metro name (e.g., "New York, NY" or "Dallas-Fort Worth, TX")
		const stateMatch = metroName.match(/,\s*([A-Z]{2})/);
		if (stateMatch) {
			const state = stateMatch[1];
			return stateToRegion[state] || null;
		}
		// Check for multi-state metros (e.g., "Washington, DC-VA-MD-WV")
		const multiStateMatch = metroName.match(/,\s*([A-Z]{2}(?:-[A-Z]{2})+)/);
		if (multiStateMatch) {
			const firstState = multiStateMatch[1].split('-')[0];
			return stateToRegion[firstState] || null;
		}
		return null;
	}

	// Parse date from YYYYMMDD format
	function parseDate(dateValue) {
		const dateStr = String(dateValue).trim();
		const year = parseInt(dateStr.substring(0, 4), 10);
		const month = parseInt(dateStr.substring(4, 6), 10) - 1;
		const day = parseInt(dateStr.substring(6, 8), 10);
		return new Date(year, month, day);
	}

	// Format date to YYYY-MM-DD
	function formatDate(date) {
		return date.toISOString().split('T')[0];
	}

	async function loadData(fileName = selectedDataset) {
		isLoading = true;
		try {
			const response = await fetch(`/canada-us-visits/${fileName}`);
			if (!response.ok) {
				throw new Error(`Could not load normalized trips CSV: ${fileName}`);
			}
			const csv = await response.text();
			const normalizedDataRaw = csvParse(csv);

			// Process the data
			processData(normalizedDataRaw);
		} catch (error) {
			console.error('Error loading CSV data:', error);
		}
		isLoading = false;
		dataLoaded = true;
	}

	function processData(normalizedDataRaw) {
		const normalizedData = [];
		normalizedDataRaw.forEach(row => {
			const metro = row.METRO || row.metro;
			const dateValue = row.DATE || row.date || row.dateNum;
			const normalizedValue = row.normalized ?? row.NORMALIZED;
			if (!metro || !dateValue) return;

			const date = parseDate(dateValue);
			if (Number.isNaN(date.getTime())) return;

			normalizedData.push({
				metro,
				date,
				dateStr: formatDate(date),
				dateNum: dateValue,
				normalized: parseFloat(normalizedValue)
			});
		});

		// Filter to our date range (April 1, 2024 to March 31, 2026)
		const startDate = new Date("2024-04-01");
		const endDate = new Date("2026-03-31");
		
		processedData = normalizedData.filter(d => d.date >= startDate && d.date <= endDate);
		if (processedData.length > 0) {
			loadedDateMin = new Date(d3Min(processedData, d => d.date.getTime()));
			loadedDateMax = new Date(d3Max(processedData, d => d.date.getTime()));
		} else {
			loadedDateMin = null;
			loadedDateMax = null;
		}
		
		// Get unique metros
		metros = [...new Set(processedData.map(d => d.metro))].sort();
	}

	onMount(() => {
		loadData();
	});

	const metroNameAliases = { "Louisville, KY-IN": "Louisville/Jefferson County, KY-IN" };
	const bigMetroKeys2025 = new Set(bigMetroPopulation2025.entries.map(entry => entry.key));

	function getMetroPopulationKey(metroName) {
		const normalized = metroName.replace(' Micro Area', '').trim();
		const aliased = metroNameAliases[normalized] || normalized;
		const stateMatch = aliased.match(/,\s*([A-Z]{2})/);
		const state = stateMatch ? stateMatch[1] : '';

		const cityPart = aliased.split(',')[0].trim();
		const city = cityPart.split(/[-/]/)[0].trim().toLowerCase();

		return `${city}|${state}`;
	}

	function isBigMetro(metroName) {
		return bigMetroKeys2025.has(getMetroPopulationKey(metroName));
	}

	// Chart dimensions
	const metroLabelWidth = 180;
	const chartHeight = 50;

	// Compute metrics for each metro
	$: metroMetrics = (() => {
		if (processedData.length === 0) return [];

		const period1Start = new Date(selection.period1Start);
		const period1End = new Date(selection.period1End);
		const period2Start = new Date(selection.period2Start);
		const period2End = new Date(selection.period2End);

		return metros.map(metro => {
			const metroData = processedData.filter(d => d.metro === metro);
			
			// Period 1: April 1, 2024 - March 31, 2025
			const period1Data = metroData.filter(d => d.date >= period1Start && d.date <= period1End);
			// Period 2: April 1, 2025 - March 31, 2026
			const period2Data = metroData.filter(d => d.date >= period2Start && d.date <= period2End);
			
			if (period1Data.length < 10 || period2Data.length < 10) return null;

			const avg1 = mean(period1Data, d => d.normalized);
			const avg2 = mean(period2Data, d => d.normalized);
			const total1 = sum(period1Data, d => d.normalized);
			const total2 = sum(period2Data, d => d.normalized);

			const percentChange = avg1 > 0 ? ((avg2 - avg1) / avg1) * 100 : 0;

			// For LOESS trend
			const sortedData = [...metroData].sort((a, b) => a.date - b.date);
			
			let regressionLine = null;
			let startCircle = null;
			let endCircle = null;
			let meanLine = null;

			if (sortedData.length >= 30) {
				try {
					const regressionGenerator = regressionLoess()
						.x(d => d.date.getTime())
						.y(d => d.normalized)
						.bandwidth(0.09);
					
					const regressionData = regressionGenerator(sortedData);
					
					if (regressionData.length > 0) {
						const allValues = regressionData.map(d => d[1]);
						const minVal = Math.min(...allValues);
						const maxVal = Math.max(...allValues);
						
						const minDateStr = period1Start.getTime();
						const maxDateStr = period2End.getTime();
						
						const xPadding = 5;
						const xScale = scaleLinear()
							.domain([minDateStr, maxDateStr])
							.range([xPadding, 360 - xPadding]);
						
						const yScale = scaleLinear()
							.domain([minVal, maxVal])
							.range([chartHeight - 5, 5]);

						const lineGenerator = line()
							.x(d => xScale(d[0]))
							.y(d => yScale(d[1]));

						regressionLine = lineGenerator(regressionData);
						
						startCircle = {
							cx: xScale(regressionData[0][0]),
							cy: yScale(regressionData[0][1])
						};
						endCircle = {
							cx: xScale(regressionData[regressionData.length - 1][0]),
							cy: yScale(regressionData[regressionData.length - 1][1])
						};
						meanLine = yScale(avg1);
					}
				} catch (e) {
					// Skip LOESS for this metro
				}
			}

			return {
				metro,
				region: getMetroRegion(metro),
				avg1,
				avg2,
				total1,
				total2,
				percentChange,
				period1Count: period1Data.length,
				period2Count: period2Data.length,
				regressionLine,
				startCircle,
				endCircle,
				meanLine,
				percentChangeDisplay: percentChange.toFixed(1) + "%"
			};
		}).filter(m => m !== null);
	})();

	// Filter by selected regions, search query, and big-metro toggle
	$: filteredMetroMetrics = metroMetrics.filter(m => {
		if (selectedRegions.length === 0) return false;
		
		const matchesRegion = m.region && selectedRegions.includes(m.region);
		const matchesSearch = !searchQuery || m.metro.toLowerCase().includes(searchQuery.toLowerCase());
		const isBig = isBigMetro(m.metro);
		const matchesBigMetro = (isBig && showBigMetros) || (!isBig && showSmallMetros);
		
		return matchesRegion && matchesSearch && matchesBigMetro;
	});

	// Sort for rankings view (worst to best)
	$: sortedByRankings = [...filteredMetroMetrics].sort((a, b) => a.percentChange - b.percentChange);

	// Sort for trends view (worst negatives first, then positives)
	$: sortedByTrends = [...filteredMetroMetrics].sort((a, b) => a.percentChange - b.percentChange);

	// The filters are already applied to filteredMetroMetrics
	$: filteredRankings = sortedByRankings;
	$: filteredTrends = sortedByTrends;

	// Statistics
	$: totalMetros = filteredMetroMetrics.length;
	$: metrosRising = filteredMetroMetrics.filter(m => m.percentChange > 0).length;
	$: metrosFalling = filteredMetroMetrics.filter(m => m.percentChange < 0).length;
	$: meanChange = filteredMetroMetrics.length > 0 ? mean(filteredMetroMetrics, m => m.percentChange) : 0;
	$: globalMaxNormalized = d3Max(metroMetrics, m => m.avg2) || 0.001;
	$: maxLegendVolume = d3Max(filteredMetroMetrics, m => m.avg2) || 0;
	$: legendSizeBins = [
		maxLegendVolume * 0.2,
		maxLegendVolume * 0.4,
		maxLegendVolume * 0.6,
		maxLegendVolume * 0.8,
		maxLegendVolume
	];

	function toggleRegion(region) {
		if (selectedRegions.includes(region)) {
			selectedRegions = selectedRegions.filter(r => r !== region);
			return;
		}
		selectedRegions = [...selectedRegions, region];
	}

</script>

<Logo logoType="Blue" backgroundColor="var(--brandWhite)"/>

<main>
		

	<TitleStandard
		title="How are different sectors faring compared to the decline in Canada to U.S. visits?"
	/>
	<!-- subtitle="An analysis of mobile footfall data across U.S. metropolitan areas, 2024–2026" -->
	<div class="text">
	
		<AuthorDate
			authors="<a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>, <a href='https://schoolofcities.utoronto.ca/people/jeff-allen/' target='_blank'>Jeff Allen</a>"
			date="May 2026."
		/>

		<p>
			Many U.S. cities have seen a significant reduction in Canadian travel from our analysis on <a href="/canada-us-visits">how much Canadian travel declined to U.S. cities</a>.
			<!-- We used cell phone activity data to investigate the magnitude and geography of this shift. -->
		</p>

		<p>
			The decline in visitation begs the question, which industries are hit hardest? To answer this, we must investigate the relation between the decline in visits with the industry makeup of U.S. cities.
		</p>

		<p>
			<!-- Estimates based primarily on <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260323/dq260323a-eng.htm">data from border crossings</a> suggest a year-over-year decline in Canadian visitations at <b>20-25%</b>. By contrast, our analysis of cell phone activity indicates a larger median decrease of approximately <b>41%</b> in visits to U.S. metropolian areas. -->

			From the <a href="https://www.bls.gov/cew/">U.S. Quarterly Census on Employment and Wages</a>, we gathered industry data on metropolitan statistical areas to conduct correlations and a regression with visits. 
			Using the share of industries per metro, our analysis finds strong predictors in the arts and entertainment sector, retail and trade, and professional and technical services in relation to the decline in U.S. metro visits.
		</p>
		


	</div>


	{#if isLoading}
		<div class="loading-container">
			<div class="loading-spinner"></div>
			<p class="loading-text">Loading data...</p>
		</div>
	{/if}

	{#if dataLoaded}





	<IndustryCorrelationSimple correlations={correlationData} metricLabel={metricLabel} />


	<div class="text" style = "margin-top: 50px">
		<p>
			From the correlations, the arts and entertainment sector in metros are impacted negatively across both the shares of jobs, signalling a worse the year-over-year percentage decline for art/entertainment oriented metros.
			This is borderline significant in the professional services industry as well (p = 0.06), where this includes legal, accounting, consulting, architecture, engineering and technical services.
			Manufacturing, retail and wholesale trade industries show better year-over-year outcomes, which may indicate that a resilience in cities' reliance on more local industries.
			<!-- Interestingly, manufacturing, retail and wholesale trade show bifurcating effects: when measured as job shares, these industries are associated with better year-over-year outcomes, while the totals show a negative correlation.
			This phenomenon likely reflects the interdependency that larger metros have with Canadian trade. -->
		</p>
	</div>

	<IndustryScatterView data={scatterData} mode={correlationMetric} />
	<div class="text" style = "margin-top: 50px">
		<p>
			When looking at strictly dominant industries per metro in the scatterplot, we see a general positive trend across all industries with the share of industries. 
			This could suggest that metros with diversified industries may be impacted harder while the more specialized metros are more resilient. 
		</p>
	</div>
	<RegressionView metric={correlationMetric} />
	<div class="text" style="margin-top: 0px;">

		<div class="caption-container">
			<p>
				<span class="caption-source">
					Job data are from the <a href="https://www.bls.gov/cew/">U.S. Census of Employment and Wages</a> aggregated for 2023's metropolitan statistical areas, the most recent complete data. Passenger enplanement data are from the <a href="https://www.faa.gov/airports/planning_capacity/passenger_allcargo_stats/passenger">Federal Aviation Administration</a>.
				</span>
			</p>
		</div>

	</div>

	<div class="text" style = "margin-top: 50px">
		<p>
			<!-- From our results, using the total number of jobs affected, the Northeast region has a statistically significant effect on whether a city is declining or not. -->
			To complement the scatterplot analysis, we ran a multivariate regression model using retail trade as the baseline as it is a large industry that is relatively stable and is in nearly every metro.
			As seen in the results, bigger metros have a significant negative effect on visits.
			We also see that metros further away from the Canada-U.S. border are affected more than metros closer to it. This could indicate that short trips are still happening, but that more dedicated longer trips are less prevalent.
		</p>

		<p>
			Furthermore, the arts/entertainment and the transportation/warehousing sectors are strong indicators of a decline in the year-over-year change in Canada to U.S. visitation compared to a retail heavy metros.
			This reveals that not only the tourism dependent metros are suffering from a loss in Canadian visits, but that the transportation sector, which includes passenger airlines, and freight trucking businesses are also at significant losses.
			The tariffs may be a major contributor to these negative predictors, which is reflective of the trade dependency between the U.S. and Canada.

		</p>
	</div>
	

	<div class="text" style = "margin-top: 50px">
		
		
		
		
		<p>
			Industry categories are based on the 2 digit North American Industrial Classification System (NAICS) codes from 2023. 
		</p>
	</div>

	<div class="text">
		<h3>Data sources and methods</h3>

		<p>
			The data used to define Canadian devices traveling to U.S. metro areas is provided by <a href="https://cuebiq.com/">Cuebiq</a>.
			See <a href={`/correlations-regression`}>our Canada to U.S. visits page</a> for more information on visit methodology.
		</p>
			
		<p>
			To gather industry shares, we extracted employment data for each metropolitan statistical area from the <a href="https://www.bls.gov/cew/">U.S. Quarterly Census on Employment and Wages</a> Python public API.
			We gathered the number of jobs for the first 2 digits of the NAICS categories and normalized them against the total number of jobs across all industries. This ratio of jobs per industry by the total across all industries defines the industry share of each city.
		</p>

		<p>
			Instead of the total number of jobs within each sector, we chose to use the share of jobs to account for different metro area's sizes for comparison across different metros. 
			With the share of jobs, we are measuring the industry concentration per metro (local workforce), neutralizing the size aspect.
		</p>

		<p>
			The correlations and regression use all industry shares of each metro, whereas the scatterplot demonstrates the industry with the most shares for each metro for visual clarity. 10 metros have been excluded in the regression due to data quality issues.
		</p>

		<p>
			You can download the correlations and regression data <a href={`/canada-us-regression/`}>from this link</a>, the normalized trip data <a href={`/canada-us-regression/${selectedDataset}`}>from this link</a>.
		</p>
		<br>
	</div>

	{/if}

	<Footer />
</main>

<style>
	main {
		margin: 0 auto;
		width: 100%;
		min-width: 0;
		max-width: 1920px;
		position: relative;
	}

	.button-group {
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
		margin-top: 8px;
	}

	.region-toggle-button {
		display: inline-flex;
		align-items: center;
		gap: 7px;
		padding: 6px 10px;
		margin-right: 0;
		border: 1px solid transparent;
		border-radius: 5px;
		cursor: pointer;
		background-color: transparent;
		color: var(--brandDarkGray);
		user-select: none;
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		font-weight: normal;
		opacity: 0.5;
		transition: opacity 0.2s ease, border 0.2s ease;
		border-color: var(--brandGray);
	}

	.region-toggle-button.selected {
		opacity: 1;
		border-color: var(--brandLightBlue);
	}

	.region-toggle-button:hover {
		opacity: 1;
		border-color: var(--brandMedBlue);
	}

	.region-swatch {
		height: 15px;
		width: 5px;
		/* border: solid 1px var(--); */
		border-radius: 0px;
		flex: 0 0 auto;
	}

	.region-name {
		line-height: 1;
	}

	/* Search styles */
	.population-search-row {
		display: flex;
		flex-wrap: wrap;
		align-items: flex-start;
		gap: 10px;
		margin-top: 8px;
	}

	.population-search-row .button-group {
		margin-top: 0;
		flex: 1 1 auto;
	}

	.search-container {
		position: relative;
		max-width: 200px;
		width: 100%;
		flex: 0 1 100px;
		min-width: 195px;
		margin-left: auto;
	}


	.search-input {
		width: 100%;
		box-sizing: border-box;
		padding: 4px 15px 4px 10px;
		font-size: 14px;
		border: 1px solid var(--brandGray);
		border-radius: 4px;
		background: var(--brandWhite);
		color: var(--brandGray90);
	}

	.search-input::placeholder {
		color: #888;
	}

	.clear-search {
		position: absolute;
		right: 5px;
		top: 50%;
		transform: translateY(-50%);
		background: none;
		border: none;
		color: var(--brandGray90);
		font-size: 20px;
		cursor: pointer;
		padding: 0 5px;
	}

	.metro-selector {
		display: flex;
		flex-direction: column;
		gap: 10px;
		margin-top: 8px;
		margin-bottom: 30px;
	}

	.metro-selector-group {
		display: flex;
		flex-direction: column;
		gap: 6px;
		margin-bottom: 0px;
	}

	.metro-selector-sublabel {
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
		opacity: 0.7;
	}

	/* Toggle styles */
	.view-toggle {
		display: flex;
		flex-wrap: wrap;
		gap: 20px;
		padding: 15px 0;
	}

	.toggle-group {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.toggle-label {
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		color: var(--brandGray90);
	}

	.toggle-btn {
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		font-weight: normal;
		padding: 6px 10px;
		border: 1px solid transparent;
		background: transparent;
		color: var(--brandDarkGray);
		cursor: pointer;
		border-radius: 5px;
		opacity: 0.5;
		transition: opacity 0.2s ease, border 0.2s ease;
		border-color: var(--brandGray);
	}

	.toggle-btn:hover {
		opacity: 1;
		border-color: var(--brandMedBlue);
	}

	.toggle-btn.active {
		opacity: 1;
		border-color: var(--brandLightBlue);
	}

	/* Loading spinner */
	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 60px 20px;
		min-height: 200px;
	}

	.loading-spinner {
		width: 50px;
		height: 50px;
		border: 4px solid var(--brandGray90);
		border-top: 4px solid var(--brandLightBlue);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.loading-text {
		margin-top: 15px;
		font-family: OpenSans;
		font-size: 14px;
		color: var(--brandGray90);
	}

	.text {
		max-width: 680px;
		margin: 0 auto;
	}

	@media (max-width: 720px) {
		.search-container {
			max-width: 300px;
			flex: 1 1 auto;
			margin-left: 0;
		}
	}

</style>
