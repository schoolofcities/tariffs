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
            base
        }
	}
};

export default config;