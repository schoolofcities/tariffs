<script>
	/** Page <head> tags: title, description, canonical URL and social cards. */
	import { page } from '$app/state';
	import { base } from '$app/paths';

	const SITE_URL = 'https://mappingtariffs.org';
	const DEFAULT_IMAGE = `${SITE_URL}/web-card.png`;

	let { title, description = '', image = DEFAULT_IMAGE, type = 'article' } = $props();

	const fullTitle = $derived(title ? `${title} | Mapping Tariffs` : 'Mapping Tariffs | School of Cities');
	// Page path within the site. In prerendered pages `base` is relative ('..', '../..'),
	// not a path prefix, so only strip it when it's an absolute prefix like '/tariffs-v2'.
	const sitePath = $derived(base.startsWith('/') ? page.url.pathname.slice(base.length) : page.url.pathname);
	const url = $derived(SITE_URL + (sitePath || '/'));
</script>

<svelte:head>
	<title>{fullTitle}</title>
	{#if description}<meta name="description" content={description} />{/if}
	<meta name="author" content="School of Cities" />
	<link rel="canonical" href={url} />

	<meta property="og:title" content={title || 'Mapping Tariffs'} />
	{#if description}<meta property="og:description" content={description} />{/if}
	<meta property="og:type" content={type} />
	<meta property="og:url" content={url} />
	<meta property="og:image" content={image} />
	<meta property="og:locale" content="en_CA" />
	<meta property="og:site_name" content="Mapping Tariffs" />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={title || 'Mapping Tariffs'} />
	{#if description}<meta name="twitter:description" content={description} />{/if}
	<meta name="twitter:image" content={image} />
</svelte:head>
