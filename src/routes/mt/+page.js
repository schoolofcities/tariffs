// Build the homepage as mt/index.html so /mt/ works on GitHub Pages (static hosts don't
// strip trailing slashes the way the dev server does). Only this page; others stay /mt/about etc.
export const trailingSlash = 'always';
