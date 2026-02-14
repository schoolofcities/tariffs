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

	<title>List of current U.S. tariffs on Canada | School of Cities</title>

	<meta name="description" content="An updated list of current U.S. tariffs on Canada" />
	<meta name="author" content="School of Cities">
	<meta rel="canonical" href="https://schoolofcities.github.io/tariffs/current-tariffs">

	<meta property="og:title" content="List of current U.S. tariffs on Canada" />
	<meta property="og:description" content="An updated list of current U.S. tariffs on Canada" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://schoolofcities.github.io/tariffs/current-tariffs" />
	<meta property="og:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" />
	<meta property="og:locale" content="en_CA">

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="List of current U.S. tariffs on Canada" />
	<meta name="twitter:description" content="An updated list of current U.S. tariffs on Canada" />
	<meta name="twitter:site" content="https://schoolofcities.github.io/tariffs/current-tariffs" />
	<meta name="twitter:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" /> 

</svelte:head>

<main>

	<Logo logoType="Blue" backgroundColor="var(--brandWhite)"/>

	<ImageSingle
		imageURL="./current-tariffs/businesscounttorontowide.png"
		caption=''
		source=''
		maxWidth='685px'
		link='No'
	/>

	<TitleStandard
		title="List of current U.S. tariffs on Canada"
		subtitle="An updated list of current U.S. tariffs on Canada"
	/>

	<div class="text">

		<AuthorDate
			authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://jamaps.github.io/' target='_blank'>Jeff Allen</a>, <a href='https://mkbs-mkbs2000.github.io/Personal-Portfolio/' target='_blank'>Muhammad Khalis Bin Samion</a>, <a href='https://www.linkedin.com/in/eli-easton-77bb60273/'  target='_blank'>Eli Easton</a>, <a href='https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco' target='_blank'>Rick DiFrancesco</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>"
			date="February 2026"
		/>
	
	</div>

	<div class="text">	
	<ul>
		<li><a href="https://www.theglobeandmail.com/business/article-economy-gdp-growth-tariff-canada-us-trump-tariff-lumber/" target="_blank">Duties
		of approximately 45% on Canadian softwood lumber (10% new tariffs, 35% anti-dumping & countervailing)</a> 
		There was a 25% tariff on upholstered furniture, kitchen cabinets, and vanities looped under this section as well which was <a href="https://www.whitehouse.gov/presidential-actions/2025/09/adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/" target="_blank">planned to be increased</a> for January 1, 2026, 
		but <a href="https://www.whitehouse.gov/fact-sheets/2025/12/fact-sheet-president-donald-j-trump-adjusts-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/">has since been delayed</a>;</li>
		<li>A <a href="https://www.tradecommissioner.gc.ca/en/market-industry-info/search-country-region/country/canada-united-states-export/us-tariffs/supporting-exporters-through-tariff-challenges.html"> 25% tariff on medium and heavy duty vehicles (trucks) and 10% on busses</a> (effective November 1, 2025); </li>	
		<li>Increased <a href="https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-president-donald-j-trump-amends-duties-to-address-the-flow-of-illicit-drugs-across-our-northern-border/" target="_blank">tariffs
		on non-CUSMA compliant Canadian goods to 35%</a> from 25%
		announced in February 2025 (effective: August 1, 2025);</li>
		<li>A <a href="https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-president-donald-j-trump-amends-duties-to-address-the-flow-of-illicit-drugs-across-our-northern-border/" target="_blank">40%
		tariff on Canadian exports that are transshipped</a> to
		avoid the above-stated tariffs (effective: August 1, 2025);</li>
		<li>A <a href="https://www.tradecommissioner.gc.ca/en/market-industry-info/search-country-region/country/canada-united-states-export/us-tariffs/supporting-exporters-through-tariff-challenges.html" target="_blank">10%
		tariff on non-CUSMA compliant potash and energy</a>
		(effective: August 1, 2025);</li>
		<li>An increase to a <a href="https://www.cbc.ca/news/business/canada-response-steel-tariffs-1.7552058" target="_blank">50%
		tariff on all Canadian steel and aluminum imports</a> to
		the U.S. from the 25% announced in February 2025 (effective: June 3,
		2025);</li>
		<li>A <a href="https://www.tradecommissioner.gc.ca/en/market-industry-info/search-country-region/country/canada-united-states-export/us-tariffs/supporting-exporters-through-tariff-challenges.html" target="_blank">25%
		tariff on automobiles and light trucks</a> imports; for
		Canada, this applies to the non-US content of vehicles imported
		under CUSMA (effective: April 3, 2025);</li>
		<li>A <a href="https://www.tradecommissioner.gc.ca/en/market-industry-info/search-country-region/country/canada-united-states-export/us-tariffs/supporting-exporters-through-tariff-challenges.html" target="_blank">25%
		tariff on non-CUSMA compliant auto parts</a> (effective:
		May 3, 2025);</li>
		<li>A <a href="https://www.whitehouse.gov/presidential-actions/2025/07/adjusting-imports-of-copper-into-the-united-states/" target="_blank">50%
		tariff on copper</a> (effective: August 1, 2025); </li>
	</ul>

	<p>
		Additionally, the U.S. government has <a href="https://www.federalregister.gov/documents/2025/09/02/2025-16802/notice-of-implementation-of-the-presidents-executive-order-14324-suspending-duty-free-de-minimis" target="_blank">eliminated <i>de minimis</i> treatment</a> for low-value shipments (defined as those under $800 in value). In other words, shipments to the U.S. from Canada that are under $800 are now subject to tariffs. 
	</p>

	<p>
		On September 1, 2025, the Canadian government lifted many of its counter-tariffs noting that many Canadian exporters (with the exceptions of those related to automotive, aluminum, and steel) are able to avoid tariffs through compliance with CUSMA. Canada’s Department of Finance maintains an up-to-date <a href="https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs/complete-list-us-products-subject-to-counter-tariffs.html" target="_blank">list of Canadian tariffs</a> on U.S. exports.
	</p>

	<p>
		As of February 2026, the U.S. government remains to enact de-minimis and the Canadian government continues to <a href="https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs/complete-list-us-products-subject-to-counter-tariffs.html" target="_blank">enforce retaliatory tariffs on steel, aluminum and autos</a>. 
		In response, the Canadian government has <a href="https://www.pm.gc.ca/en/news/backgrounders/2025/09/05/prime-minister-carney-launches-new-measures-protect-build-and">provided relief through programs</a> like the <a href="https://www.cfib-fcei.ca/en/tools-resources/regional-tariff-response-initiative-rtri">Regional Tariff Response Initiative</a>, with $1 billion funding this program over 3 years from September 5 , 2025.
	</p>

	</div>
	<Footer />
</main>