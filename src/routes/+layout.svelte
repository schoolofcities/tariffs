<script>
	import '$lib/styles/global.css';
	import SiteHeader from '$lib/components/layout/SiteHeader.svelte';
	import { page } from '$app/state';
	import { pagePath } from '$lib/site/paths.js';
	import { colourFor } from '$lib/site/nav.js';
	import { BRAND_CSS_VARS } from '$lib/styles/brand.js';

	let { children } = $props();

	// The current page's section colour (set per section in $lib/site/nav.js), passed to
	// every page as var(--section-colour): the square beside page titles, the
	// table-of-contents marker, etc.
	const sectionColour = $derived(colourFor(pagePath(page.url.pathname)));
</script>

<!-- the brand colour variables (--brandDarkBlue, …), from $lib/styles/brand.js -->
<svelte:head>
	{@html `<style>${BRAND_CSS_VARS}</style>`}
</svelte:head>

<SiteHeader />

<!-- display: contents, so this wrapper only carries the variable and doesn't affect layout -->
<div style="display: contents" style:--section-colour={sectionColour}>
	{@render children()}
</div>
