<!--
	Scenarios overview (from "Mapping Tariffs - Scenarios - Overview page_Nov8.docx"). The two
	charts are the summary report's Figures 2 and 14, drawn by the report's chart components
	from its data; the three maps are screenshots of the scenarios map.
-->
<script>
	import { base } from '$app/paths';
	import { root } from '$lib/site/paths.js';
	import PageTitle from '$lib/components/layout/PageTitle.svelte';
	import Seo from '$lib/components/post/Seo.svelte';
	import AuthorDate from '$lib/components/post/AuthorDate.svelte';
	import ImageSingle from '$lib/components/post/ImageSingle.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import ToolCards from '$lib/components/layout/ToolCards.svelte';
	import ReportFigure from '$lib/components/report/ReportFigure.svelte';
	import CanadaIcon from '$lib/components/icons/CanadaIcon.svelte';
	import BarChartIcon from '$lib/components/icons/BarChartIcon.svelte';
	import DocumentIcon from '$lib/components/icons/DocumentIcon.svelte';
	import AppendixIcon from '$lib/components/icons/AppendixIcon.svelte';
	import { PUBLISHED } from '$lib/components/maps/scenarios/config.js';
	import report from '$lib/content/scenarios-report.js';

	const REPORT = `${root}/scenarios/summary-report`;
	const MAP = `${root}/scenarios/map`;
	const RANKINGS = `${root}/scenarios/rankings`;
	const APPENDIX = `${base}/documents/scenarios-appendix-a.pdf`;

	// under each screenshot: the map in the same view (Scenario 1, ADAs, percent; see the map's URL state)
	const mapLink = (effects) =>
		`<br><a href="${MAP}?${effects ? `effects=${effects}&` : ''}geo=ADA">Click here to view interactive map</a>`;
	const MRIO_INTRO = 'https://support.implan.com/hc/en-us/articles/115009713448-MRIO-Introduction-to-Multi-Regional-Input-Output-Analysis';

	// the report and its technical appendix (PDF) get their own cards above the tools
	const reportCard = [
		{
			href: '/scenarios/summary-report',
			icon: DocumentIcon,
			published: PUBLISHED,
			title: 'Summary report',
			text: 'Modeling potential economic impacts of U.S. tariffs on Canada’s regions and industries: context, methods, and the regional and industry effects of each scenario.'
		},
		{
			url: APPENDIX,
			icon: AppendixIcon,
			published: PUBLISHED,
			title: 'Technical appendix',
			text: 'Appendix A (PDF): Measuring the Economic Impacts of U.S. Tariffs on Canada: A National, Regional and Industrial Analysis, by Richard J. DiFrancesco.'
		}
	];

	const tools = [
		{
			href: '/scenarios/map',
			icon: CanadaIcon,
			published: PUBLISHED,
			title: 'Interactive map',
			text: 'Explore modelled job losses under each scenario for neighbourhoods and municipalities, as a number of jobs or as a share of local employment, combining direct, indirect and induced effects.'
		},
		{
			href: '/scenarios/rankings',
			icon: BarChartIcon,
			published: PUBLISHED,
			title: 'Rankings',
			text: 'Compare job losses across Canada’s census metropolitan areas and provinces for each scenario and type of effect.'
		}
	];
</script>

<Seo
	title="Mapping tariff scenarios"
	description="How might a tariff-induced shock ripple across Canada’s urban and regional economies? Direct, indirect and induced job impacts under five U.S. tariff scenarios, from a multiregional input-output model."
/>

<main>
	<div class="two-col">
		<div class="intro">
			<PageTitle title="Mapping tariff scenarios" />

			<AuthorDate
				authors="<a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco' target='_blank'>Richard J. DiFrancesco</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>, <a href='https://www.linkedin.com/in/clara-turner-64764b29/' target='_blank'>Clara Turner</a>, and <a href='https://jamaps.github.io/' target='_blank'>Jeff Allen</a>"
				date="November 2026"
			/>

			<p>
				Over the past eighteen months, we have been following the Canada-U.S. trade dispute to <a href="{root}/exposure">map the locations of jobs and businesses that are directly vulnerable to the tariffs</a> imposed by the Trump administration. While our original work captured potential direct vulnerability to tariffs, we know that the effects of tariffs spill over into the rest of the economy, and we would expect those effects to be felt unevenly, reflecting Canada’s diverse economic geography. In our newest work, we ask: <strong><em>How might a tariff-induced shock ripple across Canada’s urban and regional economies?</em></strong> Based on our analysis, we have produced a <a href={REPORT}>detailed report</a> (and <a href={APPENDIX} target="_blank">technical appendix</a>), a new <a href={MAP}>scenario mapping tool</a>, and a new <a href={RANKINGS}>scenario city ranking tool</a>.
			</p>

			<h2>Understanding economic impact</h2>

			<p>
				Understanding the economic impact of tariffs in Canada is essential for assessing how changes in trade flows can affect businesses, workers, and regional economies. While tariffs may directly affect industries that export to or import from foreign markets, their effects extend beyond these sectors through supply chains and changes in household spending.
			</p>

			<p>
				We breakdown these impacts into direct, indirect, and induced effects to provide a more comprehensive understanding of how economic shocks ripple across the economy, helping policymakers and stakeholders identify vulnerabilities, assess potential job impacts, and develop targeted responses to support affected industries and communities.
			</p>

			<p>These effects can be described as follows:</p>

			<ul>
				<li><strong>Direct effects</strong> capture the impact on the affected industry itself;</li>
				<li><strong>Indirect effects</strong> capture the impact on supplier industries that provide inputs to the affected industry; and</li>
				<li><strong>Induced effects</strong> capture the impact on the rest of the economy caused by the reduced spending of the workers and businesses due to the above losses.</li>
			</ul>

			<p>
				We can illustrate these three categories of effects using a simple example using the automotive parts industry. In the first category (<em>direct effects</em>), a new tariff on the automotive parts manufacturing industry might mean that an auto parts manufacturer experiences a decline in business, resulting in the layoff of workers. As a result, the automotive parts manufacturing reduces spending, buying fewer inputs such as steel, plastics, or other materials. Therefore, suppliers across the supply chain may also reduce employment (<em>indirect effects</em>). And finally, on account of these employment reductions, workers have less income to spend at grocery stores, restaurants, retail shops, and other local businesses, leading to additional job losses (<em>induced effects</em>).
			</p>

			<p>
				While this seems relatively straightforward, determining the magnitude of the economic impact based on an external shock (such as the imposition of tariffs) or how this shock might ricochet through the economy can be quite complicated, especially at the local level.
			</p>

			<p>
				Researchers rely on economic models that draw upon input-output (IO) tables to map the relationships between different sectors of the economy. In Canada, Statistics Canada maintains <a href="https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&SDDS=1401">supply and use tables</a> at the national and provincial level that “trace the production of commodities by domestic industries, combined with imports, through their uses by industries or as final consumption, investment or exports. The system provides measures of value added by industry and total GDP.”
			</p>

			<p>
				In our work, we use a <a href={MRIO_INTRO}>Multiregional Input-Output (MRIO) model</a> developed by Professor <a href="https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco">Richard J. DiFrancesco</a> (a member of our research team), which covers all of Canada's provinces and territories. By specifying a specific level of shock, the MRIO model uses the IO tables to estimate changes in gross output, value added output ($CAD) and job changes within a specific sector, alongside the indirect and induced effects that spill across the economy.
			</p>

			<h2>Building tariff scenarios</h2>

			<p>
				To use the MRIO model, we needed to estimate the magnitude of the shock created by the introduction of US tariffs. Economists and other analysts have explored this issue extensively, but there is no consensus on what a mild, moderate or severe shock might look like. For example, <a href="https://www.scotiabank.com/ca/en/about/economics/economics-publications/post.other-publications.insights-views.cusma-scenario-note--march-5--2026-.html">Scotiabank Economics</a> has explored potential scenarios related to the fate of the Canada-United States-Mexico Agreement (CUSMA) and the <a href="https://www.bankofcanada.ca/wp-content/uploads/2025/01/mpr-2025-01-29.pdf">Bank of Canada</a> has provided economic projections based on the impact of US tariffs.
			</p>

			<p>
				After an extensive review of reports and analysis undertaken by Canada’s financial institutions and other policy researchers, we developed five moderate scenarios that capture how specific shocks to the Canadian economy resulting from US tariffs might affect jobs and output across Canada’s cities and regions. The first scenario considers what might happen if household consumption declines in Canada while the remaining four scenarios model what might happen if there are shocks to specific sectors of the Canadian economy.
			</p>

			<p>The five scenarios we developed and modeled are as follows:</p>

			<ul>
				<li><strong>Scenario 1 - Household consumption:</strong> Estimates the potential economic impacts if household consumption expenditures across Canada decline by 1%;</li>
				<li><strong>Scenario 2 - Agriculture, agri-food, and seafood:</strong> Estimates the potential economic impacts if agriculture, agrifood, and seafood exports to the U.S. decline by between 7% and 16%, depending on the specific industry in this sector;</li>
				<li><strong>Scenario 3 - Steel and aluminum:</strong> Estimates the potential economic impacts if steel and aluminum exports to the U.S. decline by 15% and 10%, respectively.</li>
				<li><strong>Scenario 4- Softwood lumber:</strong> Estimates the potential economic impacts if softwood lumber exports to the U.S. decline by 12%;</li>
				<li><strong>Scenario 5 – Automotive and automotive parts manufacturing:</strong> Estimates the potential economic impacts if motor vehicle manufacturing and motor vehicle parts manufacturing exports to the U.S. decline by 20% and 15%, respectively.</li>
			</ul>

			<p>
				You can read more about the details of how each model is defined and specified in the <a href={REPORT}>report</a> by our modelling team.
			</p>

			<p>
				Using the MRIO model results, our analysis takes two different forms. First, we capture the regional and industry effects of tariffs under each of our five tariff scenarios in an extensive and <a href={REPORT}>detailed report</a>. Second, we use the MRIO model results for 220 industries and 13 regions to estimate local level impacts (direct, indirect and induced effects) as the basis for a new <a href={MAP}>scenario mapping tool</a> and a <a href={RANKINGS}>city ranking tool</a>. Below we highlight some of our key observations and findings from our analysis.
			</p>

			<h2>Regional and sector level results</h2>

			<p>
				Overall, the MRIO results at the provincial/territorial level and sector level highlight that even relatively small tariff-induced changes in overall consumption patterns (Scenario 1) or larger shifts in exports to particular sectors (Scenarios 2 to 5) could have broader impacts beyond the industries targeted by tariffs.
			</p>

			<p>
				At the provincial/territorial level, our analysis shows that under all five scenarios, job losses are uneven across Canada, with Ontario and Quebec accruing the highest potential for job loss in almost every case, once we include direct, indirect and induced effects. For example, the graphs below demonstrate the potential job losses associated with an overall reduction in household consumption (Scenario 1). Not surprisingly, our model predicts that the largest numbers of job losses are in Canada’s most populous provinces, as would be expected given that more jobs and more economic activity take place in these provinces. However, this effect remains when job loss is normalized by population.
			</p>

			<!-- the report's charts (same components and data as the summary report); their table styles need .report-content -->
			<div class="report-content report-chart">
				<ReportFigure n={2} rows={report.figureData[2]} />
				<div class="caption-container">
					<p>Scenario 1 – Household consumption - Total estimated job loss (%) by province</p>
					<p><span class="caption-source">Note: See <a href={REPORT}>report</a> for more details.</span></p>
				</div>
			</div>

			<p>
				Additionally, the table below shows estimates of the overall potential for job losses by industry under each of our five scenarios. Under <em>Scenario 1 - Household consumption</em>, estimated job losses span every sector of the Canadian economy, with high proportions of jobs at risk in manufacturing; arts, entertainment, and hospitality industries; and the FIRE (finance, insurance and real estate) industries. This is particularly noteworthy given that these latter service-based industries are highly concentrated in cities across Canada, which our <a href={RANKINGS}>city ranking tool</a> allows us to explore in greater depth.
			</p>

			<div class="report-content report-chart">
				<ReportFigure n={14} rows={report.figureData[14]} />
				<div class="caption-container">
					<p><span class="caption-source">Note: See <a href={REPORT}>report</a> for more details.</span></p>
				</div>
			</div>

			<p>
				Across the sector-specific scenarios, job losses in manufacturing industries are projected to be high, reflecting the direct and indirect effects resulting from the decline in exports in industries targeted by US tariffs, alongside the induced effects related to the corresponding contraction in household consumption. Not surprisingly, job losses in industries related to agriculture, forestry and extraction are estimated to be higher under <em>Scenario 2 – Agriculture, agri-food, and seafood</em> and <em>Scenario 4 – Softwood lumber</em>. Our <a href={MAP}>mapping tool</a> highlights how these effects are concentrated in particular regions across Canada.
			</p>

			<h2>Mapping scenario results</h2>

			<p>
				Our <a href={MAP}>tariff scenario mapping tool</a> helps us understand the widening impact of tariffs across the economy and how that may have uneven effects across Canadian cities and regions. To illustrate this, we focus here on Scenario 1 – Household consumption. As the map below shows, the direct effects of a 1% reduction in overall household consumption are relatively even across Canada.
			</p>

			<ImageSingle
				imageURL="{base}/images/scenarios/s1-direct.png"
				caption="Scenario 1 - Household consumption – Direct effects"
				source={mapLink('DIR')}
				maxWidth="680px"
				link="No"
			/>

			<p>
				However, the story begins to evolve when we consider the knock-on effects from the initial tariff-induced shock. Next, we add indirect effects to understand the potential job losses predicted by our model across the supply chain. As the map (below) shows, in this scenario, jobs losses begin to accrue in communities across southwestern Ontario, parts of eastern Ontario, and some rural communities across Canada.
			</p>

			<ImageSingle
				imageURL="{base}/images/scenarios/s1-direct-indirect.png"
				caption="Scenario 1 - Household consumption – Direct and indirect effects"
				source={mapLink('DIR,INDIR')}
				maxWidth="680px"
				link="No"
			/>

			<p>
				Finally, we add induced effects to understand the full extent of the potential job losses predicted by our model. As the map (below) shows, the potential for job losses widens and deepens across Canada.
			</p>

			<ImageSingle
				imageURL="{base}/images/scenarios/s1-direct-indirect-induced.png"
				caption="Scenario 1 - Household consumption – Direct, indirect and induced effects"
				source={mapLink('')}
				maxWidth="680px"
				link="No"
			/>

			<p>
				The remaining sector-specific scenarios similarly show a widening and deepening as we include the knock-on effects that spill out beyond the industries targeted by tariffs. These effects become even more clear when <a href={RANKINGS}>we aggregate our results to the city-region level</a>.
			</p>

			<h2>Limitations</h2>

			<p>
				We note the following limitations to our analysis. First, these are scenarios, not predictions. As noted, we triangulated our model specifications based on other studies to estimate as best as possible realistic, moderate scenarios. Second, we assume that local economies mirror the structure of the provincial economy. Given that the MRIO model produces provincial/territorial level estimates, we needed to estimate local level impacts (measured at the municipal and neighbourhood level). To do this, we adjust our results based on the local share of provincial employment at the industry level. Thus, our results are best used to compare relative patterns across places. Finally, the model assumes the economy remains structured in its current state. It does not capture firms seeking out new geographic markets, substituting suppliers, retooling production to enter new product markets, or other adaptive business and policy responses implemented by Canadian businesses and governments at all levels. Similar assumptions and limitations underpin almost all modelling and scenario-building exercises. Our goal is to provide policymakers and the public about some of the potential outcomes if the tariffs under the Trump administration continue unabated and without political and policy responses.
			</p>

			<h2>Conclusion</h2>

			<p>
				Overall, our report and data visualization tools exploring different tariff scenarios highlight that tariffs have the potential to have widespread impacts across the Canadian economy, both directly and through downstream impacts. Our evidence underscores the need for policymakers at all levels of government to continue to engage with this issue, from assisting local businesses to pivot production and/or access new markets, to ensuring that existing and new trade deals offer opportunities for Canadian businesses to compete in global markets in North America and beyond.
			</p>

			<p>
				We invite you to explore our <a href={MAP}>Tariff Scenario Mapping tool</a> and <a href={RANKINGS}>Tariff Scenario City-Ranking tool</a>, as well as delve into our <a href={REPORT}>report</a>, which provides more details on our approach and regional and industry level findings.
			</p>
		</div>

		<aside class="sidebar">
			<ToolCards tools={reportCard} />
			<h2 class="side-heading">Tools</h2>
			<ToolCards {tools} />
		</aside>
	</div>

	<Footer />
</main>

<style>
	/* report charts: space around them like the images, note right under */
	.report-chart {
		margin: 30px 0;
	}

	.report-chart .caption-container {
		margin-top: 6px;
	}
</style>
