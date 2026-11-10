<!--
	Stack of link cards for a section's interactive tools.
	tools: [{ href, title, text, icon (component), updated?, published?, url? }]
	href is a site page path (under /mt/); url, if given, is used as-is instead (e.g. a PDF)
	and opens in a new tab.
-->
<script>
	import { root } from '$lib/site/paths.js';

	let { tools } = $props();
</script>

<div class="cards">
	{#each tools as tool (tool.url ?? tool.href)}
		<a class="card" href={tool.url ?? `${root}${tool.href}`} target={tool.url ? '_blank' : undefined} rel={tool.url ? 'noopener' : undefined}>
			{#if tool.icon}<span class="icon"><tool.icon size={52} /></span>{/if}
			<span class="card-body">
				<span class="card-title">{tool.title} →</span>
				{#if tool.updated}<span class="updated">Updated {tool.updated}</span>
				{:else if tool.published}<span class="updated">Published {tool.published}</span>{/if}
				<span class="card-text">{tool.text}</span>
			</span>
		</a>
	{/each}
</div>

<style>
	.cards {
		display: grid;
		grid-template-columns: 1fr;
		gap: 16px;
	}

	.card {
		display: flex;
		align-items: flex-start;
		gap: 16px;
		padding: 16px 18px;
		border: 1px solid var(--brandGray);
		color: inherit;
		text-decoration: none;
		transition: border-color 0.15s ease;
	}

	.card:hover {
		border-color: var(--brandDarkBlue);
	}

	.icon {
		flex-shrink: 0;
		display: flex;
		justify-content: center;
		width: 56px;
		padding-top: 4px;
		color: var(--brandDarkBlue);
	}

	.card-body {
		display: flex;
		flex-direction: column;
		gap: 8px;
		min-width: 0;
	}

	.card-title {
		font-family: TradeGothicBold, sans-serif;
		font-size: 20px;
		color: var(--brandDarkBlue);
	}

	.updated {
		margin-top: -4px;
		padding: 2px 0 6px;
		font-family: OpenSansItalic, sans-serif;
		font-size: 12px;
		line-height: 16px;
		color: var(--brandBlack);
	}

	.card-text {
		font-family: SourceSerif, serif;
		font-size: 16px;
		line-height: 22px;
		color: var(--brandGray90);
	}

	@media (max-width: 600px) {
		.card-title {
			font-size: 17px;
		}
		.card-text {
			font-size: 13.5px;
			line-height: 19px;
		}
	}
</style>
