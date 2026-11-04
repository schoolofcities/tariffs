<script>
	/** Inline direct / indirect / induced legend, for use inside a chart <svg>. */
	import { EFFECTS, INK, textWidth } from './theme.js';

	let { x = 0, y = 0 } = $props();

	const items = EFFECTS.reduce((acc, e) => {
		const prev = acc.at(-1);
		const at = prev ? prev.at + 18 + textWidth(prev.label) + 14 : 0;
		return [...acc, { ...e, at }];
	}, []);
</script>

<g transform="translate({x}, {y})">
	{#each items as e (e.key)}
		<rect x={e.at} y="-6" width="12" height="12" fill={e.colour} />
		<text x={e.at + 18} y="0" dy="0.35em" fill={INK}>{e.label}</text>
	{/each}
</g>
