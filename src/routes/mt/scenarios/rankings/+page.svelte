<script>
	import PageTitle from '$lib/components/layout/PageTitle.svelte';
	import { root } from '$lib/site/paths.js';
	import Seo from '$lib/components/post/Seo.svelte';
	import AuthorDate from '$lib/components/post/AuthorDate.svelte';
	import ScenarioRankingChart from '$lib/components/charts/rankings/ScenarioRankingChart.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
</script>

<Seo
	title="Ranked job losses by cities and provinces due to U.S. tariffs"
	description="Compare modelled job losses from U.S. tariffs across Canadian metropolitan areas and provinces, by scenario and type of effect."
/>

<main>
	<div class="two-col">
		<div class="article">
				<PageTitle title="Ranked job losses by cities and provinces due to U.S. tariffs" />

				<AuthorDate
					authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco' target='_blank'>Richard J. DiFrancesco</a>, <a href='https://www.linkedin.com/in/aniket-k-8a8b9921b/' target='_blank'>Aniket Kali</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>, and <a href='https://jamaps.github.io/' target='_blank'> Jeff Allen</a>"
					date="November 2026"
				/>

				<h2>
					A city and province level analysis
				</h2>

				<p>
					Similar to our ranking charts for direct exposure to tariffs, we have built a tool for job losses. This comes from a Multi-Regional Input Output (MRIO) model built by Richard J. DiFrancesco.
				</p>

				<h2>
					A model to understand the impact of U.S. tariffs on Canadian cities
				</h2>

				<p>
					To understand the potential Canadian job losses due to U.S. tariffs, we’ve developed an interactive tool derived from an MRIO model that allows users to explore how specific U.S. tariffs—on automotive, steel, lumber, aluminum, and more—could affect Canadians. 
					The tool provides metrics on the number and proportion of jobs and businesses potentially exposed to tariffs (see also our <a href="{root}/scenarios/map">neighbourhood mapping tool</a>).
				</p>

				<p>
					Results are based on tariffs as of September 1, 2026.
				</p>

				

				<h2>
					What the data tells us about the vulnerability job losses to Canadian cities from U.S. tariffs
				</h2>

				<p>LOREM IPSUM</p>

				<h2>Policy implications?</h2>
				
				<ul>
					<li><b>Diversify local economies</b> to reduce dependence on vulnerable sectors</li>
					<li><b>Support businesses</b> in accessing new markets and supply chains.</li>
					<li><b>Invest in workforce development</b> to build resilience in the face of trade uncertainty.</li>
				</ul>

				<p>
					As trade tensions persist, Canadian policymakers must ensure that cities—especially smaller and specialized ones—are equipped to adapt and thrive.
				</p>

				<h2>Data sources list:</h2>
				<p>
					Estimates in these charts were created by combining data from the following sources:
				</p>
				<ul>
					<li>Canadian Business Registry (Statistics Canada)</li>
					<li>Canadian Chamber of Commerce</li>
					<li>Canadian Census of Population (Statistics Canada)</li>
					<li>Canadian International Merchandise Trade Web Application (Statistics Canada Catalogue No. 71-607-X2021004)</li>
					<li>Harmonized Tariff Schedule of the United States (United States International Trade Commission )</li>
				</ul>
				<p>
					For detailed data descriptions, download links, and processing steps, please read our <a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file" target="_blank">data and methodology page</a>
				</p>
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
</style>
