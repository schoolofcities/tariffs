// Where the site's pages live. Every page sits under /mt/ (e.g. /mt/about); the old
// root URLs (/map, /lumber, …) are redirects to their new pages. Static files
// (images, data, tiles) stay at the root, under `base`.
import { base } from '$app/paths';

export const SITE_ROOT = '/mt';

/** URL prefix for pages: `${root}/exposure`, `${root}/` for the homepage (/mt/). */
export const root = `${base}${SITE_ROOT}`;

/**
 * A URL pathname as a page path within the site, matching the nav entries:
 * '/mt/exposure/map' -> '/exposure/map', '/mt/' -> '/'. Paths outside /mt/ (the old-URL
 * redirect pages) come back unchanged. Works in prerendered pages too, where `base` is
 * relative ('..') rather than a path prefix.
 */
export function pagePath(pathname) {
	let p = base.startsWith('/') && pathname.startsWith(base) ? pathname.slice(base.length) : pathname;
	if (p === SITE_ROOT || p.startsWith(`${SITE_ROOT}/`)) p = p.slice(SITE_ROOT.length) || '/';
	return p;
}
