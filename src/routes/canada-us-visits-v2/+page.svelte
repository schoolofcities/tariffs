<Password/>

<script>
	import '../../assets/global-styles.css';
	import Logo from '$lib/LogoTop.svelte';
	import Footer from '$lib/Footer.svelte';
	import { onMount, onDestroy, tick } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import * as pmtiles from 'pmtiles';
	import * as XLSX from 'xlsx'; // npm install xlsx
	import { csvParse } from 'd3-dsv';
	import AuthorDate from '$lib/AuthorDate.svelte';
	import TitleStandard from '$lib/TitleStandard.svelte';
	import Password from '$lib/Password.svelte';

	const protocol = new pmtiles.Protocol();
	maplibregl.addProtocol('pmtiles', protocol.tile);

	// ============================================================
	// SCENARIO CONFIG (from Impact Metrics sheet, MRIO workbook)
	// ============================================================
	const scenarios = [
		{ id: 1, code: 'DFD1_HHLD_CON', label: 'Household Consumption', description: 'Overall household consumption expenditures in Canada decline by 1.9%.' },
		{ id: 2, code: 'DFD2_AGG_EXP', label: 'Aggregate Exports', description: 'Overall domestic exports to the U.S. decline by 4% across the board.' },
		{ id: 3, code: 'DFD3_AG_AF_SF', label: 'Agri-food & Seafood', description: 'Agriculture, agri-food, and seafood exports to the U.S. decline (region-specific weights).' },
		{ id: 4, code: 'DFD4_ST_AL', label: 'Steel & Aluminum', description: 'Steel and aluminum manufacturing exports to the U.S. decline.' },
		{ id: 5, code: 'DFD5_FOR', label: 'Softwood Lumber', description: 'Softwood lumber exports to the U.S. decline.' },
		{ id: 6, code: 'DFD6_VEH_PTS', label: 'Autos & Parts', description: 'Automobile and auto-parts exports to the U.S. decline.' }
	];

	// Province abbreviation (as used in workbook) -> full name (matches GeoJSON "name" property)
	const abbrevToFullName = {
		NL: 'Newfoundland and Labrador', PEI: 'Prince Edward Island', NS: 'Nova Scotia',
		NB: 'New Brunswick', QC: 'Quebec', ON: 'Ontario', MB: 'Manitoba', SK: 'Saskatchewan',
		AB: 'Alberta', BC: 'British Columbia', YT: 'Yukon Territory',
		NT: 'Northwest Territories', NU: 'Nunavut'
	};

	const noDataColour = '#D0D1C9';

	const csdNameCsvUrl = '/csv/csdnames.csv';
	let csdNameByUid = {};

	function parseCsdNames(csvText) {
		const rows = csvParse(csvText.replace(/^\uFEFF/, ''));
		const map = {};
		rows.forEach((r) => {
			if (r.CSDUID) map[r.CSDUID] = r.CSDNAME;
		});
		return map;
	}

	// CSD tariff-exposure choropleth (identical to map.svelte)
	const choropleth_csd = 'pmtiles:///pmtiles/csd_all/choropleth_csd.pmtiles';
	const centroids_csd = 'pmtiles:///pmtiles/csd_all/centroids_csd.pmtiles';
	const censusDivisions = 'pmtiles:///pmtiles/census-divisions.pmtiles';
	const graduated_col = ['#f1c500', '#fb921f', '#f3603e', '#d73256', '#ab1368'];
	const graduated_siz = [5, 9, 15, 24, 34];

	// CSD fill layer, mapped per scenario to the closest matching tariff category.
	// Scenarios 1-3 fall back to "All goods" since no dedicated agriculture category
	// exists in the tariff map, and 1/2 are economy-wide (not sector-specific).
	// Breaks/colours copied from map.svelte's dataLayers config.
	const csdLayersByScenario = {
		1: { dataSource: 'Total_2', breaks: [0.04, 0.1, 0.2, 0.4], colours: graduated_col, categoryLabel: 'All goods' },
		2: { dataSource: 'Total_2', breaks: [0.04, 0.1, 0.2, 0.4], colours: graduated_col, categoryLabel: 'All goods' },
		3: { dataSource: 'Total_2', breaks: [0.04, 0.1, 0.2, 0.4], colours: graduated_col, categoryLabel: 'All goods' },
		4: { dataSource: 'Alum_2', breaks: [0.01, 0.05, 0.1, 0.2], colours: graduated_col, categoryLabel: 'Aluminum' },
		5: { dataSource: 'LumNew_2', breaks: [0.01, 0.05, 0.1, 0.2], colours: graduated_col, categoryLabel: 'Lumber (after Oct 14)' },
		6: { dataSource: 'Auto_2', breaks: [0.01, 0.04, 0.08, 0.2], colours: graduated_col, categoryLabel: 'Automobiles' }
	};

	$: csdLayer = csdLayersByScenario[selectedScenario];

	// Province outline: blue -> dark purple, scaled by modeled indirect job loss
	const blueColours = ['#71CAE3', '#4F98D6', '#3348B5', '#5C41AB', '#510F81'];

	const xlsxUrl = encodeURI('/csv/scenario summary - clsd MRIO - as of June 21 2026 - 2022 model.xlsx');
	const provinceGeojsonUrl = 'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/canada.geojson';
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

	let hoverInfo = null; // { name, value } for CSD hover
	let mouseX = 0;
	let mouseY = 0;

	let pctByFullName = {}; // full province name -> [% of provincial employment at risk, per scenario]
	

	// ============================================================
	// Parse the "Impact Metrics" sheet out of the MRIO workbook.
	// Blocks repeat per province: header row where col C === 'Shock'
	// marks a new block (col B = province abbrev, or 'Canada'),
	// followed by 6 scenario rows (col A = scenario id 1-6, col F = Delta-Jobs).
	// ============================================================
	function parseImpactMetrics(rows) {
		const byProvince = {};
		const canada = [];
		let currentLabel = null;

		rows.forEach((row) => {
			if (!row) return;
			if (row[2] === 'Shock') {
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
		const values = Object.values(pctByFullName)
			.map((arr) => arr[scenarioIdx])
			.filter((v) => Number.isFinite(v))
			.sort((a, b) => a - b);
		const n = values.length;
		if (n === 0) return [0.5, 1, 2, 4];
		const pick = (p) => values[Math.min(n - 1, Math.floor(n * p))];
		return [pick(0.2), pick(0.4), pick(0.6), pick(0.8)];
	}
	
	$: breaks = dataLoaded ? computeBreaks(selectedScenario - 1) : [0.5, 1, 2, 4];

	function buildProvinceOutlineExpression(scenarioIdx, breaksArr) {
		const prop = `scenario_pct_${scenarioIdx + 1}`;
		return [
			'case',
			['==', ['get', prop], null], noDataColour,
			[
				'step',
				['get', prop],
				blueColours[0],
				breaksArr[0], blueColours[1],
				breaksArr[1], blueColours[2],
				breaksArr[2], blueColours[3],
				breaksArr[3], blueColours[4]
			]
		];
	}

	function updateProvinceOutline() {
		if (!map || !mapLoaded || !map.getLayer('provinces-outline')) return;
		map.setPaintProperty('provinces-outline', 'line-color', buildProvinceOutlineExpression(selectedScenario - 1, breaks));
	}

	function updateCsdFill() {
		if (!map || !mapLoaded || !map.getLayer('polygons_csd')) return;
		map.setPaintProperty('polygons_csd', 'fill-color', [
			'case',
			['==', ['get', csdLayer.dataSource], null], noDataColour,
			[
				'step', ['get', csdLayer.dataSource],
				csdLayer.colours[0], csdLayer.breaks[0],
				csdLayer.colours[1], csdLayer.breaks[1],
				csdLayer.colours[2], csdLayer.breaks[2],
				csdLayer.colours[3], csdLayer.breaks[3],
				csdLayer.colours[4]
			]
		]);
	}

	$: {
		selectedScenario;
		breaks;
		updateProvinceOutline();
		updateCsdFill();
	}

	function handleMouseMove(event) {
		const rect = mapContainer.getBoundingClientRect();
		mouseX = event.clientX - rect.left + 12;
		mouseY = event.clientY - rect.top + 12;
	}

	const labourCsvUrl = '/csv/labourtotals.csv';

	// LFS doesn't cover the territories monthly — YT/NT/NU will have no baseline
	const geoToFullName = {
		'Newfoundland and Labrador': 'Newfoundland and Labrador',
		'Prince Edward Island': 'Prince Edward Island',
		'Nova Scotia': 'Nova Scotia',
		'New Brunswick': 'New Brunswick',
		'Quebec': 'Quebec',
		'Ontario': 'Ontario',
		'Manitoba': 'Manitoba',
		'Saskatchewan': 'Saskatchewan',
		'Alberta': 'Alberta',
		'British Columbia': 'British Columbia'
	};

	let employmentByFullName = {}; // full province name -> avg employed persons (actual count)
	let canadaEmployment = null;

	function parseLabourForce(csvText) {
		const rows = csvParse(csvText.replace(/^\uFEFF/, '')); // strip BOM if present
		const byGeo = {}; // geo -> array of monthly Employment estimates (thousands)

		rows.forEach((row) => {
			if (row['Labour force characteristics'] !== 'Employment') return;
			if (row['Statistics'] !== 'Estimate') return;
			const value = parseFloat(row['VALUE']);
			if (!Number.isFinite(value)) return;
			const geo = row['GEO'];
			if (!byGeo[geo]) byGeo[geo] = [];
			byGeo[geo].push(value);
		});

		const avgByGeo = {};
		Object.entries(byGeo).forEach(([geo, values]) => {
			const avgThousands = values.reduce((a, b) => a + b, 0) / values.length;
			avgByGeo[geo] = avgThousands * 1000; // thousands -> actual persons
		});
		return avgByGeo;
	}

	onMount(async () => {
		try {
			const [xlsxRes, geoRes, labourRes, csdNameRes] = await Promise.all([
				fetch(xlsxUrl),
				fetch(provinceGeojsonUrl),
				fetch(labourCsvUrl),
				fetch(csdNameCsvUrl)
			]);
			if (!csdNameRes.ok) throw new Error(`Could not load CSD name lookup: ${csdNameRes.status}`);
			if (!xlsxRes.ok) throw new Error(`Could not load workbook: ${xlsxRes.status}`);
			if (!geoRes.ok) throw new Error(`Could not load province boundaries: ${geoRes.status}`);
			if (!labourRes.ok) throw new Error(`Could not load labour force data: ${labourRes.status}`);

			const xlsxBuffer = await xlsxRes.arrayBuffer();
			const workbook = XLSX.read(xlsxBuffer, { type: 'array' });
			const sheet = workbook.Sheets['Impact Metrics'];
			if (!sheet) throw new Error('Sheet "Impact Metrics" not found in workbook');

			const rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: null });
			const { byProvince, canada } = parseImpactMetrics(rows);

			const csdNameCsvText = await csdNameRes.text();
			csdNameByUid = parseCsdNames(csdNameCsvText);

			const byFullName = {};
			Object.entries(byProvince).forEach(([abbrev, arr]) => {
				const fullName = abbrevToFullName[abbrev];
				if (fullName) byFullName[fullName] = arr;
			});

			deltaJobsByFullName = byFullName;
			canadaTotals = canada;

			// labour totals
			const labourCsvText = await labourRes.text();
			const avgEmploymentByGeo = parseLabourForce(labourCsvText);

			const employmentByFullNameLocal = {};
			Object.entries(geoToFullName).forEach(([geoName, fullName]) => {
				if (avgEmploymentByGeo[geoName] != null) employmentByFullNameLocal[fullName] = avgEmploymentByGeo[geoName];
			});
			employmentByFullName = employmentByFullNameLocal;
			canadaEmployment = avgEmploymentByGeo['Canada'] ?? null;

			const rawGeojson = await geoRes.json();
			const pctByFullNameLocal = {};
			rawGeojson.features.forEach((f) => {
				const values = deltaJobsByFullName[f.properties.name];
				const baseline = employmentByFullName[f.properties.name]; // undefined for territories
				const pcts = [];
				for (let i = 0; i < scenarios.length; i++) {
					f.properties[`scenario_${i + 1}`] = values ? values[i] : null;
					const pct = values && baseline ? (Math.abs(values[i]) / baseline) * 100 : null;
					f.properties[`scenario_pct_${i + 1}`] = pct;
					f.properties[`scenario_pct_label_${i + 1}`] = pct != null ? `${pct.toFixed(2)}%` : 'n/a';
					pcts.push(pct);
				}
				pctByFullNameLocal[f.properties.name] = pcts;
			});
			pctByFullName = pctByFullNameLocal;
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
			maxZoom: 11.9,
			pitch: 0,
			bearing: 0,
			projection: 'globe',
			attributionControl: false
		});

		map.dragRotate.disable();
		map.touchZoomRotate.disableRotation();
		map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-left');

		map.on('style.load', () => {
			map.setProjection({ type: map.getZoom() < 7 ? 'globe' : 'mercator' });
			map.on('zoom', () => {
				map.setProjection({ type: map.getZoom() < 7 ? 'globe' : 'mercator' });
			});
		});

		map.on('load', () => {
			// ---- CSD tariff-exposure choropleth (fill) ----
			map.addSource('choropleth_csd', { type: 'vector', url: choropleth_csd });
			map.addSource('centroids_csd', { type: 'vector', url: centroids_csd });
			map.addSource('censusDivisions', { type: 'vector', url: censusDivisions });

			map.addLayer({
				id: 'polygons_csd',
				type: 'fill',
				source: 'choropleth_csd',
				'source-layer': 'choropleth_csd',
				paint: {
					'fill-opacity': 0.8,
					'fill-color': [
						'case',
						['==', ['get', csdLayer.dataSource], null], noDataColour,
						[
							'step', ['get', csdLayer.dataSource],
							csdLayer.colours[0], csdLayer.breaks[0],
							csdLayer.colours[1], csdLayer.breaks[1],
							csdLayer.colours[2], csdLayer.breaks[2],
							csdLayer.colours[3], csdLayer.breaks[3],
							csdLayer.colours[4]
						]
					]
				}
			});

			map.addLayer({
				id: 'outline-csd',
				type: 'line',
				source: 'choropleth_csd',
				'source-layer': 'choropleth_csd',
				paint: {
					'line-color': '#808080',
					'line-width': ['interpolate', ['linear'], ['zoom'], 4, 0, 17, 3],
					'line-opacity': 0.4
				}
			});

			map.addLayer({
				id: 'censusDivisions',
				type: 'line',
				source: 'censusDivisions',
				'source-layer': 'censusdivisions',
				paint: { 'line-color': '#4d4d4d', 'line-width': 0.5 },
				minzoom: 6
			});

			// ---- Province outline: indirect job loss (white -> blue), on top ----
			map.addSource('provinces', { type: 'geojson', data: provincesGeojson });

			map.addLayer({
				id: 'provinces-hit',
				type: 'fill',
				source: 'provinces',
				paint: { 'fill-opacity': 0 }
			});

			map.addLayer({
				id: 'provinces-outline',
				type: 'line',
				source: 'provinces',
				paint: {
					'line-color': buildProvinceOutlineExpression(selectedScenario - 1, breaks),
					'line-width': 3,
					'line-opacity': 0.9,
					'line-offset': 1.5
				}
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

			// Hover tooltip: CSD name, direct exposure %, province indirect-loss %
			map.on('mousemove', 'polygons_csd', (e) => {
				map.getCanvas().style.cursor = 'pointer';
				if (!e.features.length) return;
				const props = e.features[0].properties;

				// NOTE: verify this matches your actual CSD tile schema —
				// console.log(props) once to confirm the real name field.
				const csduid = props.CSDDGUID ? props.CSDDGUID.slice(-7) : null;
				const csdName = csduid && csdNameByUid[csduid] ? csdNameByUid[csduid] : 'Unknown CSD';

				const value = props[csdLayer.dataSource];
				const directExposure = value != null
					? `${(value * 100).toFixed(1)}% (${csdLayer.categoryLabel})`
					: 'No data';

				const provinceFeatures = map.queryRenderedFeatures(e.point, { layers: ['provinces-hit'] });
				let provincePct = 'No data';
				if (provinceFeatures.length) {
					provincePct = provinceFeatures[0].properties[`scenario_pct_label_${selectedScenario}`] ?? 'No data';
				}

				hoverInfo = { csdName, directExposure, provincePct };
			});

			map.on('mouseleave', 'polygons_csd', () => {
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
	<TitleStandard
		title="Tariff exposure and modeled job losses"
	/>
	<div class="text">
		<AuthorDate
			authors="<a href='https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco' target='_blank'>Rick DiFrancesco</a>, <a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, <a href='https://www.linkedin.com/in/yihoi-jung-0b95351b5/' target='_blank'>Yihoi Jung</a>"
			date="July 2026"
		/>
		<p>

		</p>
		<p>
			The colour of each CSD represents the estimated share of employees (by place of work) directly exposed to U.S. tariffs.
			The province outline depicts job losses under six input-output shock scenarios.
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
					Estimated national <em>job loss</em> under this scenario:
					<strong>{Math.round(Math.abs(currentTotal)).toLocaleString()}</strong>
				</p>
			{/if}
		</div>

		<div class="map-wrapper">
			<div class="map-container" bind:this={mapContainer} on:mousemove={handleMouseMove}></div>

			{#if hoverInfo}
				<div class="map-tooltip" style="top: {mouseY}px; left: {mouseX}px;">
					<strong>{hoverInfo.csdName}</strong><br />
					Direct exposure: {hoverInfo.directExposure}<br />
					Province: {hoverInfo.provincePct} of job loss
				</div>
			{/if}
			<div class="legend">
				<span class="legend-title">Province outline &mdash; % of provincial employment at risk</span>
				<div class="legend-swatches">
					{#each blueColours as c, i}
						<div class="legend-item">
							<span class="legend-swatch" style="background-color: {c};"></span>
							<span class="legend-label">
								{#if i === 0}
									&le;{breaks[0].toFixed(2)}%
								{:else if i === blueColours.length - 1}
									&gt;{breaks[3].toFixed(2)}%
								{:else}
									{breaks[i - 1].toFixed(2)}&ndash;{breaks[i].toFixed(2)}%
								{/if}
							</span>
						</div>
					{/each}
				</div>
			</div>

			<div class="legend">
				<span class="legend-title">CSD fill &mdash; % employees exposed (all tariffs)</span>
				<div class="legend-swatches">
					{#each graduated_col as c, i}
						<div class="legend-item">
							<span class="legend-swatch" style="background-color: {c};"></span>
							<span class="legend-label">
								{#if i === 0}
									&lt;{(csdLayer.breaks[0] * 100).toFixed(0)}%
								{:else if i === graduated_col.length - 1}
									&gt;{(csdLayer.breaks[3] * 100).toFixed(0)}%
								{:else}
									{(csdLayer.breaks[i - 1] * 100).toFixed(0)}&ndash;{(csdLayer.breaks[i] * 100).toFixed(0)}%
								{/if}
							</span>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<div class="text">
			<p class="caption">
				CSD fill: estimated employees directly exposed to U.S. tariffs, based on the Canadian
				Business Register (Dec 2022) and Harmonized Tariff Schedule mapping &mdash; see Mapping
				Tariffs for full methodology. Province outline: modeled indirect + induced job-loss
				impact from a provincial multi-regional input-output model (Statistics Canada Table
				36-10-0113-01), not direct tariff exposure.
			</p>
		</div>
	{/if}

	<Footer />
</main>

<style>
	:global(html), :global(body) {
		height: auto;
		overflow: visible;
	}

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
		background-color: #08519c;
		border-color: #08519c;
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
