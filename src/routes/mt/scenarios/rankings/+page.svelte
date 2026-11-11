<script>
	import PageTitle from '$lib/components/layout/PageTitle.svelte';
	import { root } from '$lib/site/paths.js';
	import Seo from '$lib/components/post/Seo.svelte';
	import AuthorDate from '$lib/components/post/AuthorDate.svelte';
	import ScenarioRankingChart from '$lib/components/charts/rankings/ScenarioRankingChart.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
</script>

<Seo
	title="Ranking potential job impacts at the metropolitan scale based on scenario modelling"
	description="Compare modelled job losses from U.S. tariffs across Canadian metropolitan areas and provinces, by scenario and type of effect."
/>

<main>
	<div class="two-col">
		<div class="article">
			<!-- intro: on one-column screens the chart comes right after this, before the first heading -->
			<div class="article-intro">
			<PageTitle title="Ranking potential job impacts at the metropolitan scale based on scenario modelling" />

			<AuthorDate
				authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco' target='_blank'>Richard J. DiFrancesco</a>, <a href='https://www.linkedin.com/in/aniket-k-8a8b9921b/' target='_blank'>Aniket Kali</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>, and <a href='https://jamaps.github.io/' target='_blank'>Jeff Allen</a>"
				date="November 2026"
			/>

			<p>
				Recent tariffs imposed by U.S. President Donald Trump on Canada have raised pressing questions about what tariffs mean for Canadian jobs. Our <a href="{root}/exposure/rankings">exposure rankings</a> show where jobs and businesses are in the direct line of fire for specific U.S. tariffs. But exposure is not the same as loss: not every exposed job will disappear, and many jobs that are not directly exposed may still be at risk.
			</p>

			<p>
				When exports in a tariffed industry decline, the effects ripple outward. Firms that supply that industry lose orders, and workers who lose hours or jobs spend less at local stores, restaurants, and service businesses. These ripple effects can reach well beyond the industries named in a tariff order, and well beyond the places where those industries are located.
			</p>

			<p>
				Similar to our <a href="{root}/exposure/rankings">ranking charts for direct exposure to tariffs</a>, we have built a tool that ranks Canadian Census Metropolitan Areas (CMAs) and provinces and territories by their potential job losses. The estimates come from a closed multiregional input-output (MRIO) model of the Canadian economy, based on the most recent input-output data for Canada and its regions. The model covers 220 industries and 13 provinces and territories; we then estimated results for local communities and rolled them up to CMAs and provinces. For the full results and methodology, see our <a href="{root}/scenarios/summary-report">summary report</a>.
			</p>
			</div>

			<div class="article-body">
			<h2>Understanding the potential job impact of U.S. tariffs on Canadian cities</h2>

			<p>
				Drawing on an analysis based on projections from multiple sources, including major financial institutions, we created different scenarios and use an MRIO model to estimate impacts across the economy. The five scenarios we developed and modeled are as follows:
			</p>

			<ul>
				<li><strong>Scenario 1 - Household consumption:</strong> Estimates the potential economic impacts if household consumption expenditures across Canada decline by 1%;</li>
				<li><strong>Scenario 2 - Agriculture, agri-food, and seafood:</strong> Estimates the potential economic impacts if agriculture, agrifood, and seafood exports to the U.S. decline by between 7% and 16%, depending on the specific industry in this sector;</li>
				<li><strong>Scenario 3 - Steel and aluminum:</strong> Estimates the potential economic impacts if steel and aluminum exports to the U.S. decline by 15% and 10%, respectively.</li>
				<li><strong>Scenario 4- Softwood lumber:</strong> Estimates the potential economic impacts if softwood lumber exports to the U.S. decline by 12%;</li>
				<li><strong>Scenario 5 – Automotive and automotive parts manufacturing:</strong> Estimates the potential economic impacts if motor vehicle manufacturing and motor vehicle parts manufacturing exports to the U.S. decline by 20% and 15%, respectively.</li>
			</ul>

			<p>
				While tariffs may directly affect industries that export to or import from foreign markets, their effects extend beyond these sectors through supply chains and changes in household spending. These effects can be described as follows:
			</p>

			<ul>
				<li><strong>Direct effects</strong> capture the impact on the affected industry itself;</li>
				<li><strong>Indirect effects</strong> capture the impact on supplier industries that provide inputs to the affected industry; and</li>
				<li><strong>Induced effects</strong> capture the impact on the rest of the economy caused by the reduced spending of the workers and businesses due to the above losses.</li>
			</ul>

			<p>
				Using our interactive tool, users can explore three metrics measured in terms of potential job loss under each of these five macroeconomic scenarios. You can read more about our modelling work and its limitations in our project <a href="{root}/scenarios">overview</a>.
			</p>

			<h2>Job loss risk in Canadian cities due to U.S. tariffs</h2>

			<p>
				Cities are where economic impacts are most directly felt—on main streets, in industrial parks, and across neighbourhoods. Our ranking tools emphasize that cities - large and small and from coast to coast to coast have the potential to experience job losses due to US tariffs. However, there are distinct patterns that emerge depending on the scenario.
			</p>

			<p>
				A broad decline in household consumption would have the largest effect of any scenario: our estimates suggest that a 1% drop in household spending could lead to the loss of roughly 334,000 jobs nationwide. Canada’s six largest city-regions (Toronto, Montreal, Vancouver, Calgary, Ottawa-Gatineau, and Edmonton) would face the largest risks of job losses in absolute terms. For example, we estimate potential losses of about 72,000 jobs in the Toronto CMA, 40,000 in Montréal, and 27,000 in Vancouver.
			</p>

			<p>
				In relative terms, cities in Canada are at risk of losing between 1.4% and 2.7% of their jobs; in other words, there is limited variability in the expected proportions of job loss. Nonetheless, the city-regions with the highest proportions of job loss risk are all in Ontario: Thunder Bay (2.7%), Guelph (2.6%), Belleville-Quinte West (2.5%), Toronto (2.5%), Windsor (2.3%), St. Catharines-Niagara (2.3%), Kitchener-Waterloo-Cambridge (2.3%), Peterborough (2.2%), London (2.2%), and Kingston (2.2%). These Ontario cities are all part of Canada’s industrial heartland, where manufacturing supply chains are experiencing uncertainty in the face of ongoing tariffs.
			</p>

			<p>
				Among the sector-specific scenarios, tariffs on motor vehicles and parts have by far the greatest impact, with close to 250,000 potential job losses, more than the agri-food (approximately 69,000 jobs at risk), steel and aluminum (roughly 42,000 jobs at risk), and softwood lumber (approximately 23,000 jobs at risk) scenarios combined.
			</p>

			<p>
				Our sector-specific scenarios also underscore Canada’s highly regionalized industrial geography: where an industry is concentrated, so too are the losses. Our automotive scenario confirms that the impacts from automotive tariffs overwhelmingly affect Ontario, with about 176,000 potential job losses. Toronto would see the most jobs lost (about 80,000), but Guelph (6.1% of employment), Windsor (4.9%), Belleville–Quinte West (3.5%), and Kitchener–Cambridge–Waterloo (3.3%) would be hit hardest relative to their size. Our steel and aluminum scenario shows that job losses would be concentrated in Quebec and Ontario, with Saguenay (1.4% of employment), Trois-Rivières, Drummondville, Sherbrooke, and Hamilton most affected.
			</p>

			<p>
				Other tariffs have the potential to have a disproportionate impact on other parts of Canada. For example, in our agriculture, agri-food and seafood scenario, potential job losses weigh most heavily in the Prairies, with Lethbridge, Winnipeg, Regina, and Saskatoon at the top of the CMA rankings by share of employment (all effects). And while, cities like Toronto and Montreal still top the list in terms of the number of potential job losses (due to their size and the role of induced effects), Winnipeg ranks third overall. Similarly, softwood lumber tariffs affect British Columbia and New Brunswick most, especially Nanaimo, Kamloops, Chilliwack, Kelowna and Saint John.
			</p>

			<p>
				Overall, in each of our five scenarios, our evidence suggests that most of the potential job losses occur outside the industries that are directly tariffed. Direct effects account for between 9% and 14% of job losses nationally; the rest come from supply chains and, above all, from reduced household spending. Induced effects alone account for more than half of job losses under the household consumption and automotive scenarios. This means that tariffs on a specific good or industry can be felt on main streets and throughout a region, not just on factory floors.
			</p>

			<h2>Conclusions and policy implications</h2>

			<p>
				Our results reinforce the observations and policy prescriptions we offered in our earlier work. The impacts of tariffs are widespread and put cities across Canada at risk of job loss. It’s not just the places where goods are made that are affected by tariffs, but communities across Canada due to the interconnectedness of supply chains and the widespread impacts on household spending.
			</p>

			<p>
				For Canadian cities to remain resilient in a time when there is the potential for job losses across the economy due to the direct, indirect and induced effects of tariffs, business, government and civic leaders must make it a priority to assist cities and regions in adapting. In line with our previous work, we argue that there is an ongoing and urgent need for targeted policy responses at the local, provincial and national scales. These include the following actions:
			</p>

			<ul>
				<li>Support businesses and regions in <strong>accessing new markets and supply chains</strong> through trade agreements and trade missions.</li>
				<li>Support businesses and regions in <strong>retooling to enter new product markets</strong>, potentially to support federal priorities related to national sovereignty and infrastructure.</li>
				<li><strong>Diversify local economies</strong> and <strong>invest in workforce development</strong> to reduce dependence on vulnerable sectors and build resilience in the face of trade uncertainty.</li>
				<li>Implement <strong>broader measures</strong> to sustain household spending and confidence, since induced effects drive the majority of potential job losses.</li>
			</ul>

			<p>
				As trade tensions persist, Canadian policymakers must ensure that cities—especially smaller and specialized ones—are equipped to adapt and thrive.
			</p>

			<h2>Data sources:</h2>

			<p>
				Estimates for the interactive scenario city ranking tool use data from the following sources:
			</p>

			<ul>
				<li>Canadian Business Registry (Statistics Canada)</li>
				<li>Canadian Census of Population (Statistics Canada)</li>
				<li>Input-output Tables (Statistics Canada)</li>
				<li>Canadian International Merchandise Trade Web Application (Statistics Canada Catalogue No. 71-607-X2021004)</li>
				<li>Harmonized Tariff Schedule of the United States (United States International Trade Commission )</li>
				<li>Statistics Canada Input-Output Multipliers, Provincial and Territorial, Detail Level (Table 36-10-0113-01)</li>
			</ul>

			<p>
				For detailed data descriptions, download links, and processing steps, please read our <a href="https://github.com/schoolofcities/tariffs-v2/tree/main/analysis#readme" target="_blank">data and methodology page</a>
			</p>
			</div>
		</div>

		<aside class="chart-col" aria-label="Job-loss rankings chart">
			<ScenarioRankingChart />
		</aside>
	</div>

	<Footer />
</main>

<style>
	.two-col {
		--col-right: 560px;
	}

	@media (max-width: 1200px) {
		.chart-col {
			margin-top: 20px;
			padding-top: 10px;
			border-top: 1px solid var(--brandLightBlue);
		}
	}

	/* one column: intro, then the chart, then the rest of the text */
	@media (max-width: 1200px) {
		.article {
			display: contents;
		}
		.article-intro {
			order: 1;
		}
		.chart-col {
			order: 2;
		}
		.article-body {
			order: 3;
		}
	}
</style>
