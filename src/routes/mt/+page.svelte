<!--
	Homepage: the two main sub-projects as large cards (with their pages listed), then
	smaller cards for the rest of the site. Card links come from the site nav, so they
	stay in step with the header menus.
-->
<script>
	import { root } from '$lib/site/paths.js';
	import Seo from '$lib/components/post/Seo.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import { NAV } from '$lib/site/nav.js';

	const section = (href) => NAV.find((s) => s.href === href);

	// the menu uses short months ("Sep 2026"); spell them out here ("September 2026")
	const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
	const longDate = (d) => d?.replace(/\b([A-Z][a-z]{2})\b/, (m) => MONTHS.find((n) => n.startsWith(m)) ?? m);
	// a section's pages (not its overview, which the card title links to); posts are
	// listed oldest first in the menu, newest first here
	const pages = (href) =>
		section(href)
			.groups.flatMap((g) => (g.heading === 'Posts' ? [...g.links].reverse() : g.links))
			.filter((l) => l.href !== href);

	const main = [
		{
			href: '/exposure',
			title: 'Direct exposure',
			border: 'var(--brandPurple)',
			text: 'Where are the jobs and businesses that make goods subject to U.S. tariffs? Maps, city rankings, and posts on the potential direct exposure of local economies across Canada.',
			links: pages('/exposure')
		},
		{
			href: '/scenarios',
			title: 'Scenarios',
			border: 'var(--brandPink, #AB1368)',
			text: 'Modelled job losses across Canadian cities and regions under five U.S. tariff scenarios, from a multiregional input-output model.',
			links: pages('/scenarios')
		}
	];

	const more = [
		{ href: '/about', title: 'About', text: 'The project and the research team behind it.' },
		{ href: '/current-tariffs', title: 'Current tariffs', text: 'An updated list of current U.S. tariffs on Canada.' },
		{ href: section('/travel/canada-us-visits').href, title: 'Canada–U.S. travel', text: 'How much has Canadian travel to U.S. cities declined?' }
	];
</script>

<Seo
	title=""
	description="Mapping Tariffs, from the School of Cities at the University of Toronto: maps, rankings, and scenarios on how U.S. tariffs could affect jobs, businesses, and places across Canada."
	type="website"
/>

<main class="home">
	<h1 class="page-title">Mapping Tariffs</h1>
	<p class="page-subtitle">How could U.S. tariffs affect jobs, businesses, and places across Canada?</p>

	<div class="main-cards">
		{#each main as card (card.href)}
			<section class="card big" style:border-color={card.border}>
				<h2><a href="{root}{card.href}">{card.title} →</a></h2>
				<p>{card.text}</p>
				<ul>
					{#each card.links as link (link.href)}
						<li>
							<a href="{root}{link.href}">{link.label}</a>
							{#if link.date}<span class="date">{longDate(link.date)}</span>{/if}
						</li>
					{/each}
				</ul>
			</section>
		{/each}
	</div>

	<div class="more-cards">
		{#each more as card (card.href)}
			<a class="card small" href="{root}{card.href}">
				<span class="small-title">{card.title} →</span>
				<span class="small-text">{card.text}</span>
			</a>
		{/each}
	</div>
</main>

<Footer />

<style>
	/* lines up with the left edge of the other pages' content */
	.home {
		box-sizing: border-box;
		width: 100%;
		max-width: calc(1100px + var(--content-left) + var(--site-pad));
		padding: 90px var(--site-pad) 60px var(--content-left);
	}

	/* very wide screens: flush with the other pages' left edge, like .two-col */
	@media (min-width: 1800px) {
		.home {
			align-self: flex-start;
			margin-left: 0;
		}
	}

	@media (max-width: 1200px) {
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

	/* square, flat cards with a thin coloured border: purple / pink for the two
	   projects, light blue for the rest; dark blue on hover */
	.card {
		border: 1px solid var(--brandLightBlue);
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
		margin: 0 0 12px;
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
		align-items: baseline;
		gap: 16px;
		margin: 0;
		padding: 5px 0;
		font-family: SourceSerif, serif;
		font-size: 16px;
		line-height: 21px;
	}

	.big li a {
		color: var(--brandDarkBlue);
		text-decoration: none;
	}

	.big li a:hover {
		text-decoration: underline;
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
			font-size: 14px;
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
