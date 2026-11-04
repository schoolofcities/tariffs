<!-- A run of report content: HTML segments and figure segments (see build_report_content.py). -->
<script>
	import ReportFigure from './ReportFigure.svelte';

	let { segments = [], figureData = {} } = $props();
</script>

{#each segments as seg, i (i)}
	{#if seg.figure}
		<ReportFigure n={seg.figure} rows={figureData[seg.figure] ?? []} caption="Figure {seg.figure}: {seg.caption}" />
	{:else}
		{@html seg.html}
	{/if}
{/each}
