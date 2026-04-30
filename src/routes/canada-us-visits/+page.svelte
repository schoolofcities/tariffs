<Password/>

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
	let searchQuery = "";
	let showBigMetros = true;
	let showSmallMetros = true;
	let selectedDataset = 'us_normalized_trips.csv'
	// View toggle: "map", "rankings" or "trends"
	let viewMode = "trends";


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
						.bandwidth(0.05);
					
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
							.range([xPadding, 560 - xPadding]);
						
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
		title="Tracking decline in Canadians visiting U.S. cities"
		subtitle="An analysis of Canadians' visits to U.S. cities using cell phone data"
	/>

	<div class="text">
	
		<AuthorDate
			authors="<a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>, <a href='https://schoolofcities.utoronto.ca/people/jeff-allen/' target='_blank'>Jeff Allen</a>"
			date="May 2026."
		/>

		<p>
			In response to increasingly strained political relations between Canada and the United States, Canadians have reduced discretionary travel to the U.S.. 
			To investigate the magnitude and geography of this shift, we analyzed cell phone activity (footfall) data across Canada and the U.S., providing insights on the metro areas Canadians are visiting.
		</p>

		<p>
			Estimates based primarily on <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260323/dq260323a-eng.htm">data from border crossings</a> suggest a year-over-year decline in Canadian visitations at <b>20-25%</b>. By contrast, our analysis of cell phone activity indicates a larger median decrease of approximately <b>41%</b> in visits to U.S. metropolian areas.
		</p>


	</div>


	{#if isLoading}
		<div class="loading-container">
			<div class="loading-spinner"></div>
			<p class="loading-text">Loading data...</p>
		</div>
	{:else}

	

	<div class="text" style="margin-bottom: 0px;">

		<h3>Year-over-year change in trips by Canadians to U.S. metros</h3>

		<!-- View Toggle -->
		<div class="view-toggle">
			<div class="toggle-group">
				<span class="toggle-label">View:</span>
				<button
					class="toggle-btn"
					class:active={viewMode === "trends"}
					on:click={() => (viewMode = "trends")}
				>
					Trends
				</button>
				
				<button
					class="toggle-btn"
					class:active={viewMode === "map"}
					on:click={() => (viewMode = "map")}
				>
					Map
				</button>
			</div>
		</div>

		<span class="toggle-label">Select metros:</span>

		<div class="metro-selector">
			<div class="metro-selector-group">
				<span class="metro-selector-sublabel">By region</span>
				<div class="button-group">
					{#each regionOptions as region}
						<button
							type="button"
							class="region-toggle-button {selectedRegions.includes(region) ? 'selected' : ''}"
							on:click={() => toggleRegion(region)}
						>
							<span
								class="region-swatch"
								style="background-color: {getRegionColor(region)}"
							></span>
							<span class="region-name">{region}</span>
						</button>
					{/each}
				</div>
			</div>

			<div class="metro-selector-group">
				<span class="metro-selector-sublabel">By population size</span>
				<div class="population-search-row">
					<div class="button-group">

						<button
							type="button"
							class="region-toggle-button {showSmallMetros ? 'selected' : ''}"
							on:click={() => (showSmallMetros = !showSmallMetros)}
						>
							{"<"} 1,000,000
						</button>
						<button
							type="button"
							class="region-toggle-button {showBigMetros ? 'selected' : ''}"
							on:click={() => (showBigMetros = !showBigMetros)}
						>
							≥ 1,000,000
						</button>
					</div>
					<div class="search-container">
						<input
							type="text"
							class="search-input"
							placeholder="Search for a metro area"
							bind:value={searchQuery}
						/>
						{#if searchQuery}
							<button class="clear-search" on:click={() => searchQuery = ""}>×</button>
						{/if}
					</div>
				</div>
				<div class="event-legend">
					<span class="event-legend-item">
						<span class="event-swatch event-swatch-light"></span>
						Trump first mentioned Canada as 51st state (Nov. 29, 2024)
					</span>
					<span class="event-legend-item">
						<span class="event-swatch event-swatch-dark"></span>
						25% auto tariffs came in (May 3, 2025)
					</span>
				</div>
			</div>
		</div>

	</div>
	
	<!-- Rankings and Trends Views -->
	{#if viewMode !== "map"}

	<!-- Trends View -->
	{#if viewMode == "trends"}
		<TrendLinesView
			filteredTrends={filteredTrends}
			chartHeight={chartHeight}
			metroLabelWidth={metroLabelWidth}
		/>
	{/if}
	{/if}

	<!-- Map View -->
	{#if viewMode === "map"}
	<MapView
		filteredMetroMetrics={filteredMetroMetrics}
		globalMaxNormalized={globalMaxNormalized}
		legendSizeBins={legendSizeBins}
	/>
	{/if}

	<div class="text" style="margin-top: 0px;">

		<div class="caption-container">
			<p>
				<span class="caption-source">Cell phone data are from <a href="https://cuebiq.com/">Cuebiq</a>. Geographic reference data are from <a href="https://en.wikipedia.org/wiki/OpenStreetMap">OpenStreetMap</a></span>
			</p>
		</div>

	</div>

	<div class="text" style="margin-top: 50px;">

		<p>
			Consistent with media reporting, our data shows significant declines in <a href="https://archive.ph/20250812180600/https:/www.bloomberg.com/news/features/2025-08-11/trump-tariffs-and-jabs-push-canadians-to-exit-florida-enclave#selection-1237.0-1237.66">snowbird destinations</a> like Florida; 
			border-region cities in states like <a href="https://www.theguardian.com/us-news/2026/mar/28/canada-us-border-business-pay-trump-tariffs">New York</a>, <a href="https://www.travelandtourworld.com/news/article/new-hampshires-tourism-feels-the-sting-of-declining-canadian-visitors-and-strained-u-s-canada-travel-ties-everything-to-know/">New Hampshire</a> and <a href="https://www.nytimes.com/2026/01/19/us/politics/greensboro-vermont-canada-tariffs-trump.html">Vermont</a>; 
			major tourist destinations like <a href="https://www.latimes.com/politics/story/2025-10-19/trumps-america-las-vegas-lagging-economy-struggling-food-server">Las Vegas</a> and <a href="https://www.reuters.com/business/looking-disney-magic-elsewhere-canadians-lead-declines-travel-us-2026-02-12/">Disney World</a>; and <a href="https://archive.ph/20260215003924/https:/www.bloomberg.com/news/articles/2026-01-26/canadian-skiers-skip-us-mountain-resorts-this-season-thanks-to-trump#selection-1183.0-1183.38">winter recreation areas</a>.
		</p>

		<p>
			However, one of the most underreported findings is the marked decline in visits to large metropolitan economies. 
			Technocratic and financial centres like San Francisco and Houston appear to be experiencing reductions not only in tourists but also in business-related travel, reflecting changing travel preferences from broader economic uncertainties on both sides of the border.
			As another example, Grand Rapids, which has close ties to the automotive industry in Ontario, has experienced the second largest drop in visitation, likely due to the tariffs.
		</p>

		<p>
			Differences between cell phone-based estimates and border-crossing estimates likely reflect differences in measurement scope. 
			Our cell phone data includes freight traffic, whereas border-crossing data does not. Notably, January and February 2025 were among the <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/250306/dq250306a-eng.htm">strongest months for Canadian exports to the U.S.</a> likely driven by the anticipated tariff threats. 
			The introduction of major tariffs, such as the <a href="https://www.congress.gov/crs-product/IN12545">25% tariff in automotive parts</a>, may explain the following reduction in trade-related trips beginning in April 2025.
			In addition, our data measures not only Canadians crossing the border, but also Canadians living temporarily in the U.S., indicating that the decrease in activity may reflect return migration to Canada. 
		</p>

		<p>
			While Forbes estimates <a href="https://www.forbes.com/sites/suzannerowankelleher/2026/02/12/canadian-visits-fall-january-trump-slump/">tourism-based revenue loss of US$4.5 billion</a> from a 22% drop in Canadian visitation, this does not include the Canadians who are no longer living in the U.S., or the drivers moving Canadian goods.
			Therefore, these figures likely understate the total revenue lost from broader economic effects of changes in residency patterns and trade-related travel, as suggested from <a href="https://accd.vermont.gov/canada-research">recent estimates by the State of Vermont</a>.
		</p>

        <!-- <p>
			This tool analyzes Canadian travel to U.S. metro areas using geolocation data from March 2024 to March 2026. 
			The data shows normalized trips (ratio of unique Canadian devices to total Canadian devices) to understand year-over-year trends in border travel.
		</p> -->

		<!-- {#if !isLoading}
		<h2>Key findings</h2>
		<p>
			This tool offers three different ways to explore changes in Canadian foot traffic in the U.S.
			The Trend Lines show changes by month from March 2024 to March 2026 and are colour-coded by region, for summary data.
			The map shows the scale of changes across the U.S. 
		</p>

		<p>
			To only view metropolitan areas of over 1 million in population, click the 1 million+ metros button, and to see different regions, click the square next to the region name (e.g., Southeast).
		</p>

		<div class="finding-lines">
			<p class="finding-line">
				‣ {totalMetros > 0
					? `Out of ${totalMetros} U.S. metro areas in the selected region(s), ${metrosRising} saw increased Canadian visits and ${metrosFalling} saw declines comparing Year 2 (April 1, 2025 to March 31, 2026) to Year 1 (April 1, 2024 to March 31, 2025).`
					: 'No metro areas are selected. Use the region filters above to show summary metrics.'}
			</p>
			<p class="finding-line">
				‣ {totalMetros > 0
					? `The mean change in normalized trips across all metros was ${meanChange?.toFixed(1) ?? "..."}%.`
					: 'Select one or more regions to display map, rankings, and trend summaries.'}
			</p>
			<p class="finding-line">
				‣ {totalMetros > 0
					? 'These results are based on normalized trip volume for U.S. metro areas visited by Canadian devices.'
					: 'If no metrics appear, clear and reselect your region filters.'}
			</p>
		</div>
		{/if} -->
	</div>

	

	
	<div class="text">
		<h3>Data sources and methods</h3>
		<p>
			The data comes from geolocation based trips tracking Canadian devices traveling to U.S. metro areas based on <a href="https://cuebiq.com/">Cuebiq</a>'s stops table. 
			A "Canadian device" is defined as a unique device in the stops table with the country code set as "Canada" and the device type as "Home". 
			Home devices are classified based on the duration and timing of the stops, and each device is assigned a unique anonymized identifier. 
			All Canadian devices observed between March 1, 2023 - March 31, 2026 are included to account for Canadians who may have relocated to the U.S. prior to April 1, 2024.
		</p>

		<p>
			Trips are deemed to occur when a device has a stop in Canada, followed by a stop in the U.S., and finally a stop back in Canada.
			To determine which region gets a count on a specific day, the first stop that is in the U.S. metro (at a geohash level 6 level) is counted for that metro on that day. 
			Subsequent days within the same metro are not counted; however, if that device enters another metro, the first stop in that new metro is then recorded.
			In other words, this approach captures unique metro-device trip occurences for Canadians travellers to the U.S.. 
		</p>

		<p>
			All values are normalized by the total number of unique Canadian devices each day to account for daily variations in data coverage.
			The trend lines are fit via a <a href="https://en.wikipedia.org/wiki/Local_regression">LOESS</a> curve.
		</p>

		<p>
			You can download the selected normalized trip data <a href={`/canada-us-visits/${selectedDataset}`}>from this link</a>.
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


	.region-controls {
		display: flex;
		gap: 10px;
		margin-bottom: 10px;
	}

	.region-control-btn {
		padding: 6px 12px;
		border: 1px solid var(--brandGray);
		border-radius: 5px;
		cursor: pointer;
		background-color: var(--brandWhite);
		color: var(--brandDarkGray);
		font-family: OpenSans, sans-serif;
		font-size: 16px;
		line-height: 1.1;
		opacity: 0.8;
		transition: opacity 0.2s ease, border 0.2s ease;
	}

	.region-control-btn:hover {
		opacity: 1;
		border: 2px solid var(--brandMedBlue);
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

	.event-legend {
		display: flex;
		flex-wrap: wrap;
		gap: 14px;
		margin-top: 8px;
	}

	.event-legend-item {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
	}

	.event-swatch {
		display: inline-block;
		width: 14px;
		height: 3px;
		border-radius: 999px;
	}

	.event-swatch-light {
		background: #DC4633;
	}

	.event-swatch-dark {
		background: #8B1E1E;
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

	h5 {
		font-size: 14px;
		font-family: OpenSans;
		color: var(--brandGray90);
		margin-bottom: 5px;
	}

	.bold {
		font-weight: bold;
	}

	.text {
		max-width: 680px;
		margin: 0 auto;
	}

	.related-links {
		font-family: OpenSans;
		font-size: 16px;
		line-height: 26px;
	}

	.related-links a {
		font-family: OpenSans;
	}

	@media (max-width: 720px) {
		.search-container {
			max-width: 300px;
			flex: 1 1 auto;
			margin-left: 0;
		}
	}

</style>
