<!--
	Figure 1: monthly Canadian exports to the U.S. (top: unadjusted + seasonally
	adjusted, $ billions) and year-over-year change (bottom), with the March 2025
	tariff date marked.
	rows: [{ month: 'YYYY-MM', exports_unadjusted_millions, exports_seasonally_adjusted_millions, yoy_pct_change }]
-->
<script>
	import { scaleLinear } from 'd3';
	import { C, INK, INK2, SUBTITLE_STYLE } from './theme.js';

	const UNADJUSTED = '#00A189'; // brandMedGreen
	const TARIFF_COLOUR = '#6D247A'; // brandPurple

	let { rows, width } = $props();

	const pts = $derived(
		rows.map((r) => {
			const [y, m] = String(r.month).split('-').map(Number);
			return { t: y + (m - 1) / 12, un: r.exports_unadjusted_millions / 1000, sa: r.exports_seasonally_adjusted_millions / 1000, yoy: r.yoy_pct_change };
		})
	);

	const L = 46; // y-axis labels
	const R = $derived(width < 520 ? 12 : 92); // room for line labels on wide screens
	// room between the panel label and the top gridline (plus a line key on narrow screens)
	const narrow = $derived(width < 520);
	const TOP = $derived(narrow ? 62 : 40);
	const H1 = 210;
	const GAP = 62;
	const H2 = 120;
	const height = $derived(TOP + H1 + GAP + H2 + 26);
	const TARIFF = 2025 + 2 / 12;

	const x = $derived(scaleLinear().domain([2015.95, 2026.3]).range([L, width - R]));
	const y1 = $derived(scaleLinear().domain([0, 70]).range([TOP + H1, TOP]));
	const y2 = $derived(scaleLinear().domain([-85, 85]).range([TOP + H1 + GAP + H2, TOP + H1 + GAP]));

	const path = (key) => pts.map((p, i) => `${i ? 'L' : 'M'}${x(p.t).toFixed(1)},${y1(p[key]).toFixed(1)}`).join('');
	const years = $derived(Array.from({ length: 11 }, (_, i) => 2016 + i).filter((yr, i) => width >= 520 || i % 2 === 0));
	const barW = $derived(Math.max(1, ((x(2017) - x(2016)) / 12) * 0.72));
	const last = $derived(pts.at(-1));
	const covid = $derived(pts.slice(0, 60).reduce((a, b) => (b.yoy < a.yoy ? b : a)));
	const fmtPct = (v) => (v > 0 ? `+${v}%` : v < 0 ? `−${Math.abs(v)}%` : '0%');
</script>

<svg {width} {height} role="img" aria-label="Canadian exports to the U.S., January 2016 to March 2026">
	<!-- top panel -->
	<!-- panel labels centred over the plot area -->
	<text x={(L + width - R) / 2} y="12" text-anchor="middle" style={SUBTITLE_STYLE}>Exports, billions of dollars per month</text>
	{#each [0, 10, 20, 30, 40, 50, 60, 70] as v}
		<line x1={L} x2={width - R} y1={y1(v)} y2={y1(v)} stroke={C.g10} />
		<text x={L - 6} y={y1(v)} dy="0.35em" text-anchor="end" fill={INK2}>{v ? `$${v}B` : '0'}</text>
	{/each}
	<path d={path('un')} fill="none" stroke={UNADJUSTED} stroke-width="1.2" />
	<path d={path('sa')} fill="none" stroke={C.darkblue} stroke-width="2.4" stroke-linejoin="round" />
	{#if narrow}
		<!-- line key (the end-of-line labels don't fit on narrow screens) -->
		<g transform="translate({(L + width - R) / 2 - 133}, 0)">
			<line x1="0" x2="18" y1="32" y2="32" stroke={C.darkblue} stroke-width="2.4" />
			<text x="24" y="32" dy="0.35em" fill={C.darkblue} style="font-family: OpenSansBold">Seasonally adjusted</text>
			<line x1="168" x2="186" y1="32" y2="32" stroke={UNADJUSTED} stroke-width="1.6" />
			<text x="192" y="32" dy="0.35em" fill={UNADJUSTED} style="font-family: OpenSansBold">Unadjusted</text>
		</g>
	{:else}
		<text x={x(last.t) + 6} y={y1(last.sa) + 12} fill={C.darkblue} style="font-family: OpenSansBold">
			<tspan x={x(last.t) + 6} dy="0">Seasonally</tspan>
			<tspan x={x(last.t) + 6} dy="15">adjusted</tspan>
		</text>
		<text x={x(last.t) + 6} y={Math.min(y1(last.un), y1(last.sa) - 15)} dy="0.35em" fill={UNADJUSTED} style="font-family: OpenSansBold">Unadjusted</text>
	{/if}

	<!-- bottom panel -->
	<text x={(L + width - R) / 2} y={TOP + H1 + GAP - 14} text-anchor="middle" style={SUBTITLE_STYLE}>Year-over-year change</text>
	{#each [-80, -40, 0, 40, 80] as v}
		<line x1={L} x2={width - R} y1={y2(v)} y2={y2(v)} stroke={v === 0 ? C.g45 : C.g10} />
		<text x={L - 6} y={y2(v)} dy="0.35em" text-anchor="end" fill={INK2}>{fmtPct(v)}</text>
	{/each}
	{#each pts as p}
		<rect x={x(p.t) - barW / 2} y={Math.min(y2(p.yoy), y2(0))} width={barW} height={Math.abs(y2(p.yoy) - y2(0))} fill={p.yoy >= 0 ? C.medblue : C.red} />
	{/each}
	<text x={x(covid.t) + 8} y={y2(covid.yoy)} dy="0.35em" fill="#000000">COVID-19: −{Math.abs(Math.round(covid.yoy))}%</text>

	<!-- tariff marker -->
	<line x1={x(TARIFF)} x2={x(TARIFF)} y1={TOP} y2={TOP + H1 + GAP + H2} stroke={TARIFF_COLOUR} stroke-dasharray="3 2" />
	<text x={x(TARIFF) - 6} y={TOP + 10} text-anchor="end" fill={TARIFF_COLOUR} style="font-family: OpenSansBold">Initial U.S. tariffs, March 2025</text>

	<!-- x axis -->
	{#each years as yr}
		<text x={x(yr)} y={height - 6} text-anchor="middle" fill={INK2}>{yr}</text>
	{/each}
</svg>
