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

	<title>The Impacts of Truck Tariffs on Canadian Cities | School of Cities</title>

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


<Password/>


<main>

	<Logo logoType="Blue" backgroundColor="var(--brandWhite)"/>

	<ImageSingle
		imageURL="./lumber-trucks/img/truckscover.png"
		caption=''
		source=''
		maxWidth='685px'
		link='No'
	/>

	<TitleStandard
		title="The Impacts of Truck Tariffs on Canadian Cities"
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
			Canada's medium heavy duty vehicle (truck) industry is highly reliant on U.S. exports.
		</p>

		<p>	
			Medium heavy duty vehicles (MHDVs) consist of garbage trucks, long haul trucks and delivery vehicles ranging from classes 3 to 8 (8,501 - 33,000+ lbs). 
			This sector is often grouped with all vehicles and parts, which accounted for <a href="https://international.canada.ca/en/global-affairs/corporate/transparency/briefing-documents/parliamentary-committee/2023-06-13-ciit?">13.2% of the share of exported merchandises to the U.S.</a>, the second largest category.
		</p>

		<h2>
			Background: Canada-US Automotive & Trucks Trade
		</h2>

		<p>
			The trucks trade between Canada and U.S. had been protected under Section 232 of the Trade Expansion Act since 1962.
			In 2020, <a href="https://link.springer.com/article/10.1007/s10479-021-04397-2">COVID-19 caused lapses in the overall manufacturing industry</a>.
			In 2021, <a href="https://www.cbc.ca/news/business/covid-car-industry-analysis-1.6216265">a semi-conductor shortage</a> dropped manufacturing and sales across the entire automotive sector, including trucks.
			In 2023, Canada and the U.S. announced a <a href="https://www.pm.gc.ca/en/news/statements/2023/03/24/prime-minister-trudeau-and-president-biden-joint-statement">$250 million investment</a> to support semiconductor projects, so manufacturers finally had the semiconductors to go through backlogged orders. 
			Additionally, <a href="https://www.fleetowner.com/perspectives/ideaxchange/blog/21263561/navigating-the-carb-prebuy-for-truck-procurement-what-fleets-need-to-know">new environmental protection regulations for trucks were announced in California</a>.
			Commercial fleets that generate more than $50 million in gross revenue must have 50% of zero emissions MHDVs in addition to their fleets starting January 1, 2024.
			To meet this target, a rush for 2023 compliant vehicle procurement caused a pre-buy spike in imports, which carried over in 2024.
			
		</p>

		<p>
			Figure 1 depicts this phenomenon through the yearly exports of medium and heavy duty vehicle sales to the U.S..
		</p>

		<GraphicSingle
			svg360="./lumber-trucks/web-svg/mhdv_yearly_export_value-360.svg"
			svg720="./lumber-trucks/web-svg/mhdv_yearly_export_value-720.svg"
			caption="Figure 1: Yearly Export Value of Medium and Heavy Duty Vehicles to the U.S."
			source='Source: <a href="https://www150.statcan.gc.ca/t1/tbl1/en/cv!recreate.action?pid=1210017401&selectedNodeIds=3D32,4D108,4D109&checkedLevels=0D1,1D1&refPeriods=20250701,20251101&dimensionLayouts=layout2,layout3,layout3,layout2,layout2&vectorDisplay=false" target="_blank">Statistics Canada - Merchandise imports and exports</a>'
		/>

	</div>

	
	
	<div class="text">
		<p>
			Breaking it down by weight in Figure 2, we can see a 32.6% increase in value but only 22.8% increase in weight from 2023 to 2024.
			This can be explained by medium duty vehicles dominating 2024 instead of heavy duty vehicles because of the pre-buy of Class 8 fleet vehicles in 2023.
		</p>

		<GraphicSingle
			svg360="./lumber-trucks/web-svg/mhdv_yearly_export_weight-360.svg"
			svg720="./lumber-trucks/web-svg/mhdv_yearly_export_weight-720.svg"
			caption="Figure 2: Yearly Export Weight of Medium and Heavy Duty Vehicles to the U.S."
			source='Source: <a href="https://www150.statcan.gc.ca/t1/tbl1/en/cv!recreate.action?pid=1210017401&selectedNodeIds=3D32,4D108,4D109&checkedLevels=0D1,1D1&refPeriods=20250701,20251101&dimensionLayouts=layout2,layout3,layout3,layout2,layout2&vectorDisplay=false" target="_blank">Statistics Canada - Merchandise imports and exports</a>'
		/>

	</div>

	
	<div class="text">

		<p>
			Automotive tariffs (passenger vehicles and light trucks) were placed in effect in spring 2025 with medium and heavy duty vehicle tariffs coming into effect later in the fall.
			In anticipation of the tariffs to MHDVs, <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260108/dq260108a-eng.htm">October sales rose 24.7%</a> compared to September 2025. 
			In November 2025, <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260129/dq260129a-eng.htm">MHDV exports fell 53.8% compared to October 2025</a> (across the world), undoubtedly due to the tariffs. 
			The broader automotive sector was also affected by semiconductor shortages, resulting in a <a href="https://www150.statcan.gc.ca/n1/daily-quotidien/260115/dq260115a-eng.htm">6.3% decline</a> in motor vehicle parts sales month over month.
			The sector also saw a 15.9% decline in motor vehicle manufacturing sales (finished vehicles sold direct to consumers or shipped to the U.S.) from the previous month, which is down 20.7% from November 2024.
		</p>

		<p>
			On November 1st, 2025, <a href="https://www.reuters.com/legal/legalindustry/truck-tariffs-signal-broader-us-supply-chain-rebuild--pracin-2025-11-10/">medium and heavy duty vehicle and bus tariffs were imposed</a>. 
			This category not only includes the MHDVs, but also buses, which now covers the vast majority of manufactured vehicles.
			Now a month into 2026, fleet companies are preparing for the 2027 mandate announced by the Environmental Protection Agency (EPA) of the U.S. where it mandates a <a href="https://www.fleetowner.com/emissions-efficiency/article/55315480/epa27-isnt-dead-yet-will-your-fleet-be-prepared">significant reduction in NOx emissions.</a>
			This has caused <a href="https://www.fleetowner.com/equipment/article/55355309/class-8-orders-top-10-year-average-fleet-risks-persist">Class 8 vehicles (heaviest category) to reach an all time high in orders</a>.
			However, with the tariffs now in place on Canada, this weakens our relationship with U.S. fleet companies, especially for companies like Eaton Canada that makes variable valve actuation (VVA) technology that helps with emission regulations.
		</p>

		</div>

			

	<div class="text">


		<p>
			Here in Figure 3 are the export values of MHDVs via the CUSMA agreement (mainly to the U.S.), which reached $5.41 billion by November 2025, which is on par with 2024's total. 
			However, you can see the fluctuation of the prebuy in anticipation of the tariffs in October.
		</p>

			<GraphicSingle
				svg360="./lumber-trucks/web-svg/mhdv_monthly_2025-360.svg"
				svg720="./lumber-trucks/web-svg/mhdv_monthly_2025-720.svg"
				caption="Figure 3: Monthly CUSMA related Exports from Canada"
				source='Source: <a href="https://www150.statcan.gc.ca/t1/tbl1/en/cv!recreate.action?pid=1210017401&selectedNodeIds=3D32,4D108,4D109&checkedLevels=0D1,1D1&refPeriods=20250701,20251101&dimensionLayouts=layout2,layout3,layout3,layout2,layout2&vectorDisplay=false" target="_blank">Statistics Canada - Merchandise imports and exports</a>'
			/>

		<p>
			
			To further the incentive of centralizing U.S. manufacturing, the government has given an incentive of a tariff relief of 3.75% if companies build their MHDVs in the U.S..
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
			MHDVs, once protected under Section 232 national security tariffs, are undergoing turbulations with these tariffs.
		</p>

		<p>
			In 2026, the situation is still unpredictable. On one hand, layoffs are rampant in the industry due to the dependency of Canadian auto exports to the U.S.. Meanwhile, the demand for greener vehicles such as EVs and <a href="https://cleanenergycanada.org/wp-content/uploads/2024/05/ZEMHDV-AvailabilityCatalogue-V7-Online-1.pdf">zero emission vehicle compliant policies</a> are set in place.
			The question remains: What is the outlook on Canada's auto industry, and are consumers and commercial clients and government entities ready for the greener future that is promised?
		</p>

		<h2>
			The impact of truck tariffs in Ontario
		</h2>

		<p>
			In Ontario, Canada's largest exporter of trucks, tariff-hit companies have experienced layoffs due to demand-side and operational constraints.
			For example, in April 2025, <a href="https://www.cbc.ca/news/canada/toronto/gm-production-fort-wayne-1.7642742">General Motors placed 250 temporary jobs to a plant in Indiana</a> days after Trump announced a 25% tariff on automotives. 
			Then, in January 2026, <a href="https://thestar.com/business/some-1-200-jobs-to-be-lost-to-trump-tariffs-as-gm-oshawa-layoffs-ripple/article_adb35aa9-8938-43dc-bcde-a5c975c0cf91.html">GM cut approximately 500 employees in Oshawa, affecting over 1200 across the supply chain</a>.
		</p>

		<p>
			For auto families in Brampton, this news was the tipping point for them to leave the area as <a href="https://www.cbc.ca/news/canada/windsor/brampton-windsor-stellantis-workers-uprooted-9.7053353">Stellanis' Brampton plant has been on temporary pause for over 2 years</a>. 
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
			For example, in Figure 4, the Greater Golden Horseshoe displays the proportion of workers (as place of work) potentially affected by the truck tariffs. 
		</p>

	</div>

	<ImageSingle
		imageURL="./lumber-trucks/img/csdtrucksemployeeswork.png"
		caption='Figure 4: Potential direct exposure of tariffs to employees (work) in the truck industry by census subdivision in Southern Ontario.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>
	
	<div class="text">
		
		<p>
			The new MHDV tariffs heavily affected the manufacturing plants in Ontario. 
			Employees in regions like Woodstock live and work at medium and heavy duty truck assembly facilities like <a href="https://comtruck.ca/locations/woodstock/">Comtruck</a> and <a href="https://www.hinocanada.com/about-us/woodstock-plant-milestones/">Hino Canada</a> can be seen affected through their primary residence (Figure 5).
		</p>
		
	</div>

	<ImageSingle
		imageURL="./lumber-trucks/img/mhdvemployeeshome.png"
		caption='Figure 5: Employees affected (by primary residence) in Western Ontario.'
		source='<br><a href="./map">Click here to view interactive map</a>'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			Windsor is a <a href="https://www.futureautolabourforce.ca/wp-content/uploads/2020/06/Regional-Profiles_Provincial-Ontario.pdf">major original equipment manufacturer</a> in the automotive industry. Companies like Stellantis, OPmobility Canada, Linamar produce parts such as steering wheels and braking technology for U.S. companies to then assemble (Figure 6).
		</p>
	</div>

	<ImageSingle
		imageURL="./lumber-trucks/img/mhdvwindsoremployeeshomecsd.png"
		caption='Figure 6: Total number of affected employees by their primary residence by census subdivision.'
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
		imageURL="./lumber-trucks/img/mhdvemployeesworkmontreal.png"
		source='<br><a href="./map">Click here to view interactive map</a>'
		caption='Figure 7: Total affected employees (by place of work) in Montréal.'
		maxWidth='680px'
		link='No'
	/>

	<div class="text">

		<p>
			Our maps show that the impacts of the tariffs are consistent with export reports across the truck industry.
			Truck manufacturing regions like Guelph, Windsor and Ingersoll are facing a decrease in manufacturing.
			The supply chain, constrained by adjacent tariffs in steel and automotives, are hindering truck exports in many avenues.
			While the Canadian government does recognize and supports the MHDV industry through financial aid, the future remains uncertain due to the bilateral interdependency of the U.S. & Canada.
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