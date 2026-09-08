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

	<title>Mapping tariffs: Reflecting on new Section 338 Tariffs | School of Cities</title>

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


<!-- <Password/> -->


<main>

	<Logo logoType="Blue" backgroundColor="var(--brandWhite)"/>


	<TitleStandard
		title="Mapping tariffs: Reflecting on new Section 338 Tariffs"
	/>

	<div class="text">

		<AuthorDate
			authors="
			<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>
			<a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, 
			<a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>,
			<a href='https://jamaps.github.io/' target='_blank'>Jeff Allen</a>, 
			"
			date="September 9, 2026"
		/>
	
	</div>

	<div class="text">	

		<p>
			After negotiators representing Canadian and U.S. governments were unable to reach a trade deal, the Trump administration moved to impose a raft of new tariffs on Canadian goods effective as of August 22, 2026. These new tariffs, exercised under Section 338 of the 1930 US Tariff Act, include a 50% tariff on a variety of goods, ranging from honey to hockey sticks, including goods previously exempt due to their compliance with CUSMA. In response to these mounting tariffs, the Government of Canada has introduced counter-tariffs that went into effect on September 8, 2026. 
		</p>


		<p>	
			Even though Canada-U.S. trade relations continue to worsen after the collapse of recent trade talks, the Canadian economy remains deeply integrated with the U.S. economy. Statistics Canada reports that, in 2025, U.S.-Canada trade includes $562.7 billion in exports and $361.8 billion in imports. And while the United States is still Canada’s largest trading partner, there is evidence that this may be slowly shifting. Between 2024 and 2025, the proportion of exports from Canada to the United States decreased from 76.3% to 72.3%. Similarly, the proportion of imports accounted for by the United States declined from 49.2% in 2024 to 45.9% in 2025. These shifts in the relative importance of the U.S. market are likely indicators of the efforts of Canadian businesses and governments to mitigate the potential fallout from tariffs. These efforts have included extensive “buy local” and “buy Canadian” campaigns, shifts in procurement and spending patterns, the diversification of supply chains, and attempts to reach wider, global markets.		
		</p>

		<p>	
			Since we released <a href="https://mappingtariffs.org/">Mapping Tariffs</a> in October 2025, we have been tracking the potential vulnerability of Canadian cities and neighbourhoods to U.S. tariffs. The newest round of tariffs imposed by the Trump administration represents a significant escalation in the ongoing trade dispute between Canada and the United States. Therefore, we ask: Which places will be most vulnerable to new Section 338 tariffs? And, how has the tariff vulnerability landscape for Canadian cities changed, given the more expansive list of goods that are subject to tariffs?		
		</p>

		<p>	
			In our most extensive update since the release of our <a href="/map">mapping tariffs</a> and <a href="cma-ranking-charts">city ranking tools</a>, we have incorporated the following changes to help us understand the potential vulnerabilities to tariffs across Canada and its cities:
		</p>

		<ul>
			<li>
				Additional layers reflecting the new Section 338 tariffs, based on three separate orders made by the Trump administration on <a href="https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-dairy/">dairy</a>, <a href="https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-alcoholic-beverages/">alcohol</a>, and <a href="https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-motor-vehicles/">motor vehicles</a> (although we note, as do <a href="https://www.cfib-fcei.ca/en/site/us-tariffs">others</a>, that the motor vehicles tariffs target an extensive range of goods that are completely unrelated to motor vehicles); and
			</li>
			<li>
				Updates to the overall potential impacts of tariffs before and after the imposition of the Section 338 tariffs effective August 22, 2026.
			</li>
		</ul>

		<h2>Deepening vulnerabilities</h2>

		<p>
			Overall, we observe deepening and widening vulnerabilities to U.S. tariffs measured by businesses and employment (based on place of work and place of residence). 
			To illustrate how the newest round of tariffs may impact Canadian cities and regions, we begin with a map showing the overall vulnerability to tariffs across Canada
			 <i>before</i> the introduction of the new Section 338 tariffs on August 22, 2026 as measured by employment. 
		</p>

		<ImageSingle
			imageURL="./images/before_employment_work.png"
			caption='Potential direct tariff exposure to employment (place of work) in Canada due to tariffs before August 22, 2026'
			source='<br><a href="./map">Click here to view interactive map</a>'
			maxWidth='680px'
			link='No'
		/>

		<p>
			We compare the previous map by adding the tariffs that came into effect on August 22, 2026. 
			The map below shows the overall vulnerability to employment across Canada <i>after</i> the introduction of the new Section 338 tariffs on August 22, 2026. 		
		</p>

		<ImageSingle
			imageURL="./images/after_employment_work.png"
			caption='Potential direct tariff exposure to employment (place of work) in Canada due to tariffs after August 22, 2026'
			source='<br><a href="./map">Click here to view interactive map</a>'
			maxWidth='680px'
			link='No'
		/>

		<p>
			As we observed when we first released the <a href="https://mappingtariffs.org/">Mapping Tariffs</a> project, almost every city, community, and neighbourhood is vulnerable to tariffs. And, given that the new tariffs cover a range of economic activities, there is a deepening of vulnerabilities, especially in places specializing in manufacturing. For example, the map shows that while there are widespread vulnerabilities to workers, there are greater vulnerabilities in the Greater Golden Horseshoe due to the higher concentration of manufacturing industries in Canada’s industrial heartland.		
		</p>

		<p>
			Overall, our updated results continue to underscore the localized impacts of this new round of tariffs. We now turn to examining some of the specific potential impacts related to each of the three separate proclamations made by the Trump administration.
		</p>

		<h2>
			Alcohol tariffs
		</h2>

		<p>
			Tariffs may have a significant impact on wine-producing regions across Canada. For example, the map below shows the potential impact of tariffs on the Okanagan wine region, surrounding the City of Kelowna. Wine-making represents an important economic and tourism sector for the Okanagan region, and wineries export to the U.S. and other markets. 
		</p>

		<ImageSingle
			imageURL="./images/alcohol.png"
			caption='Potential direct tariff exposure to businesses in the Okanagan Valley due to alcohol-related tariffs'
			source='<br><a href="./map">Click here to view interactive map</a>'
			maxWidth='680px'
			link='No'
		/>

		<p>
			Similarly, wine-making is an important economic activity and driver of tourism in southern Ontario, including in Prince Edward County and the Niagara region. The map below shows how the impact of alcohol tariffs raises vulnerability in these two parts of the province of Ontario.
		</p>

		<ImageSingle
			imageURL="./images/alcohol_2.png"
			caption='Potential direct tariff exposure to businesses in southern Ontario due to alcohol-related tariffs'
			source='<br><a href="./map">Click here to view interactive map</a>'
			maxWidth='680px'
			link='No'
		/>

		<h2>
			Dairy
		</h2>

		<p>
			Not surprisingly, the most acute potential impacts of dairy tariffs are observed in rural areas. The map below shows the areas surrounding Sherbrooke as being particularly vulnerable. The Eastern Townships (Cantons-de-l'Est), where Sherbrooke is located, is a renowned dairy and artisan cheese-producing region. Other parts of Quebec – including the areas around Chicoutimi and the wider Saguenay–Lac-Saint-Jean region, which are famous for producing nationally and internationally recognized cheeses – also register as being vulnerable to dairy tariffs.
		</p>

		<ImageSingle
			imageURL="./images/dairy.png"
			caption='Potential direct exposure to businesses in Sherbrooke and the Eastern Townships due to dairy tariffs'
			source='<br><a href="./map">Click here to view interactive map</a>'
			maxWidth='680px'
			link='No'
		/>

		<p>
			The next map shows potential impacts of dairy tariffs on businesses in Toronto. While we often imagine activities related to dairy having an impact on areas outside urban centres (as shown above), Canadian cities are not immune to dairy tariffs. Major dairy processors, including Gay Lea, Lactalis, Saputo, and Agropur maintain office, distribution, and/or industrial operations across the Greater Toronto Area, and represent some of the region’s largest food industry employers.
		</p>

		<ImageSingle
			imageURL="./images/dairy_2.png"
			caption='Potential direct exposure to businesses in Toronto due to dairy tariffs'
			source='<br><a href="./map">Click here to view interactive map</a>'
			maxWidth='680px'
			link='No'
		/>

		<h2>
			Motor vehicles
		</h2>

		<p>
			As noted, the motor vehicle tariffs introduced by the Trump administration apply to a wide swath of goods, which are mostly unrelated to the actual manufacture of automobiles. For example, honey producers across Canada, including in honey-producing regions in the Prairies, are widely <a href="https://www.cbc.ca/news/canada/edmonton/honey-tariffs-alberta-9.7332629">reported</a> to be concerned about the growing costs of accessing their primary markets, located in the United States. 
		</p>
		<p>
			In fact, given the wide range of goods included in the Section 338 motor vehicle tariffs, it is clear that the potential vulnerabilities are widespread. The map below shows the potential exposure to employment in southern Ontario due to motor vehicle tariffs. Given that the industrial base of Canada is heavily concentrated in Ontario and Quebec, it is not surprising that these areas, already vulnerable due to tariffs on automotives, steel and aluminum, face additional vulnerabilities.
		</p>

		<ImageSingle
			imageURL="./images/motor_vehicle.png"
			caption='Potential direct tariff exposure to businesses in southern Ontario due to motor vehicle tariffs'
			source='<br><a href="./map">Click here to view interactive map</a>'
			maxWidth='680px'
			link='No'
		/>

		<h2>
			Conclusion
		</h2>

		<p>
			Overall, our mapping and visualization tools provide a window into the highly localized, widening, and deepening impacts of U.S. tariffs across Canada’s cities and regions. We have highlighted only a few examples of the uneven tariff exposure across Canada and its cities. But these patterns extend across Canada’s urban system. For example, there are localized vulnerabilities to alcohol tariffs in neighbourhoods that are home to local breweries in cities such as Toronto, Montreal, and Vancouver. And the widening net of tariffs on manufactured goods has an outsized impact on the vulnerability of cities around the Greater Golden Horseshoe, including those along the edges of Lake Ontario (yes, Lake ONTARIO). Vulnerabilities to sector-specific tariffs bring into sharp relief underlying regional specialization patterns across Canada and its cities.
		</p>

		<p>
			Our visualizations represent an estimate of the potential direct impacts on Canadian jobs and businesses. These estimates cannot account for the actual economic activity of Canadian businesses since the Trump administration first introduced tariffs on Canadian goods in February 2025. Our current analysis also cannot account for the downstream impacts of tariffs, referred to as the indirect and induced impacts related to these external shocks to urban and regional economies. Stay tuned for our upcoming release of models that include these extended effects. In the meantime, we invite you to explore our updated online <a href="https://mappingtariffs.org/map">mapping and visualization tool</a>, as well as our <a href="https://mappingtariffs.org/cma-ranking-charts">city ranking tool</a>.
		</p>
			
	</div>





	<Footer />

</main>