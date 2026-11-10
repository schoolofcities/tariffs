<!--
	A run of report content: HTML segments and figure segments (see $lib/content/scenarios-report.js).
	Links to the site's own files in that HTML use a {base} placeholder (e.g. the appendix PDF),
	filled in here so they work under any base path.
-->
<script>
	import { base } from '$app/paths';
	import ReportFigure from './ReportFigure.svelte';

	let { segments = [], figureData = {} } = $props();
</script>

{#each segments as seg, i (i)}
	{#if seg.figure}
		<ReportFigure n={seg.figure} rows={figureData[seg.figure] ?? []} caption="Figure {seg.figure}: {seg.caption}" />
	{:else}
		{@html seg.html.replaceAll('{base}', base)}
	{/if}
{/each}
