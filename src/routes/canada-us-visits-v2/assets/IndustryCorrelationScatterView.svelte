<script>
	import { onMount } from 'svelte';
	import { visitJobsScatterData } from './visitJobsScatterData.js';

	let plotContainer;
	let plotlyReady = false;
	let plotlyLoadPromise;
	const chartRows = visitJobsScatterData.filter((item) => Number.isFinite(item.visitChange) && Number.isFinite(item.totalJobs));

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
		if (chartRows.length === 0) {
			window.Plotly.react(plotContainer, [], { margin: { l: 20, r: 20, t: 20, b: 20 } }, { displayModeBar: false });
			return;
		}

		const colorSequence = [
			'rgb(127, 60, 141)',
			'rgb(17, 165, 121)',
			'rgb(57, 105, 172)',
			'rgb(242, 183, 1)',
			'rgb(231, 63, 116)',
			'rgb(128, 186, 90)',
			'rgb(230, 131, 16)',
			'rgb(0, 134, 149)',
			'rgb(207, 28, 144)',
			'rgb(225, 157, 168)'
		];

		const industries = [...new Set(chartRows.map((item) => item.dominantIndustry))].sort();
		const colorMap = new Map(industries.map((industry, index) => [industry, colorSequence[index % colorSequence.length]]));
		const traces = industries.map((industry) => {
			const rows = chartRows.filter((item) => item.dominantIndustry === industry);
			return {
				type: 'scatter',
				mode: 'markers',
				name: industry,
				x: rows.map((item) => item.visitChange),
				y: rows.map((item) => item.totalJobs),
				text: rows.map((item) => item.metro),
				customdata: rows.map((item) => [item.dominantIndustry, item.dominantJobs]),
				hovertemplate: '<b>%{text}</b><br><br>Dominant Industry=%{customdata[0]}<br>Canada to US Visits YoY % Change=%{x:.1f}<br>Total Jobs (2023)=%{y:,}<br>Dominant-sector Jobs=%{customdata[1]:,}<extra></extra>',
				marker: {
					color: colorMap.get(industry),
					size: 9,
					opacity: 0.85,
					line: { color: 'rgba(255,255,255,0.4)', width: 0.5 }
				}
			};
		});

		const xAll = chartRows.map((item) => item.visitChange);
		const yAll = chartRows.map((item) => item.totalJobs);
		const xMean = xAll.reduce((sum, value) => sum + value, 0) / xAll.length;
		const yMean = yAll.reduce((sum, value) => sum + value, 0) / yAll.length;
		let num = 0;
		let den = 0;
		for (let i = 0; i < xAll.length; i += 1) {
			const dx = xAll[i] - xMean;
			const dy = yAll[i] - yMean;
			num += dx * dy;
			den += dx * dx;
		}
		const slope = den === 0 ? 0 : num / den;
		const intercept = yMean - slope * xMean;
		const xMin = Math.min(...xAll);
		const xMax = Math.max(...xAll);
		const trendX = [xMin, xMax];
		const trendY = trendX.map((xVal) => slope * xVal + intercept);

		const data = [
			...traces,
			{
				type: 'scatter',
				mode: 'lines',
				name: 'Trendline',
				x: trendX,
				y: trendY,
				line: { color: 'black', width: 1.5, dash: 'dash' },
				showlegend: true
			}
		];

		const layout = {
			template: 'plotly_dark',
			paper_bgcolor: 'rgba(0,0,0,0)',
			plot_bgcolor: 'rgba(0,0,0,0)',
			autosize: true,
			height: 700,
			margin: { l: 70, r: 70, t: 20, b: 60 },
			xaxis: {
				title: 'Canada to US Visits YoY % Change',
				ticksuffix: '%',
				zeroline: true,
				zerolinecolor: 'rgba(255,255,255,0.2)'
			},
			yaxis: {
				title: 'Total Jobs (2023)',
				tickformat: '~s',
				rangemode: 'tozero'
			},
			legend: {
				title: { text: 'Dominant NAICS Sector' },
				orientation: 'v',
				x: 1.02,
				y: 1,
				font: { size: 11 }
			},
			shapes: [
				{
					type: 'line',
					x0: 0,
					x1: 0,
					y0: 0,
					y1: 1,
					xref: 'x',
					yref: 'y domain',
					line: { color: 'rgba(255,255,255,0.3)', dash: 'dash', width: 1 }
				}
			],
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
		<h3>Canadian visit decline vs. total jobs by dominant industry</h3>
		<p>
			Each point is a metro. Color shows the dominant NAICS sector by 2023 jobs.
			The dotted line shows the overall trendline, and the vertical reference is 0% visit change.
		</p>
	</div>

	<div class="plotly-shell">
		<div class="plotly-chart" bind:this={plotContainer}></div>
		{#if !plotlyReady}
			<div class="loading-note">Loading Plotly chart…</div>
		{/if}
		{#if plotlyReady && chartRows.length === 0}
			<div class="loading-note">No visit/jobs sample available for this view.</div>
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
		width: 1000px;
		max-width: 1000px;
		margin-left: calc(50% - 450px);
		position: relative;
	}

	.plotly-chart {
		width: 100%;
		margin: 0 auto;
		min-height: 620px;
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

	@media (max-width: 900px) {
		.plotly-chart {
			min-height: 720px;
		}
	}
</style>
