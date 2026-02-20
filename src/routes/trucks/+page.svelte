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

	<title>The impacts of truck tariffs on Canadian cities | School of Cities</title>

	<meta name="description" content="An update on potential local truck tariff impacts on jobs and businesses across Canada via maps and charts" />
	<meta name="author" content="School of Cities">
	<meta rel="canonical" href="https://schoolofcities.github.io/tariffs/trucks">

	<meta property="og:title" content="The Impact of Truck Tariffs on Canadian Cities" />
	<meta property="og:description" content="An update on potential local truck tariff impacts on jobs and businesses across Canada via maps and charts" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://schoolofcities.github.io/tariffs/trucks" />
	<meta property="og:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" />
	<meta property="og:locale" content="en_CA">

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="The Impact of Truck Tariffs on Canadian Cities" />
	<meta name="twitter:description" content="An update on potential local truck tariff impacts on jobs and businesses across Canada via maps and charts" />
	<meta name="twitter:site" content="https://schoolofcities.github.io/tariffs/trucks" />
	<meta name="twitter:image" content="https://raw.githubusercontent.com/schoolofcities/tariffs/main/static/web-card.png" /> 

</svelte:head>


<!-- <Password/> -->


<main>

	<Logo logoType="Blue" backgroundColor="var(--brandWhite)"/>

	<ImageSingle
		imageURL="./trucks/img/truckscover.png"
		caption=''
		source=''
		maxWidth='685px'
		link='No'
	/>

	<TitleStandard
		title="The impacts of truck tariffs on Canadian cities"
		subtitle="An update on potential local truck tariff impacts on jobs and businesses across Canada"
	/>

	<div class="text">

		<AuthorDate
			authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://jamaps.github.io/' target='_blank'>Jeff Allen</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>"
			date="February 2026"
		/>
	
	</div>

	<div class="text">	

		<p>
			Canada's Medium Heavy Duty Vehicles (MHDVs) industry is highly reliant on U.S. exports.
		</p>

		<p>	
			MHDVs consist of garbage trucks, long haul trucks and delivery vehicles ranging from classes 3 to 8 (8,501 - 33,000+ lbs). 
			In terms of trade, this sector is often grouped with all vehicles and parts, which accounts for <a href="https://international.canada.ca/en/global-affairs/corporate/transparency/briefing-documents/parliamentary-committee/2023-06-13-ciit?">13.2% of the share of exported merchandises to the U.S.</a>, the second largest category.
			In 2024, <a href="https://wits.worldbank.org/trade/comtrade/en/country/CAN/year/2024/tradeflow/Exports/partner/ALL/product/870990">87.1% of work truck parts</a> were exported to the U.S..
		</p>

		<h2>
			Background: Canada-U.S. automotive & trucks trade
		</h2>

		<p>
			The trucks trade between Canada and U.S. had been protected under Section 232 of the Trade Expansion Act since 1962. 
			Under the Obama administration, the U.S. Environmental Protection Agency <a href="https://www.epa.gov/regulations-emissions-vehicles-and-engines/regulations-greenhouse-gas-emissions-commercial-trucks">issued greenhouse gas emissions standards</a> across the MHDV models for 2014-2018 and 2019-2027, called Phase 1 and Phase 2 respectively.
			The sector met these standards well until 2020, <a href="https://link.springer.com/article/10.1007/s10479-021-04397-2">when COVID-19 caused lapses in the overall manufacturing industry</a>.
			Then, in 2021, <a href="https://www.cbc.ca/news/business/covid-car-industry-analysis-1.6216265">a semi-conductor shortage</a> dropped manufacturing and sales across the entire automotive sector, including trucks.
			Therefore, in 2023, Canada and the U.S. announced a <a href="https://www.pm.gc.ca/en/news/statements/2023/03/24/prime-minister-trudeau-and-president-biden-joint-statement">$250 million investment</a> to support semiconductor projects, so that manufacturers can acquire the semiconductors to go through backlogged orders. 
			Additionally, the U.S. EPA set out Phase 3 regulations that year, which pushed stronger GHG emission standards across MHDVs such as the 
			<a href="https://www.fleetowner.com/perspectives/ideaxchange/blog/21263561/navigating-the-carb-prebuy-for-truck-procurement-what-fleets-need-to-know">California Air Resources Board mandating zero emission truck purchases</a> from January 1, 2024 onwards.
			This regulation applied to commercial fleets that generate more than $50 million in gross revenue or have 50 or more fleets.
			To meet this target, a rush for 2023 compliant vehicle procurement caused a pre-buy spike in imports, which carried over to 2024.
			
		</p>

		<p>
			The chart below depicts this phenomenon through the yearly exports of medium and heavy duty vehicle sales to the U.S..
		</p>

		<GraphicSingle
			svg360="./trucks/web-svg/mhdv_yearly_export_value-360.svg"
			svg720="./trucks/web-svg/mhdv_yearly_export_value-720.svg"
			source='Source: <a href="https://www.trade.gov/data-visualization/medium-and-heavy-duty-truck-trade-data-visualization">U.S. International Trade Administration - Medium and Heavy Duty Truck Trade Data</a>'
		/>

	</div>

	
	
	<!-- <div class="text">
		<p>
			Breaking it down by weight in Figure 2, we can see a 22.8% increase in quantity from 2023 to 2024, but a 32.6% increase in value from Figure 1.
			This can be potentially explained by Class 8 (>35,000 ton) vehicles dominating in expenses instead of medium duty vehicles because of the new zero emission mandates.
		</p>

		<GraphicSingle
			svg360="./trucks/web-svg/mhdv_yearly_export_weight-360.svg"
			svg720="./trucks/web-svg/mhdv_yearly_export_weight-720.svg"
			caption="Figure 2: Yearly Export Quantity of Medium and Heavy Duty Vehicles to the U.S."
			source='Source: <a href="https://www.trade.gov/data-visualization/medium-and-heavy-duty-truck-trade-data-visualization">U.S. International Trade Administration - Medium and Heavy Duty Truck Trade Data</a>'
		/>

	</div> -->

	
	<div class="text">

		<p>
			Automotive tariffs (passenger vehicles and light trucks) were placed in effect in spring 2025 with medium and heavy duty vehicle tariffs coming into effect later in the fall.
			On October 17, 2025, the Trump administration <a href="https://www.whitehouse.gov/presidential-actions/2025/10/adjusting-imports-of-medium-and-heavy-duty-vehicles-medium-and-heavy-duty-vehicle-parts-and-buses-into-the-united-states/">announced tariffs</a> on medium and heavy duty vehicles (25%) and busses (10%) effective November 1st, 2025.
			This category shook the industry as it not only includes the MHDVs, but also buses, which now covers the vast majority of manufactured vehicles.
			In anticipation of these new tariffs, <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260108/dq260108a-eng.htm">October sales rose 24.7%</a> compared to September 2025. 
		</p>

		<p>
			In November 2025, <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260129/dq260129a-eng.htm">Canadian MHDV exports fell 53.8% </a> compared to October 2025, undoubtedly due to the tariffs. 
			The broader automotive sector was also affected by recent semiconductor shortages, resulting in a <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260115/dq260115a-eng.htm">6.3% decline</a> in motor vehicle parts sales month over month.
			The sector also saw a 15.9% decline in motor vehicle manufacturing sales (finished vehicles sold direct to consumers or shipped to the U.S.) from the previous month, which is down 20.7% from November 2024.
		</p>

		<p>
			Now a month into 2026, fleet companies are preparing for the 2027 mandate announced by the Environmental Protection Agency (EPA) of the U.S. where it mandates a <a href="https://www.fleetowner.com/emissions-efficiency/article/55315480/epa27-isnt-dead-yet-will-your-fleet-be-prepared">significant reduction in nitric oxide (NOx) emissions.</a>
			This has caused <a href="https://www.fleetowner.com/equipment/article/55355309/class-8-orders-top-10-year-average-fleet-risks-persist">Class 8 vehicles (heaviest category) to reach an all time high in orders</a>.
			Companies like Linamar are <a href="https://www.bnnbloomberg.ca/business/2025/11/12/linamar-reports-1692m-in-q3-profit-up-from-the-previous-year/">avoiding tariffs through meeting CUSMA</a> thresholds, but parts regarding NOx / EPA compliance systems are <a href="https://www.ccjdigital.com/regulations/emissions/article/15771994/epa-rejects-trucking-industry-plea-will-keep-2027-nox-rule-timeline?">strained through the EPA 2027 standards</a>.
			With the tariffs now in place on Canada, this weakens our relationship with U.S. truck assemblers and original equipment manufacturers as companies must either supply parts to comply under CUSMA or pay the tariffed rates.
		</p>

		</div>

			

	<div class="text">


		<p>
			The char below represents the prebuy surge and drop for 2025 using export values of trucks via the CUSMA agreement, which reached $5.41 billion by November 2025, which was around on par with 2024 numbers.
		</p>

			<GraphicSingle
				svg360="./trucks/web-svg/mhdv_monthly_2025-360.svg"
				svg720="./trucks/web-svg/mhdv_monthly_2025-720.svg"
				caption=""
				source='Source: <a href="https://www150.statcan.gc.ca/t1/tbl1/en/cv!recreate.action?pid=1210017401&selectedNodeIds=3D32,4D108,4D109&checkedLevels=0D1,1D1&refPeriods=20250701,20251101&dimensionLayouts=layout2,layout3,layout3,layout2,layout2&vectorDisplay=false" target="_blank">Statistics Canada - Merchandise imports and exports</a>'
			/>

		<p>
			
			To further the incentive of centralizing U.S. manufacturing, the government has given an incentive of a <a href="https://www.supplychaindive.com/news/trump-truck-bus-tariffs-nov-1/803171/">tariff relief of 3.75% per year</a> if companies finish their truck builds in the states.
			On February 5, 2026, Carney announced a push for <a href="https://www.ttnews.com/articles/canada-scrap-eve-rules">an import credit system</a>, which would alleviate tariffs for companies that meet a certain production threshold. This follows a $2.3 billion program for Canadians to purchase EV vehicles in partnerships with Chinese automakers.
		</p>


		<p>
			Similar to the findings in our <a href="../potential-local-impacts">preliminary findings</a>, Canada's truck industry is highly tied to the U.S. due to the geographic convenience and demand of U.S. imports.
		</p>

		<h2>
			Current tariff landscape
		</h2>

		<p>
			The U.S. government continues to enact and change plans with tariffs as negotiations continue. See our <a href="../current-tariffs">current tariffs</a> page for a full list of tariffs currently in place.
		</p>

		<p>
			In 2026, the situation is still unpredictable. Trucks, once protected under Section 232 national security tariffs, are seeing unprecedented effects from the tariffs. On one hand, layoffs are rampant in the industry due to the dependency of Canadian auto exports to the U.S.. 
			Meanwhile, the demand for greener vehicles such as EVs and <a href="https://cleanenergycanada.org/wp-content/uploads/2024/05/ZEMHDV-AvailabilityCatalogue-V7-Online-1.pdf">zero emission vehicle compliant policies</a> may motivate production in this sector.
			The question remains: What is the outlook on Canada's auto industry, and are consumers and commercial clients and government entities ready for the greener future that is promised?
		</p>

		<h2>
			The impact of truck tariffs in Ontario
		</h2>

		<p>
			In Ontario, Canada's largest exporter of trucks, tariff-hit companies have experienced layoffs due to demand-side and operational constraints.
			For example, in April 2025, <a href="https://www.cbc.ca/news/canada/toronto/gm-production-fort-wayne-1.7642742">General Motors placed 250 temporary jobs to a plant in Indiana</a> days after Trump announced a 25% tariff on automotives. 
			Then, in January 2026, <a href="https://thestar.com/business/some-1-200-jobs-to-be-lost-to-trump-tariffs-as-gm-oshawa-layoffs-ripple/article_adb35aa9-8938-43dc-bcde-a5c975c0cf91.html">GM cut approximately 500 employees in Oshawa</a>, affecting over 1200 across the supply chain.
		</p>

		<p>
			For auto families in Brampton, this news was the tipping point for them to leave the area as <a href="https://www.cbc.ca/news/canada/windsor/brampton-windsor-stellantis-workers-uprooted-9.7053353">Stellanis' Brampton plant had already been on temporary pause for over 2 years</a>. 
			Stellanis is currently under <a href="https://www.cbc.ca/news/canada/windsor/canada-stellantis-sue-brampton-jobs-default-contracts-joly-9.7003596">federal government scrutiny</a> due to their contracts with commitments to invest in Canadian plants as they have been moving production to the U.S. instead. 
			With the tariffs now in place, it makes it much more difficult to manufacture in Canada.
		</p>
		
		<p>
			On the federal level, Industry Minister Mélanie Joly responded by saying that <a href="https://www.cbc.ca/news/canada/toronto/gm-oshawa-lay-offs-friday-9.7068425">the nation will "invest in other players"</a> and ensure that those displaced by jobs will be supported.

		</p>

		<h2>
			Map findings
		</h2>

		<p>
			Using our  <a href="./map">mapping and visualization tool</a> we can trace potential tariff vulnerabilities across Canada. 
			The medium heavy duty vehicle section highlights the regional specialization of manufacturing dependent cities.
			For example, the Greater Golden Horseshoe displays the proportion of workers (as place of work) potentially affected by the truck tariffs. 
		</p>

	</div>

	<ImageSingle
		imageURL="./trucks/img/csdtrucksemployeeswork.png"
		caption='Potential direct exposure of tariffs to employees (work) in the truck industry by census subdivision in Southern Ontario.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>
	
	<div class="text">
		
		<p>
			Truck manufacturing plants were heavily affected.
			Employees in regions like Woodstock live and work at medium and heavy duty truck assembly facilities like <a href="https://comtruck.ca/locations/woodstock/">Comtruck</a> and <a href="https://www.hinocanada.com/about-us/woodstock-plant-milestones/">Hino Canada</a> can be seen affected through their primary residence .
		</p>
		
	</div>

	<ImageSingle
		imageURL="./trucks/img/mhdvemployeeshome.png"
		caption='Employees affected (by primary residence) in Western Ontario.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			Windsor is a <a href="https://www.futureautolabourforce.ca/wp-content/uploads/2020/06/Regional-Profiles_Provincial-Ontario.pdf">major original equipment manufacturer</a> in the automotive industry. Companies like Stellantis, OPmobility Canada, Linamar produce parts such as steering wheels and braking technology for U.S. companies to then assemble .
		</p>
	</div>

	<ImageSingle
		imageURL="./trucks/img/mhdvwindsoremployeeshomecsd.png"
		caption='Total number of affected employees by their primary residence by census subdivision.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">
		<p>
			Montreal also ships class 7 trucks at Kenworth and Peterbilt dealerships through PACCAR's Sainte-Therese plant, where according to their website, <a href="https://www.paccar.com/careers/canada-opportunities/">a vast majority are exported to the U.S.</a>.
			<!-- where <a href="https://www.journaldemontreal.com/2025/03/11/tarifs-vives-inquietudes-chez-paccar-de-sainte-therese">97% of their trucks are exported to the U.S.</a>. -->
		</p>
	</div>

	<ImageSingle
		imageURL="./trucks/img/mhdvemployeesworkmontreal.png"
		source='<br><a href="./map">Click here to view interactive map</a>'
		caption='Total affected employees (by place of work) in Montréal.'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			Our maps show that the impacts of the tariffs are consistent with export reports across the truck industry.
			Truck manufacturing regions like Guelph, Windsor and Ingersoll are facing a decrease in manufacturing.
			The supply chain, constrained by adjacent tariffs in steel and automotives, are hindering truck exports in many avenues.
			While the Canadian government does recognize and supports the MHDV industry through financial aid, 
			the industry remains volatile and unpredictable due to the codependency of truck production between Canada & the U.S..
		</p>

		<p>
			Read about the <a href="../lumber">impact of lumber tariffs</a> on Canadian cities, check out the <a href="../potential-local-impacts">preliminary report</a> on our findings, explore our <a href="../map">interactive mapping tool</a> to see the potential impacts across Canadian neighbourhoods, or view the <a href="../cma-ranking-charts">city ranking charts</a> for aggregate impacts.
		</p>

		<p>
			<a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file">A full accounting of the technical details, data processing steps, and associated code can be found here.</a>
		</p>

	</div>

	<Footer />

</main>