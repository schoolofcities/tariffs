<script>
	import { regressionData } from './regressionData.js';
	import jstat from 'jstat';

	export let metric = "share";

	const naicsLabels = {
		"11": "Agriculture",
		"21": "Mining/Oil & Gas",
		"22": "Utilities",
		"23": "Construction",
		"31-33": "Manufacturing",
		"42": "Wholesale Trade",
		"44-45": "Retail Trade",
		"48-49": "Transportation/Warehousing",
		"51": "Information",
		"52": "Finance & Insurance",
		"53": "Real Estate",
		"54": "Professional Services",
		"55": "Management",
		"56": "Admin/Support",
		"61": "Education",
		"62": "Health Care",
		"71": "Arts/Entertainment",
		"72": "Accommodation/Food",
		"81": "Other Services",
		"99": "Unclassified"
	};

	const regionOrder = ["Northeast", "Southwest", "Southeast", "Pacific"];
	const baseRegion = "Midwest";

	const stateToRegion = {
		// Midwest
		IL: "Midwest", IN: "Midwest", MI: "Midwest", OH: "Midwest", WI: "Midwest",
		IA: "Midwest", KS: "Midwest", MN: "Midwest", MO: "Midwest", NE: "Midwest",
		ND: "Midwest", SD: "Midwest",
		// Northeast
		CT: "Northeast", ME: "Northeast", MA: "Northeast", NH: "Northeast", RI: "Northeast",
		VT: "Northeast", NJ: "Northeast", NY: "Northeast", PA: "Northeast",
		DE: "Northeast", MD: "Northeast",
		// Southwest
		AZ: "Southwest", NM: "Southwest", OK: "Southwest", TX: "Southwest",
		CO: "Southwest", NV: "Southwest", UT: "Southwest",
		// Southeast
		AL: "Southeast", AR: "Southeast", FL: "Southeast", GA: "Southeast", KY: "Southeast",
		LA: "Southeast", MS: "Southeast", NC: "Southeast", SC: "Southeast", TN: "Southeast",
		VA: "Southeast", WV: "Southeast", DC: "Southeast",
		// Pacific
		AK: "Pacific", CA: "Pacific", HI: "Pacific", OR: "Pacific", WA: "Pacific", ID: "Pacific", MT: "Pacific"
	};

	function getMetroRegion(metroName) {
		const stateMatch = metroName.match(/,\s*([A-Z]{2})/);
		if (stateMatch) {
			return stateToRegion[stateMatch[1]] || null;
		}
		const multiStateMatch = metroName.match(/,\s*([A-Z]{2}(?:-[A-Z]{2})+)/);
		if (multiStateMatch) {
			const firstState = multiStateMatch[1].split("-")[0];
			return stateToRegion[firstState] || null;
		}
		return null;
	}

	const industryCodes = Object.keys(naicsLabels);
	const baseIndustryCode = industryCodes.includes("44-45") ? "44-45" : industryCodes[industryCodes.length - 1];
	const featureIndustryCodes = industryCodes.filter((code) => code !== baseIndustryCode);
	$: shareMode = metric === "share";
	$: industryFeatureCodes = shareMode ? featureIndustryCodes : industryCodes;

	$: rows = regressionData
		.map((row) => ({
			...row,
			region: getMetroRegion(row.metro)
		}))
		.filter((row) => Number.isFinite(row.visitChange))
		.filter((row) => row.population2025 && row.region);

	function buildDesignMatrix(useShares, featureCodes) {
		const predictors = [];
		const y = [];
		const metroLabels = [];

		rows.forEach((row) => {
			const features = [];
			features.push(row.population2025 / 1_000_000); // population in millions

			regionOrder.forEach((region) => {
				features.push(row.region === region ? 1 : 0);
			});

			featureCodes.forEach((code) => {
				const value = useShares
					? row.industryShares?.[code] ?? 0
					: row.industryTotals?.[code] ?? 0;
				features.push(value);
			});

			predictors.push(features);
			y.push(row.visitChange);
			metroLabels.push(row.metro);
		});

		return { predictors, y, metroLabels };
	}

	function transpose(matrix) {
		return matrix[0].map((_, i) => matrix.map((row) => row[i]));
	}

	function multiply(a, b) {
		const rows = a.length;
		const cols = b[0].length;
		const shared = b.length;
		const result = Array.from({ length: rows }, () => Array(cols).fill(0));
		for (let i = 0; i < rows; i += 1) {
			for (let k = 0; k < shared; k += 1) {
				const val = a[i][k];
				for (let j = 0; j < cols; j += 1) {
					result[i][j] += val * b[k][j];
				}
			}
		}
		return result;
	}

	function invert(matrix) {
		const n = matrix.length;
		const augmented = matrix.map((row, i) => [
			...row,
			...Array.from({ length: n }, (_, j) => (i === j ? 1 : 0))
		]);

		for (let i = 0; i < n; i += 1) {
			let pivot = augmented[i][i];
			if (pivot === 0) {
				for (let r = i + 1; r < n; r += 1) {
					if (augmented[r][i] !== 0) {
						const temp = augmented[i];
						augmented[i] = augmented[r];
						augmented[r] = temp;
						pivot = augmented[i][i];
						break;
					}
				}
			}
			if (pivot === 0) {
				return null;
			}

			for (let j = 0; j < 2 * n; j += 1) {
				augmented[i][j] /= pivot;
			}

			for (let r = 0; r < n; r += 1) {
				if (r === i) continue;
				const factor = augmented[r][i];
				for (let c = 0; c < 2 * n; c += 1) {
					augmented[r][c] -= factor * augmented[i][c];
				}
			}
		}

		return augmented.map((row) => row.slice(n));
	}

	function standardize(matrix) {
		const cols = matrix[0].length;
		const means = Array(cols).fill(0);
		const stds = Array(cols).fill(0);
		const rowsCount = matrix.length;

		for (let j = 0; j < cols; j += 1) {
			means[j] = matrix.reduce((sum, row) => sum + row[j], 0) / rowsCount;
			stds[j] = Math.sqrt(matrix.reduce((sum, row) => sum + (row[j] - means[j]) ** 2, 0) / rowsCount) || 1;
		}

		const standardized = matrix.map((row) =>
			row.map((value, j) => (value - means[j]) / stds[j])
		);

		return { standardized, means, stds };
	}

	function normalCdf(x) {
		return jstat.normal.cdf(x, 0, 1);
	}

	function fitRegression(useShares, featureCodes) {
		if (rows.length < 5) return null;
		const { predictors, y, metroLabels } = buildDesignMatrix(useShares, featureCodes);
		const { standardized } = standardize(predictors);
		const X = standardized.map((row) => [1, ...row]);
		const yCol = y.map((value) => [value]);

		const Xt = transpose(X);
		const XtX = multiply(Xt, X);
		const XtXInv = invert(XtX);
		if (!XtXInv) return null;
		const XtY = multiply(Xt, yCol);
		const beta = multiply(XtXInv, XtY).map((row) => row[0]);

		const yHat = X.map((row) => row.reduce((sum, val, idx) => sum + val * beta[idx], 0));
		const yMean = y.reduce((sum, val) => sum + val, 0) / y.length;
		const ssTot = y.reduce((sum, val) => sum + (val - yMean) ** 2, 0);
		const ssRes = y.reduce((sum, val, idx) => sum + (val - yHat[idx]) ** 2, 0);
		const r2 = ssTot === 0 ? 0 : 1 - ssRes / ssTot;

		const n = y.length;
		const p = beta.length;
		const dof = n - p;
		const sigma2 = dof > 0 ? ssRes / dof : 0;
		const variance = XtXInv.map((row, idx) => row[idx] * sigma2);
		const stdErrors = variance.map((val) => (val > 0 ? Math.sqrt(val) : 0));
		const tStats = beta.map((value, idx) => (stdErrors[idx] ? value / stdErrors[idx] : 0));
		const pValues = tStats.map((t) => 2 * (1 - normalCdf(Math.abs(t))));

		return { beta, y, yHat, r2, metroLabels, predictors, stdErrors, tStats, pValues };
	}

	$: model = fitRegression(shareMode, industryFeatureCodes);

	$: coefficients = (() => {
		if (!model) return [];
		const industryPrefix = shareMode ? "Share" : "Jobs";
		const names = [
			"Intercept",
			"Population (millions, std)",
			...regionOrder.map((region) => `Region: ${region}`),
			...industryFeatureCodes.map((code) => `${industryPrefix}: ${naicsLabels[code] || code}`)
		];
		const length = Math.min(names.length, model.beta.length);
		return names.slice(0, length).map((name, idx) => ({
			name,
			value: model.beta[idx]
		}));
	})();

	function formatCoefficient(value) {
		return Number.isFinite(value) ? value.toFixed(3) : "n/a";
	}

	function formatPValue(value) {
		if (!Number.isFinite(value)) return "n/a";
		if (value < 0.001) return "<0.001";
		return value.toFixed(3);
	}

	let chartWidth = 0;
	const scatterMargin = { top: 36, right: 20, bottom: 50, left: 60 };
	$: scatterHeight = Math.max(360, Math.round(chartWidth * 0.6));
	$: scatterInnerWidth = Math.max(1, chartWidth - scatterMargin.left - scatterMargin.right);
	$: scatterInnerHeight = Math.max(1, scatterHeight - scatterMargin.top - scatterMargin.bottom);

	$: actualValues = model ? model.y : [];
	$: predictedValues = model ? model.yHat : [];
	$: scatterMinPad = -100;
	$: scatterMaxPad = 40;

	$: scatterScale = (value) =>
		scatterMargin.left + ((value - scatterMinPad) / (scatterMaxPad - scatterMinPad)) * scatterInnerWidth;
	$: scatterYScale = (value) =>
		scatterMargin.top + (1 - (value - scatterMinPad) / (scatterMaxPad - scatterMinPad)) * scatterInnerHeight;
	$: scatterTicks = [-100, -80, -60, -40, -20, 0, 20, 40];
	const tooltipWidth = 200;
	const tooltipHeight = 100;

	function formatTick(value) {
		return `${value.toFixed(0)}%`;
	}

	function getTooltipX(value) {
		const rawX = scatterScale(value) + 10;
		const minX = scatterMargin.left;
		const maxX = scatterMargin.left + scatterInnerWidth - tooltipWidth;
		return Math.max(minX, Math.min(rawX, maxX));
	}

	function getTooltipY(value) {
		const rawY = scatterYScale(value) - 60;
		const minY = scatterMargin.top;
		const maxY = scatterMargin.top + scatterInnerHeight - tooltipHeight;
		return Math.max(minY, Math.min(rawY, maxY));
	}

	let selectedPoint = null;
</script>

<div class="regression-panel">
	<div class="intro">
		<h3>Regression: visit change vs. industry {#if shareMode}shares {:else}totals{/if}</h3>
		<p>
			Single multivariate regression predicting visit YoY % change using industry {#if shareMode}shares {:else}totals{/if}, population, and region dummies.
			Baseline region is {baseRegion}.
		</p>
		{#if shareMode}
			<p>
                Baseline industry is {naicsLabels[baseIndustryCode]}, meaning it's dropped from the regression to avoid multicollinearity.
				Coefficients are standardized and relative to the baselines. Because industry shares sum to 1, each share coefficient
				captures a tilt away from the baseline industry rather than an independent standalone effect.
			</p>
		{/if}
	</div>

	{#if !model}
		<div class="loading-note">Not enough data to compute regression.</div>
	{:else}
		<div class="stats">
			<!-- <div>Metros: {model.y.length}</div> -->
			<div>R²: {model.r2.toFixed(3)}</div>
			<div>Predictors: {coefficients.length - 1}</div>
		</div>

		<div class="table-shell">
			<table>
				<thead>
					<tr>
						<th>Variable</th>
						<th>Coefficient (std)</th>
						<th>p-value</th>
					</tr>
				</thead>
				<tbody>
					{#each coefficients as coef, idx}
						<tr>
							<td>{coef.name}</td>
							<td>{formatCoefficient(coef.value)}</td>
							<td>{formatPValue(model?.pValues?.[idx])}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<div class="chart-shell" bind:offsetWidth={chartWidth}>
			<svg class="chart" width={chartWidth} height={scatterHeight}>
				<text
					x={scatterMargin.left + 50}
					y={scatterMargin.top - 12}
					text-anchor="middle"
					class="axis-title"
				>
					Predicted visit YoY change (%)
				</text>

				<line
					x1={scatterMargin.left}
					y1={scatterMargin.top + scatterInnerHeight}
					x2={scatterMargin.left + scatterInnerWidth}
					y2={scatterMargin.top + scatterInnerHeight}
					class="axis-line"
				/>
				<line
					x1={scatterMargin.left}
					y1={scatterMargin.top}
					x2={scatterMargin.left}
					y2={scatterMargin.top + scatterInnerHeight}
					class="axis-line"
				/>

				{#each scatterTicks as tick}
					<line
						x1={scatterScale(tick)}
						y1={scatterMargin.top + scatterInnerHeight}
						x2={scatterScale(tick)}
						y2={scatterMargin.top + scatterInnerHeight + 6}
						class="axis-tick"
					/>
					<text
						x={scatterScale(tick)}
						y={scatterMargin.top + scatterInnerHeight + 22}
						text-anchor="middle"
						class="axis-label"
					>
						{formatTick(tick)}
					</text>
					<line
						x1={scatterMargin.left - 6}
						y1={scatterYScale(tick)}
						x2={scatterMargin.left}
						y2={scatterYScale(tick)}
						class="axis-tick"
					/>
					<text
						x={scatterMargin.left - 10}
						y={scatterYScale(tick) + 4}
						text-anchor="end"
						class="axis-label"
					>
						{formatTick(tick)}
					</text>
				{/each}
				<line
					x1={scatterScale(scatterMinPad)}
					y1={scatterYScale(scatterMinPad)}
					x2={scatterScale(scatterMaxPad)}
					y2={scatterYScale(scatterMaxPad)}
					class="ref-line"
				/>

				{#each actualValues as actual, idx}
					<circle
						cx={scatterScale(actual)}
						cy={scatterYScale(predictedValues[idx])}
						r="4"
						fill="#007FA3"
						stroke="#000000"
						stroke-width="0.6"
						on:mouseenter={() => (selectedPoint = {
							metro: model.metroLabels[idx],
							actual,
							predicted: predictedValues[idx]
						})}
						on:mouseleave={() => (selectedPoint = null)}
					/>
				{/each}

				{#if selectedPoint}
					<foreignObject
						x={getTooltipX(selectedPoint.actual)}
						y={getTooltipY(selectedPoint.predicted)}
						width={tooltipWidth}
						height={tooltipHeight}
						style="pointer-events: none;"
					>
						<div class="tooltip" style="pointer-events: none;">
							<div class="tooltip-title">{selectedPoint.metro}</div>
							<div>Actual: {selectedPoint.actual.toFixed(1)}%</div>
							<div>Predicted: {selectedPoint.predicted.toFixed(1)}%</div>
						</div>
					</foreignObject>
				{/if}

				<text
					x={scatterMargin.left + scatterInnerWidth / 2}
					y={scatterHeight - 10}
					text-anchor="middle"
					class="axis-title"
				>
					Actual visit YoY change (%)
				</text>
			</svg>
		</div>
	{/if}
</div>

<style>
	.regression-panel {
		max-width: 680px;
		margin: 0 auto;
		padding-top: 10px;
	}

	.intro {
		max-width: 680px;
		margin: 0 auto 20px auto;
	}

	.stats {
		display: flex;
		gap: 16px;
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
		margin-bottom: 18px;
	}

	.table-shell {
		max-width: 680px;
		margin: 0 auto 30px auto;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray90);
	}

	th,
	td {
		padding: 6px 10px;
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

	th:first-child,
	td:first-child {
		border-left: none;
	}

	th:last-child,
	td:last-child {
		border-right: none;
	}

	.chart-shell {
		max-width: 700px;
		margin: 0 auto;
		position: relative;
	}

	.chart {
		width: 100%;
	}

	.loading-note {
		padding: 20px 0;
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: OpenSans, sans-serif;
		color: var(--brandGray90);
	}

	.ref-line {
		stroke: rgba(30, 55, 101, 0.4);
		stroke-width: 1.2;
		stroke-dasharray: 5 4;
	}

	.axis-line {
		stroke: rgba(30, 55, 101, 0.45);
		stroke-width: 1;
	}

	.axis-tick {
		stroke: rgba(30, 55, 101, 0.5);
		stroke-width: 1;
}

	.axis-label {
		fill: var(--brandGray90);
		font-size: 11px;
		font-family: OpenSans, sans-serif;
	}

	.axis-title {
		fill: var(--brandGray90);
		font-size: 13px;
		font-family: OpenSansBold, sans-serif;
	}

	.tooltip {
		background: rgba(255, 255, 255, 0.95);
		border: 1px solid rgba(30, 55, 101, 0.2);
		border-radius: 6px;
		padding: 8px 10px;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray90);
	}

	.tooltip-title {
		font-family: OpenSansBold, sans-serif;
		margin-bottom: 4px;
	}
</style>
