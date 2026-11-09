// Old URLs and where they now go. Keys are old paths (no leading slash; '' is the site
// root); values are new page paths within the site (under /mt/, which Redirect adds).
// Served by routes/[...old]: each key is prerendered as a small redirect page.
export const REDIRECTS = {
	// the site now lives under /mt/
	'': '/',
	// pages of the original site
	map: '/exposure/map',
	'cma-ranking-charts': '/exposure/rankings',
	'potential-local-impacts': '/exposure',
	lumber: '/exposure/lumber',
	trucks: '/exposure/trucks',
	'section-338': '/exposure/section-338',
	'canada-us-visits': '/travel/canada-us-visits',
	'current-tariffs': '/current-tariffs',
	// earlier paths within /mt/
	'mt/exposure/backgrounder': '/exposure',
	'mt/travel': '/travel/canada-us-visits'
};
