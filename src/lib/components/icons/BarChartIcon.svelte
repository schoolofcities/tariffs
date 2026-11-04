<script>
	/** Ranked horizontal bar chart icon. */
	let { size = 56, title = '' } = $props();

	const bars = [92, 74, 58, 44, 30];
</script>

<svg
	viewBox="0 0 100 87.4"
	width={size}
	height={(size * 87.4) / 100}
	role={title ? 'img' : undefined}
	aria-hidden={title ? undefined : 'true'}
>
	{#if title}<title>{title}</title>{/if}
	{#each bars as w, i}
		<rect x="4" y={4 + i * 17} width={w} height="11" fill="currentColor" />
	{/each}
</svg>
