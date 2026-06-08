<script>
	export let correlations = [];
	export let metricLabel = 'job share';

	const minSampleSize = 4;
	$: rows = correlations
		.filter((item) => Number.isFinite(item.correlation) && item.sampleSize >= minSampleSize)
		.map((item) => ({
			industry: item.industry,
			correlation: item.correlation,
			pValue: Number.isFinite(item.pValue) ? item.pValue : null
		}))
		.sort((a, b) => a.correlation - b.correlation);

	function formatPValue(value) {
		if (!Number.isFinite(value)) return 'n/a';
		if (value < 0.001) return '<0.001';
		return value.toFixed(4);
	}
</script>

<div class="simple-panel">
	<div class="intro">
		<h3>Industry job correlations with Canadian visit percent change (table)</h3>
		<p>
			Industry and correlation values using {metricLabel} within each metro.
		</p>
	</div>

	<div class="table-shell">
		<table>
			<thead>
				<tr>
					<th>Industry</th>
					<th>Correlation</th>
					<th>p-value</th>
				</tr>
			</thead>
			<tbody>
				{#each rows as row}
					<tr
						class:negative={row.correlation < 0}
						class:positive={row.correlation >= 0}
						class:insignificant={row.pValue === null || row.pValue > 0.05}
					>
						<td>{row.industry}</td>
						<td>{row.correlation.toFixed(3)}</td>
						<td>{formatPValue(row.pValue)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

<style>
	.simple-panel {
		max-width: 680px;
		margin: 0 auto;
		padding-top: 10px;
	}

	.intro {
		max-width: 680px;
		margin: 0 auto 20px auto;
	}

	.table-shell {
		max-width: 680px;
		margin: 0 auto;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
	}

	th,
	td {
		padding: 8px 10px;
		border: 1px solid rgba(30, 55, 101, 0.2);
		text-align: left;
	}

	th {
		font-family: OpenSansBold, sans-serif;
	}

	tr:first-child th {
		border-top: none;
	}

	tr:last-child td {
		border-bottom: none;
	}

	tr.negative {
		color: var(--brandRed);
		font-family: OpenSansBold, sans-serif;
	}

	tr.positive {
		color: var(--brandMedBlue);
		font-family: OpenSansBold, sans-serif;
	}

	tr.insignificant {
		opacity: 0.5;
	}

	tr.negative td:first-child,
	tr.positive td:first-child,
	tr.negative td:last-child,
	tr.positive td:last-child {
		color: var(--brandGray90);
		font-family: OpenSans, sans-serif;
	}

	th:first-child,
	td:first-child {
		border-left: none;
	}

	th:last-child,
	td:last-child {
		border-right: none;
	}
</style>
