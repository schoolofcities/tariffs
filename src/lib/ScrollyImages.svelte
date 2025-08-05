<script>

	import "../assets/global-styles.css"	
	import { fade } from "svelte/transition";
	import { onMount, onDestroy } from "svelte";

	export let imageAlign = "center";
	export let imageWidth = "100%";
	export let imageHeight = "100%";
	export let textSectionAlign = "right";
	export let textSectionMaxWidth = "500px";
	export let fadeDuration = 250;
	export let sections = [
		{
		image: "/images/1.jpg",
		text: "<h2>Header</h2> <p>body text </p>",
		},
		{
		image: "/images/2.jpg",
		text: "<h2>Header</h2> <p>body text </p>",
		},
		{
		image: "/images/3.jpg",
		text: "<h2>Header</h2> <p>body text </p>",
		},
	];

	// $: topImageMargin = 0;

	// if ("%" or "dvh" or "vh" in imageHeight)

	// 	topImageMargin = (100 - imageHeight) / 2;

	// else ("px" in imageHeight)

		// imgDivHeight = min(0 ,(window.height - imageHeight) / 2)

	// $: topImageMargin = (100 - imageHeight) / 2;

	$: console.log(imageHeight,windowHeight,topImageMargin);

	let windowHeight = 0;
	let imgDivHeight = 0;
	let topImageMargin = "0px";

	onMount(() => {
		windowHeight = window.innerHeight;

		const resizeHandler = () => {
			windowHeight = window.innerHeight;
		};
		window.addEventListener('resize', resizeHandler);

		return () => window.removeEventListener('resize', resizeHandler);
	});

	$: {
		if (typeof imageHeight === 'string') {
			if (imageHeight.includes('%') || imageHeight.includes('vh') || imageHeight.includes('dvh')) {
				const num = parseFloat(imageHeight);
				topImageMargin = `${(100 - num) / 2}dvh`;
			} else if (imageHeight.includes('px')) {
				const px = parseFloat(imageHeight);
				imgDivHeight = Math.max(0, (windowHeight - px) / 2);
				topImageMargin = `${imgDivHeight}px`;
			}
		}
	}

	
	let container;
	let currentIndex = 0;
	let textSections = [];

	const handleScroll = () => {
		let newIndex = currentIndex;
		textSections.forEach((section, index) => {
		const rect = section.getBoundingClientRect();
		if (
			rect.top <= window.innerHeight * 0.5 &&
			rect.bottom > window.innerHeight * 0.5
		) {
			newIndex = index;
		}
		});

		currentIndex = newIndex;
	};

	onMount(() => {
		window.addEventListener("scroll", handleScroll);
		handleScroll();
		return () => {
			window.removeEventListener("scroll", handleScroll);
		};
	});

</script>



<div class="scrolly-wrapper" bind:this={container}>

	<div class="sticky-image">

		{#each sections as section, i}

			{#if currentIndex === i}
				<div class="image-container">
					<img
						class={imageAlign}
						src={section.image}
						alt={section.heading}
						transition:fade={{ duration: fadeDuration }}
						loading="lazy"
						style="max-height: {imageHeight}; max-width: {imageWidth}; top: {topImageMargin};"	
					/>
				</div>
				
			{/if}

		{/each}

	</div>

	{#each sections as section, i}

		<div
			class="text-section {textSectionAlign}"
			bind:this={textSections[i]}
			style="max-width: {textSectionMaxWidth};"
		>

			<div class="text-wrapper {section.text.trim() ? '' : 'transparent'}">
				{@html section.text}
			</div>
		
		</div>

	{/each}

</div>



<style>
	
	.scrolly-wrapper {
		/* border-top: solid 1px var(--brandGray);
		border-bottom: solid 1px var(--brandGray); */
		display: flex;
		flex-direction: column;
		position: relative;
		background-color: white;
		margin-top: 40px;
		margin-bottom: 40px;
	}

	.sticky-image {
		position: sticky;
		top: 0vh;
		height: 100dvh;
		width: 100%;
		z-index: 0;
	}

	.sticky-image img {
		position: absolute;
		object-fit: cover;
		height: 100%;
		width: 100%;
		border: 1px solid #ccc;
	}

	img.right {
		right: 0;
	}

	img.left {
		left: 0;
	}

	img.center {
		left: 50%;
		transform: translateX(-50%);
	}

	.text-wrapper {
		padding-left: 20px;
		padding-right: 20px;
		position: relative;
		z-index: 1;
		background: rgba(255, 255, 255, 0.9);
		border: 1px solid #ccc;
	}

	.text-wrapper.transparent {
		background: transparent !important;
		border: none !important;
		opacity: 0;
		pointer-events: none;
		box-shadow: none;
	}

	.text-section.center {
		margin: 0 auto;
	}
	.text-section.right {
		margin: 0 0 0 auto;
	}
	.text-section.left {
		margin: 0 0 0 0;
	}

	.text-section {
		padding: 30vh 2rem;
		position: relative;
		z-index: 1;
		text-align: left;
		height: 90vh;
	}

	@media (max-width: 600px) {
		.text-section {
			padding: 30vh 1rem;
		}
	}

</style>
