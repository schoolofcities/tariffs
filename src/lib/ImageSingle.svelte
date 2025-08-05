<script>
	import "../assets/global-styles.css"

	export let imageURL = '';
	export let caption = '';
	export let source = '';
	export let altText = '';
	export let maxWidth = '';
	export let link = 'Yes'; // Yes or No open link in new tab

	// adjust left-padding based on if image fits the full screen or not
	let containerWidth = 0;
	$: numericMaxWidth = parseInt(maxWidth); // remove "px"
	$: paddingLeft = containerWidth < numericMaxWidth ? '20px' : '1px';

</script>

<div 
	class="img-container" 
	style="max-width: {maxWidth}"
	bind:offsetWidth={containerWidth}
	>
	{#if link === 'Yes'}
		<a href={imageURL} target="_blank">
			<img src={imageURL} alt={altText} loading="lazy" />
		</a>
	{:else}
		<img src={imageURL} alt={altText} loading="lazy" />
	{/if}
	<p 
		class="img-caption" 
		style="padding-left: {paddingLeft}"
	>{@html caption} <span id="image-source">{@html source}</span></p>
</div>

<style>

	.img-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		margin: 0 auto;
		padding-top: 10px;
		padding-bottom: 0px;
		margin-bottom: 30px;
	}

	img {
		width: 100%;
		height: auto;
		max-height: 80%;
		min-height: 200px;
		display: block;
		object-fit: cover;
		object-position: center;
	}

	a {
		display: block;
		width: 100%;
	}

	a:hover {
		opacity: 0.95;
	}

	a img {
		width: 100%;
		height: auto;
		display: block;
	}

	p {
		text-align: left;
		padding-left: 1px;
		margin: 0px;
		box-sizing: border-box;
		width: 100%;
	}

	.img-caption {
		font-family: OpenSansBold;
		font-weight: normal;
		color: var(--brandGray70);
		font-size: 12px;
		line-height: 18px;
		margin-top: 2px;
		margin-bottom: 0px;
		padding-top: 0px;
	}

	#image-source {
		font-family: OpenSans;
		font-weight: normal;
		color: var(--brandGray50);
	}

	@media screen and (max-width: 600px) {
		p {
			padding-left: 15px;
		}
	}

</style>
