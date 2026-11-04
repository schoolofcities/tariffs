<!--
	Horizontal bars, largest at top, every value labelled, one colour per chart
	(optional highlighted rows in highlightColour). Optional dashed reference line (e.g. Canada's rate).
	rows: [{ label, value }]
-->
<script>
	import { RANKED, INK, INK2, C, FONT, SUBTITLE_STYLE, textWidth, wrapLabel } from './theme.js';
	import AxisLabel from './AxisLabel.svelte';

	let { rows, width, highlight = [], ref = null, format = (v) => v.toLocaleString('en-CA'), heading = '', refSpace = false, highlightColour = RANKED.total, contextColour = RANKED.per1000 } = $props();

	const BAR = 15;

	const sorted = $derived([...rows].sort((a, b) => b.value - a.value));
	const labelW = $derived(Math.min(width * 0.6, Math.max(...sorted.map((r) => textWidth(r.label, FONT.label, highlight.includes(r.label)))) + 8));
	const wraps = $derived(sorted.some((r) => wrapLabel(r.label, labelW - 8, FONT.label, highlight.includes(r.label)).length > 1));
	const ROW = $derived(wraps ? 32 : 22);
	const valueW = $derived(Math.max(...sorted.map((r) => textWidth(format(r.value), FONT.value, true))) + 8);
	const max = $derived(Math.max(...sorted.map((r) => r.value), ref?.value ?? 0));
	const plotW = $derived(Math.max(40, width - labelW - valueW));
	const x = (v) => labelW + (v / max) * plotW;

	// refSpace: reserve the reference-label row even without a line, so side-by-side panels align
	const headH = $derived((heading ? 22 : 0) + (ref || refSpace ? 18 : 4));
	const height = $derived(headH + sorted.length * ROW + 4);
</script>

<svg {width} {height} role="img" aria-label={heading || 'Ranked bar chart'}>
	{#if heading}
		<!-- centred over the bars, kept inside the chart -->
		{@const half = textWidth(heading, 12, true) / 2 + 2}
		<text x={Math.min(Math.max(labelW + (width - labelW) / 2, half), width - half)} y="14" text-anchor="middle" style={SUBTITLE_STYLE}>{heading}</text>
	{/if}
	<line x1={labelW} x2={labelW} y1={headH - 2} y2={height} stroke={C.g30} stroke-width="1" />
	{#each sorted as r, i (r.label)}
		{@const y = headH + i * ROW}
		{@const hi = highlight.includes(r.label)}
		<AxisLabel x={labelW - 6} y={y + ROW / 2} text={r.label} maxW={labelW - 8} fill={hi ? INK : INK2} bold={hi} />
		<rect x={labelW} y={y + (ROW - BAR) / 2} width={Math.max(0, x(r.value) - labelW)} height={BAR} fill={hi ? highlightColour : contextColour} />
		<!-- value in the bar's colour, with a thin white halo so it reads over the reference line -->
		<text x={x(r.value) + 4} y={y + ROW / 2} dy="0.35em" fill={hi ? highlightColour : contextColour} stroke="white" stroke-width="3" paint-order="stroke" stroke-linejoin="round" style="font-family: OpenSansBold">{format(r.value)}</text>
	{/each}
	{#if ref}
		<!-- Canada reference line + label in brandRed -->
		<line x1={x(ref.value)} x2={x(ref.value)} y1={headH - 4} y2={height} stroke={C.red} stroke-width="1.2" stroke-dasharray="3 2" />
		<text x={x(ref.value)} y={headH - 7} text-anchor="middle" fill={C.red} style="font-family: OpenSansBold">{ref.label} {format(ref.value)}</text>
	{/if}
</svg>
