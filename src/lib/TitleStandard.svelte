<script>

	import "../assets/global-styles.css";

	export let title = '';
	export let subtitle = '';
	
</script>


<div class="title-text-container">
	
	<h1>{title}</h1>
	
	{#if subtitle}
		<h2>{subtitle}</h2>
	{/if}
	
</div>


<style>

	.title-text-container {
		background-color: none;
		max-width: 680px;
		margin: 0 auto;
		position: relative;
		padding-left: 20px;
		padding-right: 20px;
		padding-top: 15px;
		margin-bottom: 45px;

	}

	.title-text-container h1 {
		font-family: TradeGothicBold;
		font-weight: normal;
		font-size: 48px;
		color: var(--brandGray90);
		text-decoration: none;
		margin-bottom: 10px;
		padding: 0px;
	}

	.title-text-container h2 {
		text-align: left;
		font-family: SourceSerifItalic;
		font-weight: normal;
		font-size: 24px;
		margin-top: 0px;
		color: var(--brandGray90);
	}

</style>