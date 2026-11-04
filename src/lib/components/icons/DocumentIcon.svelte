<script>
	/** Report / document icon: page with text lines. */
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
	<path fill="currentColor" d="M24 2h40l18 18v65H24z" />
	<path fill="white" d="M64 2v18h18z" opacity="0.5" />
	{#each [30, 42, 54, 66] as y, i}
		<rect x="34" {y} width={i === 3 ? 26 : 38} height="6" fill="white" />
	{/each}
</svg>
