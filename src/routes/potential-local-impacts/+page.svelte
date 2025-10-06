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


	<!-- <ImageSingle
		imageURL="./potential-local-impacts/img/business-impact-all-720.png"
		caption='Map of Canada showing % potential direct exposure to businesses related to all goods currently subject to tariffs'
		source='<a href="./map">Click here to view interactive map</a>'
		maxWidth='720px'
		link='No'
	/> -->

	<TitleStandard
		title="Mapping tariffs"
		subtitle="Potential local impacts on jobs and businesses across Canada"
	/>

	<div class="text">

		<AuthorDate
			authors="<a href='' target='_blank'>Tara Vinodrai</a>, <a href='' target='_blank'>Karen Chapple</a>, <a href='' target='_blank'>Jeff Allen</a>, Muhammad Khalis Bin Samion, Eli Easton, Rick DiFrancesco"
			date="October 2025"
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
			Since Donald Trump was elected as the 47th President of the United States, tariffs and trade have become hot topics. The US government has continued to announce tariffs on goods exported from Canada and other countries to the United States. For Canada, one of the largest trading partners with the US, the introduction of tariffs has led policymakers, politicians and the public to ask questions about where the impacts might be felt now and in the longer run. From resource-dependent communities to manufacturing hubs, local economies across Canada are tied to the US and the global economy in complex ways. But, what places are most vulnerable to Trump’s tariffs? To answer this question, we created a <a href="./map">mapping and visualization tool</a> to trace out the tariff exposure of local economies across Canada’s vast geography. In doing so, our work offers a window into how jobs and businesses are influenced and how the fortunes of cities and regions across Canada may be altered.
		</p>

		<h2>
			Background: Canada-US Trade
		</h2>
		<p>
			The Canadian economy is deeply integrated with the US economy. In 2023, Canada-US trade surpassed $1.3 trillion (CAD), with approximately $3.5 billion (CAD) worth of goods and services being exchanged daily. Indeed, the United States is Canada’s largest export destination, accounting for 76.4% of Canadian exports, with no other trading partner accounting for more than 4% of export trade. While Canada relies heavily on the US market for sales, there is greater diversity in the source of imports to Canada. Still, almost half of Canada’s imports (49.2%) are from the United States.
		</p>

	</div>

	<GraphicSingle
		svg360="./potential-local-impacts/web-svg/export-import-table-360.svg"
		svg720="./potential-local-impacts/web-svg/export-import-table-720.svg"
	/>


	<div class="text">

		<p>
			This pattern holds true over time. The charts below show Canada’s exports to the US and the rest of the world between 2005 and 2024. The proportion of Canada’s exports to the US has decreased slowly over time, from 83.8% in 2005 to 76.4% in 2024. There was a slight decline in the proportion of Canada’s exports to the US between 2018 and 2020, potentially due to the imposition of tariffs by the US under the first Trump administration.
		</p>

		<p>
			This longstanding trading relationship is codified into various trade agreements, beginning with the Canada-US Free Trade Agreement (1989) and the North American Free Trade Agreement (1994), which extended trade relations to include Mexico. In 2020, NAFTA was replaced by Canada-United States-Mexico Agreement (CUSMA), an updated trilateral agreement that provides preferential, duty-free treatment for goods that meet specific rules of origin.  
		</p>

	</div>

	<GraphicSingle
		svg360="./potential-local-impacts/web-svg/exports-over-time-360.svg"
		svg720="./potential-local-impacts/web-svg/exports-over-time-720.svg"
	/>

	<div class="text">

		<p>
			Overall, due to the tight integration of supply chains, trade agreements, proximity, and longstanding business relationships, Canada’s trading activities remain tied to the US economy. Given Canada’s dependence on the US market, it is no surprise that the ongoing trade war and escalation of tariffs on various goods is cause for deep concern amongst Canadian politicians, policymakers and the public.
		</p>

		<h2>
			Current tariff landscape
		</h2>

		<p>
			Beginning in February 2025, the US government has announced (as well as retracted and changed) an extensive suite of tariffs targeting Canada and other countries. The unpredictable shifts in tariff actions introduce challenges in keeping track and staying up to date. Several organizations maintain real-time information on tariff announcements affecting Canada and other trading nations (<a href="https://www.piie.com/blogs/realtime-economics/2025/trumps-trade-war-timeline-20-date-guide" target="_blank">for example, here</a>). 
		</p>

		<ul>
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
			the US from the 25% announced in February 2025 (effective: June 3,
			2025);</li>
			<li>A <a href="https://www.tradecommissioner.gc.ca/en/market-industry-info/search-country-region/country/canada-united-states-export/us-tariffs/supporting-exporters-through-tariff-challenges.html" target="_blank">25%
			tariff on automobiles and light trucks</a> imports; for
			Canada, this applies to the non-US content of vehicles imported
			under CUSMA (effective: April 3, 2025);</li>
			<li>A <a href="https://www.tradecommissioner.gc.ca/en/market-industry-info/search-country-region/country/canada-united-states-export/us-tariffs/supporting-exporters-through-tariff-challenges.html" target="_blank">25%
			tariff on non-CUSMA compliant auto parts</a> (effective:
			May 3, 2025);</li>
			<li>A <a href="https://www.whitehouse.gov/presidential-actions/2025/07/adjusting-imports-of-copper-into-the-united-states/" target="_blank">50%
			tariff on copper</a> (effective: August 1, 2025); and</li>
			<li><a href="https://globalnews.ca/news/11324819/softwood-lumber-duties/" target="_blank">Duties
			of approximately 35% on Canadian softwood lumber</a> (at
			time of writing, we note that lumber tariffs are <a href="https://www.whitehouse.gov/presidential-actions/2025/09/adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/" target="_blank">set
			to increase</a> and widen in their scope).</li>
		</ul>

		<p>
			Additionally, the US government has <a href="https://www.federalregister.gov/documents/2025/09/02/2025-16802/notice-of-implementation-of-the-presidents-executive-order-14324-suspending-duty-free-de-minimis" target="_blank">eliminated <i>de minimis</i> treatment</a> for low-value shipments (defined as those under $800 in value). In other words, shipments to the US from Canada that are under $800 are now subject to tariffs. 
		</p>

		<p>
			In response, the Canadian government has announced retaliatory tariffs and other measures, although not all of these have been implemented. And, trade negotiations and discussions with the US continue. As of September 1, 2025, the Canadian government lifted many of its counter-tariffs noting that many Canadian exporters (with the exceptions of those related to automotive, aluminum, and steel) are able to avoid tariffs through compliance with CUSMA. Canada’s Department of Finance maintains an up-to-date <a href="https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs/complete-list-us-products-subject-to-counter-tariffs.html" target="_blank">list of Canadian tariffs</a> on US exports.
		</p>

		<p>
			Overall, the situation remains fluid and unpredictable, adding uncertainty to markets and confounding analysis.
		</p>

		<h2>
			Measuring the impact of US tariffs on Canada
		</h2>

		<p>
			A recent report from the <a href="https://www.rbc.com/en/thought-leadership/a-playbook-for-how-to-measure-a-tariff-shock-in-canada/"target="_blank">Royal Bank of Canada</a> notes that estimating the impacts of tariffs on the Canadian economy is tricky business, especially due to uncertainty created by an ever-changing tariff landscape. Factors that influence these impacts include which goods are subject to tariffs and the magnitude of those tariffs. The responses of consumers, businesses, banks, and governments also play a role. These actions may include retaliatory measures, interest rate changes, and efforts to diversify markets and supply chains. Some consumers may choose to buy local or Canadian products or curb travel to the United States. In addition, spending and investment decisions, as well as programs designed to support businesses and industries at risk, can shape outcomes.
		</p>

		<p>
			Economists and policymakers at banks, think tanks and other organizations have published extensively on the possible impacts on the Canadian economy. At the national level, the <a href="https://www.bankofcanada.ca/publications/mpr/mpr-2025-01-29/in-focus-1/" target="_blank">Bank of Canada</a> has used models to demonstrate how US tariffs may affect inflation and GDP growth.
		</p>

		<p>
			Observers have also considered sub-national impacts. For example, the Business Data Lab at the Canadian Chamber of Commerce conducted an analysis to <a href="https://businessdatalab.ca/publications/which-canadian-cities-are-most-exposed-to-trumps-tariffs/" target="_blank">examine which Canadian cities might be most exposed to tariffs</a>. Similarly, the Conference Board of Canada has estimated the <a href="https://www.conferenceboard.ca/insights/the-true-cost-of-trump-tariffs-city-impacts/" target="_blank">impact of tariffs across Canada’s largest metropolitan regions</a>.
		</p>

		<h2>Methods</h2>

		<p>
			In our initial work, we focus on identifying potential direct exposure to tariffs. In other words, we look at where the jobs and businesses are that make goods subject to US tariffs and that are more likely to be exported to the US market. 
		</p>

		<p>
			Estimating the potential exposure of jobs and business to US tariffs at the local level is a complex task and proved to be a challenging undertaking, especially as the scope and magnitude of US-imposed tariffs are constantly evolving and changing. Our analysis required accessing data, concordance tables, and information from several Canadian and US government agencies, including Statistics Canada, US Customs and Border Protection, the US International Trade Commission, the US Department of Commerce, and the US Census Bureau, amongst others. We identified the specifics goods subject to tariffs, using the Harmonized Tariff Schedule for the United States and matched those goods (classified using HS codes) to specific industries (classified using the North American Industrial Classification System, NAICS). Using this information, we were able to map the location of jobs (based both on where people work and where people live) and businesses at the dissemination area level for all of Canada. To focus on how vulnerable these places were to US-related tariffs, we weight our estimates based on the extent to which the industries involved were oriented to the US market measured by export intensity. 
		</p>

		<p>
			<a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file">A full accounting of the technical details, data processing steps, and associated code can be found here.</a>
		</p>

		<h2>
			Uneven geographies of trade exposure
		</h2>

		<p>
			Using our  <a href="./map">mapping and visualization tool</a> we can trace potential tariff vulnerabilities across Canada. Overall, our results show that tariffs impact Canadian cities and communities from coast to coast to coast. 
		</p>

	</div>

	<ImageSingle
		imageURL="./potential-local-impacts/img/business-impact-all-720.png"
		caption='Potential direct exposure to businesses related to all goods currently subject to tariffs (as of September 1, 2025)'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			However, our sector-specific results underscore underlying regional specialization patterns across Canada. For example, the following map shows that there are widespread vulnerabilities to workers (based on place of residence) due to US automotive tariffs across the Greater Golden Horseshoe. This is not surprising given the historic presence of the automotive industry in southern Ontario.
		</p>

	</div>

	<ImageSingle
		imageURL="./potential-local-impacts/img/auto-southern-ontario-all-720.png"
		caption='Potential direct exposure of tariffs to employees in the automotive industry.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>


	<div class="text">

		<p>
			The next map shows the total proportion of employees by place of work estimated to be vulnerable to Trump’s tariffs in the Vancouver metropolitan region. The jobs and businesses most at risk are on the outer edges of the metropolitan region. This reflects the areas of Vancouver’s regional economy where there are designated employment lands, especially along the Fraser River where there is a concentration of industrial activity. 
		</p>

	</div>

	<ImageSingle
		imageURL="./potential-local-impacts/img/vancouver-noncusma-placeofwork-720.png"
		caption='Proportion of employees by place of work estimated to be vulnerable to Trump’s tariffs in the Vancouver metropolitan region.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			Lastly, this map shows the number of businesses that have the potential to be directly exposed to tariffs on energy and natural resources in Calgary. In this case, our map shows that it is the headquarters of companies located in Calgary’s downtown that are most likely to be affected.			
		</p>

	</div>

	<ImageSingle
		imageURL="./potential-local-impacts/img/calgary-businesses-energy-720.png"
		caption='Number of businesses that have the potential to be directly exposed to tariffs on energy and natural resources in Calgary.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			While we have provided only a few examples of the highly uneven patterns of potential direct exposure across some of Canada’s largest cities, these patterns extend to other parts of Canada. For example, potential vulnerabilities to aluminum and steel tariffs can be seen across Canada, but are more acute across southwestern Ontario and parts of Quebec. And, we can identify vulnerabilities related to lumber tariffs, which are set to <a href="https://www.whitehouse.gov/presidential-actions/2025/09/adjusting-imports-of-timber-lumber-and-their-derivative-products-into-the-united-states/" target="_blank">increase to 45% on October 14, 2025</a>, and widen in their scope to include more goods. Our maps show that the immediate impacts will more likely to be found in more resource-dependent cities like Kelowna, Kamloops and Nanaimo in British Columbia, as well as across cities in Quebec and Atlantic Canada. 			
		</p>

		<p>
			Overall, our mapping and visualization tools provide a window into the highly localized and uneven impact of US tariffs across Canada’s cities and regions. We invite you to explore our online <a href="./map">mapping and visualization tool</a>, and you can also investigate our <a href="./cma-ranking-charts">city ranking tool</a>. Over the next few months, stay tuned for additional analysis focused on different goods and industry sectors. We will also explore scenarios that visualize the possible long-run impacts of US tariffs on cities and neighbourhoods across Canada.
		</p>

	</div>

	<Footer />

</main>