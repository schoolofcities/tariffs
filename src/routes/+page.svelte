<script>

	import '../assets/global-styles.css';

	import Logo from '$lib/LogoTop.svelte';
	import TitleFullPage from '$lib/TitleFullPage.svelte';
	import TitleHalfSplit from '$lib/TitleHalfSplit.svelte';
	import TitleStandard from '$lib/TitleStandard.svelte';
	import AuthorDate from '$lib/AuthorDate.svelte';
	import ImageSingle from '$lib/ImageSingle.svelte';
	import GraphicSingle from '$lib/GraphicSingle.svelte';
	import GraphicsMultiples from '$lib/GraphicMultiples.svelte';
	import HorizontalBarChart from '$lib/HorizontalBarChart.svelte';
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


	<ImageSingle
		imageURL="./lumber/img/allgoodsada.png"
		caption=''
		source=''
		maxWidth='680px'
		link='No'
	/>

	<TitleStandard
		title="Mapping Tariffs"
		subtitle=""
	/>

	<!-- <div class="text">

		<AuthorDate
			authors="<a href='' target='_blank'>Tara Vinodrai</a>, <a href='' target='_blank'>Karen Chapple</a>, <a href='' target='_blank'>Jeff Allen</a>, Muhammad Khalis Bin Samion, Eli Easton, Rick DiFrancesco"
			date="October 2025"
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

		<p>
			New tariffs imposed by U.S. President Donald Trump on Canada and other countries have sparked interest—and concern—about their effects on jobs and businesses across Canada. As details about tariffs on Canadian goods continue to emerge, policymakers, business leaders, and the public are asking where the impacts will be felt—now and over the longer term. What places are most vulnerable?
		</p>

		<p>
			Measuring trade impacts is complex because there are many factors at play. The immediate impacts of tariffs are on the businesses (and their employees) that produce goods subject to tariffs. However, there may also be downstream, indirect impacts. And, the situation is not static as businesses, consumers and governments respond and adjust to a changing economy. Businesses may diversify their markets and seek new (or substitute) suppliers. Citizens may alter their purchasing habits by buying local or Canadian products. Governments may try to spur local purchasing and help support businesses. And the federal government may adjust monetary policy, fiscal policy, and trade policy (e.g. counter tariffs, new trade agreements) to ensure the resilience of the Canadian economy.
		</p>

		<p>
			Since May 2025, <a href="">Tara Vinodrai</a> and <a href="">Karen Chapple</a> have led a team of researchers at the School of Cities to develop interactive mapping and visualization tools that measure and explore the potential impacts of tariffs on jobs and businesses across Canadian cities and communities at the neighbourhood and city level. Our tools illustrate the highly localized and uneven potential impacts of U.S. tariffs reflecting Canada’s underlying urban, regional and sectoral specializations.
		</p>

		<ul>
		<li>
			<a href="./map">Examine maps of the potential direct exposure to U.S. tariffs</a> related to specific goods (e.g. automotive, steel, copper, lumber, energy & natural resources) across Canada at the neighbourhood level, measured by 1) businesses 2) employment (based on place of work) and 3) employment (based on place of residence).
		</li>

		<li>
			<a href="./cma-ranking-charts">Review these same impacts in aggregate across Canadian cities</a>.	
		</li>

		<li>
			<a href="./potential-local-impacts">Read our backgrounder and blog</a> on Canada-U.S. trade and mapping direct exposure to tariffs.
		</li>

		<li>
			<a href="./lumber">Read our blog on the effect of softwood lumber tariffs</a> on Canadian jobs and businesses.
		</li>

		<li>
			<a href="./trucks">Read our blog about the impact of truck tariffs</a> on medium & heavy duty vehicle manufacturing and exports.
		</li>

		<li>
			<a href="./current-tariffs">View the current list of U.S. tariffs on Canada</a>.
		</li>

		<li>
			<a href="https://github.com/schoolofcities/tariffs" target="_blank">Learn more about our research methodology</a>.
		</li>
		</ul>

		<h2>
			Research team
		</h2>

		<p>
			<a href="https://discover.research.utoronto.ca/8035-tara-vinodrai">Tara Vinodrai, PhD</a> is Professor in the Institute for Management and Innovation at the University of Toronto, where she directs the Master of Urban Innovation program.
		</p>

		<p>
			<a href="https://schoolofcities.utoronto.ca/people/karen-chapple/" targe="_blank">Karen Chapple, PhD</a> is the Director of the School of Cities and Professor in the Department of Geography & Planning at the University of Toronto.
		</p>

		<p>
			<a href="https://jamaps.github.io/" target="_blank">Jeff Allen, PhD</a> is a Senior Research Associate and the Lead of Data Visualization at the School of Cities at the University of Toronto. 
		</p>

		<p>
			<a href="https://mkbs-mkbs2000.github.io/Personal-Portfolio/" target="_blank">Muhammad Khalis Bin Samion</a> completed his honours undergraduate degree at the University of Toronto in human geography and urban studies. He is currently earning a master’s degree in urban spatial science at University College London. 
		</p>

		<p>
			<a href="https://www.linkedin.com/in/yihoi-jung-0b95351b5/" target="_blank">Yihoi Jung</a>  is a Data Analyst Research Assistant at the School of Cities and has completed his undergraduate degree at the University of Toronto Scarborough in Statistics and City Studies.
		</p>

		<p>
			<a href="https://www.linkedin.com/in/eli-easton-77bb60273/" target="_blank">Eli Easton</a> is a senior undergraduate student at the University of Toronto where he is studying economics and public policy.
		</p>

		<p>
			<a href="https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco" target="_blank">Richard DiFrancesco, PhD</a> is Associate Professor in the Department of Geography and Planning at the University of Toronto and has expertise in input-output data and models.
		</p>

	</div>

	<Footer />

</main>