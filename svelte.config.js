import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		// Output goes to build/ (gitignored). Deploy via GitHub Actions rather than
		// committing build output, so diffs stay clean.
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			strict: true
		}),
		alias: {
			$assets: 'src/assets'
		},
		paths: {
			// '' locally and on mappingtariffs.org. The GitHub Actions deploy sets
			// BASE_PATH=/tariffs-v2 for testing at schoolofcities.github.io/tariffs-v2/.
			base: process.env.BASE_PATH ?? ''
		},
		prerender: {
			handleHttpError: 'warn'
		}
	}
};

export default config;
