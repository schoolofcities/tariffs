<!--
	Site header: SoC/UofT logo, project wordmark, and section menus built from
	$lib/site/nav.js.

	Desktop: sections with sub-pages open a dropdown on click (Escape or a click
	outside closes it). Mobile (< 840px): a single "Menu" button opens a panel
	with every section expanded.
-->
<script>
	import { root } from '$lib/site/paths.js';
	import { page } from '$app/state';
	import { afterNavigate } from '$app/navigation';
	import logo from '$assets/logos/sofc-uoft-logo-blue-colour.svg';
	import { NAV, SITE_NAME, isActive } from '$lib/site/nav.js';

	let openSection = $state(null); // label of the open desktop dropdown
	let mobileOpen = $state(false);
	let headerEl;

	// path within the site (/mt/exposure -> /exposure), to match the nav entries
	const pathname = $derived(page.url.pathname.startsWith(root) ? page.url.pathname.slice(root.length) || '/' : page.url.pathname);
	const href = (path) => `${root}${path}`;

	function closeAll() {
		openSection = null;
		mobileOpen = false;
	}

	afterNavigate(closeAll);

	function onWindowClick(e) {
		if (headerEl && !headerEl.contains(e.target)) openSection = null;
	}

	function onKeydown(e) {
		if (e.key === 'Escape' && (openSection || mobileOpen)) closeAll();
	}
</script>

<svelte:window onclick={onWindowClick} onkeydown={onKeydown} />

<header class="site-header" bind:this={headerEl}>
	<div class="bar">
		<div class="brand">
			<a href="https://schoolofcities.utoronto.ca/" target="_blank" rel="noopener" class="logo-link">
				<img src={logo} alt="University of Toronto School of Cities" class="logo" />
			</a>
			<a href={href('/')} class="wordmark" aria-current={pathname === '/' ? 'page' : undefined}>{SITE_NAME}</a>
		</div>

		<nav class="desktop-nav" aria-label="Main">
			<ul>
				{#each NAV as section (section.label)}
					{@const active = isActive(pathname, section.href)}
					<li class="section">
						{#if section.groups}
							<button
								type="button"
								class="section-link"
								class:active
								aria-expanded={openSection === section.label}
								aria-controls="menu-{section.href.slice(1)}"
								onclick={() => (openSection = openSection === section.label ? null : section.label)}
							>
								{section.label}<span class="chevron" aria-hidden="true">▾</span>
							</button>
							{#if openSection === section.label}
								<div class="dropdown" id="menu-{section.href.slice(1)}">
									{#each section.groups as group}
										<div class="group">
											{#if group.heading}<p class="group-heading">{group.heading}</p>{/if}
											<ul>
												{#each group.links as link (link.href)}
													<li>
														<a href={href(link.href)} aria-current={pathname === link.href ? 'page' : undefined}>
															<span>{link.label}</span>
															{#if link.date}<span class="date">{link.date}</span>{/if}
														</a>
													</li>
												{/each}
											</ul>
										</div>
									{/each}
								</div>
							{/if}
						{:else}
							<a href={href(section.href)} class="section-link" class:active aria-current={active ? 'page' : undefined}>
								{section.label}
							</a>
						{/if}
					</li>
				{/each}
			</ul>
		</nav>

		<button
			type="button"
			class="menu-button"
			aria-expanded={mobileOpen}
			aria-controls="mobile-menu"
			onclick={() => (mobileOpen = !mobileOpen)}
		>
			{mobileOpen ? 'Close' : 'Menu'}
		</button>
	</div>

	{#if mobileOpen}
		<nav class="mobile-nav" id="mobile-menu" aria-label="Main">
			{#each NAV as section (section.label)}
				<div class="mobile-section">
					<a href={href(section.href)} class="mobile-section-link" class:active={isActive(pathname, section.href)}>
						{section.label}
					</a>
					{#if section.groups}
						{#each section.groups as group}
							{#if group.heading}<p class="group-heading">{group.heading}</p>{/if}
							<ul>
								{#each group.links as link (link.href)}
									<li>
										<a href={href(link.href)} aria-current={pathname === link.href ? 'page' : undefined}>
											<span>{link.label}</span>
											{#if link.date}<span class="date">{link.date}</span>{/if}
										</a>
									</li>
								{/each}
							</ul>
						{/each}
					{/if}
				</div>
			{/each}
		</nav>
	{/if}
</header>

<style>
	.site-header {
		--header-pad: var(--site-pad);
		position: relative;
		z-index: 20;
		background: var(--brandWhite);
		border-bottom: 1px solid var(--brandDarkBlue);
	}

	.bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		/* total header height incl. the 1px border = --header-height */
		height: calc(var(--header-height, 60px) - 1px);
		padding: 0 var(--header-pad);
		box-sizing: border-box;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: var(--brand-gap);
		min-width: 0;
	}

	.logo {
		display: block;
		width: var(--logo-width);
		height: 45px;
	}

	.logo-link:hover .logo {
		opacity: 0.75;
	}

	.wordmark {
		padding: 4px 12px;
		background: var(--brandDarkBlue);
		font-family: TradeGothicBold, sans-serif;
		font-size: 20px;
		line-height: 32px;
		color: var(--brandWhite);
		text-decoration: none;
		white-space: nowrap;
	}

	.wordmark:hover {
		background: var(--brandMedBlue);
	}

	/* ---------- desktop */

	.desktop-nav > ul {
		display: flex;
		gap: 4px;
		margin: 0;
		padding: 0;
		list-style: none;
	}

	.section {
		position: relative;
		padding: 0;
		margin: 0;
	}

	.section-link {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		padding: 8px 10px;
		border: none;
		border-radius: 0;
		background: none;
		font-family: TradeGothicBold, sans-serif;
		font-size: 16px;
		color: var(--brandDarkBlue);
		text-decoration: none;
		cursor: pointer;
		white-space: nowrap;
	}

	.section-link:hover {
		background: #f2f6f9;
		color: var(--brandDarkBlue);
	}

	/* selected: current section, or the open dropdown */
	.section-link.active,
	.section-link[aria-expanded='true'] {
		background: var(--brandDarkBlue);
		color: var(--brandWhite);
	}

	.chevron {
		font-size: 12px;
		transition: transform 0.15s ease;
	}

	[aria-expanded='true'] .chevron {
		transform: rotate(180deg);
	}

	.dropdown {
		position: absolute;
		top: 100%;
		left: 0;
		min-width: 320px;
		padding: 8px 0;
		background: var(--brandWhite);
		border: 1px solid var(--brandGray);
		border-top: 2px solid var(--brandDarkBlue);
		border-radius: 0;
		box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
	}

	/* the right-most menu opens leftwards so it stays on screen */
	.section:last-child .dropdown {
		left: auto;
		right: 0;
	}

	.group + .group {
		margin-top: 6px;
		padding-top: 6px;
		border-top: 1px solid var(--brandGray);
	}

	.group-heading {
		margin: 4px 0 2px;
		padding: 0 16px;
		font-family: OpenSansBold, sans-serif;
		font-size: 13px;
		line-height: 18px;
		color: var(--brandGray60);
	}

	.dropdown ul,
	.mobile-nav ul {
		margin: 0;
		padding: 0;
		list-style: none;
	}

	.dropdown li,
	.mobile-nav li {
		padding: 0;
		margin: 0;
	}

	.dropdown a,
	.mobile-nav li a {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		gap: 16px;
		padding: 7px 16px;
		font-family: SourceSerif, serif;
		font-size: 16px;
		line-height: 21px;
		color: var(--brandDarkBlue);
		text-decoration: none;
	}

	.dropdown a:hover,
	.mobile-nav li a:hover {
		background: #f2f6f9;
		color: var(--brandDarkBlue);
	}

	.dropdown a[aria-current='page'],
	.mobile-nav li a[aria-current='page'] {
		color: var(--brandDarkBlue);
		box-shadow: inset 3px 0 0 var(--brandLightBlue);
	}

	.date {
		flex-shrink: 0;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray60);
	}

	/* ---------- mobile */

	.menu-button {
		display: none;
		padding: 6px 12px;
		border: 1px solid var(--brandDarkBlue);
		border-radius: 0;
		background: var(--brandWhite);
		font-family: TradeGothicBold, sans-serif;
		font-size: 15px;
		color: var(--brandDarkBlue);
		cursor: pointer;
	}

	.menu-button[aria-expanded='true'] {
		background: var(--brandDarkBlue);
		color: var(--brandWhite);
	}

	.mobile-nav {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		max-height: calc(100dvh - var(--header-height, 60px));
		overflow-y: auto;
		padding: 8px 0 16px;
		background: var(--brandWhite);
		border-bottom: 1px solid var(--brandDarkBlue);
		box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
	}

	.mobile-section {
		padding: 6px 0;
	}

	.mobile-section + .mobile-section {
		border-top: 1px solid var(--brandGray);
	}

	.mobile-section-link {
		display: block;
		padding: 6px var(--header-pad);
		font-family: TradeGothicBold, sans-serif;
		font-size: 18px;
		color: var(--brandDarkBlue);
		text-decoration: none;
	}

	.mobile-section-link.active {
		color: var(--brandDarkBlue);
	}

	.mobile-nav .group-heading {
		padding: 0 var(--header-pad);
	}

	.mobile-nav li a {
		padding-left: var(--header-pad);
		padding-right: var(--header-pad);
	}

	@media (max-width: 1080px) {
		.desktop-nav {
			display: none;
		}
		.menu-button {
			display: block;
		}
	}

	@media (max-width: 480px) {
		.site-header {
			--header-pad: 16px;
		}
		.logo {
			width: 136px;
			height: 34px;
		}
		.brand {
			gap: 10px;
		}
		.wordmark {
			padding: 2px 8px;
			font-size: 17px;
		}
	}
</style>
