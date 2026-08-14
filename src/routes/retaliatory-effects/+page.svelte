<Password/>

<script>

	import '../../assets/global-styles.css';

	import Logo from '$lib/LogoTop.svelte';
	import TitleFullPage from '$lib/TitleFullPage.svelte';
	import TitleHalfSplit from '$lib/TitleHalfSplit.svelte';
	import TitleStandard from '$lib/TitleStandard.svelte';
	import AuthorDate from '$lib/AuthorDate.svelte';
	import ImageSingle from '$lib/ImageSingle.svelte';
	import MapView from './assets/MapView.svelte';
	import GraphicSingle from '$lib/GraphicSingle.svelte';
	import GraphicsMultiples from '$lib/GraphicMultiples.svelte';
	import HorizontalBarChart from '$lib/HorizontalBarChart.svelte';
	import Footer from '$lib/Footer.svelte';
	import Password from '$lib/Password.svelte';
	import CountyMap from './assets/CountyMap.svelte';
	import { onMount } from 'svelte';


	import ScrollyImages from "$lib/ScrollyImages.svelte";

	import Footnote from '$lib/Footnote.svelte';
	import Footnotes from '$lib/Footnotes.svelte';
	import { createFootnoteStore } from '$lib/footnoteUtils';

	const footnoteStore = createFootnoteStore();
	const { footnotes, addFootnote } = footnoteStore;

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

	let mapPeriod = 'pre';
	

	let countyGeojson = null;
	let mapColorMode = 'exposure'; // 'exposure' | 'political'
	let geoLoading = true;

	const conversativeColour = '#E81B23'
	const democraticColour = '#0055A4'

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

	async function loadData(fileName = selectedDataset) {
		isLoading = true;
		try {
			const response = await fetch(`/geojson/${fileName}`);
			if (!response.ok) {
				throw new Error(`could not load geojson: ${fileName}`);
			}

		} catch (error) {
			console.error('Error loading geojson data:', error);
		}
		isLoading = false;
		dataLoaded = true;
	}

	onMount(async () => {
		const res = await fetch('/geojson/county_exposure.geojson');
		countyGeojson = await res.json();
		geoLoading = false;
	});


</script>




<svelte:head>

	<title>Mapping tariffs | School of Cities</title>

	<meta name="description" content="Examining potential local impacts on jobs and businesses across Canada via maps and charts" />
	<meta name="author" content="School of Cities">
	<meta rel="canonical" href="https://schoolofcities.github.io/tariffs/">

	<meta property="og:title" content="Mapping tariffs" />
	<meta property="og:description" content="Examining potential local impacts on jobs and businesses across Canada via maps and charts" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://schoolofcities.github.io/tariffs/" />
	<meta property="og:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" />
	<meta property="og:locale" content="en_CA">

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="Mapping tariffs" />
	<meta name="twitter:description" content="Examining potential local impacts on jobs and businesses across Canada via maps and charts" />
	<meta name="twitter:site" content="https://schoolofcities.github.io/tariffs/" />
	<meta name="twitter:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" /> 

</svelte:head>




<!-- <Password/> -->


<main>


	<div class="text">	

		
		<h1>Effects of retaliatory tariffs across the border</h1>

		<AuthorDate
			authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://www.linkedin.com/in/aniket-k-8a8b9921b/' target='_blank'>Aniket Kali</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>, & <a href='https://jamaps.github.io/' target='_blank'> Jeff Allen</a>"
			date="July 2026"
		/>

		<p>
			The tariffs imposed by the Trump administration onto Canada launched a trade war between Canada and the U.S..
			Since early 2025, the U.S. imposed numerous tariffs, and Canada showed resilience with retaliatory tariffs.
		</p>

		<p>
			Previously, we mapped the U.S. tariffs' potential effect on Canadian businesses. Soon after Mark Carney became Prime Minister, he implmented a <a href="https://www.pm.gc.ca/en/news/news-releases/2025/04/03/canada-announces-new-countermeasures-response-tariffs-from-united-states">25% tariff on $30 billion worth of goods </a>imported from the U.S. on March 4, 2025. Additional retaliatory tariffs were implemented March 13, 2025 on steel and aluminum at 25% as well to match U.S. tariffs.
		</p>

		<p>
			While we see how urban economies have been impacted in Canada through tariffed Canadian exports to the U.S., how will U.S. metros fare with Canada as the <a href="https://ustr.gov/countries-regions/americas/canada">top destination for U.S. exports</a>?
		</p>

		<h2>
			Political representation
		</h2>

		<p>
			Recently, a report from X found that red states were affected more than blue states due to retaliatory tariffs from China.
		</p>

		<p>
			Note that all results are based on tariffs as of June, 2026.
		</p>

		<br>
		

	</div>


	<div class="text">
		<div class="filter-row" style="margin-bottom: 12px;">
			<span class="filter-label">Colour by:</span>
			<button class="toggle-btn" class:active={mapColorMode === 'exposure'} on:click={() => mapColorMode = 'exposure'}>Tariff exposure</button>
			<button class="toggle-btn" class:active={mapColorMode === 'political'} on:click={() => mapColorMode = 'political'}>Political lean</button>
		</div>

		{#if mapColorMode === 'exposure'}
		<div class="filter-row" style="margin-bottom: 12px;">
			<span class="filter-label">Tariff period:</span>
			<button class="toggle-btn" class:active={mapPeriod === 'pre'}     on:click={() => mapPeriod = 'pre'}>Pre Aug 31</button>
			<button class="toggle-btn" class:active={mapPeriod === 'post'}    on:click={() => mapPeriod = 'post'}>Post Sep 1</button>
			<button class="toggle-btn" class:active={mapPeriod === 'removed'} on:click={() => mapPeriod = 'removed'}>Removed Sep 1</button>
		</div>
		{/if}
	</div>


	{#if geoLoading}
		<div class="loading-container">
			<div class="loading-spinner"></div>
			<p class="loading-text">Loading county data...</p>
		</div>
	{:else}
		<CountyMap geojson={countyGeojson} colorMode={mapColorMode} period={mapPeriod}/>
	{/if}

	<div class="text">	

		<h2>
			How vulnerable are U.S. cities from retaliatory Canadian tariffs?
		</h2>

		<p>
		</p>

		<p>
		</p>

		


		<h2>Data sources list:</h2>
		<p>
			Estimates in these charts were created by combining data from the following sources:
		</p>
		<ul>
			<li>Canadian Business Registry (Statistics Canada)</li>
			<li>Canadian Chamber of Commerce</li>
			<li>Canadian Census of Population (Statistics Canada)</li>
			<li>Canadian International Merchandise Trade Web Application (Statistics Canada Catalogue No. 71-607-X2021004)</li>
			<li>Cargo Systems Messaging Service (United States Customs and Border Protection)</li>
			<li>Harmonized Tariff Schedule of the United States (United States International Trade Commission )</li>
			<li>International Trade and Development Division (Statistics Canada)</li>
			<li>US Department of Commerce</li>
			<li>US Census Bureau</li>
		</ul>
		<p>
			For detailed data descriptions, download links, and processing steps, please read our <a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file" target="_blank">data and methodology page</a>
		</p>

	</div>


	<!-- <div class="text">

		<Footnotes footnotes={footnotes} />
		
	</div> -->

	<Footer />

</main>