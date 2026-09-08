<script>

	import '../../assets/global-styles.css';

	import Logo from '$lib/LogoTop.svelte';
	import TitleFullPage from '$lib/TitleFullPage.svelte';
	import TitleHalfSplit from '$lib/TitleHalfSplit.svelte';
	import TitleStandard from '$lib/TitleStandard.svelte';
	import AuthorDate from '$lib/AuthorDate.svelte';
	import ImageSingle from '$lib/ImageSingle.svelte';
	import GraphicSingle from '$lib/GraphicSingle.svelte';
	import GraphicsMultiples from '$lib/GraphicMultiples.svelte';
	import RollupBarChart from '$lib/RollupBarChart.svelte';
	import Footer from '$lib/Footer.svelte';
	import Password from '$lib/Password.svelte';

	import ScrollyImages from "$lib/ScrollyImages.svelte";

	import Footnote from '$lib/Footnote.svelte';
	import Footnotes from '$lib/Footnotes.svelte';
	import { createFootnoteStore } from '$lib/footnoteUtils';

	const footnoteStore = createFootnoteStore();
	const { footnotes, addFootnote } = footnoteStore;

	const fns = [
		'Hello I am a footnote',
		'Hello I am a second <a href="https://example.com" target="_blank">footnote</a> with a link',
		'Author (Year) Publication information etc this might be a citation or a reference to a source',
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas consequat lacus eu dolor dapibus sodales. Aenean venenatis metus id eleifend tincidunt. Nulla ut lacus et urna finibus bibendum sit amet et ante. Aliquam tristique, ex sed porttitor hendrerit, ex odio accumsan ex, eu maximus leo quam quis nulla.'
	];

</script>

<Password/>


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

	<!-- Full page title example -->

	<!-- <TitleFullPage
		title="Fun Captivating Project Title"
		subtitle="Maybe a slightly longer more detailed wordier project subtitle"
		image="https://jamaps.github.io/photos/picimgs/halifax2_2024.jpg"
		imageOpacity=0.9
		imageAltText="A photo"
		titleFontColour="var(--brandWhite)"
		subtitleFontColour="var(--brandWhite)"
		logoType="White"
	/> -->


	<!-- Here is a half split title example: -->

	<!-- <TitleHalfSplit
		title="Fun Captivating Project Title"
		subtitle="Maybe a slightly longer more detailed wordier project subtitle that explains the project"
		image="https://schoolofcities.github.io/eddit/_app/immutable/assets/wood-buffalo-title-img-2.CpYjt7SE.jpg"
		imageAltText="A photo"
		imageCaption="Wood Buffalo skyline."
		imageSource="Wikimedia Commons."
		titleFontColour="var(--brandWhite)"
		titleBorderColour="var(--brandYellow)"
		subtitleFontColour="var(--brandWhite)"
		backgroundColour="var(--brandDarkBlue)"
		logoStyle="Dark"
	/> -->

	
	<!-- Simple title example with logo and subtitle: -->

	<Logo logoType="Blue" backgroundColor="var(--brandWhite)"/>

	<!-- <TitleStandard
		title="Potential direct exposure of U.S. tariffs in Canadian metropolitan areas"
		subtitle="Maybe a slightly longer more detailed wordier subtitle"
	/>

	<div class="text">

		<AuthorDate
			authors="<a href='' target='_blank'>Author Name</a>, <a href='' target='_blank'>Author Name</a>, and <a href='' target='_blank'>Author Name</a>"
			date="August 2025"
		/>
	
	</div> -->

	<!-- <ImageSingle
		imageURL="./images/border-rainbow-bridge.jpg"
		caption="Rainbow Bridge, Niagara River."
		source='Photo by Lennon Kong on Unsplash.'
		altText=""
		maxWidth="680px"
		link="no"
	/> -->

	<div class="text">	

		
		<h1>Ranked job losses by cities and provinces due to U.S. tariffs</h1>

		<AuthorDate
			authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco' target='_blank'>Richard DiFrancesco</a>, <a href='https://www.linkedin.com/in/aniket-k-8a8b9921b/' target='_blank'>Aniket Kali</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>, & <a href='https://jamaps.github.io/' target='_blank'> Jeff Allen</a>"
			date="First published September 2026."
		/>

		<h2>
			A city and province level analysis
		</h2>

		<p>
			Similar to our ranking charts for direct exposure to tariffs, we have built a tool for job losses. This comes from a Multi-Regional Input Output (MRIO) model built by Richard DiFrancesco.
		</p>

		<h2>
			A model to understand the impact of U.S. tariffs on Canadian cities
		</h2>

		<p>
			To understand the potential Canadian job losses due to U.S. tariffs, we’ve developed an interactive tool (below) derived from an MRIO model that allows users to explore how specific U.S. tariffs—on automotive, steel, lumber, aluminum, and more—could affect Canadians. 
			The tool provides metrics on the number and proportion of jobs and businesses potentially exposed to tariffs (see also our <a href="./map-scenarios">neighbourhood mapping tool</a>).
		</p>

		<p>
			Results are based on tariffs as of September 1, 2026.
		</p>

		<br>
		

	</div>

	<RollupBarChart />

	<div class="text">	

		<h2>
			What the data tells us about the vulnerability job losses to Canadian cities from U.S. tariffs
		</h2>

		<p>LOREM IPSUM</p>

		<h2>Policy implications?</h2>
		
		<ul>
			<li><b>Diversify local economies</b> to reduce dependence on vulnerable sectors</li>
			<li><b>Support businesses</b> in accessing new markets and supply chains.</li>
			<li><b>Invest in workforce development</b> to build resilience in the face of trade uncertainty.</li>
		</ul>

		<p>
			As trade tensions persist, Canadian policymakers must ensure that cities—especially smaller and specialized ones—are equipped to adapt and thrive.
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
			<li>Harmonized Tariff Schedule of the United States (United States International Trade Commission )</li>
		</ul>
		<p>
			For detailed data descriptions, download links, and processing steps, please read our <a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file" target="_blank">data and methodology page</a>
		</p>

	</div>


	<Footer />

</main>