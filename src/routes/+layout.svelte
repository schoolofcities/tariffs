<script>
	import '$lib/styles/global.css';
	import SiteHeader from '$lib/components/layout/SiteHeader.svelte';
	import PasswordGate from '$lib/components/layout/PasswordGate.svelte';
	import { page } from '$app/state';
	import { root } from '$lib/site/paths.js';
	import { colourFor } from '$lib/site/nav.js';
	import { BRAND_CSS_VARS } from '$lib/styles/brand.js';

	let { children } = $props();

	// The current page's section colour (set per section in $lib/site/nav.js), passed to
	// every page as var(--section-colour): the square beside page titles, the
	// table-of-contents marker, etc.
	const sitePath = $derived(page.url.pathname.startsWith(root) ? page.url.pathname.slice(root.length) || '/' : page.url.pathname);
	const sectionColour = $derived(colourFor(sitePath));
</script>

<!-- the brand colour variables (--brandDarkBlue, …), from $lib/styles/brand.js -->
<svelte:head>
	{@html `<style>${BRAND_CSS_VARS}</style>`}
</svelte:head>

<!-- while in development: one password for the whole site, remembered per browser -->
<PasswordGate />

<SiteHeader />

<!-- display: contents, so this wrapper only carries the variable and doesn't affect layout -->
<div style="display: contents" style:--section-colour={sectionColour}>
	{@render children()}
</div>
