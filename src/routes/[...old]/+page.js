// Redirect pages for old URLs, from the list in $lib/site/redirects.js. Every listed
// path is prerendered; anything else is a 404.
import { error } from '@sveltejs/kit';
import { REDIRECTS } from '$lib/site/redirects.js';

export const entries = () => Object.keys(REDIRECTS).map((old) => ({ old }));

export function load({ params }) {
	const to = REDIRECTS[params.old];
	if (to === undefined) error(404, 'Not found');
	return { to };
}
