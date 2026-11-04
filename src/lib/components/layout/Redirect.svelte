<script>
	/**
	 * Redirect for an old URL on a static host (GitHub Pages can't send 301s).
	 * An inline head script redirects immediately and keeps any ?query/#hash;
	 * the delayed meta refresh is a no-JS fallback; the canonical link tells
	 * search engines where the page moved.
	 *
	 * to: the new page's path within the site (e.g. "/exposure/map"); pages live under
	 * /mt/, which is added here.
	 */
	import { root, SITE_ROOT } from '$lib/site/paths.js';

	let { to } = $props();
	const target = $derived(`${root}${to}`);
	const script = $derived(
		`<script>location.replace(${JSON.stringify(target)} + location.search + location.hash)</` + `script>`
	);
</script>

<svelte:head>
	<title>Moved | Mapping Tariffs</title>
	{@html script}
	<meta http-equiv="refresh" content="2; url={target}" />
	<link rel="canonical" href="https://mappingtariffs.org{SITE_ROOT}{to}" />
	<meta name="robots" content="noindex" />
</svelte:head>

<main class="text">
	<p>This page has moved to <a href={target}>{target}</a>.</p>
</main>
