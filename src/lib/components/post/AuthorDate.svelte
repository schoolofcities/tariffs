<script>
	/** Byline. Author strings may contain links, so they are rendered as HTML. */
	let { authors = '', research = '', graphics = '', writing = '', date = '' } = $props();
</script>

<div class="author-date">
	<p>
		{#if authors}By {@html authors}{/if}
		{#if research}<br />Research: {@html research}{/if}
		{#if graphics}<br />Graphics: {@html graphics}{/if}
		{#if writing}<br />Writing: {@html writing}{/if}
		{#if date}<br /><span class="date">~ {date}</span>{/if}
	</p>
</div>

<style>
	.author-date {
		margin: 0 0 25px;
		border-bottom: 1px solid var(--brandGray);
	}

	.author-date p {
		font-size: 16px;
		line-height: 24px;
		color: var(--brandBlack);
	}

	.date {
		font-family: SourceSerifBold;
		font-size: 13px;
	}

	@media (max-width: 600px) {
		.author-date p {
			font-size: 13.5px;
			line-height: 20px;
		}
		.date {
			font-size: 11px;
		}
	}
</style>
