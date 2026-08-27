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

<!-- <Password/> -->

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
			date="August 2026"
		/>
	
	</div>

	<div class="text">	
	<ul>
		<li>A <a href="https://www.whitehouse.gov/fact-sheets/2026/07/fact-sheet-president-donald-j-trump-imposes-additional-tariffs-on-canada/">50% tariff</a> on <a href="https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-dairy/">dairy</a>, 
			<a href="https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-alcoholic-beverages/">alcohol</a>, 
			and <a href="https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-motor-vehicles/">motor vehicles</a> under Section 338 of the Tariff Act (effective August 22, 2026);</li>
		<li>
			A <a href="https://www.whitehouse.gov/presidential-actions/2026/07/actions-by-the-united-states-in-the-investigations-under-section-301-of-the-trade-act-of-1974-of-the-acts-policies-and-practices-of-60-economies-related-to-the-failure-of-each-economy-to-impose-and/">10% tariff</a> on Canadian on imports of most goods under Section 301 due to alleged forced labour practices (effective July 24, 2026);
		</li>
		<li>A <a href="https://www.whitehouse.gov/presidential-actions/2026/04/strengthening-actions-taken-to-adjust-imports-of-aluminum-steel-and-copper-into-the-united-states/">10-50% tariff on the full value of steel, aluminum and copper derivative products</a> depending on the percentage of metal content (effective April 6, 2026) — this is a bolder action by the U.S. to products containing these metals, resulting in higher total costs for manufacturers;</li>
		<li>A <a href="https://www.whitehouse.gov/presidential-actions/2025/09/adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/">10% tariff on softwood lumber</a>, totalling <a href="https://www.theglobeandmail.com/business/article-economy-gdp-growth-tariff-canada-us-trump-tariff-lumber/" target="_blank">duties
		of approximately 45% on Canadian softwood lumber</a> (10% tariffs, 35% anti-dumping & countervailing) (effective October 14, 2025);</li>
		<li>A <a href="https://www.whitehouse.gov/presidential-actions/2025/09/adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/">25% tariff on upholstered furniture, kitchen cabinets, and vanities</a>, (effective October 14, 2025);</li>
		<li>A <a href="https://www.tradecommissioner.gc.ca/en/market-industry-info/search-country-region/country/canada-united-states-export/us-tariffs/supporting-exporters-through-tariff-challenges.html"> 25% tariff on medium and heavy duty vehicles (trucks) and 10% on busses and other vehicles</a> (effective November 1, 2025); </li>	
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
		On December 31, 2025, the U.S. <a href="https://www.whitehouse.gov/fact-sheets/2025/12/fact-sheet-president-donald-j-trump-adjusts-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/">delayed a planned increase to the 25% tariff on upholstered furniture, and kitchen cabinets and vanities</a> set for January 1, 2026, 
		which would have <a href="https://www.whitehouse.gov/presidential-actions/2025/09/adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/" target="_blank">increased to 35% and 50% respectively</a>.
	</p>
	 
	<p>
		On February 20, 2026, the <a href="https://www.cbc.ca/news/world/livestory/scotus-tariff-ruling-9.7099048">U.S. Supreme Court ruled against the Trump administration's use of emergency powers to impose tariffs</a> under the 1977 International Emergency Economic Powers Act (IEEPA).
		Although this is a win for Canada, Trump's reaction was to impose a <a href="https://www.whitehouse.gov/fact-sheets/2026/02/fact-sheet-president-donald-j-trump-imposes-a-temporary-import-duty-to-address-fundamental-international-payment-problems/">tariff of 10%</a>, effective as of February 24, 2026 and initially lasting for 150 days under Section 122 of the Trade Act.
	</p>

	<p>
		As of August 2026, the U.S. government continues to enact <i>de minimis</i> and threaten further tariffs, such as <a href="https://www.nytimes.com/2026/08/24/business/economy/trump-canada-tariffs.html">50% tariffs on all automotive goods</a> for January 2027.
		The Canadian government endures these challenges by <a href="https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs/complete-list-us-products-subject-to-counter-tariffs.html" target="_blank">enforcing retaliatory tariffs on steel, aluminum and autos</a>, and <a href="https://www.pm.gc.ca/en/news/backgrounders/2025/09/05/prime-minister-carney-launches-new-measures-protect-build-and">providing relief through programs</a> like the <a href="https://www.cfib-fcei.ca/en/tools-resources/regional-tariff-response-initiative-rtri">Regional Tariff Response Initiative</a> ($1 billion in funding over 3 years).
		<a href="https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs/complete-list-us-products-subject-to-counter-tariffs.html">Countermeasures in retaliatory tariffs</a> against the Section 338 tariffs recently imposed on August 22, 2026 will take place on September 8, 2026.
	</p>

	</div>
	<Footer />
</main>