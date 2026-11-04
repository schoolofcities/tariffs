<script>
	/** Right-aligned category label inside a chart <svg>, wrapped to 2 lines when it doesn't fit `maxW`. */
	import { wrapLabel, FONT } from './theme.js';

	let { x, y, text, maxW, fill, bold = false } = $props();
	const lines = $derived(wrapLabel(text, maxW, FONT.label, bold));
</script>

<text {x} {y} text-anchor="end" {fill} style:font-family={bold ? 'OpenSansBold' : null}>
	{#each lines as line, k}
		<tspan {x} dy={k === 0 ? `${0.35 - (lines.length - 1) * 0.6}em` : '1.2em'}>{line}</tspan>
	{/each}
</text>
