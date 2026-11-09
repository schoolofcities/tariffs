<script>
	/**
	 * "On this page" menu (from the place-and-politics five-torontos story): lists the page's
	 * sections, highlights the one being read, and jumps on click. Fixed top left: just below the
	 * site header, then near the top of the screen once that scrolls away. Wide screens: the list
	 * in the left margin. Narrower screens: a "Sections" button, top left, that opens the list.
	 *
	 * items: [{ id, label, level? }] in page order; `id` is the section/heading element's id;
	 * level 2 entries are sub-sections, shown indented.
	 * title: optional heading above the list (wide screens only), linking to the first item.
	 * The site footer has priority: the menu stops at the footer's top edge (scrolling inside
	 * if it's longer) and hides once there's no room left.
	 */
	import { onMount } from 'svelte';

	let { items = [], title = '' } = $props();

	let activeId = $state(items[0]?.id);
	let open = $state(false);
	let scrollY = $state(0);

	const TOP_START = 76; // px: below the 60px site header
	const TOP_MIN = 8; // px: once scrolled past the header
	const top = $derived(Math.max(TOP_MIN, TOP_START - scrollY));

	// The site footer has priority: the menu never extends past its top edge. `space` is
	// the height available between the menu's top and the footer (or the window bottom),
	// less a 16px gap; the list scrolls inside it, and the menu hides once it's too small.
	const GAP = 16;
	const MIN_SPACE = 60; // px: below this, hide the menu rather than show a sliver
	let limit = $state(Infinity); // px from the window top: footer top, or window height
	const space = $derived(limit - top - GAP);

	function measure() {
		const footer = document.querySelector('footer.footer');
		const footerTop = footer ? footer.getBoundingClientRect().top : Infinity;
		limit = Math.min(window.innerHeight, footerTop);
	}

	// The current section is the last one whose heading has passed a line a quarter of the
	// way down the screen. After a click, the clicked entry is held while the jump scrolls.
	let lockUntil = 0;
	let frame = 0;

	function update() {
		frame = 0;
		measure();
		if (Date.now() < lockUntil) return;
		const line = window.innerHeight * 0.25;
		let current = items[0]?.id;
		for (const item of items) {
			const el = document.getElementById(item.id);
			if (el && el.getBoundingClientRect().top <= line) current = item.id;
		}
		activeId = current;
	}

	onMount(() => {
		const onScroll = () => {
			if (!frame) frame = requestAnimationFrame(update);
		};
		window.addEventListener('scroll', onScroll, { passive: true });
		window.addEventListener('resize', onScroll);
		update();
		return () => {
			window.removeEventListener('scroll', onScroll);
			window.removeEventListener('resize', onScroll);
			cancelAnimationFrame(frame);
		};
	});

	function jump(event, id) {
		const el = document.getElementById(id);
		if (!el) return;
		event.preventDefault();
		const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		el.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
		history.replaceState(history.state, '', `${location.search}#${id}`);
		activeId = id;
		lockUntil = Date.now() + (reduceMotion ? 100 : 1200);
		open = false;
	}
</script>

<svelte:window bind:scrollY />

<nav
	class="section-nav"
	class:open
	class:no-room={space < MIN_SPACE}
	aria-label="Sections on this page"
	style:--nav-top="{top}px"
	style:--nav-space={Number.isFinite(space) ? `${space}px` : null}
>
	<button type="button" class="nav-toggle" aria-expanded={open} aria-controls="section-nav-list" onclick={() => (open = !open)}>
		Sections
	</button>
	{#if title}
		<a class="nav-title" href="#{items[0]?.id}" onclick={(e) => jump(e, items[0]?.id)}>{title}</a>
	{/if}
	<ol id="section-nav-list">
		{#each items as item, i (item.id)}
			<li class:sub={item.level === 2} class:top={i === 0}>
				<a
					href="#{item.id}"
					class:active={item.id === activeId}
					aria-current={item.id === activeId ? 'location' : undefined}
					onclick={(e) => jump(e, item.id)}
				>
					{item.label}
				</a>
			</li>
		{/each}
	</ol>
</nav>

<style>
	/* pages can place the list with --section-nav-left / --section-nav-width */
	.section-nav {
		position: fixed;
		top: var(--nav-top);
		left: var(--section-nav-left, 16px);
		z-index: 15;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		line-height: 1.3;
	}

	/* footer fills (nearly) the whole screen: hide the menu so it never sits on the footer */
	.section-nav.no-room {
		visibility: hidden;
	}

	ol {
		list-style: none;
		margin: 0;
		padding: 0;
	}

	/* explicit font: the site's global li/a styles would otherwise switch to the serif body font */
	li,
	a {
		padding: 0;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		line-height: 1.3;
	}

	li + li {
		margin-top: 2px;
	}

	li.sub a {
		padding-left: 18px;
		color: var(--brandGray80);
	}

	li:not(.sub) + li:not(.sub) {
		margin-top: 6px;
	}

	a {
		display: block;
		padding: 3px 8px;
		border-left: 2px solid transparent;
		color: var(--brandGray90);
		text-decoration: none;
	}

	a:hover,
	li.sub a:hover {
		background: #f2f6f9;
		color: var(--brandBlack);
	}

	/* current section: the line on the left matches the page's heading colours —
	   first entry (page top / title) in the section colour (the square beside the title),
	   main sections light blue (h2 bars), sub-sections light green (h3 lines) */
	a.active,
	li.sub a.active {
		border-left-color: var(--brandLightBlue);
		color: var(--brandBlack);
		font-family: OpenSansBold, sans-serif;
	}

	li.sub a.active {
		border-left-color: var(--brandLightGreen);
	}

	li.top a.active {
		border-left-color: var(--section-colour, var(--brandLightBlue));
	}

	/* the page's title above the list (wide screens only; hidden behind the button below) */
	a.nav-title {
		display: none;
	}

	/* Wide screens: the list in the left margin, beside the content column */
	@media (min-width: 1250px) {
		a.nav-title {
			display: block;
			margin-bottom: 12px;
			padding: 0 8px 10px 10px;
			border-left: none;
			border-bottom: 1px solid var(--brandGray20, #cccccc);
			/* same text style as the section entries below */
			font-family: OpenSans, sans-serif;
			font-size: 12px;
			line-height: 1.3;
			color: var(--brandGray90);
		}
		a.nav-title:hover {
			background: none;
			color: var(--brandMedBlue);
		}
		.section-nav {
			width: var(--section-nav-width, 190px);
			/* up to the footer's top edge (or the window bottom); scrolls inside if longer */
			max-height: var(--nav-space, calc(100vh - var(--nav-top) - 16px));
			overflow-y: auto;
		}
		.nav-toggle {
			display: none;
		}
	}

	/* Narrower screens: a small button, top left (below the header, then near the top of
	   the screen once it scrolls away); the list opens below it */
	@media (max-width: 1249px) {
		.section-nav {
			left: 12px;
		}
		.nav-toggle {
			padding: 5px 10px;
			border: 1px solid #c8c8c8;
			background: white;
			box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
			font-family: OpenSans, sans-serif;
			font-size: 13px;
			color: var(--brandGray90);
			cursor: pointer;
		}
		.nav-toggle:hover {
			border-color: #9ba1a8;
		}
		ol {
			display: none;
			position: absolute;
			left: 0;
			top: calc(100% + 6px);
			/* below the button (~36px with its gap), never past the footer's top edge */
			max-height: min(70vh, calc(var(--nav-space, 70vh) - 36px));
			overflow-y: auto;
			width: 230px;
			padding: 6px 0;
			background: white;
			border: 1px solid #c8c8c8;
			box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
		}
		.open ol {
			display: block;
		}
	}
</style>
