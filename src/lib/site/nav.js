// Site structure: the single source for the header menus, footer, homepage cards and
// section colours. Paths are relative to the site pages' root; prefix with `root` from
// $lib/site/paths.js when rendering links.

import { UPDATED as MAP_UPDATED } from '$lib/components/maps/exposure/config.js';
import { UPDATED as RANKINGS_UPDATED } from '$lib/components/charts/rankings/config.js';
import { PUBLISHED as SCENARIOS_PUBLISHED } from '$lib/components/maps/scenarios/config.js';

export const SITE_NAME = 'Mapping Tariffs';

/** 'September 2026' -> 'Sep 2026' (menu dates use short months) */
const shortMonth = (monthYear) => monthYear.replace(/^([A-Za-z]{3})[a-z]*/, '$1');

/** Colour for pages outside any section with its own colour (e.g. the homepage). */
export const DEFAULT_COLOUR = 'var(--brandLightBlue)';

/**
 * @typedef {{ label: string, href: string, date?: string, note?: string }} NavLink
 * @typedef {{ heading?: string, links: NavLink[] }} NavGroup
 * @typedef {{ label: string, href: string, colour: string, match?: string, groups?: NavGroup[] }} NavSection
 *   colour: the section's colour (homepage card border, square beside page titles,
 *     table-of-contents marker), as a CSS value.
 *   match: path prefix for "is this page in the section", when it differs from href.
 */

/** @type {NavSection[]} */
export const NAV = [
	{ label: 'About', href: '/about', colour: 'var(--brandYellow)' },
	{
		label: 'Direct exposure',
		href: '/exposure',
		colour: 'var(--brandPurple)',
		groups: [
			{
				links: [
					{ label: 'Overview', href: '/exposure' },
					{ label: 'Interactive map', href: '/exposure/map', date: `Updated ${shortMonth(MAP_UPDATED)}` },
					{ label: 'Rankings', href: '/exposure/rankings', date: `Updated ${shortMonth(RANKINGS_UPDATED)}` }
				]
			},
			{
				heading: 'Posts',
				links: [
					// publication order, oldest first
					{ label: 'Lumber tariffs', href: '/exposure/lumber', date: 'Feb 2026' },
					{ label: 'Truck tariffs', href: '/exposure/trucks', date: 'Feb 2026' },
					{ label: 'Reflecting on new Section 338 tariffs', href: '/exposure/section-338', date: 'Sep 2026' }
				]
			}
		]
	},
	{
		label: 'Scenarios',
		href: '/scenarios',
		colour: 'var(--brandPink)',
		groups: [
			{
				links: [
					{ label: 'Overview', href: '/scenarios' },
					{ label: 'Interactive map', href: '/scenarios/map', date: shortMonth(SCENARIOS_PUBLISHED) },
					{ label: 'Rankings', href: '/scenarios/rankings', date: shortMonth(SCENARIOS_PUBLISHED) },
					{ label: 'Report', href: '/scenarios/report', date: shortMonth(SCENARIOS_PUBLISHED) }
				]
			}
		]
	},
	{ label: 'Current tariffs', href: '/current-tariffs', colour: 'var(--brandLightBlue)' },
	// only one travel post so far, so link straight to it (no dropdown)
	{ label: 'Canada–U.S. travel', href: '/travel/canada-us-visits', match: '/travel', colour: 'var(--brandRed)' }
];

/** True when `pathname` is inside `href` (or equal to it). */
export function isActive(pathname, href) {
	const p = pathname.replace(/\/$/, '') || '/';
	return p === href || (href !== '/' && p.startsWith(href + '/'));
}

/** The nav section a site path (e.g. '/exposure/lumber') belongs to, or undefined. */
export function sectionFor(pathname) {
	return NAV.find((s) => isActive(pathname, s.match ?? s.href));
}

/** The section colour for a site path, or DEFAULT_COLOUR. */
export function colourFor(pathname) {
	return sectionFor(pathname)?.colour ?? DEFAULT_COLOUR;
}
