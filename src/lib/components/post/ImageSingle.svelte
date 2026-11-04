<script>
	/** Full-width image with optional caption/source (HTML allowed). */
	let { imageURL = '', caption = '', source = '', altText = '', maxWidth = '680px', link = 'Yes' } = $props();

	let containerWidth = $state(0);
	// Inset the caption when the image is narrower than its max width (i.e. on small screens).
	const paddingLeft = $derived(containerWidth < parseInt(maxWidth) ? '20px' : '0px');
</script>

<figure class="img-container" style="max-width: {maxWidth}" bind:offsetWidth={containerWidth}>
	{#if link === 'Yes'}
		<a href={imageURL} target="_blank" rel="noopener"><img src={imageURL} alt={altText} loading="lazy" /></a>
	{:else}
		<img src={imageURL} alt={altText} loading="lazy" />
	{/if}
	{#if caption || source}
		<figcaption class="caption-text" style="padding-left: {paddingLeft}">
			{@html caption} <span class="caption-source">{@html source}</span>
		</figcaption>
	{/if}
</figure>

<style>
	.img-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		margin: 0 auto 30px;
		padding-top: 10px;
	}

	img {
		width: 100%;
		height: auto;
		min-height: 100px;
		display: block;
		object-fit: cover;
	}

	a {
		width: 100%;
	}

	.caption-text {
		box-sizing: border-box;
		width: 100%;
		margin: 2px 0 0;
		font-family: OpenSansBold;
		color: var(--brandGray70);
		font-size: 12px;
		line-height: 18px;
		text-align: left;
	}

	.caption-text :global(a) {
		font-family: OpenSansBold;
		color: var(--brandGray80);
	}

	.caption-text :global(a:hover) {
		color: var(--brandMedGreen);
	}

	.caption-source,
	.caption-source :global(a) {
		font-family: OpenSans;
		color: var(--brandGray60);
	}

	@media screen and (max-width: 600px) {
		.caption-text {
			padding-left: 15px;
			padding-right: 15px;
		}
	}
</style>
