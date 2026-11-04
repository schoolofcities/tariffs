<script>
	let { title = '', subtitle = '' } = $props();
</script>

<div class="title-text-container">
	<h1>{title}</h1>
	{#if subtitle}
		<p class="subtitle">{subtitle}</p>
	{/if}
</div>

<style>
	.title-text-container {
		max-width: 680px;
		margin: 0 auto 45px;
		padding: 5px 20px 0;
		position: relative;
	}

	h1 {
		font-family: TradeGothicBold;
		font-weight: normal;
		font-size: var(--title-size);
		line-height: 1.1;
		color: var(--brandDarkBlue);
		margin: 30px 0 10px;
		padding: 0;
	}

	.subtitle {
		font-family: SourceSerifItalic;
		font-size: var(--subtitle-size);
		line-height: 1.35;
		margin-top: 0;
		color: var(--brandGray90);
	}

</style>
