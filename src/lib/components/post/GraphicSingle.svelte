<script>
	/**
	 * Responsive inline SVG graphic: loads the 1080/720/360 variant that fits the
	 * window, lazily (once scrolled near), and swaps on resize.
	 */
	import { onMount } from 'svelte';

	let { svg1080 = '', svg720 = '', svg360 = '', caption = '', source = '' } = $props();

	let container;
	let svgMarkup = $state('');
	let svgWidth = $state(0);
	let containerWidth = $state(0);
	const paddingLeft = $derived(containerWidth < svgWidth ? '20px' : '0px');

	const cache = new Map();

	function pick(width) {
		if (width >= 1080 && svg1080) return [svg1080, 1080];
		if (width >= 720 && svg720) return [svg720, 720];
		return [svg360, 360];
	}

	async function load(width) {
		const [path, w] = pick(width);
		if (w === svgWidth && svgMarkup) return;
		if (!cache.has(path)) {
			cache.set(path, fetch(path).then((r) => (r.ok ? r.text() : '')).catch(() => ''));
		}
		const markup = await cache.get(path);
		svgWidth = w;
		svgMarkup = markup;
	}

	onMount(() => {
		const onResize = () => load(window.innerWidth);
		const observer = new IntersectionObserver(
			([entry]) => {
				if (!entry.isIntersecting) return;
				observer.disconnect();
				onResize();
				window.addEventListener('resize', onResize);
			},
			{ rootMargin: '400px' }
		);
		observer.observe(container);
		return () => {
			observer.disconnect();
			window.removeEventListener('resize', onResize);
		};
	});
</script>

<div class="svg-container-wrapper" bind:this={container} bind:offsetWidth={containerWidth} style="--svg-width: {svgWidth}px;">
	{#if svgMarkup}
		<div class="svg-container">{@html svgMarkup}</div>
		{#if caption || source}
			<p class="caption-text" style="padding-left: {paddingLeft}">
				{@html caption} <span class="caption-source">{@html source}</span>
			</p>
		{/if}
	{/if}
</div>

<style>
	.svg-container-wrapper {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin: 0 auto;
		min-height: 1px;
	}

	.svg-container {
		width: var(--svg-width);
		max-width: 100%;
	}

	.svg-container :global(svg) {
		max-width: 100%;
		height: auto;
	}

	p {
		box-sizing: border-box;
		width: var(--svg-width);
		max-width: 100%;
		margin: -10px 0 0;
		text-align: left;
	}

	.caption-text {
		font-family: OpenSansBold;
		color: var(--brandGray70);
		font-size: 12px;
		line-height: 18px;
	}

	.caption-text :global(a) {
		color: var(--brandGray80);
	}

	.caption-source,
	.caption-source :global(a) {
		font-family: OpenSans;
		color: var(--brandGray60);
	}

	@media screen and (max-width: 600px) {
		p {
			padding-left: 15px;
			padding-right: 15px;
		}
	}
</style>
