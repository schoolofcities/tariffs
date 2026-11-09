<!--
	Frame for a report chart: the figure's caption from the report docx as the title
	(Open Sans Bold, black, same as the table captions), then the chart, rendered by the
	`chart` snippet with the measured width. No added titles or subtitles: text comes
	from the docx as written. A small button under the chart saves the figure (caption +
	chart) as a PNG.
-->
<script>
	/** e.g. "Figure 7: Scenario 3 (steel and aluminum): job loss by province" (may include a footnote marker) */
	import { tick } from 'svelte';

	let { title, chart } = $props();
	let width = $state(0);
	let figure;
	let saving = $state(false);

	// "Figure 7: ..." -> "figure-7.png"; otherwise a slug of the caption
	const fileName = $derived.by(() => {
		const text = title.replace(/<[^>]*>/g, '');
		const n = text.match(/^Figure\s+(\w+)/i);
		const base = n ? `figure-${n[1]}` : text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60);
		return `mapping-tariffs-${base}.png`;
	});

	async function download() {
		if (saving) return;
		saving = true;
		try {
			const { toPng } = await import('html-to-image');
			// tables (Figure 14) scroll sideways on small screens: show them in full while exporting
			const scroller = figure.querySelector('.table-scroll');
			const fullW = Math.max(figure.offsetWidth, scroller ? scroller.scrollWidth : 0);
			figure.classList.add('exporting');
			figure.style.width = `${fullW}px`;
			await tick();
			// the image is the figure without its button, plus a white margin all round
			const PAD = 16;
			const button = figure.querySelector('.chart-download');
			const w = fullW + PAD * 2;
			const h = figure.offsetHeight - (button ? button.offsetHeight + 10 : 0) + PAD * 2;
			const url = await toPng(figure, {
				backgroundColor: '#ffffff',
				pixelRatio: 2,
				// leave out the button itself and footnote markers in the caption
				filter: (node) => !node.classList?.contains('chart-download') && !node.classList?.contains('footnote-ref-wrapper'),
				// size the copy so the chart keeps its on-screen width inside the margin
				style: { margin: '0', padding: `${PAD}px`, boxSizing: 'border-box', width: `${w}px`, height: `${h}px` },
				width: w,
				height: h
			});
			const a = document.createElement('a');
			a.href = url;
			a.download = fileName;
			a.click();
		} catch (err) {
			console.error('Chart download failed', err);
		} finally {
			figure.classList.remove('exporting');
			figure.style.width = '';
			saving = false;
		}
	}
</script>

<figure class="chart-frame" bind:this={figure}>
	<figcaption class="chart-title">{@html title}</figcaption>
	<div class="chart-body" bind:clientWidth={width}>
		{#if width}{@render chart(width)}{/if}
	</div>
	<button type="button" class="chart-download" onclick={download} disabled={saving}>
		<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true">
			<path d="M6 1v7M3 5l3 3 3-3M1.5 10.5h9" fill="none" stroke="currentColor" stroke-width="1.4" />
		</svg>
		{saving ? 'Saving…' : 'Download PNG'}
	</button>
</figure>

<style>
	.chart-frame {
		margin: 28px 0 34px;
	}

	.chart-title {
		margin: 0 0 12px;
		/* same as the table captions */
		font-family: OpenSansBold, sans-serif;
		font-size: 15px;
		line-height: 1.2;
		color: var(--brandBlack);
	}

	.chart-body {
		width: 100%;
	}

	.chart-body :global(svg) {
		display: block;
		overflow: visible;
	}

	.chart-body :global(text) {
		font-family: OpenSans, sans-serif;
		font-size: 12px;
	}

	.chart-frame:global(.exporting) :global(.table-scroll) {
		overflow: visible;
	}

	/* small, flat, square: sits under the chart on the right */
	.chart-download {
		display: flex;
		align-items: center;
		gap: 5px;
		margin: 10px 0 0 auto;
		padding: 3px 8px;
		border: 1px solid var(--brandGray20, #cccccc);
		border-radius: 0;
		background: var(--brandWhite);
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		line-height: 1.3;
		color: var(--brandGray70);
		cursor: pointer;
	}

	.chart-download:hover {
		border-color: var(--brandDarkBlue);
		color: var(--brandDarkBlue);
	}

	.chart-download:disabled {
		cursor: wait;
		opacity: 0.6;
	}

	@media (max-width: 600px) {
		.chart-title {
			font-size: 13px;
		}
	}
</style>
