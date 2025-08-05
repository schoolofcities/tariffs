<script>
	export let svgPaths = []; // Array of paths to SVG files

	let layoutClass = '';
	let svgs = []; // This will hold the loaded SVG strings
	let container;

	const updateLayout = () => {
		const width = window.innerWidth;

		if (svgPaths.length === 2) {
			layoutClass = width < 740 ? 'stack-2' : 'row-2';
		} else if (svgPaths.length === 3) {
			if (width < 360 * 3) {
				layoutClass = width < 740 ? 'stack-3' : 'two-plus-one';
			} else {
				layoutClass = 'row-3';
			}
		} else if (svgPaths.length === 4) {
			layoutClass = width < 740 ? 'stack-4' : 'grid-2x2';
		}
	};

	async function loadSVG(path) {
		try {
			const response = await fetch(path);
			if (!response.ok) throw new Error(`Failed to load SVG from ${path}`);
			return await response.text(); // Return the SVG content as a string
		} catch (e) {
			console.error(`Error loading SVG from ${path}:`, e);
			return '';
		}
	}

	async function loadAllSVGs() {
		const loadedSVGs = [];
		for (const path of svgPaths) {
			const svgContent = await loadSVG(path);
			loadedSVGs.push(svgContent);
		}
		svgs = loadedSVGs;
	}

	import { onMount, onDestroy } from 'svelte';

	onMount(() => {
		const observer = new IntersectionObserver(async ([entry]) => {
			if (entry.isIntersecting) {
				await loadAllSVGs();
				updateLayout();
				
				// Setup resize listener after loading
				window.addEventListener('resize', updateLayout);
				
				observer.disconnect();
			}
		}, {
			rootMargin: '200px' // Start loading when within 200px of viewport
		});

		if (container) observer.observe(container);

		onDestroy(() => {
			window.removeEventListener('resize', updateLayout);
		});
	});
</script>

<style>
	.svg-grid {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 10px;
	}

	.svg-box {
		width: 360px;
		height: auto;
	}

	/* Layout classes */
	.row-2, .row-3 {
		flex-direction: row;
	}

	.stack-2, .stack-3, .stack-4 {
		flex-direction: column;
		align-items: center;
	}

	.two-plus-one {
		display: grid;
		grid-template-columns: repeat(2, 360px);
		grid-template-rows: auto auto;
		justify-content: center;
	}

	.two-plus-one .svg-box:nth-child(3) {
		grid-column: 1 / span 2;
		justify-self: center;
	}

	.grid-2x2 {
		display: grid;
		grid-template-columns: repeat(2, 360px);
		grid-template-rows: repeat(2, auto);
		justify-content: center;
	}
</style>

<div class="svg-grid {layoutClass}" bind:this={container}>
	{#each svgs as svg}
		<div class="svg-box">
			{@html svg}
		</div>
	{/each}
</div>