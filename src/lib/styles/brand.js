// Brand colours: the single source. Use BRAND in JavaScript (map styles, chart SVG
// attributes, d3), where CSS variables don't work. CSS uses the matching variables
// (--brandDarkBlue, --brandGray70, …), which routes/+layout.svelte writes onto :root
// from this object via BRAND_CSS_VARS. Change a colour here and both follow.

export const BRAND = {
	darkBlue: '#1E3765',
	medBlue: '#007FA3',
	lightBlue: '#6FC7EA',
	purple: '#6D247A',
	pink: '#AB1368',
	darkGreen: '#0D534D',
	medGreen: '#00A189',
	lightGreen: '#8DBF2E',
	red: '#DC4633',
	yellow: '#F1C500',
	orange: '#EBA00F',
	black: '#000000',
	white: '#ffffff',
	gray: '#D0D1C9',
	gray10: '#E6E6E6',
	gray15: '#D9D9D9',
	gray50: '#858585',
	gray60: '#727272',
	gray70: '#4d4d4d',
	gray80: '#333333',
	gray90: '#191919'
};

/** ':root { --brandDarkBlue: #1E3765; … }' for the page <head>. */
export const BRAND_CSS_VARS = `:root {${Object.entries(BRAND)
	.map(([name, value]) => `--brand${name[0].toUpperCase()}${name.slice(1)}: ${value};`)
	.join('')}}`;
