<script>
	import ExposureMap from '$lib/components/maps/exposure/ExposureMap.svelte';

	const title = 'Mapping potential direct exposure of U.S. tariffs in Canada';
	const description = 'Interactive map of businesses and jobs directly exposed to U.S. tariffs across Canadian neighbourhoods and municipalities.';
</script>

<svelte:head>
	<title>{title} | Mapping Tariffs</title>
	<meta name="description" content={description} />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={description} />
</svelte:head>

<ExposureMap />
