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

	<title>Tariffs | School of Cities</title>

	<!-- <meta name="description" content="Repository of design and web components for building data stories, visualizations, maps, and other custom web projects" />
	<meta name="author" content="Jeff Allen">

	<meta property="og:title" content="Design Components" />
	<meta property="og:description" content="Repository of design and web components for building data stories, visualizations, maps, and other custom web projects" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://schoolofcities.github.io/design-components/" />
	<meta property="og:image" content="https://raw.githubusercontent.com/schoolofcities/design-components/main/static/web-card.png" />
	<meta property="og:locale" content="en_CA">

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="Design Components" />
	<meta name="twitter:description" content="Repository of design and web components for building data stories, visualizations, maps, and other custom web projects" />
	<meta name="twitter:site" content="https://schoolofcities.github.io/design-components/" />
	<meta name="twitter:image" content="https://raw.githubusercontent.com/schoolofcities/design-components/main/static/web-card.png" />  -->

</svelte:head>




<Password/>


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

		
		<h1>Ranking Canadian urban areas by their potential direct exposure of U.S. tariffs</h1>

		<AuthorDate
			authors="<a href='' target='_blank'>Author Name</a>, <a href='' target='_blank'>Author Name</a>, and <a href='' target='_blank'>Author Name</a>"
			date="August 2025"
		/>

		<p>
			Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas consequat lacus eu dolor dapibus sodales. Aenean venenatis metus id eleifend tincidunt. Nulla ut lacus et urna finibus bibendum sit amet et ante. Aliquam tristique, ex sed porttitor hendrerit, ex odio accumsan ex, eu maximus leo quam quis nulla. 
		</p>

		<br>
		

	</div>

	<HorizontalBarChart />

	<div class="text">	

		<p>
			Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas consequat lacus eu dolor dapibus sodales. Aenean venenatis metus id eleifend tincidunt. Nulla ut lacus et urna finibus bibendum sit amet et ante. Aliquam tristique, ex sed porttitor hendrerit, ex odio accumsan ex, eu maximus leo quam quis nulla. 
		</p>

		<p>
			Fusce sed sem nulla. Praesent congue sapien pellentesque sodales fermentum. Pellentesque dapibus ultrices lacus consectetur laoreet. Integer imperdiet sed sapien sed pharetra. Praesent sodales nunc ut lorem venenatis laoreet vitae et neque. Etiam condimentum tincidunt dignissim. 
		</p>
		<p>	
			Praesent placerat purus vitae rhoncus auctor. Aliquam faucibus porta scelerisque. In bibendum ornare sagittis. Nam accumsan turpis sit amet elementum sollicitudin. Mauris auctor nec velit id iaculis. Proin venenatis nisl a iaculis dignissim. Nunc volutpat nulla at dolor mollis eleifend. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam commodo purus in risus placerat, sed vehicula enim viverra. 
		</p>
		
		<h3>Data sources list:</h3>
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
		<h3>
			Project team:
		</h3>
		<p>
			- Data processing and analysis: <a href="https://mkbs-mkbs2000.github.io/Personal-Portfolio/">Muhammad Khalis Bin Samion</a>.
			<br>
			- Interactive map and website design: <a href="https://jamaps.github.io/" target="_blank">Jeff Allen</a>.
			<br>
			- Data modelling scenarios: Rick DiFrancesco and Eli Easton
			<br>
			- Scientific direction: Karen Chapple and Tara Vinodrai
		</p>

	</div>


	<!-- <div class="text">

		<Footnotes footnotes={footnotes} />
		
	</div> -->

	<Footer />

</main>