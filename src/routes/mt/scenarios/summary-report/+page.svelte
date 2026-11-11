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
	import { base } from '$app/paths';
	import ToolCards from '$lib/components/layout/ToolCards.svelte';
	import AppendixIcon from '$lib/components/icons/AppendixIcon.svelte';
	import { PUBLISHED } from '$lib/components/maps/scenarios/config.js';
	import report from '$lib/content/scenarios-report.js';

	const TITLE = 'Modeling Potential Economic Impacts of U.S. Tariffs on Canada’s Regions and Industries';

	// the technical appendix (PDF), as a card under the byline (same card as on the Scenarios overview)
	const appendix = [
		{
			url: `${base}/documents/scenarios-appendix-a.pdf`,
			icon: AppendixIcon,
			title: 'Technical appendix',
			text: 'Appendix A (PDF): Measuring the Economic Impacts of U.S. Tariffs on Canada: A National, Regional and Industrial Analysis, by Richard J. DiFrancesco.'
		}
	];

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
		<article class="post-body report report-content" use:footnoteTooltips={report.footnotes}>
			<PageTitle id="introduction" title={TITLE} />
			<AuthorDate
				authors="<a href='https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco' target='_blank'>Richard J. DiFrancesco</a> and <a href='https://www.linkedin.com/in/clara-turner-64764b29/' target='_blank'>Clara Turner</a>"
				date={PUBLISHED}
			/>

			<div class="appendix-card">
				<ToolCards tools={appendix} />
			</div>

			<ReportSegments segments={report.body} figureData={report.figureData} />

			<section id="references">
				<Footnotes footnotes={report.footnotes} />
			</section>
		</article>
	</div>

	<Footer />
</main>

<style>
	/* Technical appendix card. In the text column under the byline by default; on wide
	   screens with room beside the report column (640px + 40px gap + 240px card), it moves
	   to the right of the text, its top level with the line under the byline. Room exists at 1164–1249px (column
	   starts at --content-left) and from 1524px (column starts after the contents list). */
	.report {
		position: relative;
	}

	.appendix-card {
		margin: 24px 0 36px;
	}

	@media (min-width: 1164px) and (max-width: 1249px), (min-width: 1524px) {
		.appendix-card {
			position: absolute;
			left: calc(100% + 40px);
			width: 240px;
			margin: -26px 0 0;
		}
	}

	/* above phone width (beside the text or above it): smaller icon and text than the
	   standard tool card, so the card stays secondary to the report */
	@media (min-width: 701px) {
		/* icon 20% smaller and tighter spacing, so the text has more width */
		.appendix-card :global(.card) {
			gap: 12px;
			padding: 14px 16px;
		}

		.appendix-card :global(.card .icon) {
			width: 44px;
		}

		.appendix-card :global(.card .icon svg) {
			width: 42px;
			height: auto;
		}

		/* card text 20% smaller (ToolCards sizes 20 / 12 / 16px) */
		.appendix-card :global(.card .card-title) {
			font-size: 16px;
		}

		.appendix-card :global(.card .updated) {
			font-size: 9.6px;
		}

		.appendix-card :global(.card .card-text) {
			font-size: 12.8px;
			line-height: 1.4;
		}
	}

	/* phones: keep it under the byline but smaller than the text around it */
	@media (max-width: 700px) {
		.appendix-card {
			zoom: 0.8;
		}
	}

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
		background: #f4f4f7;
	}

	.report :global(.report-callout p) {
		margin: 0;
		font-size: 16px;
		line-height: 25px;
	}

	@media (max-width: 600px) {
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
