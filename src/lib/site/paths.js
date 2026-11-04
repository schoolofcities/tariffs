// Where the site's pages live. Every page sits under /mt/ (e.g. /mt/about); the old
// root URLs (/map, /lumber, …) are redirects to their new pages. Static files
// (images, data, tiles) stay at the root, under `base`.
import { base } from '$app/paths';

export const SITE_ROOT = '/mt';

/** URL prefix for pages: `${root}/exposure`, `${root}/` for the homepage (/mt/). */
export const root = `${base}${SITE_ROOT}`;
