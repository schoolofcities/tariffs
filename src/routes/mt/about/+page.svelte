<script>
	import { base } from '$app/paths';
	import { root } from '$lib/site/paths.js';
	import Seo from '$lib/components/post/Seo.svelte';
	import PageTitle from '$lib/components/layout/PageTitle.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
</script>

<Seo
	title="About"
	description="About Mapping Tariffs: a School of Cities project examining potential local impacts of U.S. tariffs on jobs and businesses across Canada, and the research team behind it."
/>

<main>
	<div class="two-col about">
		<div class="intro">
			<PageTitle title="About" />

			<p>
				New tariffs imposed by U.S. President Donald Trump on Canada and other countries have sparked interest—and concern—about their effects on jobs and businesses across Canada. As details about tariffs on Canadian goods continue to emerge, policymakers, business leaders, and the public are asking where the impacts will be felt—now and over the longer term. What places are most vulnerable?
			</p>

			<p>
				Measuring trade impacts is complex because there are many factors at play. The immediate impacts of tariffs are on the businesses (and their employees) that produce goods subject to tariffs. However, there may also be downstream, indirect impacts. And, the situation is not static as businesses, consumers and governments respond and adjust to a changing economy. Businesses may diversify their markets and seek new (or substitute) suppliers. Citizens may alter their purchasing habits by buying local or Canadian products. Governments may try to spur local purchasing and help support businesses. And the federal government may adjust monetary policy, fiscal policy, and trade policy (e.g. counter tariffs, new trade agreements) to ensure the resilience of the Canadian economy.
			</p>

			<p>
				Since May 2025, <a href="https://discover.research.utoronto.ca/8035-tara-vinodrai" target="_blank">Tara Vinodrai</a> and <a href="https://schoolofcities.utoronto.ca/people/karen-chapple/" target="_blank">Karen Chapple</a> have led a team of researchers at the School of Cities to develop interactive mapping and visualization tools that measure and explore the potential impacts of tariffs on jobs and businesses across Canadian cities and communities at the neighbourhood and city level. Our tools illustrate the highly localized and uneven potential impacts of U.S. tariffs reflecting Canada’s underlying urban, regional and sectoral specializations.
			</p>

			<ul>
			<li>
				<a href="{root}/exposure/map">Examine maps of the potential direct exposure to U.S. tariffs</a> related to specific goods (e.g. automotive, steel, copper, lumber, energy & natural resources) across Canada at the neighbourhood level, measured by 1) businesses 2) employment (based on place of work) and 3) employment (based on place of residence).
			</li>

			<li>
				<a href="{root}/exposure/rankings">Review these same impacts in aggregate across Canadian cities</a>.	
			</li>

			<li>
				<a href="{root}/exposure">Read our backgrounder and blog</a> on Canada-U.S. trade and mapping direct exposure to tariffs.
			</li>

			<li>
				<a href="{root}/scenarios">Read our backgrounder and blog</a> on mapping direct, indirect and induced impacts under different tariff scenarios.
			</li>

			<li>
				<a href="{root}/scenarios/map">Explore maps of the potential direct, indirect and induced impacts on jobs</a> under five different tariff scenarios across Canada at the municipal and neighbourhood level.
			</li>

			<li>
				<a href="{root}/scenarios/rankings">Review these same potential impacts on jobs across Canadian cities and provinces</a>.
			</li>

			<li>
				<a href="{root}/scenarios/summary-report">Read our report on how different tariff scenarios may impact jobs across Canada</a> (see the <a href="{base}/documents/scenarios-appendix-a.pdf" target="_blank">Appendix</a> for technical details).
			</li>

			<li>
				<a href="{root}/exposure/section-338">Read our blog on alcohol, dairy, and motor vehicle tariffs from Section 338 of the Tariff Act of 1930</a>.
			</li>

			<li>
				<a href="{root}/travel/canada-us-visits">Read our blog on the decline in Canadian travel to the U.S.</a>.
			</li>
			
			<li>
				<a href="{root}/exposure/lumber">Read our blog on the effect of softwood lumber tariffs</a> on Canadian jobs and businesses.
			</li>

			<li>
				<a href="{root}/exposure/trucks">Read our blog about the impact of truck tariffs</a> on medium & heavy duty vehicle manufacturing and exports.
			</li>

			<li>
				<a href="{root}/current-tariffs">View the current list of U.S. tariffs on Canada</a>.
			</li>

			<li>
				<a href="https://github.com/schoolofcities/tariffs" target="_blank">Learn more about our research methodology</a>.
			</li>
			</ul>
		</div>

		<aside class="team" aria-labelledby="team-heading">
			<h2 id="team-heading">Research team</h2>

			<p>
				<a href="https://discover.research.utoronto.ca/8035-tara-vinodrai">Tara Vinodrai, PhD</a> is Professor in the Institute for Management and Innovation at the University of Toronto, where she directs the Master of Urban Innovation program.
			</p>

			<p>
				<a href="https://schoolofcities.utoronto.ca/people/karen-chapple/" target="_blank">Karen Chapple, PhD</a> is the Director of the School of Cities and Professor in the Department of Geography & Planning at the University of Toronto.
			</p>

			<p>
				<a href="https://jamaps.github.io/" target="_blank">Jeff Allen, PhD</a> is a Senior Research Associate and the Lead of Maps and Data Visualization at the School of Cities at the University of Toronto. 
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
				<a href="https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco" target="_blank">Richard J. DiFrancesco, PhD</a> is Associate Professor in the Department of Geography and Planning at the University of Toronto and has expertise in input-output data and models.
			</p>

			<p>
				<a href="https://www.linkedin.com/in/clara-turner-64764b29/" target="_blank">Clara Turner, PhD</a> is a Researcher with the School of Cities. 
				She holds a doctorate from the University of California, Berkeley and has expertise related to urban planning, economic development, and economic geography.
			</p>
		</aside>
	</div>

	<Footer />
</main>

<style>
	/* heading look, links and side-column text size come from the global standard-text styles */
	.team h2 {
		margin-top: 0;
	}

	@media (max-width: 1200px) {
		.team h2 {
			margin-top: 10px;
		}
	}
</style>
