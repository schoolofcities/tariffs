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
		IL: "Midwest", IN: "Midwest", MI: "Midwest", OH: "Midwest", WI: "Midwest",
		IA: "Midwest", KS: "Midwest", MN: "Midwest", MO: "Midwest", NE: "Midwest",
		ND: "Midwest", SD: "Midwest",
		CT: "Northeast", ME: "Northeast", MA: "Northeast", NH: "Northeast", RI: "Northeast",
		VT: "Northeast", NJ: "Northeast", NY: "Northeast", PA: "Northeast",
		DE: "Northeast", MD: "Northeast",
		AZ: "Southwest", NM: "Southwest", OK: "Southwest", TX: "Southwest",
		CO: "Southwest", NV: "Southwest", UT: "Southwest",
		AL: "Southeast", AR: "Southeast", FL: "Southeast", GA: "Southeast", KY: "Southeast",
		LA: "Southeast", MS: "Southeast", NC: "Southeast", SC: "Southeast", TN: "Southeast",
		VA: "Southeast", WV: "Southeast", DC: "Southeast",
		AK: "Pacific", CA: "Pacific", HI: "Pacific", OR: "Pacific", WA: "Pacific", ID: "Pacific", MT: "Pacific"
	};

	function getMetroRegion(metroName) {
		const stateMatch = metroName.match(/,\s*([A-Z]{2})/);
		if (stateMatch) return stateToRegion[stateMatch[1]] || null;
		const multiStateMatch = metroName.match(/,\s*([A-Z]{2}(?:-[A-Z]{2})+)/);
		if (multiStateMatch) return stateToRegion[multiStateMatch[1].split("-")[0]] || null;
		return null;
	}

	const industryCodes = Object.keys(naicsLabels);

	let selectedBaseCode = "44-45";
	let regressionMode = "full";  // "full" | "stepwise"

	$: baseIndustryCode = selectedBaseCode;
	$: featureIndustryCodes = industryCodes.filter((code) => code !== baseIndustryCode);
	$: shareMode = metric === "share";
	$: industryFeatureCodes = shareMode ? featureIndustryCodes : industryCodes;

	$: rows = regressionData
		.map((row) => ({ ...row, region: getMetroRegion(row.metro) }))
		.filter((row) => Number.isFinite(row.visitChange))
		.filter((row) => row.population2025 && row.region)
		.filter((row) => Number.isFinite(row.distToBorderKm) && Number.isFinite(row.cy24Enplanements));

	// ── Matrix helpers ────────────────────────────────────────────────────────
	function transpose(matrix) {
		return matrix[0].map((_, i) => matrix.map((row) => row[i]));
	}

	function multiply(a, b) {
		const rows = a.length, cols = b[0].length, shared = b.length;
		const result = Array.from({ length: rows }, () => Array(cols).fill(0));
		for (let i = 0; i < rows; i++)
			for (let k = 0; k < shared; k++) {
				const val = a[i][k];
				for (let j = 0; j < cols; j++) result[i][j] += val * b[k][j];
			}
		return result;
	}

	function invert(matrix) {
		const n = matrix.length;
		const aug = matrix.map((row, i) => [...row, ...Array.from({ length: n }, (_, j) => (i === j ? 1 : 0))]);
		for (let i = 0; i < n; i++) {
			let pivot = aug[i][i];
			if (pivot === 0) {
				for (let r = i + 1; r < n; r++) {
					if (aug[r][i] !== 0) { [aug[i], aug[r]] = [aug[r], aug[i]]; pivot = aug[i][i]; break; }
				}
			}
			if (pivot === 0) return null;
			for (let j = 0; j < 2 * n; j++) aug[i][j] /= pivot;
			for (let r = 0; r < n; r++) {
				if (r === i) continue;
				const f = aug[r][i];
				for (let c = 0; c < 2 * n; c++) aug[r][c] -= f * aug[i][c];
			}
		}
		return aug.map((row) => row.slice(n));
	}

	function standardize(matrix) {
		const cols = matrix[0].length, n = matrix.length;
		const means = Array(cols).fill(0), stds = Array(cols).fill(0);
		for (let j = 0; j < cols; j++) {
			means[j] = matrix.reduce((s, r) => s + r[j], 0) / n;
			stds[j] = Math.sqrt(matrix.reduce((s, r) => s + (r[j] - means[j]) ** 2, 0) / n) || 1;
		}
		return { standardized: matrix.map((row) => row.map((v, j) => (v - means[j]) / stds[j])), means, stds };
	}

	function normalCdf(x) { return jstat.normal.cdf(x, 0, 1); }

	// ── Core regression ───────────────────────────────────────────────────────
	function buildPredictors(useShares, extraCodes) {
		const predictors = [], y = [], metroLabels = [];
		rows.forEach((row) => {
			const f = [];
			f.push(row.population2025 / 1_000_000);
			regionOrder.forEach((r) => f.push(row.region === r ? 1 : 0));
			f.push(row.distToBorderKm / 1000);
			f.push(row.cy24Enplanements / 1_000_000);
			extraCodes.forEach((code) => {
				f.push(useShares ? row.industryShares?.[code] ?? 0 : row.industryTotals?.[code] ?? 0);
			});
			predictors.push(f);
			y.push(row.visitChange);
			metroLabels.push(row.metro);
		});
		return { predictors, y, metroLabels };
	}

	function fitWithCodes(useShares, codes) {
		if (rows.length < 5) return null;
		const { predictors, y, metroLabels } = buildPredictors(useShares, codes);
		const { standardized } = standardize(predictors);
		const X = standardized.map((r) => [1, ...r]);
		const yCol = y.map((v) => [v]);
		const Xt = transpose(X);
		const XtXInv = invert(multiply(Xt, X));
		if (!XtXInv) return null;
		const beta = multiply(XtXInv, multiply(Xt, yCol)).map((r) => r[0]);
		const yHat = X.map((r) => r.reduce((s, v, i) => s + v * beta[i], 0));
		const yMean = y.reduce((s, v) => s + v, 0) / y.length;
		const ssTot = y.reduce((s, v) => s + (v - yMean) ** 2, 0);
		const ssRes = y.reduce((s, v, i) => s + (v - yHat[i]) ** 2, 0);
		const r2 = ssTot === 0 ? 0 : 1 - ssRes / ssTot;
		const n = y.length, p = beta.length, dof = n - p;
		const sigma2 = dof > 0 ? ssRes / dof : 0;
		const adjR2 = dof > 0 ? 1 - (ssRes / dof) / (ssTot / (n - 1)) : r2;
		const variance = XtXInv.map((row, idx) => row[idx] * sigma2);
		const stdErrors = variance.map((v) => (v > 0 ? Math.sqrt(v) : 0));
		const tStats = beta.map((v, i) => (stdErrors[i] ? v / stdErrors[i] : 0));
		const pValues = tStats.map((t) => 2 * (1 - normalCdf(Math.abs(t))));
		return { beta, y, yHat, r2, adjR2, metroLabels, predictors, stdErrors, tStats, pValues, includedCodes: codes };
	}

	// ── Full model ────────────────────────────────────────────────────────────
	$: model = fitWithCodes(shareMode, industryFeatureCodes);

	$: coefficients = (() => {
		if (!model) return [];
		const prefix = shareMode ? "Share" : "Jobs";
		const names = [
			"Intercept", "Population (M, std)",
			...regionOrder.map((r) => `Region: ${r}`),
			"Distance to border (1000 km, std)",
			"Airport enplanements (M, std)",
			...model.includedCodes.map((c) => `${prefix}: ${naicsLabels[c] || c}`)
		];
		return names.slice(0, model.beta.length).map((name, i) => ({
			name, value: model.beta[i], pValue: model.pValues[i]
		}));
	})();

	// ── backward stepwise ─────────────────────────────────────────────────────
	$: stepwiseResult = (() => {
		if (rows.length < 5) return null;

		const steps = [];
		let included = [...industryFeatureCodes]; // start with ALL industry variables

		// Step 0: full model
		let current = fitWithCodes(shareMode, included);
		if (!current) return null;
		steps.push({
			step: 0,
			label: `Full model (${included.length} industry variables)`,
			r2: current.r2, adjR2: current.adjR2, deltaAdjR2: null, model: current
		});

		while (included.length > 0) {
			let best = null, bestCode = null, bestAdjR2 = current.adjR2;

			for (const code of included) {
				const candidate = fitWithCodes(shareMode, included.filter(c => c !== code));
				if (candidate && candidate.adjR2 > bestAdjR2) {
					bestAdjR2 = candidate.adjR2;
					best = candidate;
					bestCode = code;
				}
			}

			if (!bestCode) break; // removing anything hurts adj R² — stop

			included = included.filter(c => c !== bestCode);
			current = best;
			steps.push({
				step: steps.length,
				label: `− ${shareMode ? "Share" : "Jobs"}: ${naicsLabels[bestCode] || bestCode}`,
				removedCode: bestCode,
				r2: current.r2,
				adjR2: current.adjR2,
				deltaAdjR2: bestAdjR2 - steps[steps.length - 1].adjR2,
				model: current
			});
		}

		return { steps, finalModel: current };
	})();

	$: activeStepIdx = stepwiseResult ? stepwiseResult.steps.length - 1 : 0;

	$: stepCoefficients = (() => {
		if (!stepwiseResult || !stepwiseResult.steps[activeStepIdx]) return [];
		const m = stepwiseResult.steps[activeStepIdx].model;
		if (!m) return [];
		const prefix = shareMode ? "Share" : "Jobs";
		const names = [
			"Intercept", "Population (M, std)",
			...regionOrder.map((r) => `Region: ${r}`),
			"Distance to border (1000 km, std)",
			"Airport enplanements (M, std)",
			...m.includedCodes.map((c) => `${prefix}: ${naicsLabels[c] || c}`)
		];
		return names.slice(0, m.beta.length).map((name, i) => ({
			name, value: m.beta[i], pValue: m.pValues[i],
			isIndustry: i >= 6  // base predictors = 6 slots (intercept + pop + 4 regions + dist + airports)
		}));
	})();

	// ── Scatter helpers ───────────────────────────────────────────────────────
	$: activeModel = regressionMode === "stepwise"
		? stepwiseResult?.steps[activeStepIdx]?.model
		: model;

	function formatCoefficient(v) { return Number.isFinite(v) ? v.toFixed(3) : "n/a"; }
	function formatPValue(v) {
		if (!Number.isFinite(v)) return "n/a";
		if (v < 0.001) return "<0.001";
		return v.toFixed(3);
	}

	let chartWidth = 0;
	const scatterMargin = { top: 36, right: 20, bottom: 50, left: 60 };
	$: scatterHeight = Math.max(360, Math.round(chartWidth * 0.6));
	$: scatterInnerWidth = Math.max(1, chartWidth - scatterMargin.left - scatterMargin.right);
	$: scatterInnerHeight = Math.max(1, scatterHeight - scatterMargin.top - scatterMargin.bottom);
	$: actualValues = activeModel ? activeModel.y : [];
	$: predictedValues = activeModel ? activeModel.yHat : [];
	const scatterMinPad = -100, scatterMaxPad = 40;
	$: scatterScale = (v) => scatterMargin.left + ((v - scatterMinPad) / (scatterMaxPad - scatterMinPad)) * scatterInnerWidth;
	$: scatterYScale = (v) => scatterMargin.top + (1 - (v - scatterMinPad) / (scatterMaxPad - scatterMinPad)) * scatterInnerHeight;
	const scatterTicks = [-100, -80, -60, -40, -20, 0, 20, 40];
	const tooltipWidth = 200, tooltipHeight = 100;
	function formatTick(v) { return `${v.toFixed(0)}%`; }
	function getTooltipX(v) {
		return Math.max(scatterMargin.left, Math.min(scatterScale(v) + 10, scatterMargin.left + scatterInnerWidth - tooltipWidth));
	}
	function getTooltipY(v) {
		return Math.max(scatterMargin.top, Math.min(scatterYScale(v) - 60, scatterMargin.top + scatterInnerHeight - tooltipHeight));
	}
	let selectedPoint = null;
</script>

<div class="regression-panel">
	<div class="intro">
		<h3>Regression: visit change vs. industry {#if shareMode}shares{:else}totals{/if}</h3>
		<p>
			Multivariate regression predicting visit YoY % change using industry {#if shareMode}shares{:else}totals{/if},
			population, region dummies, distance to Canadian border, and airport enplanements.
			Baseline region: {baseRegion}.
		</p>
		{#if shareMode}
			<p>
				Baseline industry: {naicsLabels[baseIndustryCode]} (dropped to avoid multicollinearity;
				each share coefficient captures a tilt away from this baseline).
			</p>
		{/if}

		<div class="mode-row">
			{#if shareMode}
				<div class="inline-filter">
					<label for="baseline-industry">Baseline industry:</label>
					<select id="baseline-industry" bind:value={selectedBaseCode}>
						{#each [...industryCodes].sort((a, b) => naicsLabels[a].localeCompare(naicsLabels[b])) as code}
							<option value={code}>{naicsLabels[code]}</option>
						{/each}
					</select>
				</div>
			{/if}

			<div class="mode-toggle">
				<button class="toggle-btn" class:active={regressionMode === 'full'} on:click={() => regressionMode = 'full'}>
					Full model
				</button>
				<button class="toggle-btn" class:active={regressionMode === 'stepwise'} on:click={() => regressionMode = 'stepwise'}>
					Stepwise
				</button>
			</div>
		</div>
	</div>

	<!-- STEPWISE VIEW ──────────────────────────────────────────────────────── -->
	{#if regressionMode === 'stepwise'}
		{#if !stepwiseResult}
			<div class="loading-note">Not enough data.</div>
		{:else}
			<p class="stepwise-note">
				Backwards stepwise selection — each step removes the industry variable with the lowest improvement
				in adjusted R². Click a step to inspect its coefficients.
			</p>

			<!-- Step table -->
			<div class="table-shell">
				<table>
					<thead>
						<tr>
							<th>Step</th>
							<th>Variable removed</th>
							<th>R²</th>
							<th>Adj. R²</th>
							<th>ΔAdj. R²</th>
						</tr>
					</thead>
					<tbody>
						{#each stepwiseResult.steps as step, i}
							<tr
								class:step-active={i === activeStepIdx}
								on:click={() => activeStepIdx = i}
								style="cursor:pointer"
							>
								<td>{step.step}</td>
								<td>{step.label}</td>
								<td>{step.r2.toFixed(3)}</td>
								<td>{step.adjR2.toFixed(3)}</td>
								<td>{step.deltaAdjR2 !== null ? '+' + step.deltaAdjR2.toFixed(4) : '-'}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<!-- Coefficients for selected step -->
			<div class="step-coef-header">
				Coefficients at step {activeStepIdx}: {stepwiseResult.steps[activeStepIdx]?.label}
				<span class="step-r2">R² = {stepwiseResult.steps[activeStepIdx]?.r2.toFixed(3)}</span>
			</div>
			<div class="table-shell">
				<table>
					<thead>
						<tr><th>Variable</th><th>Coef. (std)</th><th>p-value</th></tr>
					</thead>
					<tbody>
						{#each stepCoefficients as coef, idx}
							<tr
								class:negative={coef.value < 0}
								class:positive={coef.value >= 0}
								class:insignificant={(coef.pValue ?? 1) > 0.10}
								class:industry-row={coef.isIndustry}
							>
								<td>{coef.name}</td>
								<td>{formatCoefficient(coef.value)}</td>
								<td>{formatPValue(coef.pValue)}{(coef.pValue ?? 1) < 0.10 ? ' *' : ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}

	<!-- FULL MODEL VIEW ────────────────────────────────────────────────────── -->
	{:else}
		{#if !model}
			<div class="loading-note">Not enough data to compute regression.</div>
		{:else}
			<div class="stats">
				<div>R²: {model.r2.toFixed(3)}</div>
				<div>Adj. R²: {model.adjR2.toFixed(3)}</div>
				<div>Predictors: {coefficients.length - 1}</div>
			</div>

			<div class="table-shell">
				<table>
					<thead>
						<tr><th>Variable</th><th>Coefficient (std)</th><th>p-value</th></tr>
					</thead>
					<tbody>
						{#each coefficients as coef, idx}
							<tr
								class:negative={coef.value < 0}
								class:positive={coef.value >= 0}
								class:insignificant={(model?.pValues?.[idx] ?? 1) > 0.10}
							>
								<td>{coef.name}</td>
								<td>{formatCoefficient(coef.value)}</td>
								<td>{formatPValue(model?.pValues?.[idx])}{(model?.pValues?.[idx] ?? 1) < 0.10 ? ' *' : ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	{/if}

	<!-- SCATTER (shared) ─────────────────────────────────────────────────────
	{#if activeModel}
		<div class="chart-shell" bind:offsetWidth={chartWidth}>
			<svg class="chart" width={chartWidth} height={scatterHeight}>
				<text x={scatterMargin.left + 50} y={scatterMargin.top - 12} text-anchor="middle" class="axis-title">
					Predicted visit YoY change (%)
				</text>
				<line x1={scatterMargin.left} y1={scatterMargin.top + scatterInnerHeight}
					x2={scatterMargin.left + scatterInnerWidth} y2={scatterMargin.top + scatterInnerHeight} class="axis-line" />
				<line x1={scatterMargin.left} y1={scatterMargin.top}
					x2={scatterMargin.left} y2={scatterMargin.top + scatterInnerHeight} class="axis-line" />
				{#each scatterTicks as tick}
					<line x1={scatterScale(tick)} y1={scatterMargin.top + scatterInnerHeight}
						x2={scatterScale(tick)} y2={scatterMargin.top + scatterInnerHeight + 6} class="axis-tick" />
					<text x={scatterScale(tick)} y={scatterMargin.top + scatterInnerHeight + 22} text-anchor="middle" class="axis-label">
						{formatTick(tick)}
					</text>
					<line x1={scatterMargin.left - 6} y1={scatterYScale(tick)}
						x2={scatterMargin.left} y2={scatterYScale(tick)} class="axis-tick" />
					<text x={scatterMargin.left - 10} y={scatterYScale(tick) + 4} text-anchor="end" class="axis-label">
						{formatTick(tick)}
					</text>
				{/each}
				<line x1={scatterScale(scatterMinPad)} y1={scatterYScale(scatterMinPad)}
					x2={scatterScale(scatterMaxPad)} y2={scatterYScale(scatterMaxPad)} class="ref-line" />
				{#each actualValues as actual, idx}
					<circle cx={scatterScale(actual)} cy={scatterYScale(predictedValues[idx])}
						r="4" fill="#007FA3" stroke="#000000" stroke-width="0.6"
						on:mouseenter={() => (selectedPoint = { metro: activeModel.metroLabels[idx], actual, predicted: predictedValues[idx] })}
						on:mouseleave={() => (selectedPoint = null)} />
				{/each}
				{#if selectedPoint}
					<foreignObject x={getTooltipX(selectedPoint.actual)} y={getTooltipY(selectedPoint.predicted)}
						width={tooltipWidth} height={tooltipHeight} style="pointer-events:none;">
						<div class="tooltip" style="pointer-events:none;">
							<div class="tooltip-title">{selectedPoint.metro}</div>
							<div>Actual: {selectedPoint.actual.toFixed(1)}%</div>
							<div>Predicted: {selectedPoint.predicted.toFixed(1)}%</div>
						</div>
					</foreignObject>
				{/if}
				<text x={scatterMargin.left + scatterInnerWidth / 2} y={scatterHeight - 10}
					text-anchor="middle" class="axis-title">Actual visit YoY change (%)
				</text>
			</svg>
		</div>
	{/if} -->
</div>

<style>
	.regression-panel { max-width: 680px; margin: 0 auto; padding-top: 10px; }
	.intro { max-width: 680px; margin: 0 auto 20px auto; }

	.mode-row {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 16px;
		margin-top: 12px;
	}

	.mode-toggle {
		display: flex;
		gap: 6px;
	}

	.toggle-btn {
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		padding: 5px 12px;
		border: 1px solid var(--brandGray);
		background: var(--brandWhite);
		color: var(--brandGray90);
		cursor: pointer;
		border-radius: 4px;
		opacity: 0.6;
		transition: opacity 0.15s;
	}
	.toggle-btn.active {
		opacity: 1;
		border-color: var(--brandMedBlue);
		color: var(--brandMedBlue);
		font-family: OpenSansBold, sans-serif;
	}
	.toggle-btn:hover { opacity: 1; }

	.inline-filter {
		display: flex;
		align-items: center;
		gap: 8px;
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
	}
	.inline-filter select {
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
		border-radius: 4px;
		padding: 3px 6px;
	}

	.stepwise-note {
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray70);
		margin-bottom: 12px;
	}

	.step-coef-header {
		font-family: OpenSansBold, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
		margin: 20px 0 8px 0;
		display: flex;
		align-items: baseline;
		gap: 12px;
	}
	.step-r2 {
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray70);
	}

	.stats {
		display: flex;
		gap: 16px;
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandGray90);
		margin-bottom: 18px;
	}

	.table-shell { max-width: 680px; margin: 0 auto 20px auto; overflow-x: auto; }

	table { width: 100%; border-collapse: collapse; font-family: OpenSans, sans-serif; font-size: 12px; color: var(--brandGray90); }
	th, td { padding: 6px 10px; border: 1px solid rgba(30,55,101,0.2); text-align: left; }
	th { font-family: OpenSansBold, sans-serif; }
	tr:first-child th { border-top: none; }
	tr:last-child td { border-bottom: none; }
	th:first-child, td:first-child { border-left: none; }
	th:last-child, td:last-child { border-right: none; }

	tr.negative { color: var(--brandRed); font-family: OpenSansBold, sans-serif; }
	tr.positive { color: var(--brandMedBlue); font-family: OpenSansBold, sans-serif; }
	tr.insignificant { opacity: 0.5; }
	tr.negative td:first-child, tr.positive td:first-child,
	tr.negative td:last-child,  tr.positive td:last-child {
		color: var(--brandGray90); font-family: OpenSans, sans-serif;
	}
	tr.step-active { background: rgba(0,127,163,0.08); }
	tr.industry-row td:first-child { padding-left: 18px; }

	.loading-note { padding: 20px 0; display: flex; align-items: center; justify-content: center; font-family: OpenSans, sans-serif; color: var(--brandGray90); }
	.chart-shell { max-width: 700px; margin: 0 auto; position: relative; }
	.chart { width: 100%; }
	.ref-line { stroke: rgba(30,55,101,0.4); stroke-width: 1.2; stroke-dasharray: 5 4; }
	.axis-line { stroke: rgba(30,55,101,0.45); stroke-width: 1; }
	.axis-tick { stroke: rgba(30,55,101,0.5); stroke-width: 1; }
	.axis-label { fill: var(--brandGray90); font-size: 11px; font-family: OpenSans, sans-serif; }
	.axis-title { fill: var(--brandGray90); font-size: 13px; font-family: OpenSansBold, sans-serif; }
	.tooltip { background: rgba(255,255,255,0.95); border: 1px solid rgba(30,55,101,0.2); border-radius: 6px; padding: 8px 10px; font-family: OpenSans, sans-serif; font-size: 12px; color: var(--brandGray90); }
	.tooltip-title { font-family: OpenSansBold, sans-serif; margin-bottom: 4px; }
</style>
