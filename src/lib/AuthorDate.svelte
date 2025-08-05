<script>

	import "../assets/global-styles.css";

	export let authors = "";
	export let graphics = ""
	export let research = "";
	export let writing = "";
	export let date = "";

</script>


<div class="author-date">

	<p>
		{#if authors}
			By {@html authors}
		{/if}
		{#if research}
			<br>
			Research: {@html research}
		{/if}
		{#if graphics}
			<br>
			Graphics: {@html graphics}
		{/if}
		{#if writing}
			<br>
			Writing: {@html writing}
		{/if}

		<br>
		<span id="date">~ {date}</span>
	</p>

</div>


<style>

	.author-date {
		margin-top: 0px;
		padding-bottom: 0px;
		border-bottom: solid 1px var(--brandGray);
		margin-bottom: 25px;
	}

	.author-date p {
		font-size: 16px;
		line-height: 24px;
		color: var(--brandBlack);
	}

	.author-date b {
		color: var(--brandGray80);
		font-family: SourceSerifBold;
		font-weight: normal;
	}

	.author-date strong {
		color: var(--brandGray80);
		font-family: SourceSerifBold;
		font-weight: normal;
	}

	.author-date #date {
		font-family: SourceSerifBold;
		font-size: 13px;
		font-weight: normal;
	}

</style>