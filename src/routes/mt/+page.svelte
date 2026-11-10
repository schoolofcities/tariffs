<!--
	Homepage: the two main sub-projects as large cards (with their pages listed), then
	smaller cards for the rest of the site. Card links come from the site nav, so they
	stay in step with the header menus.
-->
<script>
	import { root } from '$lib/site/paths.js';
	import Seo from '$lib/components/post/Seo.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import { NAV, longDate } from '$lib/site/nav.js';
	import CanadaIcon from '$lib/components/icons/CanadaIcon.svelte';
	import BarChartIcon from '$lib/components/icons/BarChartIcon.svelte';
	import DocumentIcon from '$lib/components/icons/DocumentIcon.svelte';
	import PostIcon from '$lib/components/icons/PostIcon.svelte';

	// tools get their own icon (as on the section pages); everything else is a post
	const ICONS = { map: CanadaIcon, rankings: BarChartIcon, 'summary-report': DocumentIcon };
	const iconFor = (href) => ICONS[href.split('/').pop()] ?? PostIcon;

	const section = (href) => NAV.find((s) => s.href === href);

	// all of a section's pages, overview first (as in the menu); posts are listed oldest
	// first in the menu, newest first here
	const pages = (href) =>
		section(href).groups.flatMap((g) => (g.heading === 'Posts' ? [...g.links].reverse() : g.links));

	// card titles, links and border colours come from the nav; only the blurbs are here
	const card = (href, text) => {
		const s = section(href);
		return { href: s.href, title: s.label, border: s.colour, text };
	};

	const main = [
		{
			...card('/exposure', 'Where are the jobs and businesses that make goods subject to U.S. tariffs? Maps, city rankings, and posts on the potential direct exposure of local economies across Canada.'),
			links: pages('/exposure')
		},
		{
			...card('/scenarios', 'Modelled job losses across Canadian cities and regions under five U.S. tariff scenarios, from a multiregional input-output model.'),
			links: pages('/scenarios')
		}
	];

	const more = [
		card('/about', 'The project and the research team behind it.'),
		card('/current-tariffs', 'An updated list of current U.S. tariffs on Canada.'),
		card('/travel/canada-us-visits', 'How much has Canadian travel to U.S. cities declined?')
	];
</script>

<Seo
	title=""
	description="Mapping Tariffs, from the School of Cities at the University of Toronto: maps, rankings, and scenarios on how U.S. tariffs could affect jobs, businesses, and places across Canada."
	type="website"
/>

<main>
	<div class="home">
		<!-- same structure as PageTitle, with the homepage's own (larger) title -->
		<header class="page-heading">
			<h1 class="page-title">Mapping Tariffs</h1>
			<p class="page-subtitle">How could U.S. tariffs affect jobs, businesses, and places across Canada?</p>
		</header>

		<div class="main-cards">
			{#each main as card (card.href)}
				<section class="card big" style:border-color={card.border} style:--accent={card.border}>
					<h2><a href="{root}{card.href}">{card.title} →</a></h2>
					<p>{card.text}</p>
					<ul>
						{#each card.links as link (link.href)}
							{@const Icon = iconFor(link.href)}
							<li>
								<span class="link">
									<span class="link-icon"><Icon size={18} /></span>
									<a href="{root}{link.href}">{link.label}</a>
								</span>
								{#if link.date}<span class="date">{longDate(link.date)}</span>{/if}
							</li>
						{/each}
					</ul>
				</section>
			{/each}
		</div>

		<div class="more-cards">
			{#each more as card (card.href)}
				<a class="card small" href="{root}{card.href}" style:border-color={card.border}>
					<span class="small-title">{card.title} →</span>
					<span class="small-text">{card.text}</span>
				</a>
			{/each}
		</div>
	</div>

	<Footer />
</main>

<style>
	/* lines up with the left edge of the other pages' content */
	.home {
		box-sizing: border-box;
		width: 100%;
		max-width: calc(1100px + var(--content-left) + var(--site-pad));
		padding: 90px var(--site-pad) 60px var(--content-left);
	}

	/* above 1400px: flush left, so the title and cards line up under the
	   "Mapping Tariffs" box in the header */
	@media (min-width: 1401px) {
		.home {
			align-self: flex-start;
			margin-left: 0;
		}
	}

	/* 1400px and below: not enough room for the indent, so centre with equal side padding */
	@media (max-width: 1400px) {
		.home {
			max-width: calc(1100px + 12vw);
			margin: 0 auto;
			padding: 90px 6vw 60px;
		}
	}

	@media (max-width: 700px) {
		.home {
			padding: 50px 16px 40px;
		}
	}

	/* homepage title: its own look, separate from the other pages' titles; 12px bigger */
	.page-title {
		font-size: calc(var(--title-size) + 12px);
	}

	/* square cards with a thin border in the section's colour (from $lib/site/nav.js,
	   set inline) and a soft drop shadow; dark blue on hover */
	.card {
		border: 1px solid var(--brandLightBlue);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		transition: border-color 0.15s ease;
	}

	.card:hover {
		border-color: var(--brandDarkBlue) !important;
	}

	.main-cards {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 20px;
		margin-top: 10px;
	}

	.more-cards {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 20px;
		margin-top: 20px;
	}

	.big {
		padding: 24px 26px 20px;
	}

	.big h2 {
		margin: 0 0 14px;
		padding-bottom: 10px;
		border-bottom: 2px solid var(--accent);
		font-size: 27px;
	}

	.big h2 a {
		color: var(--brandDarkBlue);
		text-decoration: none;
	}

	.big h2 a:hover {
		color: var(--brandMedBlue);
	}

	.big p {
		margin: 0 0 18px;
		font-size: 17px;
		line-height: 26px;
		color: var(--brandGray90);
	}

	.big ul {
		margin: 0;
		padding: 12px 0 0;
		border-top: 1px solid var(--brandGray);
		list-style: none;
	}

	.big li {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 16px;
		margin: 0;
		padding: 5px 0;
		font-family: OpenSans, sans-serif;
		font-size: 15px;
		line-height: 21px;
	}

	/* fixed-width icon column, so all link titles line up */
	.link {
		display: flex;
		align-items: center;
		gap: 8px;
		min-width: 0;
	}

	.link-icon {
		display: flex;
		flex-shrink: 0;
		width: 18px;
		color: var(--brandMedBlue);
	}

	.big li a {
		color: var(--brandMedBlue);
		text-decoration: underline;
		text-underline-offset: 3px;
	}

	.big li a:hover {
		color: var(--brandDarkBlue);
	}

	.date {
		flex-shrink: 0;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray60);
	}

	.small {
		display: flex;
		flex-direction: column;
		gap: 6px;
		padding: 16px 18px;
		color: inherit;
		text-decoration: none;
	}

	.small-title {
		font-family: TradeGothicBold, sans-serif;
		font-size: 20px;
		color: var(--brandDarkBlue);
	}

	.small-text {
		font-family: SourceSerif, serif;
		font-size: 15px;
		line-height: 21px;
		color: var(--brandGray90);
	}

	@media (max-width: 900px) {
		.main-cards,
		.more-cards {
			grid-template-columns: minmax(0, 1fr);
		}
	}

	@media (max-width: 600px) {
		.big {
			padding: 18px 18px 14px;
		}
		.big h2 {
			font-size: 23px;
		}
		.big p {
			font-size: 15px;
			line-height: 23px;
		}
		.big li {
			font-size: 13.5px;
		}
		.small-title {
			font-size: 17px;
		}
		.small-text {
			font-size: 13.5px;
			line-height: 19px;
		}
	}
</style>
