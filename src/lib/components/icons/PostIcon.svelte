<script>
	/**
	 * Post / article icon: an outlined page with a picture block and text lines, like a
	 * news story. Outline-only frame keeps it distinct from DocumentIcon (solid page) and
	 * BarChartIcon (solid bars).
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
	<!-- drawn at 85% of the box, centred: the outline makes it look bigger than the solid icons -->
	<g transform="translate(50 43.7) scale(0.85) translate(-50 -43.7)">
		<!-- page outline -->
		<rect x="8" y="5" width="84" height="77.4" fill="none" stroke="currentColor" stroke-width="8" />
		<!-- picture, top left -->
		<rect x="22" y="19" width="26" height="24" fill="currentColor" />
		<!-- text beside and below it -->
		<rect x="55" y="20" width="23" height="7" fill="currentColor" />
		<rect x="55" y="35" width="23" height="7" fill="currentColor" />
		<rect x="22" y="52" width="56" height="7" fill="currentColor" />
		<rect x="22" y="65" width="38" height="7" fill="currentColor" />
	</g>
</svg>
