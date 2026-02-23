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

	<title>The impacts of lumber tariffs on Canadian cities | School of Cities</title>

	<meta name="description" content="An update on potential local lumber impacts on jobs and businesses across Canada via maps and charts" />
	<meta name="author" content="School of Cities">
	<meta rel="canonical" href="https://schoolofcities.github.io/tariffs/lumber">

	<meta property="og:title" content="Lumber and Trucks" />
	<meta property="og:description" content="An update on potential local lumber impacts on jobs and businesses across Canada via maps and charts" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://schoolofcities.github.io/tariffs/lumber" />
	<meta property="og:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" />
	<meta property="og:locale" content="en_CA">

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="Lumber and Trucks" />
	<meta name="twitter:description" content="An update on potential local lumber impacts on jobs and businesses across Canada via maps and charts" />
	<meta name="twitter:site" content="https://schoolofcities.github.io/tariffs/lumber" />
	<meta name="twitter:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" /> 

</svelte:head>


<Password/>


<main>

	<Logo logoType="Blue" backgroundColor="var(--brandWhite)"/>

	<ImageSingle
		imageURL="./lumber/img/lumberhorizontal.png"
		caption=''
		source=''
		maxWidth='685px'
		link='No'
	/>

	<TitleStandard
		title="The impacts of lumber tariffs on Canadian cities"
		subtitle="An update on potential local lumber impacts on jobs and businesses across Canada"
	/>

	<div class="text">

		<AuthorDate
			authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://jamaps.github.io/' target='_blank'>Jeff Allen</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>"
			date="February 2026"
		/>
	
	</div>

	<div class="text">	

		<p>
			Canada's lumber industry is a big export item for Canada.
		</p>

		<p>	
			Canada is one of the world's largest producers of softwood lumber, which <a href="https://www150.statcan.gc.ca/n1/pub/11-621-m/11-621-m2022023-eng.htm"> was valued at $10 billion</a> and supplied <a href="https://natural-resources.canada.ca/forest-forestry/forest-industry-trade/canada-s-softwood-lumber-industry">80% of the United States' softwood lumber imports</a> in 2020. 
			Softwood, fast growing trees that have a wide range of uses in framing material and furniture, accounts for <a href="https://www150.statcan.gc.ca/n1/pub/11-621-m/11-621-m2022023-eng.htm">98%</a> of all lumber types in Canada and is a major industry across the interior regions of provinces — especially in British Columbia, where the softwood industry accounts for <a href="https://edac.ca/wp-content/uploads/2025/02/Canada-U.S.-Core-Facts-January-2025.pdf?">~46% of Canada's lumber exports</a> to the U.S.. 
			<!-- B.C., Quebec, Ontario, Alberta, and New Brunswick account for <a href="https://edac.ca/wp-content/uploads/2025/02/Canada-U.S.-Core-Facts-January-2025.pdf?">95% of softwood lumber production</a>. -->
		</p>

		<h2>
			Background: Canada-U.S. lumber trade
		</h2>
		<p>
			The Canadian lumber economy is deeply integrated with the U.S. materials industry.
			In 2020, nearly 70% of all softwood lumber production was exported, with <a href="https://natural-resources.canada.ca/forest-forestry/forest-industry-trade/canada-s-softwood-lumber-industry">84% of those exports to the U.S.</a> due to the demand for lumber in housing and construction.
		</p>

		<p>	
			Despite Canada being its primary source of imported lumber (<a href="https://wits.worldbank.org/CountryProfile/en/Country/USA/Year/LTST/TradeFlow/Import/Partner/by-country/Product/44-49_Wood">~40% of U.S. wood product imports</a>), the U.S. has imposed duties over the past four decades to leverage their domestic lumber industry. 
			Canadian lumber companies have fought against anti-dumping (AD) and countervailing duties (CVD) through NAFTA, WTO, U.S. courts, and more recently, CUSMA. 
			Both countries have agreed upon a <a href="https://www.treaty-accord.gc.ca/text-texte.aspx?id=105072&lang=eng">Softwood Lumber Agreement</a> (SLA) from 2006-2015, which proved stability for Canadians; however, the duties returned in 2017, 19 months after the agreement expired.
			During COVID-19, <a href="https://www150.statcan.gc.ca/n1/pub/62f0014m/62f0014m2022011-eng.htm?">the producer price of softwood lumber more than tripled</a> because of an increase in demand for single detached home construction driven by excess household savings and low interest rates.
			Since then, lumber has been <a href="https://international.canada.ca/en/global-affairs/corporate/reports/chief-economist/monthly/2025-08">falling in exports</a>, a trend exacerbated by the tariffs.
		</p>

		<p>	
			The chart below shows Canada’s lumber exports to the U.S. in dollar amounts for HS code 4407, which is mainly softwood lumber. 
			While the proportion of Canada’s exports to the U.S. compared to the world has remained consistent from 2019 - 2024, the <a href="https://tradingeconomics.com/commodity/lumber">dollar value of lumber fluctuated</a> due to inflation, COVID-19, and supply & demand, leading to rises and falls.
			
		</p>

		<GraphicSingle
			svg360="./lumber/web-svg/slw_yearly_export_value-360.svg"
			svg720="./lumber/web-svg/slw_yearly_export_value-720.svg"
			source='Source: <a href="https://comtradeplus.un.org/" target="_blank">United Nations Trade Statistics</a>'
		/>

		<p>
			Due to the price surges from the home improvement boom in 2021, <a href="https://fortune.com/2021/07/20/lumber-prices-2021-chart-price-of-lumber-july-2021-update-cost-of-wood/">houseowners decreased their DIY projects and mills caught up on supply</a>. 
			Lumber briefly returned to the pre-pandemic price range in July 2021, but in November, a <a href="https://www.cbc.ca/news/canada/british-columbia/landslides-disaster-logging-wildfires-study-1.7490041">historic landslide event</a> that killed 5 and forced 18,000 people to evacuate, seized supply from Canada's largest softwood exporter, causing prices to surge again.
			After supply recovered in 2022, the <a href="https://www.congress.gov/crs-product/IN12388">Federal Reserve hiked up interest rates to over 5% to combat inflation</a>, which plummeted demand. 
			Therefore, the lack of demand decreased the overall export valuation of softwood lumber.
		</p>
			

	</div>



	<div class="text">

		<p>
			Economic fluctuation between the borders affects lumber value as seen in the figure below. In August 2025, the <a href="https://www.trade.gov/press-release/commerce-department-announces-final-results-softwood-lumber-canada-countervailing">U.S. Department of Commerce doubled CVDs</a>, lowering imports from Canada.
			On October 14, 2025, Trump's second administration imposed a 10% global tariff on softwood lumber with 25% on certain furniture & kitchen cabinet items. This 25% was set to increase to 30% for furniture and 50% for kitchen cabinets, but was <a href="https://www.whitehouse.gov/presidential-actions/2025/12/amendments-to-adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/">delayed until January 2027</a>. 
			Across all countries, the Canadian forestry industry experienced <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260130/dq260130a-eng.htm">a 3 month consecutive decline in late 2025</a>.
			For exports to the U.S., Global Affairs Canada <a href="https://www.international.gc.ca/controls-controles/softwood-bois_oeuvre/index.aspx?view=d&lang=eng">reported an estimated $6.06 billion</a> in softwood lumber exports in 2025 (calculated from the monthly U.S. exports report).
		</p>

			<GraphicSingle
					svg360="./lumber/web-svg/slw_monthly_2025-360.svg"
					svg720="./lumber/web-svg/slw_monthly_2025-720.svg"
					source='Source: <a href="https://www.international.gc.ca/controls-controles/softwood-bois_oeuvre/index.aspx?view=d&lang=eng" target="_blank">Global Affairs Canada on softwood lumber</a>'
			/>

		</div>

		
			<div class="text">


		<p>
			In response, the Carney government retaliated with <a href="https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs/complete-list-us-products-subject-to-counter-tariffs.html">their own tariffs</a> and is bolstering the sector by granting loans to help companies pivot into new markets <a href="https://www.cbc.ca/news/canada/british-columbia/bc-canada-lumber-understanding-china-carney-visit-9.7047096">export overseas such as China</a>.
			A focus on domestic investment and diversification is in motion with an emphasis on <a href="https://www.pm.gc.ca/en/news/news-releases/2025/11/26/prime-minister-carney-announces-new-measures-protect-and-transform">building with local lumber</a>.
		</p>

		<h2>
			Current tariff landscape
		</h2>

		<p>
			Similar to the findings in our <a href="/potential-local-impacts">preliminary analysis</a>, Canada’s lumber and truck industry is highly tied to the U.S. due to the geographic convenience and demand of U.S. imports.
			The U.S. government continues to enact and change plans with tariffs as negotiations continue. 
			See our <a href="../current-tariffs">current tariffs</a> page for a full list of tariffs currently in place.
		</p>

		<p>
			AD and CVD rates have been imposed since the 1980s. However, from 2019 to 2023, these rates increased significantly for imported softwood lumber, reaching <a href="https://www.congress.gov/crs-product/R48781?">17% in 2019 to 35% in 2023 for AD</a>, with combined AD/CVD rates pushing in the 40th percentile range depending on the year & company. 
			These tariffs have impacted MHDVs which used to be protected by Section 232 national security tariffs.
		</p>

		<p>
			In 2026, the situation is still unpredictable, (for example, the recent last minute tariff changes to upholstered furniture, kitchen cabinets and vanities.)
			Lumber is <a href="https://natural-resources.canada.ca/domestic-international-markets/current-lumber-pulp-panel-prices#softwood">up in price in January 2026</a> according to the <a href="https://madisonsreport.com/lumber-market-updates/">Madison's Lumber Reporter</a>, a weekly newsletter on Canadian & US lumber, but producers are hesitant to push production due to the uncertainties.
		</p>

		<h2>
			The impact of lumber in British Columbia
		</h2>

		<p>
			For British Columbia, Canada's largest exporter of lumber, the quantity of exported softwood lumber has dropped year over year since 2019. Even in 2025, across January to October, <a href="https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/forest-industry-economics/forest-product-exports/forests_product_exports_-_2025-10.pdf">export volume dropped another ~10%</a>.
		</p>

		<GraphicSingle
			svg360="./lumber/web-svg/slw_quan_share_BC-360.svg"
			svg720="./lumber/web-svg/slw_quan_share_BC-720.svg"
			source='Source: <a href="https://www2.gov.bc.ca/gov/content/industry/forestry/competitive-forest-industry/forest-industry-economics/forest-product-exports" target="_blank">B.C. forest product exports</a>'
		/>
		
		<p>
			Note that the percent share of exports to the U.S. hasn't fluctuated much and that lumber quantity fell from 2022, similar to the global lumber exports (4407) shown in the first graph. We can also infer that while lumber fell from 2019 to 2020, B.C. tried to keep up with high demand in 2021.
		</p>

		<h2>
			Map findings
		</h2>

		<p>
			Using our  <a href="./map">mapping and visualization tool</a> we can trace potential tariff vulnerabilities across Canada. 
			The new softwood lumber tariffs widely affected interior regions of provinces, most notably the B.C. Interior, Northern Québec, Northern Ontario, and the Maritimes.
		</p>
		
		
	</div>

	<ImageSingle
		imageURL="./lumber/img/beforeafter.png"
		caption='Jobs in the lumber industry before and after October 14, 2025, when softwood lumber tariffs were enacted.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			The next map shows the total proportion of employees by primary residence estimated to be vulnerable to Trump’s tariffs in the B.C. Interior, which produces the most softwood lumber for the province.
		</p>

	</div>

	<ImageSingle
		imageURL="./lumber/img/interiorbcemployeeshome.png"
		caption='Proportion of employees by place of residence estimated to be vulnerable in the B.C. Interior region.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">
		<p>
			Finally, here is an example of New Brunswick's impacted businesses across census subdivisions before and after October 14. 
			Due to the tough financial pressure on lumber companies across the province, Susan Holt, the Premier, has <a href="https://www.ctvnews.ca/atlantic/new-brunswick/article/nb-premier-says-province-needs-tariff-deal-on-softwood-lumber-soon/">advocated for progress on negotiations</a>.
		</p>
	</div>

	<ImageSingle
		imageURL="./lumber/img/newbrunswickcsd.png"
		caption='Proportion of businesses estimated as vulnerable in New Brunswick by census subdivision.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			Our maps show that the impacts of the tariffs are consistent with export reports across the lumber industry. 
			Logging dependent cities like Quesnel, Campbell River, Prince George, Kapuskasing and La Tuque are feeling the brunt of these effects today.
			The supply chain, constrained by log shortages and adjacent tariffs in steel and automotives, are hindering lumber exports in many avenues.
			While the Canadian government does recognize and supports the industry through financial aid, the future remains uncertain due the bilateral interdependency of the U.S. and Canada.
		</p>

		<p>
			Read about the <a href="../trucks">impact of truck tariffs</a> on Canadian cities, check out the <a href="../potential-local-impacts">preliminary report</a> on our findings, explore our <a href="../map">interactive mapping tool</a> to see the potential impacts across Canadian neighbourhoods, or view the <a href="../cma-ranking-charts">city ranking charts</a> for aggregate impacts.
		</p>

		<p>
			<a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file">A full accounting of the technical details, data processing steps, and associated code can be found here.</a>
		</p>

	</div>

	<Footer />

</main>