// Shared look for the report charts (matches the site's charts: Open Sans labels,
// Trade Gothic titles, brand colours). Nothing below 12px so text stays >= 11px.

export const C = {
	darkblue: '#1E3765',
	medblue: '#007FA3',
	lightblue: '#6FC7EA',
	red: '#DC4633', // brandRed
	g10: '#E6E6E6',
	g20: '#CCCCCC',
	g30: '#B3B3B3',
	g45: '#8C8C8C',
	g70: '#4D4D4D',
	g90: '#1A1A1A'
};

/** direct -> indirect -> induced: ordinal blue ramp (from the report's chart script) */
export const EFFECTS = [
	{ key: 'direct', label: 'Direct', colour: C.darkblue, text: 'white' },
	{ key: 'indirect', label: 'Indirect', colour: C.medblue, text: 'white' },
	{ key: 'induced', label: 'Induced', colour: '#59B9DC', text: C.g90 }
];

export const HIGHLIGHT = C.darkblue;
/** job-loss bars (Figures 2, 4, 7, 10, 12): total jobs lost purple, per 1,000 residents pink; no regions emphasised */
export const RANKED = { total: '#6D247A', per1000: '#AB1368' }; // brandPurple / brandPink
export const CONTEXT = C.medblue; // non-highlighted bars (brandMedBlue)
export const INK = C.g90;
export const INK2 = C.g70;

export const FONT = { label: 12, value: 12 };

/** Width of the direct / indirect / induced legend (see EffectLegend.svelte). */
export const effectLegendWidth = () => EFFECTS.reduce((w, e, i) => w + (i ? 14 : 0) + 18 + String(e.label).length * FONT.label * 0.56, 0);

/** Chart subtitles (panel headings): black Open Sans Bold Italic. */
export const SUBTITLE_STYLE = 'font-family: OpenSansBoldItalic; fill: #000000';

/** Rough text width for Open Sans at `size` px (good enough for layout). */
export const textWidth = (s, size = FONT.label, bold = false) => String(s).length * size * (bold ? 0.6 : 0.56);

/** Word-wrap a label into at most 2 lines that fit `maxW` px (keeps text >= 12px instead of shrinking). */
export function wrapLabel(text, maxW, size = FONT.label, bold = false) {
	if (textWidth(text, size, bold) <= maxW) return [text];
	const words = String(text).split(' ');
	let best = [text];
	for (let i = 1; i < words.length; i++) {
		const a = words.slice(0, i).join(' ');
		const b = words.slice(i).join(' ');
		const w = Math.max(textWidth(a, size, bold), textWidth(b, size, bold));
		if (w <= maxW) return [a, b];
		if (best.length === 1 || w < Math.max(...best.map((l) => textWidth(l, size, bold)))) best = [a, b];
	}
	return best;
}
