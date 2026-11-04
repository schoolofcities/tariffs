<!--
	100% stacked bars: each region's loss split into direct / indirect / induced.
	rows: [{ label, direct, indirect, induced }] in display order; a "Canada" row is
	drawn first and set apart.
-->
<script>
	import { EFFECTS, INK, INK2, C, FONT, textWidth, effectLegendWidth, wrapLabel } from './theme.js';
	import AxisLabel from './AxisLabel.svelte';
	import EffectLegend from './EffectLegend.svelte';

	let { rows, width, highlight = [] } = $props();

	const BAR = 18;
	const GAP = 10; // after the Canada row

	const ordered = $derived([...rows.filter((r) => r.label === 'Canada'), ...rows.filter((r) => r.label !== 'Canada')]);
	const labelW = $derived(Math.min(width * 0.45, Math.max(...ordered.map((r) => textWidth(r.label, FONT.label, true))) + 8));
	const plotW = $derived(Math.max(60, width - labelW));
	// every section gets its %: inside when it fits, otherwise just above the bar
	const pct = (v) => `${Math.round(v)}%`;
	const fits = (s) => s.w >= textWidth(pct(s.v), FONT.value, s.key === 'direct') + 6;
	const anyOutside = $derived(ordered.some((r) => segments(r).some((s) => !fits(s))));
	const LABEL_ABOVE = 14;
	const ROW = $derived((ordered.some((r) => wrapLabel(r.label, labelW - 8, FONT.label, true).length > 1) ? 32 : 24) + (anyOutside ? LABEL_ABOVE : 0));
	/** x positions (text-anchor start) for labels above the bar, nudged so they don't overlap */
	function aboveX(segs) {
		const out = {};
		let end = -Infinity;
		for (const s of segs) {
			if (fits(s)) continue;
			const tw = textWidth(pct(s.v), FONT.value);
			const want = s.key === 'direct' ? Math.max(s.x, labelW) : s.x + s.w / 2 - tw / 2;
			const x = Math.max(want, end + 6);
			out[s.key] = x;
			end = x + tw;
		}
		return out;
	}
	const barTop = (y) => y + ROW - (ROW - (anyOutside ? LABEL_ABOVE : 0) + BAR) / 2;
	const y0 = 30;
	const yOf = (i) => y0 + i * ROW + (i > 0 && ordered[0]?.label === 'Canada' ? GAP : 0);
	const height = $derived(yOf(ordered.length) + 4);

	function segments(r) {
		let left = 0;
		return EFFECTS.map((e) => {
			const w = (r[e.key] / 100) * plotW;
			const seg = { ...e, x: labelW + left, w, v: r[e.key] };
			left += w;
			return seg;
		});
	}
</script>

<svg {width} {height} role="img" aria-label="Share of losses by effect type">
	<EffectLegend x={Math.max(0, Math.min(labelW, width - effectLegendWidth()))} y={10} />
	{#each ordered as r, i (r.label)}
		{@const y = yOf(i)}
		{@const bold = r.label === 'Canada' || highlight.includes(r.label)}
		<AxisLabel x={labelW - 6} y={barTop(y) + BAR / 2} text={r.label} maxW={labelW - 8} fill={bold ? INK : INK2} {bold} />
		{@const segs = segments(r)}
		{@const above = aboveX(segs)}
		{#each segs as s (s.key)}
			<rect x={s.x} y={barTop(y)} width={Math.max(0, s.w - 1)} height={BAR} fill={s.colour} />
			{#if fits(s)}
				<text x={s.x + s.w / 2} y={barTop(y) + BAR / 2} dy="0.35em" text-anchor="middle" fill={s.text} style:font-family={s.key === 'direct' ? 'OpenSansBold' : null}>{pct(s.v)}</text>
			{:else}
				<!-- too narrow: label just above the section -->
				<text x={above[s.key]} y={barTop(y) - 4} fill={INK2}>{pct(s.v)}</text>
			{/if}
		{/each}
	{/each}
	{#if ordered[0]?.label === 'Canada'}
		<line x1="0" x2={width} y1={yOf(1) - GAP / 2} y2={yOf(1) - GAP / 2} stroke={C.g20} />
	{/if}
</svg>
