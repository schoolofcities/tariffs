<script>
	import { onMount } from 'svelte';
	import { industryCorrelations } from './industryCorrelations.js';

	let plotContainer;
	let plotlyReady = false;
	let plotlyLoadPromise;
	const chartRows = industryCorrelations.filter((item) => Number.isFinite(item.correlation) && item.sampleSize >= 4);

	function loadPlotly() {
		if (window.Plotly) return Promise.resolve(window.Plotly);
		if (plotlyLoadPromise) return plotlyLoadPromise;

		plotlyLoadPromise = new Promise((resolve, reject) => {
			const existing = document.querySelector('script[data-plotly-cdn]');
			if (existing) {
				existing.addEventListener('load', () => resolve(window.Plotly), { once: true });
				existing.addEventListener('error', reject, { once: true });
				return;
			}

			const script = document.createElement('script');
			script.src = 'https://cdn.plot.ly/plotly-2.35.2.min.js';
			script.async = true;
			script.dataset.plotlyCdn = 'true';
			script.onload = () => resolve(window.Plotly);
			script.onerror = reject;
			document.head.appendChild(script);
		});

		return plotlyLoadPromise;
	}

	function renderPlotly() {
		if (!plotContainer || !window.Plotly) return;

		const sorted = [...chartRows].sort((a, b) => a.correlation - b.correlation);
		const y = sorted.map((item) => item.industry);
		const x = sorted.map((item) => item.correlation);
		const hoverText = sorted.map((item) => {
			const ptxt = item.pValue && Number.isFinite(item.pValue) ? `<br>p = ${item.pValue.toFixed(3)}` : '';
			return `NAICS ${item.code}<br>Sample size: ${item.sampleSize}${ptxt}`;
		});
		const colors = sorted.map((item) => (item.correlation >= 0 ? '#007FA3' : '#DC4633'));

		const data = [{
			type: 'bar',
			orientation: 'h',
			x,
			y,
			text: x.map((value) => value.toFixed(3)),
			textposition: 'inside',
			textfont: { color: '#ffffff', size: 12 },
			hovertext: hoverText,
			hovertemplate: '%{y}<br>Correlation: %{x:.3f}<br>%{hovertext}<extra></extra>',
			marker: { color: colors },
			width: 0.7
		}];

		const layout = {
			template: 'plotly_dark',
			paper_bgcolor: 'rgba(0,0,0,0)',
			plot_bgcolor: 'rgba(0,0,0,0)',
			margin: { l: 130, r: 12, t: 12, b: 50 },
			height: 680,
			xaxis: {
				title: 'Correlation: visit decline vs. industry employment',
				range: [-0.5, 0],
				zeroline: true,
				zerolinecolor: 'rgba(255,255,255,0.35)',
				gridcolor: 'rgba(255,255,255,0.10)',
				tickformat: '.2f'
			},
			yaxis: {
				autorange: 'reversed',
				title: ''
			},
			showlegend: false,
			font: { family: 'OpenSans, sans-serif', color: '#1E3765' },
			hoverlabel: {
				font: { family: 'OpenSans, sans-serif', size: 11 },
				align: 'left'
			}
		};

		const config = {
			responsive: true,
			displayModeBar: false
		};

		window.Plotly.react(plotContainer, data, layout, config);
	}

	onMount(async () => {
		plotlyReady = false;
		await loadPlotly();
		plotlyReady = true;
		renderPlotly();

		return () => {
			if (plotContainer && window.Plotly) {
				window.Plotly.purge(plotContainer);
			}
		};
	});

	$: if (plotlyReady) {
		renderPlotly();
	}
</script>

<div class="correlation-panel">
	<div class="intro">
		<h3>Industry correlations with Canadian visit decline</h3>
		<p>
			Each bar uses only metros where that industry is the dominant employer. Sample size is shown in the hover.
			Bars for industries with fewer than 4 dominant metros are excluded due to Pearson's Correlation coefficient.
		</p>
	</div>

	<div class="plotly-shell">
		<div class="plotly-chart" bind:this={plotContainer}></div>
		{#if !plotlyReady}
			<div class="loading-note">Loading Plotly chart…</div>
		{/if}
		{#if plotlyReady && chartRows.length === 0}
			<div class="loading-note">No dominant-industry sample available for this view.</div>
		{/if}
	</div>
</div>

<style>
	.correlation-panel {
		max-width: 680px;
		margin: 0 auto;
		padding-top: 10px;
	}

	.intro {
		max-width: 680px;
		margin: 0 auto 20px auto;
	}

	.plotly-shell {
		max-width: 680px;
		margin: 0 auto;
		position: relative;
	}

	.plotly-chart {
		width: 100%;
		min-height: 680px;
	}

	.loading-note {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: OpenSans, sans-serif;
		color: var(--brandGray90);
		background: rgba(255, 255, 255, 0.45);
	}

	.intro p {
		margin-bottom: 0;
	}

	@media (max-width: 680px) {
		.plotly-chart {
			min-height: 760px;
		}
	}
</style>
