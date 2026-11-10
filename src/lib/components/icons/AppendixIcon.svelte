<script>
	/**
	 * Appendix / technical document icon: two stacked pages, the front one with a small
	 * table (vs DocumentIcon's single page with text lines).
	 */
	let { size = 56, title = '' } = $props();
</script>

<svg
	viewBox="0 0 100 87.4"
	width={size}
	height={(size * 87.4) / 100}
	role={title ? 'img' : undefined}
	aria-hidden={title ? undefined : 'true'}
>
	{#if title}<title>{title}</title>{/if}
	<!-- back page, offset up and right -->
	<path fill="currentColor" opacity="0.45" d="M34 2h36l14 14v57H34z" />
	<!-- front page with folded corner -->
	<path fill="currentColor" d="M20 14h36l14 14v57H20z" />
	<path fill="white" d="M56 14v14h14z" opacity="0.5" />
	<!-- a small table: header row + 3 rows x 2 columns -->
	<rect x="28" y="38" width="34" height="6" fill="white" />
	{#each [50, 60, 70] as y}
		<rect x="28" {y} width="15" height="5" fill="white" />
		<rect x="47" {y} width="15" height="5" fill="white" />
	{/each}
</svg>
