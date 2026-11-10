<!--
	Figure 14: share of each scenario's job loss by industry, as a table with each cell
	shaded white -> yellow -> orange -> red (red at 30% and over). Uses the report's
	table styling (the .report-content table rules in global.css).
	rows: [{ industry, '1. Household consumption': %, ... }]
-->
<script>
	let { rows } = $props();

	const scenarios = $derived(Object.keys(rows[0]).filter((k) => k !== 'industry'));
	// short two-line headers so the table fits narrow screens
	const SHORT = ['Households', 'Agri-food', 'Steel', 'Lumber', 'Autos'];
	const header = (s) => {
		const n = parseInt(s, 10);
		return [`Scenario ${n}`, SHORT[n - 1] ?? s.replace(/^\d+\.\s*/, '')];
	};

	// colour stops (share %, rgb): white, brand yellow, orange, brand red
	const STOPS = [
		[0, [255, 255, 255]],
		[10, [241, 197, 0]],
		[20, [242, 135, 30]],
		[30, [220, 70, 51]]
	];
	function shade(v) {
		if (v >= STOPS.at(-1)[0]) return STOPS.at(-1)[1];
		const i = STOPS.findIndex(([s]) => s > v);
		const [a, ca] = STOPS[i - 1];
		const [b, cb] = STOPS[i];
		const t = (v - a) / (b - a);
		return ca.map((c, k) => Math.round(c + (cb[k] - c) * t));
	}
	const fill = (v) => `rgb(${shade(v).join(',')})`;
	// white text once the cell is dark enough
	const ink = (v) => (v >= 24 ? 'white' : 'var(--brandDarkBlue)');
	const gradient = `linear-gradient(to right, ${STOPS.map(([s, c]) => `rgb(${c.join(',')}) ${(s / 30) * 100}%`).join(', ')})`;
</script>

<div class="table-scroll">
	<table class="heatmap">
		<thead>
			<tr>
				<th>Industry</th>
				{#each scenarios as s (s)}
					{@const [a, b] = header(s)}
					<th class="num">{a}<br />{b}</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each rows as r (r.industry)}
				<tr>
					<td>{r.industry}</td>
					{#each scenarios as s (s)}
						<td class="num cell" style:background={fill(r[s])} style:color={ink(r[s])}>{Math.round(r[s])}%</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<div class="key" aria-hidden="true">
	<span>0%</span>
	<span class="ramp" style:background={gradient}></span>
	<span>30%+</span>
</div>

<style>
	.heatmap td {
		vertical-align: middle;
	}

	.cell {
		font-family: OpenSansBold, sans-serif;
		border-left: 2px solid var(--brandWhite);
	}

	@media (max-width: 600px) {
		.heatmap :is(th, td) {
			padding-left: 5px;
			padding-right: 5px;
		}

		/* phones scroll the table sideways: keep the industry names in view */
		.heatmap :is(th, td):first-child {
			position: sticky;
			left: 0;
			z-index: 1;
			min-width: 110px;
		}

		.heatmap th:first-child {
			background: var(--brandWhite);
		}
	}

	.key {
		display: flex;
		align-items: center;
		gap: 8px;
		margin-top: 10px;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray70);
	}

	.ramp {
		width: 160px;
		height: 10px;
		border: 1px solid var(--brandGray10);
	}
</style>
