import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';


const dev = "production" === "development";

const base = process.env.BASE_PATH ?? '';

const config = {

	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter({
		    pages: "docs",
		    assets: "docs"
		}),
		paths: {
			base,
			relative: true
		},
		prerender: {
            // Fork-only: base is hardcoded to /tariffs, so root-absolute links
            // and asset paths elsewhere in the site fail the crawler's base
            // check. Downgrade to a warning -- only /map needs to work here.
            handleHttpError: ({ path, referrer, message }) => {
                console.warn(`[prerender] ignoring: ${message}`);
                return;
            }
        }
	}
};

export default config;