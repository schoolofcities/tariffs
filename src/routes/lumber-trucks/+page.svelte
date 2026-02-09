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

	<title>Lumber and Trucks | School of Cities</title>

	<meta name="description" content="An update on potential local impacts on jobs and businesses across Canada via maps and charts" />
	<meta name="author" content="School of Cities">
	<meta rel="canonical" href="https://schoolofcities.github.io/tariffs/lumber-trucks">

	<meta property="og:title" content="Lumber and Trucks" />
	<meta property="og:description" content="An update on potential local impacts on jobs and businesses across Canada via maps and charts" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://schoolofcities.github.io/tariffs/lumber-trucks" />
	<meta property="og:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" />
	<meta property="og:locale" content="en_CA">

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="Lumber and Trucks" />
	<meta name="twitter:description" content="An update on potential local impacts on jobs and businesses across Canada via maps and charts" />
	<meta name="twitter:site" content="https://schoolofcities.github.io/tariffs/lumber-trucks" />
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
		imageURL="./lumber-trucks/img/lumberhorizontal.png"
		caption=''
		source=''
		maxWidth='685px'
		link='No'
	/>

	<TitleStandard
		title="Lumber and Trucks"
		subtitle="An update on potential local impacts on jobs and businesses across Canada"
	/>

	<div class="text">

		<AuthorDate
			authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://jamaps.github.io/' target='_blank'>Jeff Allen</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>"
			date="February 2026"
		/>
	
	</div>

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
			Canada's softwood lumber and medium heavy duty vehicle (truck) industries are some of the country's biggest export items. 
			We are one of the largest producers of softwood lumber across the world, which <a href="https://www150.statcan.gc.ca/n1/pub/11-621-m/11-621-m2022023-eng.htm"> was valued at $10 billion in 2020</a> and supplied <a href="https://natural-resources.canada.ca/forest-forestry/forest-industry-trade/canada-s-softwood-lumber-industry">80% of U.S.'s softwood lumber imports</a>. 
			Softwood, fast growing trees that have a wide range of uses in framing material and furniture, accounts for <a href="https://www150.statcan.gc.ca/n1/pub/11-621-m/11-621-m2022023-eng.htm">98%</a> of all lumber types in Canada and is a major industry across the interior regions of provinces. 
			Especially in British Columbia, the softwood industry fills in <a href="https://edac.ca/wp-content/uploads/2025/02/Canada-U.S.-Core-Facts-January-2025.pdf?">~46% of Canada's lumber exports</a> to the U.S.. 
			<!-- B.C., Quebec, Ontario, Alberta, and New Brunswick account for <a href="https://edac.ca/wp-content/uploads/2025/02/Canada-U.S.-Core-Facts-January-2025.pdf?">95% of softwood lumber production</a>. -->
			Medium heavy duty vehicles (MHDVs) consist of garbage trucks, long haul trucks and delivery vehicles ranging from classes 2B to 8 (8,501 - 33,000+ lbs). 
			This sector is often grouped with all vehicles and parts, which accounted for <a href="https://international.canada.ca/en/global-affairs/corporate/transparency/briefing-documents/parliamentary-committee/2023-06-13-ciit?">13.2% of the share of exported merchandises to the U.S.</a>, the second largest category.
		</p>

		<h2>
			Background: Canada-US Lumber and Trucks Trade
		</h2>
		<p>
			The Canadian lumber economy is deeply integrated with the U.S. materials industry.
			In 2020, nearly 70% of all softwood lumber production was exported, with <a href="https://natural-resources.canada.ca/forest-forestry/forest-industry-trade/canada-s-softwood-lumber-industry">84% of those exports to the U.S.</a> due to the demand for lumber in housing and construction.
			Despite Canada being the primary source of imported lumber (<a href="https://wits.worldbank.org/CountryProfile/en/Country/USA/Year/LTST/TradeFlow/Import/Partner/by-country/Product/44-49_Wood">~40% of U.S. wood product imports</a>), the U.S. has imposed duties over the past four decades to protect their domestic lumber industry. 
			Canadian lumber companies have fought against anti-dumping (AD) and countervailing duties (CVD) through NAFTA, WTO, U.S. courts, and more recently, CUSMA. 
			Canada and the U.S. have agreed upon a <a href="https://www.treaty-accord.gc.ca/text-texte.aspx?id=105072&lang=eng">Softwood Lumber Agreement</a> (SLA) from 2006-2015, which proved stable for Canadians; however, the duties returned in 2017 19 months after the agreement expired.
			During COVID-19, <a href="https://www150.statcan.gc.ca/n1/pub/62f0014m/62f0014m2022011-eng.htm?">the producer price of softwood lumber more than tripled</a> because of an increase in demand for single detached home construction driven by excess household savings and low interest rates.
			Since then, lumber has been <a href="https://international.canada.ca/en/global-affairs/corporate/reports/chief-economist/monthly/2025-08">falling in exports since 2020</a>, a trend exacerbated by the tariffs.
			
			The chart below shows Canada’s lumber exports to the U.S. in dollar amounts for HS code 4407, which is mainly softwood lumber. While the proportion of Canada’s exports to the U.S. compared to the world has remained consistent from 2019 - 2024, it dropped in 2025 due to Trump's second administration. 

			For exports to the U.S., Global Affairs Canada <a href="https://www.international.gc.ca/controls-controles/softwood-bois_oeuvre/index.aspx?view=d&lang=eng">reported an estimated $6.06 billion</a> in exports in 2025 (calculated from the monthly U.S. exports report).
		</p>

		<p>
			Tensions between Canada and U.S.'s automotive and truck industry have increased since Trump's presidency. 
			Canada makes roughly <a href="https://edac.ca/wp-content/uploads/2025/02/Canada-U.S.-Core-Facts-January-2025.pdf?">4% of U.S. auto parts</a> and builds <a href="https://www.cvma.ca/wp-content/uploads/2025/03/CVMA-5-facts-about-Canada-US-auto-trade.pdf">9% of U.S. vehicles</a>, but is a key component in keeping their assembly factories running. 
			For example, in 2023, <a href="https://edco.on.ca/wp-content/uploads/EN_Canada-U.S.-Core-Facts_Feb-21-2025-update.pdf?">50% of Canadian auto exports went to Michigan alone</a>, where many of Windsor's engine plants supply Ford's assembly plants. 
			Automotive tariffs (passenger vehicles and light trucks) were placed in effect in spring 2025 with medium and heavy duty vehicle tariffs coming into effect later in the fall.
			In anticipation of the tariffs to MHDVs, <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260108/dq260108a-eng.htm">October sales rose 24.7%</a> compared to September 2025. 
			In November 2025, <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260129/dq260129a-eng.htm">MHDV exports fell 53.8% compared to October 2025</a>, denoting significant changes due to the tariffs. The broader automotive sector was also affected by semiconductor shortages, resulting in a <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260115/dq260115a-eng.htm">15.9% decline in motor vehicle manufacturing sales, a 6.3% decline in motor vehicle parts sales month over month, and motor vehicle sales down 20.7% from November 2024.</a> 
		</p>

	</div>

	<ImageSingle
		imageURL="./lumber-trucks/img/estimated_exports_lumber_2019_2024.png"
		caption='Estimated export value of Canadian HS code 4407 (sawn wood >6mm) by year to the U.S.'
		source='<br><a href="https://comtradeplus.un.org/">United Nations Trade Statistics</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			This pattern holds true in 2025. On October 14, 2025, Trump's second administration imposed a 10% global tariff on softwood lumber with 25% on certain furniture & kitchen cabinet items. This 25% was set to increase to 30% for furniture and 50% for kitchen cabinets, but was <a href="https://www.whitehouse.gov/presidential-actions/2025/12/amendments-to-adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/">delayed until January 2027</a>. 
			Across all countries, the Canadian forestry industry experienced <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260130/dq260130a-eng.htm">a 3 month consecutive decline in late 2025</a>.
			In response, the Carney government retaliated with <a href="https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs/complete-list-us-products-subject-to-counter-tariffs.html">their own tariffs</a> and is bolstering the sector by granting loans to help companies pivot into new markets <a href="https://www.cbc.ca/news/canada/british-columbia/bc-canada-lumber-understanding-china-carney-visit-9.7047096">export overseas such as China</a>.
			A focus on domestic investment and diversification is in motion with an emphasis on <a href="https://www.pm.gc.ca/en/news/news-releases/2025/11/26/prime-minister-carney-announces-new-measures-protect-and-transform">building with local lumber</a>.
		</p>

		<p>
			On November 1st, 2025, <a href="https://www.reuters.com/legal/legalindustry/truck-tariffs-signal-broader-us-supply-chain-rebuild--pracin-2025-11-10/">medium and heavy duty vehicle and bus tariffs were imposed</a>. 
			This category not only includes the MHDVs, but also buses, which now covers the vast majority of manufactured vehicles.
			To further the incentive of centralizing U.S. manufacturing, the government has given an incentive of a tariff relief of 3.75% if companies build their MHDVs in the U.S..
			On February 5, 2026, Carney announced a push for <a href="https://www.ttnews.com/articles/canada-scrap-eve-rules">an import credit system</a>, which would alleviate tariffs for companies that meet a certain production threshold. This follows a $2.3 billion program for Canadians to purchase EV vehicles in partnerships with Chinese automakers.
		</p>

	</div>

	<ImageSingle
		imageURL="./lumber-trucks/img/estimated_exports_lumber_2025.png"
		caption='Estimated export value of Canadian softwood lumber by foot board measure and monthly reference price'
		source='<br><a href="https://www.international.gc.ca/controls-controles/softwood-bois_oeuvre/index.aspx?view=d&lang=eng">Global Affairs Canada on softwood lumber</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			Similar to the findings in our <a href="/potential-local-impacts">preliminary findings</a>, Canada’s lumber and truck industry is highly tied to the U.S. due to the geographic convenience and demand of U.S. imports.
		</p>

		<h2>
			Current tariff landscape
		</h2>

		<p>
			The U.S. government continues to enact and change plans with tariffs as negotiations continue. Here is an updated list of all the tariffs currently in place:
		</p>

		<ul>
			<li><a href="https://www.theglobeandmail.com/business/article-economy-gdp-growth-tariff-canada-us-trump-tariff-lumber/" target="_blank">Duties
			of approximately 45% on Canadian softwood lumber (10% new tariffs, 35% anti-dumping & countervailing)</a> 
			There was a 25% tariff on upholstered furniture, kitchen cabinets, and vanities looped under this section as well which was <a href="https://www.whitehouse.gov/presidential-actions/2025/09/adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/" target="_blank">planned to be increased</a> for January 1, 2026, 
			but <a href="https://www.whitehouse.gov/fact-sheets/2025/12/fact-sheet-president-donald-j-trump-adjusts-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/">the increase has been delayed</a>;</li>
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
			The U.S. government remains to enact de-minimis and the Canadian government continues to <a href="https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs/complete-list-us-products-subject-to-counter-tariffs.html" target="_blank">enforce retaliatory tariffs on steel, aluminum and autos</a>. 
			The Canadian government has <a href="https://www.pm.gc.ca/en/news/backgrounders/2025/09/05/prime-minister-carney-launches-new-measures-protect-build-and">provided relief through programs</a> like the <a href="https://www.cfib-fcei.ca/en/tools-resources/regional-tariff-response-initiative-rtri">Regional Tariff Response Initiative</a>, with $1 billion going into it over 3 years from September 5 , 2025.
		</p>

		<p>
			AD and CVD rates have been imposed since the 1980s. However, from 2019 to 2023, AD & CVD rates of imported softwood lumber increased significantly with rates reaching <a href="https://www.congress.gov/crs-product/R48781?">17% in 2019 to 35% in 2023 for AD</a>, with combined AD/CVD rates pushing in the 40 percentile range depending on the company. 
			Meanwhile, MHDVs used to remain safe under Section 232 national security tariffs until these tariffs.
		</p>

		<p>
			In 2026, the situation is still unpredictable, such as with the last minute tariff changes to upholstered furniture, kitchen cabinets and vanities. 
			Lumber is <a href="https://natural-resources.canada.ca/domestic-international-markets/current-lumber-pulp-panel-prices#softwood">up in price in January 2026</a> according to the <a href="https://madisonsreport.com/lumber-market-updates/">Madison's Lumber Reporter</a>, a weekly newsletter on Canadian & US lumber, but producers are hesitant to push production due to the uncertainties.
		</p>

		<h2>
			The impact of lumber in British Columbia
		</h2>

		<p>
			For British Columbia, Canada's largest exporter of lumber, the quantity of exported softwood lumber has dropped year over year since 2019. Even in 2025, across January to October, export volume dropped another ~10%.
		</p>

		<ImageSingle
			imageURL="./lumber-trucks/img/bcquantshare.png"
			caption='British Columbia quantity of softwood lumber in x1000m<sup>3</sup> and percentage of lumber exported to the U.S. year over year.'
			source='<br><a href="https://www2.gov.bc.ca/gov/content/industry/forestry/competitive-forest-industry/forest-industry-economics/forest-product-exports">B.C. forest product exports</a>'
			maxWidth='680px'
			link='No'
		/>
		
		<p>
			While the percent share of exports to the U.S. hasn't dropped, the quantity of exports follow a similar pattern to the global lumber exports (4407) shown in the first graph.
		</p>

		<h2>
			Map findings
		</h2>

		<p>
		</p>
		Using our  <a href="./map">mapping and visualization tool</a> we can trace potential tariff vulnerabilities across Canada. 
		The new softwood lumber tariffs widely affected interior regions of provinces, most notably the B.C. Interior, Northern Québec, Northern Ontario, and the Maritimes.

	</div>

	<ImageSingle
		imageURL="./lumber-trucks/img/beforeafter.png"
		caption='Potential effects of lumber before and after October 14, 2025, when softwood lumber tariffs were enacted.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			The next map shows the total proportion of employees by primary residence estimated to be vulnerable to Trump’s tariffs in the B.C. Interior. 
			The employees and businesses in the B.C. forestry industry has been hit hard for this region as they produce the most softwood lumber for the province.
		</p>

	</div>

	<ImageSingle
		imageURL="./lumber-trucks/img/interiorbcemployeeshome.png"
		caption='Proportion of employees by place of residence estimated to be vulnerable in the B.C. Interior region.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			The medium heavy duty vehicle section highlights the regional specialization of manufacturing dependent cities.
			For example, the Greater Golden Horseshoe displays the proportion of workers (as place of work) potentially affected by the truck tariffs. 
		</p>

	</div>

	<ImageSingle
		imageURL="./lumber-trucks/img/csdtrucksemployeeswork.png"
		caption='Potential direct exposure of tariffs to employees (work) in the truck industry by census subdivision.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			Our maps show that the impacts of the tariffs are consistent with export reports across lumber and truck industries. 
			Logging dependent cities like Quesnel, Campbell River, Prince George, Kapuskasing and La Tuque are feeling the brunt of these effects today.
			Likewise, truck manufacturing regions like Guelph, Windsor and Ingersoll are facing a decrease in manufacturing.
			The supply chain, constrained by log shortages and adjacent tariffs in steel and automotives, are hindering lumber and truck exports in many avenues.
			While the Canadian government does recognize and supports these industries through financial aid, the future remains uncertain for the bilateral interdependency the two countries have.
		</p>

		<p>
			Check out the <a href="../potential-local-impacts">preliminary report</a> on our findings, explore our <a href="../map">interactive mapping tool</a> to see the potential impacts across Canadian neighbourhoods, or view the <a href="../cma-ranking-charts">city ranking charts</a> for aggregate impacts.
		</p>

		<p>
			<a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file">A full accounting of the technical details, data processing steps, and associated code can be found here.</a>
		</p>

	</div>

	<Footer />

</main>