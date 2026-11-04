<!--
	Full-height map page: side panel (title, byline, controls, legend, hover
	readout, notes) + AreaMap. Each map supplies its content as snippets and its
	data through `geographies` / `view` / `derive`; everything else is shared.

	Snippet content is styled through the `.panel :global(...)` rules below, so
	maps get consistent labels, selects, notes etc. without repeating CSS.
-->
<script>
	import AreaMap from './AreaMap.svelte';
	import Legend from './Legend.svelte';

	let {
		title,
		geographies,
		view,
		/** (value|null) => string, for the tooltip and hover readout */
		format,
		/** optional computed columns, see AreaMap */
		derive = null,
		/** text above the legend */
		description = '',
		/** legend tick formatter */
		formatBreak,
		byline,
		controls,
		notes
	} = $props();

	let hovered = $state(null);
</script>

<div class="layout">
	<aside class="panel">
		<h1>{title}</h1>
		{#if byline}<div class="byline">{@render byline()}</div>{/if}

		<section class="controls">
			{@render controls()}
		</section>

		<section class="legend">
			<p class="description">{description}</p>
			<Legend mode={view.mode} breaks={view.breaks} colours={view.colours} sizes={view.sizes} {formatBreak} />
		</section>

		<p class="hovered" aria-live="polite">
			<i>Hovered area</i>:
			{#if hovered}
				{#if hovered.name}{`${hovered.name}: `}{/if}<strong>{format(hovered.value)}</strong>
			{:else}
				hover over the map to see values
			{/if}
		</p>

		{#if notes}<section class="notes">{@render notes()}</section>{/if}
	</aside>

	<div class="map">
		<AreaMap {geographies} {view} {format} {derive} bind:hovered />
	</div>
</div>

<style>
	.layout {
		display: flex;
		height: calc(100dvh - var(--header-height));
		overflow: hidden;
	}

	.panel {
		flex: 0 0 450px;
		height: 100%;
		overflow-y: auto;
		box-sizing: border-box;
		padding: 20px;
		background: var(--brandWhite);
		border-right: 1px solid var(--brandDarkBlue);
	}

	.map {
		flex: 1;
		min-width: 0;
		height: 100%;
	}

	@media (max-width: 840px) {
		.layout {
			flex-direction: column;
		}
		.map {
			order: -1;
			flex: 0 0 50dvh;
			border-bottom: 1px solid var(--brandDarkBlue);
		}
		.panel {
			flex: 1 1 auto;
			width: 100%;
			border-right: none;
		}
	}

	h1 {
		margin-top: 4px;
		font-size: 28px;
		line-height: 36px;
	}

	.byline :global(p) {
		font-size: 14px;
		line-height: 20px;
		margin-top: 20px;
	}

	.controls {
		border-top: 1px solid var(--brandGray);
		padding-top: 5px;
	}

	.panel :global(.control-label) {
		display: block;
		margin: 14px 0 8px;
		padding: 0;
		font-family: SourceSerif, serif;
		font-size: 16px;
		line-height: 22px;
		color: var(--brandGray90);
	}

	.panel :global(select) {
		width: 100%;
		padding: 8px 10px;
		border: 1px solid var(--brandGray);
		border-radius: 5px;
		background: var(--brandWhite);
		font-family: TradeGothicBold, sans-serif;
		font-size: 16px;
		color: var(--brandGray90);
		cursor: pointer;
	}

	.panel :global(select:hover),
	.panel :global(select:focus) {
		border-color: var(--brandMedBlue);
	}

	/* explanatory note under a control (e.g. tariff or scenario description) */
	.panel :global(.control-note) {
		margin: 8px 0 0;
		padding: 4px 10px;
		border-left: 3px solid var(--brandLightBlue);
		background-color: #f7f9fb;
		font-size: 13px;
		line-height: 18px;
	}

	.panel :global(.summary) {
		font-size: 15px;
		line-height: 21px;
	}

	.legend {
		margin-top: 20px;
		border-top: 1px solid var(--brandGray);
	}

	.description {
		font-size: 16px;
		line-height: 22px;
	}

	.hovered {
		margin-top: 10px;
		padding-bottom: 20px;
		border-bottom: 1px solid var(--brandGray);
		font-size: 16px;
	}

	.notes :global(p),
	.notes :global(li) {
		font-size: 14px;
		line-height: 20px;
	}

	.notes :global(li) {
		padding-bottom: 4px;
	}

	.notes :global(h2) {
		font-size: 18px;
		margin-top: 20px;
	}

	.panel :global(a) {
		color: var(--brandBlack);
		text-decoration: underline;
	}

	.panel :global(a:hover) {
		color: var(--brandMedGreen);
	}
</style>
