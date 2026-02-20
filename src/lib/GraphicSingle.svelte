<script>
	export let svg1080 = '';
	export let svg720 = '';
	export let svg360 = '';
	export let caption = '';
	export let source = '';

	let inputSVG = '';
	let svgWidth = 0;
	let container;
	let containerWidth = 0;
	let resizeHandler;

	// adjust left-padding based on if image fits the full screen or not
	$: paddingLeft = containerWidth < svgWidth ? '20px' : '0px';

	// Function to select which SVG to load based on screen width
	function pickSVGPath(width) {
		if (width >= 1080 && svg1080) return [svg1080, 1080];
		if (width >= 720 && svg720) return [svg720, 720];
		return [svg360, 360];
	}
  
	// Fetch SVG content as text
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
  
	async function handleVisibility(width) {
		const [path, widthValue] = pickSVGPath(width);
		svgWidth = widthValue;
	
		inputSVG = await loadSVG(path);
	}
  
	import { onMount, onDestroy } from 'svelte';
  
	onMount(() => {
		const observer = new IntersectionObserver(async ([entry]) => {
		if (entry.isIntersecting) {
			await handleVisibility(window.innerWidth);

			resizeHandler = () => handleVisibility(window.innerWidth);
			window.addEventListener('resize', resizeHandler);

			observer.disconnect();
		}
		});

		if (container) observer.observe(container);
  
		onDestroy(() => {
			window.removeEventListener('resize', resizeHandler);
		});
	});
</script>
  

  
<div class="svg-container-wrapper" bind:this={container} bind:offsetWidth={containerWidth} style="--svg-width: {svgWidth}px;">
	{#if inputSVG}
		<div class="svg-container">
			{@html inputSVG}
		</div>
		<p 
			class="caption-text" 
			style="padding-left: {paddingLeft}"
		>{@html caption} <span class="caption-source">{@html source}</span></p>
	{/if}
</div>

<style>

	.svg-container-wrapper {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		margin: 0 auto;
		padding-left: 0px;
		padding-right: 0px;
	}
	
	.svg-container {
		width: var(--svg-width);
		height: auto;
	}

	p {
		text-align: left;
		padding-left: 0px;
		margin: 0px;
		box-sizing: border-box;
		width: var(--svg-width);
	}

	.caption-text {
		font-family: OpenSansBold;
		font-weight: normal;
		color: var(--brandGray70);
		font-size: 12px;
		line-height: 18px;
		margin-top: -10px;
		margin-bottom: 0px;
		padding-top: 0px;
	}

	.caption-text a {
		font-family: OpenSansBold;
		font-weight: normal;
		color: var(--brandGray80);
	}

	.caption-text a:hover {
		color: var(--brandMedGreen);
	}

	.caption-source {
		font-family: OpenSans;
		font-weight: normal;
		color: var(--brandGray60);
	}

	.caption-source a {
		font-family: OpenSans;
		font-weight: normal;
		color: var(--brandGray60);
	}

	.caption-source a:hover {
		color: var(--brandMedGreen);
	}

	@media screen and (max-width: 600px) {
		p {
			padding-left: 15px;
			padding-right: 15px;
		}
	}
</style>