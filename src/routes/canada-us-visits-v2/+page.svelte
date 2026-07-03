<script>
	import '../../assets/global-styles.css';
	import Logo from '$lib/LogoTop.svelte';
	import Footer from '$lib/Footer.svelte';
	import { onMount, onDestroy, tick } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import * as XLSX from 'xlsx'; // npm install xlsx
	import Select from "svelte-select";

	// ============================================================
	// SCENARIO CONFIG
	// (from Impact Metrics sheet, MRIO scenario summary workbook)
	// ============================================================
	const scenarios = [
		{
			id: 1,
			code: 'DFD1_HHLD_CON',
			label: 'Household Consumption',
			description: 'Overall household consumption expenditures in Canada decline by 1.9%.'
		},
		{
			id: 2,
			code: 'DFD2_AGG_EXP',
			label: 'Aggregate Exports',
			description: 'Overall domestic exports to the U.S. decline by 4% across the board.'
		},
		{
			id: 3,
			code: 'DFD3_AG_AF_SF',
			label: 'Agri-food & Seafood',
			description: 'Agriculture, agri-food, and seafood exports to the U.S. decline (region-specific weights).'
		},
		{
			id: 4,
			code: 'DFD4_ST_AL',
			label: 'Steel & Aluminum',
			description: 'Steel and aluminum manufacturing exports to the U.S. decline.'
		},
		{
			id: 5,
			code: 'DFD5_FOR',
			label: 'Softwood Lumber',
			description: 'Softwood lumber exports to the U.S. decline.'
		},
		{
			id: 6,
			code: 'DFD6_VEH_PTS',
			label: 'Autos & Parts',
			description: 'Automobile and auto-parts exports to the U.S. decline.'
		}
	];

	// Province abbreviation (as used in the workbook) -> full name
	// (matching the "name" property in the boundary GeoJSON below)
	const abbrevToFullName = {
		NL: 'Newfoundland and Labrador',
		PEI: 'Prince Edward Island',
		NS: 'Nova Scotia',
		NB: 'New Brunswick',
		QC: 'Quebec',
		ON: 'Ontario',
		MB: 'Manitoba',
		SK: 'Saskatchewan',
		AB: 'Alberta',
		BC: 'British Columbia',
		YT: 'Yukon Territory',
		NT: 'Northwest Territories',
		NU: 'Nunavut'
	};

	// Sequential loss-severity palette (light -> dark), consistent with Mapping Tariffs site
	//const colours = ['#f1c500', '#fb921f', '#f3603e', '#d73256', '#ab1368'];
	const noDataColour = '#D0D1C9';
	let graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];
	let graduated_siz = [5, 9, 15, 24, 34];

	

	const xlsxUrl = encodeURI(
		'/csv/scenario summary - clsd MRIO - as of June 21 2026 - 2022 model.xlsx'
	);
	const provinceGeojsonUrl =
		'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/canada.geojson';
	// NOTE: province boundaries pulled from a public GitHub-hosted file for convenience.
	// Consider self-hosting a copy in /geojson for production reliability.

	let selectedScenario = 1;
	$: currentScenario = scenarios[selectedScenario - 1];

	let deltaJobsByFullName = {};
	let canadaTotals = [];
	let dataLoaded = false;
	let loadError = null;

	$: currentTotal = canadaTotals[selectedScenario - 1] ?? null;

	let map;
	let mapContainer;
	let mapLoaded = false;
	let provincesGeojson = null;

	let hoverInfo = null; // { name, value }
	let mouseX = 0;
	let mouseY = 0;

	// ============================================================
	// Parse the "Impact Metrics" sheet out of the MRIO workbook
	// Sheet layout: repeating blocks per province, each block is:
	//   [ID/0, ProvinceLabel, 'Shock', 'Delta-X', 'Delta-VA', 'Delta-Jobs']   <- header row
	//   [1, 'DFD1_HHLD_CON', shock, deltaX, deltaVA, deltaJobs]              <- scenario rows 1-6
	//   ... x6
	// First block's ProvinceLabel is 'Canada' (national totals); skip mapping that one.
	// ============================================================
	function parseImpactMetrics(rows) {
		const byProvince = {}; // abbreviation -> [deltaJobs for scenario 1..6]
		const canada = [];
		let currentLabel = null;

		rows.forEach((row) => {
			if (!row) return;
			if (row[2] === 'Shock') {
				// Start of a new province/Canada block
				currentLabel = row[1];
				return;
			}
			const scenarioId = row[0];
			if (currentLabel && typeof scenarioId === 'number' && scenarioId >= 1 && scenarioId <= 6) {
				const deltaJobs = row[5];
				if (currentLabel === 'Canada') {
					canada[scenarioId - 1] = deltaJobs;
				} else {
					if (!byProvince[currentLabel]) byProvince[currentLabel] = [];
					byProvince[currentLabel][scenarioId - 1] = deltaJobs;
				}
			}
		});

		return { byProvince, canada };
	}

	function computeBreaks(scenarioIdx) {
		const values = Object.values(deltaJobsByFullName)
			.map((arr) => Math.abs(arr[scenarioIdx]))
			.filter((v) => Number.isFinite(v))
			.sort((a, b) => a - b);
		const n = values.length;
		if (n === 0) return [1, 2, 3, 4];
		const pick = (p) => values[Math.min(n - 1, Math.floor(n * p))];
		return [pick(0.2), pick(0.4), pick(0.6), pick(0.8)];
	}

	$: breaks = dataLoaded ? computeBreaks(selectedScenario - 1) : [1, 2, 3, 4];

	function buildFillExpression(scenarioIdx, breaksArr) {
		const prop = `scenario_${scenarioIdx + 1}`;
		return [
			'case',
			['==', ['get', prop], null], noDataColour,
			[
				'step',
				['abs', ['get', prop]],
				colours[0],
				breaksArr[0], colours[1],
				breaksArr[1], colours[2],
				breaksArr[2], colours[3],
				breaksArr[3], colours[4]
			]
		];
	}

	function updateMapColours() {
		if (!map || !mapLoaded || !map.getLayer('provinces-fill')) return;
		map.setPaintProperty('provinces-fill', 'fill-color', buildFillExpression(selectedScenario - 1, breaks));
	}

	$: {
		selectedScenario;
		breaks;
		updateMapColours();
	}

	function handleMouseMove(event) {
		const rect = mapContainer.getBoundingClientRect();
		mouseX = event.clientX - rect.left + 12;
		mouseY = event.clientY - rect.top + 12;
	}

	onMount(async () => {
		try {
			const [xlsxRes, geoRes] = await Promise.all([
				fetch(xlsxUrl),
				fetch(provinceGeojsonUrl)
			]);

			if (!xlsxRes.ok) throw new Error(`Could not load workbook: ${xlsxRes.status}`);
			if (!geoRes.ok) throw new Error(`Could not load province boundaries: ${geoRes.status}`);

			const xlsxBuffer = await xlsxRes.arrayBuffer();
			const workbook = XLSX.read(xlsxBuffer, { type: 'array' });
			const sheet = workbook.Sheets['Impact Metrics'];
			if (!sheet) throw new Error('Sheet "Impact Metrics" not found in workbook');

			const rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: null });
			const { byProvince, canada } = parseImpactMetrics(rows);

			// Re-key by full province name to match the boundary GeoJSON's "name" property
			const byFullName = {};
			Object.entries(byProvince).forEach(([abbrev, arr]) => {
				const fullName = abbrevToFullName[abbrev];
				if (fullName) byFullName[fullName] = arr;
			});

			deltaJobsByFullName = byFullName;
			canadaTotals = canada;

			const rawGeojson = await geoRes.json();
			rawGeojson.features.forEach((f) => {
				const values = deltaJobsByFullName[f.properties.name];
				for (let i = 0; i < scenarios.length; i++) {
					f.properties[`scenario_${i + 1}`] = values ? values[i] : null;
				}
			});
			provincesGeojson = rawGeojson;
			dataLoaded = true;

			// Wait for the {#if dataLoaded} block to render so mapContainer is bound
			await tick();

			if (!mapContainer) {
				loadError = 'Map container failed to render.';
				return;
			}
		} catch (err) {
			console.error('Error loading scenario data:', err);
			loadError = err.message;
			return;
		}

		map = new maplibregl.Map({
			container: mapContainer,
			style: {
				version: 8,
				glyphs: 'https://schoolofcities.github.io/fonts/fonts/{fontstack}/{range}.pbf',
				sources: {
					osm: {
						type: 'vector',
						tiles: ['https://vector.openstreetmap.org/shortbread_v1/{z}/{x}/{y}.mvt']
					}
				},
				layers: [
					{ id: 'background', type: 'background', paint: { 'background-color': '#fbfbfb' } },
					{ id: 'ocean', type: 'fill', source: 'osm', 'source-layer': 'ocean', paint: { 'fill-color': '#E3F4FB' } }
				]
			},
			center: [-95, 60],
			zoom: 2.6,
			minZoom: 2,
			maxZoom: 8,
			pitch: 0,
			bearing: 0,
			projection: 'globe',
			attributionControl: false
		});

		map.dragRotate.disable();
		map.touchZoomRotate.disableRotation();
		map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-left');

		map.on('style.load', () => {
			map.setProjection({ type: (map.getZoom() < 7) ? 'globe' : 'mercator' });
			map.on('zoom', () => {
				map.setProjection({ type: (map.getZoom() < 7) ? 'globe' : 'mercator' });
			});
		});

		map.on('load', () => {
			map.addSource('provinces', { type: 'geojson', data: provincesGeojson });

			map.addLayer({
				id: 'provinces-fill',
				type: 'fill',
				source: 'provinces',
				paint: {
					'fill-color': buildFillExpression(selectedScenario - 1, breaks),
					'fill-opacity': 0.85
				}
			});

			map.addLayer({
				id: 'provinces-outline',
				type: 'line',
				source: 'provinces',
				paint: { 'line-color': '#ffffff', 'line-width': 1 }
			});

			map.addLayer({
				id: 'country_labels',
				type: 'symbol',
				source: 'osm',
				'source-layer': 'boundary_labels',
				filter: ['==', ['get', 'admin_level'], 2],
				layout: {
					'text-field': ['get', 'name'],
					'text-font': ['Open Sans Regular'],
					'text-size': ['interpolate', ['linear'], ['zoom'], 2, 12, 5, 15],
					'text-transform': 'uppercase'
				},
				paint: {
					'text-color': '#999999',
					'text-halo-color': '#ffffff',
					'text-halo-width': 1.5,
					'text-opacity': 0.4
				}
			});

			map.on('mousemove', 'provinces-fill', (e) => {
				map.getCanvas().style.cursor = 'pointer';
				if (!e.features.length) return;
				const props = e.features[0].properties;
				const value = props[`scenario_${selectedScenario}`];
				hoverInfo = {
					name: props.name,
					value: value != null ? Math.round(Math.abs(value)).toLocaleString() : 'No data'
				};
			});

			map.on('mouseleave', 'provinces-fill', () => {
				map.getCanvas().style.cursor = '';
				hoverInfo = null;
			});

			

			mapLoaded = true;
		});
	});

	onDestroy(() => {
		if (map) {
			map.remove();
			map = null;
		}
	});
</script>

<Logo logoType="Blue" backgroundColor="var(--brandWhite)" />

<main>
	<div class="text">
		<h1>Modeled job losses by province under six tariff scenarios</h1>
		<p class="subtitle">
			Total (direct + indirect + induced) estimated employment impact, by province, under six
			Statistics Canada multi-regional input-output shock scenarios.
		</p>
	</div>

	{#if loadError}
		<div class="text">
			<p class="error">Failed to load scenario data: {loadError}</p>
		</div>
	{/if}

	{#if !dataLoaded && !loadError}
		<div class="loading-container">
			<div class="loading-spinner"></div>
			<p class="loading-text">Loading scenario data...</p>
		</div>
	{/if}

	{#if dataLoaded}
		<div class="scenario-panel">
			<h3 class="scenario-title">Scenario {currentScenario.id}: {currentScenario.label}</h3>

			<div class="slider-track">
				<div class="slider-line"></div>
				{#each scenarios as s}
					<button
						class="slider-node {selectedScenario === s.id ? 'active' : ''}"
						on:click={() => (selectedScenario = s.id)}
						aria-label={`Scenario ${s.id}: ${s.label}`}
					>
						{s.id}
					</button>
				{/each}
			</div>

			<p class="scenario-description">{currentScenario.description}</p>
			{#if currentTotal !== null}
				<p class="scenario-total">
					Estimated national job loss under this scenario:
					<strong>{Math.round(Math.abs(currentTotal)).toLocaleString()}</strong>
				</p>
			{/if}
		</div>

		<div class="map-wrapper">
			<div class="map-container" bind:this={mapContainer} on:mousemove={handleMouseMove}></div>

			{#if hoverInfo}
				<div class="map-tooltip" style="top: {mouseY}px; left: {mouseX}px;">
					<strong>{hoverInfo.name}</strong><br />
					{hoverInfo.value} jobs
				</div>
			{/if}

			<div class="legend">
				<span class="legend-title">Estimated jobs lost</span>
				<div class="legend-swatches">
					{#each colours as c, i}
						<div class="legend-item">
							<span class="legend-swatch" style="background-color: {c};"></span>
							<span class="legend-label">
								{#if i === 0}
									&le;{Math.round(breaks[0]).toLocaleString()}
								{:else if i === colours.length - 1}
									&gt;{Math.round(breaks[3]).toLocaleString()}
								{:else}
									{Math.round(breaks[i - 1]).toLocaleString()}&ndash;{Math.round(breaks[i]).toLocaleString()}
								{/if}
							</span>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<div class="text">
			<p class="caption">
				Delta-Jobs values represent the full modeled impact (direct + indirect + induced effects)
				from a provincial multi-regional input-output model, not direct tariff exposure alone.
				Source: Statistics Canada Input-output multipliers, provincial and territorial, detail
				level (Table 36-10-0113-01).
			</p>
		</div>
	{/if}

	<Footer />
</main>

<style>
	main {
		margin: 0 auto;
		width: 100%;
		max-width: 1080px;
	}

	.text {
		max-width: 680px;
		margin: 0 auto;
	}

	h1 {
		font-size: 28px;
		line-height: 36px;
		margin-bottom: 8px;
	}

	.subtitle {
		font-family: OpenSans, sans-serif;
		font-size: 15px;
		color: var(--brandGray90);
		margin-bottom: 30px;
	}

	.error {
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		color: #ab1368;
	}

	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 60px 20px;
		min-height: 200px;
	}

	.loading-spinner {
		width: 50px;
		height: 50px;
		border: 4px solid var(--brandGray90);
		border-top: 4px solid var(--brandLightBlue);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.loading-text {
		margin-top: 15px;
		font-family: OpenSans;
		font-size: 14px;
		color: var(--brandGray90);
	}

	.scenario-panel {
		max-width: 680px;
		margin: 0 auto 30px auto;
		padding: 20px;
		border: 1px solid var(--brandGray);
		border-radius: 8px;
	}

	.scenario-title {
		text-align: center;
		margin-top: 0;
		margin-bottom: 20px;
		font-size: 18px;
	}

	.slider-track {
		position: relative;
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: 0 10px 16px 10px;
		height: 32px;
	}

	.slider-line {
		position: absolute;
		left: 0;
		right: 0;
		top: 50%;
		height: 2px;
		background-color: var(--brandGray);
		transform: translateY(-50%);
		z-index: 0;
	}

	.slider-node {
		position: relative;
		z-index: 1;
		width: 30px;
		height: 30px;
		border-radius: 50%;
		border: 2px solid var(--brandGray);
		background-color: var(--brandWhite);
		color: var(--brandDarkGray);
		font-family: OpenSansBold, sans-serif;
		font-size: 14px;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.15s ease;
	}

	.slider-node:hover {
		border-color: var(--brandMedBlue);
	}

	.slider-node.active {
		background-color: var(--brandDarkBlue);
		border-color: var(--brandDarkBlue);
		color: var(--brandWhite);
		width: 34px;
		height: 34px;
	}

	.scenario-description {
		text-align: center;
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		color: var(--brandGray90);
		margin-bottom: 8px;
	}

	.scenario-total {
		text-align: center;
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		color: var(--brandDarkGray);
	}

	.map-wrapper {
		position: relative;
		max-width: 1080px;
		margin: 0 auto 20px auto;
	}

	.map-container {
		width: 100%;
		height: 600px;
		max-height: 80dvh;
		border: 1px solid var(--brandGray);
		border-radius: 4px;
	}

	.map-tooltip {
		position: absolute;
		background-color: var(--brandGray80);
		color: var(--brandWhite);
		border-radius: 4px;
		padding: 4px 8px;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		pointer-events: none;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
		white-space: nowrap;
		z-index: 999;
	}

	.legend {
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		margin-top: 12px;
		padding: 0 10px;
	}

	.legend-title {
		font-weight: bold;
		color: var(--brandGray90);
	}

	.legend-swatches {
		display: flex;
		flex-wrap: wrap;
		gap: 14px;
		margin-top: 6px;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 6px;
	}

	.legend-swatch {
		width: 14px;
		height: 14px;
		border-radius: 2px;
		flex: 0 0 auto;
	}

	.legend-label {
		color: var(--brandGray90);
	}

	.caption {
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray90);
		line-height: 18px;
		margin-top: 10px;
	}
</style>
