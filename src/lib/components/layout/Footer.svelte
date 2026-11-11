<!--
	Site footer: the header's contents as a site map. The project name with the
	SoC/UofT logo underneath on the left; the header's sections and their pages on the
	right, built from $lib/site/nav.js (same source as the header, so they stay in step).
	Sections with sub-pages get a column each (all their pages in one list: overview,
	tools, posts); About comes first in its own column; the other single-page sections
	share the last.

	The layout follows the footer's own width (container queries), not the screen's, so
	it adapts wherever it's placed: full width on normal pages, or the narrow side panel
	on the map pages. Space above it: --footer-gap (set by the container, e.g. MapPage).
-->
<script>
	import logo from '$assets/logos/sofc-uoft-logo-white-colour.svg';
	import { root } from '$lib/site/paths.js';
	import { NAV, SITE_NAME } from '$lib/site/nav.js';

	const href = (path) => `${root}${path}`;

	// About gets its own first column (as it comes first in the header); the other
	// single-page sections share the last column
	const about = NAV.find((s) => s.href === '/about');
	const withPages = NAV.filter((s) => s.groups);
	const singles = NAV.filter((s) => !s.groups && s !== about);
</script>

<footer class="footer">
	<div class="inner">
		<div class="brand">
			<a href={href('/')} class="wordmark">{SITE_NAME}</a>
			<a href="https://schoolofcities.utoronto.ca/" target="_blank" rel="noopener" class="logo-link">
				<img src={logo} alt="University of Toronto School of Cities" class="logo" />
			</a>
		</div>

		<nav class="sitemap" aria-label="Site map">
			{#if about}
				<div class="col narrow">
					<a href={href(about.href)} class="section-link">{about.label}</a>
				</div>
			{/if}

			{#each withPages as section (section.label)}
				<div class="col pages">
					<a href={href(section.href)} class="section-link big">{section.label}</a>
					<!-- all the section's pages in one evenly spaced list: overview, tools, posts -->
					<ul>
						{#each section.groups.flatMap((g) => g.links) as link (link.href)}
							<li><a href={href(link.href)}>{link.label}</a></li>
						{/each}
					</ul>
				</div>
			{/each}

			<div class="col singles">
				{#each singles as section (section.label)}
					<a href={href(section.href)} class="section-link">{section.label}</a>
				{/each}
				<a href="https://github.com/schoolofcities/tariffs-v2" target="_blank" rel="noopener" class="github-link">
					<!-- GitHub mark -->
					<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" fill="currentColor">
						<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
					</svg>
					Code and data on GitHub
				</a>
			</div>
		</nav>
	</div>
</footer>

<style>
	.footer {
		container-type: inline-size; /* the @container rules below follow this width */
		width: 100%;
		margin-top: var(--footer-gap, 100px);
		background-color: var(--brandDarkBlue);
		border-top: 1px solid var(--brandGray);
		color: var(--brandWhite);
	}

	@media (max-width: 800px) {
		.footer {
			margin-top: var(--footer-gap, 25px);
		}
	}

	.inner {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 40px 60px;
		/* left edge = --content-left: lines up with the header's "Mapping Tariffs"
		   wordmark and the page text */
		padding: 40px var(--site-pad) 50px var(--content-left);
	}

	/* ---- project name, with the SoC/UofT logo underneath */
	.brand {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 18px;
		flex-shrink: 0;
	}

	/* Sized so the logo's University of Toronto half (crest to the end of "TORONTO",
	   x = 3.1%–50.1% of the file's width, i.e. 47.1%) is as wide as the "Mapping Tariffs"
	   box above (152px at 20px type: 128px text + 2 × 12px padding). 152 / 0.471 = 322px.
	   The negative margin removes the file's 3.1% left inset so the crest lines up with
	   the box's left edge. Re-measure if the wordmark text, its size, or the logo change. */
	.logo-link {
		--footer-logo: 322px;
		display: block;
		margin-left: calc(var(--footer-logo) * -0.031);
	}

	.logo {
		display: block;
		width: var(--footer-logo);
		height: auto;
	}

	.logo-link:hover .logo {
		opacity: 0.75;
	}

	/* the header's wordmark, inverted for the dark background: dark-blue text on white */
	.wordmark {
		padding: 4px 12px;
		background: var(--brandWhite);
		font-family: TradeGothicBold, sans-serif;
		font-size: 20px;
		line-height: 32px;
		color: var(--brandDarkBlue);
		text-decoration: none;
		white-space: nowrap;
	}

	.wordmark:hover {
		background: var(--brandLightBlue);
	}

	/* ---- site map */
	/* columns never wrap: the footer is either one row (logos + columns) or stacked
	   (logos above the columns), nothing in between; narrow footers use a grid, below */
	.sitemap {
		display: flex;
		flex-wrap: nowrap;
		gap: 30px 50px;
	}

	.col {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 8px;
		min-width: 150px;
	}

	/* separate sections stacked in one column (Current tariffs, travel): more space
	   between them than between a section's own links */
	.col.singles {
		gap: 18px;
	}

	/* a column with a single short link: only as wide as its text */
	.col.narrow {
		min-width: 0;
	}

	/* single-page sections (About, Current tariffs, travel) */
	.section-link {
		font-family: TradeGothicBold, sans-serif;
		font-size: 16px;
		color: var(--brandWhite);
		text-decoration: none;
	}

	/* sections with pages (Direct exposure, Scenarios) */
	.section-link.big {
		font-size: 20px;
	}

	/* GitHub link under the single-page sections: page-link style, not a section heading.
	   The footer columns stretch to the tallest (Direct exposure), so margin-top: auto puts
	   it at the bottom, level with that column's last link; same 3px padding as those links. */
	.github-link {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		margin-top: auto;
		padding: 3px 0;
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		line-height: 19px;
		color: var(--brandWhite);
		opacity: 0.85;
		text-decoration: none;
	}

	.github-link:hover {
		color: var(--brandLightBlue);
		opacity: 1;
		text-decoration: underline;
	}

	ul {
		margin: 0;
		padding: 0;
		list-style: none;
	}

	li {
		margin: 0;
		padding: 3px 0;
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		line-height: 19px;
		color: var(--brandWhite);
	}

	li a {
		color: var(--brandWhite);
		opacity: 0.85;
		text-decoration: none;
	}

	.section-link:hover,
	li a:hover {
		color: var(--brandLightBlue);
		opacity: 1;
		text-decoration: underline;
	}

	/* ---- by footer width */

	/* 1200–1360px: the --content-left indent no longer leaves room for one row, so drop
	   to the normal page margin (one row then needs ~1140px) */
	@container (max-width: 1360px) {
		.inner {
			padding-left: var(--site-pad);
		}
	}

	/* below 1200px: stack the logos above the columns */
	@container (max-width: 1199px) {
		.inner {
			flex-direction: column;
		}
	}

	/* 800px and below (phones, the map side panel): smaller logos, and the site map on
	   a 6-column grid in two rows.
	   Row 1: Direct exposure | Scenarios (3 columns each).
	   Row 2: About | Current tariffs | Canada–U.S. travel (2 columns each). The column
	   that stacks Current tariffs + travel is dissolved (display: contents) so each
	   becomes its own grid cell; `order` moves About from first to the second row. */
	@container (max-width: 800px) {
		.inner {
			padding: 30px 20px 40px;
		}
		/* same logo match for the smaller box (17px type, 8px padding: 125px) -> 264px */
		.logo-link {
			--footer-logo: 264px;
		}
		.brand {
			gap: 14px;
		}
		.wordmark {
			padding: 2px 8px;
			font-size: 17px;
		}
		.sitemap {
			display: grid;
			grid-template-columns: repeat(6, minmax(0, 1fr));
			gap: 28px 20px;
		}
		.col {
			min-width: 0;
		}
		.col.pages {
			grid-column: span 3;
		}
		.col.narrow {
			grid-column: span 2;
			order: 1;
		}
		.col.singles {
			display: contents;
		}
		.col.singles .section-link {
			grid-column: span 2;
			order: 2;
		}
		.col.singles .github-link {
			grid-column: 1 / -1;
			order: 3;
			margin-top: 0;
			justify-self: start;
		}
	}
</style>
