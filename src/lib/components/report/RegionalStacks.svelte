<!--
	Regional distribution: one 100% stacked bar per effect type (direct / indirect /
	induced), split by where Canada's loss occurs. Each region keeps the same colour
	in every figure; regions under 5% of every bar are grouped as "All other regions".
	Regions are named directly under the bottom bar (no separate colour key).
	rows: [{ label, direct, indirect, induced }] (shares of Canada's total, %).
-->
<script>
	import { EFFECTS, INK, C, FONT, textWidth } from './theme.js';

	let { rows, width } = $props();

	// warm palette used only by these charts (rust -> terracotta -> amber -> sand), fixed per
	// region so a province reads the same across Figures 5, 8, 11, 13; names label each section
	const REGION_COLOURS = {
		Ontario: { fill: '#6B2410', text: 'white' },
		Quebec: { fill: '#9A3412', text: 'white' },
		'British Columbia': { fill: '#C2410C', text: 'white' },
		Alberta: { fill: '#B45309', text: 'white' },
		Saskatchewan: { fill: '#D97706', text: C.g90 },
		Manitoba: { fill: '#E07A5F', text: C.g90 },
		'New Brunswick': { fill: '#A16207', text: 'white' },
		'Nova Scotia': { fill: '#F2A65A', text: C.g90 },
		'Newfoundland & Labrador': { fill: '#8C4A2F', text: 'white' },
		'Prince Edward Island': { fill: '#F6C28B', text: C.g90 }
	};
	const OTHER = { label: 'All other regions', fill: C.g30, text: C.g90 };
	const MIN_SHARE = 5;

	// regions shown on their own, largest overall first; the rest grouped
	const shown = $derived(
		rows
			.filter((r) => REGION_COLOURS[r.label] && EFFECTS.some((e) => r[e.key] >= MIN_SHARE))
			.sort((a, b) => EFFECTS.reduce((s, e) => s + b[e.key] - a[e.key], 0))
	);
	const other = $derived(
		Object.fromEntries(EFFECTS.map((e) => [e.key, rows.filter((r) => !shown.includes(r)).reduce((s, r) => s + r[e.key], 0)]))
	);
	const series = $derived([
		...shown.map((r) => ({ label: r.label, ...REGION_COLOURS[r.label], values: r })),
		...(EFFECTS.some((e) => other[e.key] >= 0.5) ? [{ ...OTHER, values: other }] : [])
	]);

	// full-width bars, each with its name left-aligned above it
	const LABEL_W = 0;
	const BAR = 24;
	const NAME_H = 18; // effect name above each bar
	const GAP = 12;
	const TOP = 0;
	const plotW = $derived(Math.max(100, width - LABEL_W));
	const barY = (i) => TOP + i * (NAME_H + BAR + GAP) + NAME_H;
	const barsBottom = barY(EFFECTS.length - 1) + BAR;

	// region names directly under the bottom bar's sections (same order in every bar).
	// Each name goes centred under its section (row 0) when it fits; otherwise it steps
	// down to the highest free row with its text ending at its own leader line. No name
	// may sit across a leader, and no leader may run through a name.
	const LINE = 17;
	const NAMES_TOP = 24; // bar bottom -> first row's baseline (leaves a visible stub)
	const rowY = (row) => barsBottom + NAMES_TOP + row * LINE;
	const names = $derived.by(() => {
		const placed = [];
		const clear = (c) =>
			placed.every((p) => {
				if (p.row === c.row && c.left < p.right + 10 && c.right > p.left - 10) return false;
				// my leader runs down through rows above mine
				if (c.row > p.row && c.cx > p.left - 3 && c.cx < p.right + 3) return false;
				// p's leader runs down through rows above p's
				if (p.row > c.row && p.cx > c.left - 3 && p.cx < c.right + 3) return false;
				return true;
			});
		const segs = segments(EFFECTS.at(-1).key);
		const centres = segs.map((s) => s.x + s.w / 2);
		return segs.map((s, i) => {
			const tw = textWidth(s.label);
			const cx = centres[i];
			const cl = Math.min(Math.max(cx - tw / 2, LABEL_W), width - tw);
			let n = { ...s, cx, left: cl, right: cl + tw, row: 0, beside: false };
			// a centred name must not sit over any other section's leader (every section has one)
			const coversLeader = centres.some((c, j) => j !== i && c > cl - 4 && c < cl + tw + 4);
			if (cl > cx || cl + tw < cx || coversLeader || !clear(n)) {
				const left = Math.max(LABEL_W, cx - 4 - tw);
				const beside = left === cx - 4 - tw;
				let row = 1;
				for (; row < 12; row++) {
					n = { ...s, cx, left, right: beside ? cx : left + tw, row, beside };
					if (clear(n)) break;
				}
			}
			placed.push(n);
			return n;
		});
	});
	const nameRows = $derived(Math.max(1, ...names.map((n) => n.row + 1)));
	const height = $derived(rowY(nameRows - 1) + 6);

	function segments(effectKey) {
		let left = 0;
		return series.map((s) => {
			const v = s.values[effectKey];
			const w = (v / 100) * plotW;
			const seg = { ...s, v, x: LABEL_W + left, w };
			left += w;
			return seg;
		});
	}
	const pct = (v) => `${Math.round(v)}%`;
</script>

<svg {width} {height} role="img" aria-label="Where Canada's loss occurs, by effect type">
	{#each EFFECTS as e, i (e.key)}
		{@const y = barY(i)}
		<text x={LABEL_W} y={y - 6} fill={INK} style="font-family: OpenSansBold">{e.label}</text>
		{#each segments(e.key) as s (s.label)}
			<rect x={s.x} y={y} width={Math.max(0, s.w - 1)} height={BAR} fill={s.fill} />
			{#if s.w >= textWidth(pct(s.v), FONT.value, true) + 8}
				<text x={s.x + s.w / 2} y={y + BAR / 2} dy="0.35em" text-anchor="middle" fill={s.text} style="font-family: OpenSansBold">{pct(s.v)}</text>
			{/if}
		{/each}
	{/each}
	<!-- leaders first, names on top with a thin white halo in case one still touches -->
	{#each names as n (n.label)}
		{@const ty = rowY(n.row)}
		<!-- centred names: stop just above the text; stepped names: run down beside the text's end -->
		<line x1={n.cx} x2={n.cx} y1={barsBottom + 1} y2={n.beside ? ty - 4 : ty - 13} stroke={n.fill} stroke-width="1.5" />
	{/each}
	{#each names as n (n.label)}
		<text x={n.beside ? n.cx - 4 : n.left} y={rowY(n.row)} text-anchor={n.beside ? 'end' : 'start'} fill={INK} stroke="white" stroke-width="2" paint-order="stroke" stroke-linejoin="round">{n.label}</text>
	{/each}
</svg>
