<script>
	/**
	 * Legend for AreaMap. Uses the same breaks/colours/sizes as the map, so it
	 * can't disagree with it.
	 *   mode 'fill':   5 colour steps + "no data" swatch, ticks at the breaks
	 *   mode 'circle': graduated circles, largest first
	 */
	import { NO_DATA_COLOUR } from '$lib/maps/styleExpressions.js';

	let { mode, breaks, colours, sizes = [], formatBreak = (b) => String(b) } = $props();

	const BOX = 56;
	const GAP = 1;

	// Circle rows, largest first, spaced by their radii.
	const circleRows = $derived.by(() => {
		const labels = [
			`> ${formatBreak(breaks[3])}`,
			`${formatBreak(breaks[2] + 1)} – ${formatBreak(breaks[3])}`,
			`${formatBreak(breaks[1] + 1)} – ${formatBreak(breaks[2])}`,
			`${formatBreak(breaks[0] + 1)} – ${formatBreak(breaks[1])}`,
			`1 – ${formatBreak(breaks[0])}`
		];
		let y = 4;
		return [4, 3, 2, 1, 0].map((k, row) => {
			const r = sizes[k];
			const cy = y + r;
			y = cy + r + 8;
			return { r, cy, colour: colours[k], label: labels[row] };
		});
	});

	const circleHeight = $derived(circleRows.at(-1).cy + circleRows.at(-1).r + 4);
</script>

{#if mode === 'fill'}
	<svg width={5 * (BOX + GAP) + 80} height="40" role="img" aria-label="Map legend">
		{#each colours as colour, i}
			<rect x={i * (BOX + GAP)} y="0" width={BOX} height="18" fill={colour} />
		{/each}
		{#each breaks as b, i}
			<text x={(i + 1) * (BOX + GAP) - GAP / 2} y="34" text-anchor="middle">{formatBreak(b)}</text>
		{/each}
		<rect x={5 * (BOX + GAP) + 16} y="0" width={BOX} height="18" fill={NO_DATA_COLOUR} />
		<text x={5 * (BOX + GAP) + 16 + BOX / 2} y="34" text-anchor="middle">no data</text>
	</svg>
{:else}
	<svg width="300" height={circleHeight} role="img" aria-label="Map legend">
		{#each circleRows as row}
			<circle cx="40" cy={row.cy} r={row.r} fill={row.colour} fill-opacity="0.5" stroke={row.colour} />
			<text x="90" y={row.cy} dy="0.35em">{row.label}</text>
		{/each}
	</svg>
{/if}

<style>
	svg {
		display: block;
		max-width: 100%;
		overflow: visible;
	}

	text {
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		fill: var(--brandGray90);
	}
</style>
