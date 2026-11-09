<!--
	MRIO scenarios report, in the order of the report docx. Text, tables, footnotes,
	table of contents and chart data are in $lib/content/scenarios-report.js; figures
	are drawn by $lib/components/report/.
-->
<script>
	import PageTitle from '$lib/components/layout/PageTitle.svelte';
	import Seo from '$lib/components/post/Seo.svelte';
	import AuthorDate from '$lib/components/post/AuthorDate.svelte';
	import Footnotes from '$lib/components/post/Footnotes.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import SectionNav from '$lib/components/layout/SectionNav.svelte';
	import ReportSegments from '$lib/components/report/ReportSegments.svelte';
	import { footnoteTooltips } from '$lib/utils/footnoteTooltips.js';
	import { PUBLISHED } from '$lib/components/maps/scenarios/config.js';
	import report from '$lib/content/scenarios-report.js';

	const TITLE = 'Modeling Potential Economic Impacts of U.S. Tariffs on Canada’s Regions and Industries';

	const contents = [
		{ id: 'introduction', label: 'Introduction', level: 1 },
		...report.toc,
		{ id: 'references', label: 'References', level: 1 }
	];
</script>

<Seo
	title={TITLE}
	description="Projected job losses and economic impacts of five U.S. tariff scenarios on Canada’s regions and industries, from a multi-regional input-output model."
/>

<main class="report-page">
	<SectionNav items={contents} title={TITLE} />

	<div class="two-col post">
		<article class="post-body report" use:footnoteTooltips={report.footnotes}>
			<PageTitle id="introduction" title={TITLE} />
			<AuthorDate
				authors="<a href='https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco' target='_blank'>Richard J. DiFrancesco</a> and <a href='https://www.linkedin.com/in/clara-turner-64764b29/' target='_blank'>Clara Turner</a>"
				date={PUBLISHED}
			/>

			<ReportSegments segments={report.body} figureData={report.figureData} />

			<section id="references">
				<Footnotes footnotes={report.footnotes} />
			</section>
		</article>
	</div>

	<Footer />
</main>

<style>
	/* Wide screens: contents list directly under the "Mapping Tariffs" box, text to its right */
	.report-page {
		--section-nav-left: var(--content-left);
		--section-nav-width: 200px;
	}

	@media (min-width: 1250px) {
		.report-page :global(.two-col.post) {
			padding-left: calc(var(--content-left) + var(--section-nav-width) + 160px);
		}
	}

	.report :global(h2),
	.report :global(h3),
	.report :global(h4),
	.report :global(#introduction),
	.report :global(#references) {
		scroll-margin-top: 16px;
	}

	/* heading looks come from the global standard-text styles; the report only adds
	   extra space above its (long) sections, not the "References" heading in the footnotes box */
	.report :global(h2:not(.footnotes h2)) {
		margin-top: 90px;
	}

	.report :global(h4) {
		margin: 28px 0 0;
	}

	/* ---- tables: same look as the trading-partners table on /exposure */
	.report :global(.report-table) {
		margin: 28px 0 34px;
	}

	.report :global(.report-table figcaption) {
		margin: 0 0 10px;
		font-family: OpenSansBold, sans-serif;
		font-size: 15px;
		line-height: 1.2;
		color: var(--brandBlack);
	}

	.report :global(.table-scroll) {
		overflow-x: auto;
	}

	.report :global(table) {
		width: 100%;
		border-collapse: collapse;
		border-top: 2px solid #e9e9ee; /* same as the body rows */
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		line-height: 1.35;
		color: var(--brandDarkBlue);
	}

	.report :global(th) {
		padding: 6px 10px;
		font-family: OpenSansBold, sans-serif;
		font-weight: normal;
		text-align: left;
		vertical-align: bottom;
		border-bottom: 2px solid var(--brandGray10);
	}

	.report :global(td) {
		padding: 4px 10px;
		background: #e9e9ee;
		border-bottom: 2px solid var(--brandWhite);
		vertical-align: top;
	}

	.report :global(td.num),
	.report :global(th.num) {
		text-align: right;
		white-space: nowrap;
	}

	/* ---- the one-line scenario assumption under each scenario heading: white box, thin border */
	.report :global(.scenario-lead) {
		margin: 16px 0 24px;
		padding: 16px 20px;
		background: var(--brandWhite);
		border: 1px solid #cccccc;
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		line-height: 22px;
		color: var(--brandBlack);
	}

	/* ---- pop-out boxes (author "pop-out" notes in the report) */
	.report :global(.report-callout) {
		margin: 24px 0 28px;
		padding: 16px 20px;
		/* same fill as the table rows */
		background: #e9e9ee;
	}

	.report :global(.report-callout p) {
		margin: 0;
		font-size: 16px;
		line-height: 25px;
	}

	@media (max-width: 600px) {
		.report :global(table) {
			font-size: 12px;
		}
		.report :global(.report-table figcaption) {
			font-size: 13px;
		}
		.report :global(.scenario-lead) {
			font-size: 13px;
			line-height: 20px;
		}
		.report :global(.report-callout p) {
			font-size: 14px;
			line-height: 22px;
		}
	}
</style>
