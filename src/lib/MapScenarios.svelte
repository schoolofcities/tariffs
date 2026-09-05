<script>
	// (as of September 1, 2025)
	import logoBlueColour from '../assets/sofc-uoft-logo-blue-colour.svg';
	import "../assets/global-styles.css";

	import { onMount } from "svelte";

	import maplibregl from "maplibre-gl";
	import "maplibre-gl/dist/maplibre-gl.css";
	import * as pmtiles from "pmtiles";
	import Select from "svelte-select";

	const protocol = new pmtiles.Protocol();
	maplibregl.addProtocol('pmtiles', protocol.tile);

	let map;

	let addressQuery = "";
	let addressResults = "";

	// ------------------------------------------------------------------
	// PMTILES SOURCES – update paths to your actual files
	// ------------------------------------------------------------------
	let choropleth_csd   = "/pmtiles/all_scenarios_csd.pmtiles";
	let centroids_csd    = "/pmtiles/all_scenarios_csd_centroids.pmtiles";
	let choropleth_ada   = "/pmtiles/all_scenarios_ada.pmtiles";
	let centroids_ada    = "/pmtiles/all_scenarios_ada_centroids.pmtiles";
	let censusDivisions  = "/pmtiles/census-divisions.pmtiles";

	// Scenario-independent denominator for Percent mode: total employment per
	// geography. Lives in small side CSVs (not the tiles) since it never changes
	// by scenario/effect. Loaded once, joined to tiles via setFeatureState so the
	// paint expression can divide by it. One lookup per geography.
	const CSD_TOTAL_EMP_CSV = "/csv/csd_total_emp.csv";
	const ADA_TOTAL_EMP_CSV = "/csv/ada_total_emp.csv";
	let csdTotalEmp = {};        // { CSDDGUID: totalEmployment }
	let adaTotalEmp = {};        // { ADADGUID: totalEmployment }
	let empLoaded = false;

	// Source-layer names INSIDE the pmtiles (must match tippecanoe --layer=).
	const POLY_LAYER     = 'all_scenarios_csd';
	const CENTROID_LAYER = 'all_scenarios_csd_centroids';
	const POLY_LAYER_ADA     = 'all_scenarios_ada';
	const CENTROID_LAYER_ADA = 'all_scenarios_ada_centroids';

	// Per-geography config so updateMap/hover stay geography-agnostic: they read
	// GEO[geoType] instead of hardcoding CSD names/ids.
	const GEO = {
		CSD: {
			polySource: 'choropleth_csd', centSource: 'centroids_csd',
			polyLayer: 'polygons_csd', centLayer: 'centroids_csd',
			polySrcLayer: POLY_LAYER, centSrcLayer: CENTROID_LAYER,
			guid: 'CSDDGUID', hover: 'outline-hover-csd',
			totals: () => csdTotalEmp,
		},
		ADA: {
			polySource: 'choropleth_ada', centSource: 'centroids_ada',
			polyLayer: 'polygons_ada', centLayer: 'centroids_ada',
			polySrcLayer: POLY_LAYER_ADA, centSrcLayer: CENTROID_LAYER_ADA,
			guid: 'ADADGUID', hover: 'outline-hover-ada',
			totals: () => adaTotalEmp,
		},
	};

	// ------------------------------------------------------------------
	// CONSTANTS & BREAKS
	// ------------------------------------------------------------------
	const graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];
	const graduated_siz = [5, 9, 15, 24, 34];
	
	const EFFECT_SUFFIX = {
		Direct:   '_DIR_Jobs',
		Indirect: '_INDIR_Jobs',
		Induced:  '_INDCD_Jobs'
	};

	const PERCENT_BREAKS = [1, 3, 5, 7];
	// Household Consumption (1) and Aggregate Exports (2)
	const PERCENT_BREAKS_BROAD = [1, 3, 5, 7];
	// Scenario 4
	const PERCENT_BREAKS_S4 = [0.1, 0.5, 1, 2];

	const PERCENT_BREAKS_BY_SCENARIO = {
		1: PERCENT_BREAKS_BROAD,
		2: PERCENT_BREAKS_BROAD,
		4: PERCENT_BREAKS_S4,
	};
	// Count mode is absolute jobs. Most CSDs lose very little; the auto/metal
	// towns carry the tail. These are a starting point -- retune from the
	// quantile command against all_scenarios_csd.csv if bands look lopsided.
	const COUNT_BREAKS   = [5, 25, 500, 2000];

	let metricType = "Percent";
	function metricSelect(value) {
		metricType = value;
	}

	// Geographic unit toggle: "CSD" or "ADA".
	let geoType = "CSD";
	function geoTypeSelect(value) {
		geoType = value;
	}


	// ============================================================
	// SCENARIO CONFIG
	// ============================================================
	const scenarios = [
		{ id: 1, code: 'DFD1_HHLD_CON', label: 'Household Consumption', description: 'Overall household consumption expenditures in Canada decline by 1%. <a href="https://www.scotiabank.com/ca/en/about/economics/economics-publications/post.other-publications.insights-views.cusma-scenario-note--march-5--2026-.html", target = "_blank">Scotiobank Economics</a> and the <a href="https://www.bankofcanada.ca/wp-content/uploads/2025/01/mpr-2025-01-29.pdf">Bank of Canada</a> have given their projections of consumption decline, ranging from 0.5% to 2% of GDP consumption in Canada due to the tariffs.' },
		{ id: 3, code: 'DFD3_AG_AF_SF', label: 'Agri-food & Seafood', description: 'Agriculture, agri-food, and seafood exports to the U.S. decline. Although not as directly affected, analysis from <a href="https://www.agri-pulse.com/articles/23170-analysis-chttps://www.rbc.com/en/economics/canadian-analysis/featured-analysis/insights/tracking-the-impact-of-u-s-tariffs-on-five-targeted-canadian-industries/hecking-in-on-us-canada-agricultural-trade">Agri-Pulse</a> and <a href="https://retail-insider.com/retail-insider/opinion/2025/08/canadas-agri-food-sector-hit-by-35-u-s-tariff-after-ottawa-stalls/">Retail Insider</a> show significant declines in this sector in terms of agri-food exports' },
		{ id: 4, code: 'DFD4_ST_AL', label: 'Steel & Aluminum', description: 'Steel and aluminum manufacturing exports to the U.S. decline. The <a href="https://fao-on.org/en/report/impacts-of-us-tariffs/">Financial Accountability Office (FAO) of Ontario</a> reported a potential 137,900 job decrease in Ontario by 2029 under the April 2025 tariff scenario.' },
		{ id: 5, code: 'DFD5_FOR', label: 'Softwood Lumber', description: 'Softwood lumber exports to the U.S. decline. The softwood lumber tariffs have affected the industry drastically, leading to declining lumber production and exports as noted by a report from the <a href="https://www.rbc.com/en/economics/canadian-analysis/featured-analysis/insights/tracking-the-impact-of-u-s-tariffs-on-five-targeted-canadian-industries/">Royal Bank of Canada</a> and our <a href="https://mappingtariffs.org/lumber">softwood lumber blog</a>.' },
		{ id: 6, code: 'DFD6_VEH_PTS', label: 'Autos & Parts', description: 'Automobile and auto-parts exports to the U.S. decline. The FAO noted a potential 20% decrease in U.S. motor vehicles exports and a 30% decrease for motor parts by 2029.' }
	];

	let selectedScenario = 1;
	function scenarioSelect(event) {
		selectedScenario = event.detail.value;
	}
	const scenarioSelectList = scenarios.map((s) => ({ value: s.id, label: s.label }));

	// ============================================================
	// EFFECT CONFIG
	// ============================================================
	const effectOptions = [
		{ id: 'Direct', label: 'Direct', dataAvailable: true },
		{ id: 'Indirect', label: 'Indirect', dataAvailable: true },
		{ id: 'Induced', label: 'Induced', dataAvailable: true }
	];

	let selectedEffects = ['Direct'];

	function toggleEffect(effectId) {
		if (selectedEffects.includes(effectId)) {
			selectedEffects = selectedEffects.filter((e) => e !== effectId);
		} else {
			selectedEffects = [...selectedEffects, effectId];
		}
	}

	// ============================================================
	// DENOMINATOR LOADING (total employment per geography, for Percent mode)
	// ============================================================
	// async function loadTotalEmployment() {
	// 	const parseCsv = (text, into) => {
	// 		const lines = text.trim().split(/\r?\n/);
	// 		for (let i = 1; i < lines.length; i++) {   // skip header
	// 			const [guid, emp] = lines[i].split(',');
	// 			const v = Number(emp);
	// 			if (guid && Number.isFinite(v)) into[guid] = v;
	// 		}
	// 	};
	// 	const [csdText, adaText] = await Promise.all([
	// 		fetch(CSD_TOTAL_EMP_CSV).then(r => r.text()),
	// 		fetch(ADA_TOTAL_EMP_CSV).then(r => r.text()),
	// 	]);
	// 	parseCsv(csdText, csdTotalEmp);
	// 	parseCsv(adaText, adaTotalEmp);
	// 	empLoaded = true;
	// 	console.log(`[emp] loaded CSD ${Object.keys(csdTotalEmp).length}, ADA ${Object.keys(adaTotalEmp).length}`);
	// }

	async function loadTotalEmployment() {
		console.log('[emp] loadTotalEmployment STARTED');   // critical log
		try {
			const csdResponse = await fetch(CSD_TOTAL_EMP_CSV);
			if (!csdResponse.ok) throw new Error(`CSD CSV status ${csdResponse.status}`);
			const csdText = await csdResponse.text();
			console.log('[emp] CSD CSV length:', csdText.length);

			const adaResponse = await fetch(ADA_TOTAL_EMP_CSV);
			if (!adaResponse.ok) throw new Error(`ADA CSV status ${adaResponse.status}`);
			const adaText = await adaResponse.text();
			console.log('[emp] ADA CSV length:', adaText.length);

			const parseCsv = (text, into) => {
				const lines = text.trim().split(/\r?\n/);
				for (let i = 1; i < lines.length; i++) {
					const [guid, emp] = lines[i].split(',');
					const v = Number(emp);
					if (guid && Number.isFinite(v)) into[guid] = v;
				}
			};
			parseCsv(csdText, csdTotalEmp);
			parseCsv(adaText, adaTotalEmp);
			empLoaded = true;
			console.log(`[emp] loaded: CSD ${Object.keys(csdTotalEmp).length}, ADA ${Object.keys(adaTotalEmp).length}`);
		} catch (err) {
			console.error('[emp] FAILED to load CSVs:', err);
		}
	}

	// Push total employment into a geography's sources as feature-state, so paint
	// expressions can read ['feature-state','totalEmp']. Applies to both
	// geographies' sources when present. Safe to call repeatedly.
	function applyEmploymentState() {
		console.log('[emp] applyEmploymentState called', {
			empLoaded,
			hasMap: !!map,
			hasStyle: !!(map && map.style)
		});

		if (!empLoaded || !map || !map.style) {
			console.log('[emp] bailing out – prerequisites missing');
			return;
		}

		for (const key of ['CSD', 'ADA']) {
			const g = GEO[key];
			const polySrc = map.getSource(g.polySource);
			const centSrc = map.getSource(g.centSource);
			if (!polySrc || !centSrc) {
				console.log(`[emp] source missing for ${key} (poly: ${!!polySrc}, cent: ${!!centSrc})`);
				continue;
			}
			const totals = g.totals();
			let count = 0;
			for (const [guid, emp] of Object.entries(totals)) {
				try {
					map.setFeatureState(
						{ source: g.polySource, sourceLayer: g.polySrcLayer, id: guid },
						{ totalEmp: emp }
					);
					map.setFeatureState(
						{ source: g.centSource, sourceLayer: g.centSrcLayer, id: guid },
						{ totalEmp: emp }
					);
					count++;
				} catch (err) {
					console.warn(`[emp] setFeatureState failed for ${guid}:`, err);
				}
			}
			console.log(`[emp] applied totalEmp to ${count} ${key} features`);
		}
	}

	// ============================================================
	// MAIN LAYER LOGIC
	// ============================================================
	function getScenarioLayer(scenarioId, effectIds, metric) {
		const fields = effectIds.map(id => `S${scenarioId}${EFFECT_SUFFIX[id]}`);

		const selectedSumExpr = fields.length === 1
			? ['coalesce', ['get', fields[0]], 0]
			: ['+', ...fields.map(f => ['coalesce', ['get', f], 0])];

		// Absolute loss (values are stored negative = losses).
		const selectedLossAbs = ['abs', selectedSumExpr];

		let valueExpr;
		if (metric === 'Percent') {
			// Percent = jobs lost / total CSD workforce * 100.
			// Denominator comes from feature-state (external CSV), NOT the tile.
			// max(emp,1) guards divide-by-zero for CSDs with 0 / missing workforce.
			const emp = ['to-number', ['feature-state', 'totalEmp']];
			valueExpr = ['*', ['/', selectedLossAbs, ['max', emp, 1]], 100];
		} else {
			// Count mode: absolute jobs lost.
			valueExpr = selectedLossAbs;
		}

		// Guarantee a number (coalesce with 0)
		valueExpr = ['coalesce', valueExpr, 0];

		const allNullExpr = fields.length === 1
			? ['==', ['get', fields[0]], null]
			: ['all', ...fields.map(f => ['==', ['get', f], null])];

		const breaks = metric === 'Percent'
			? (PERCENT_BREAKS_BY_SCENARIO[scenarioId] ?? PERCENT_BREAKS)
			: COUNT_BREAKS;

		const effectLabel = effectIds
			.map(id => effectOptions.find(e => e.id === id)?.label ?? id)
			.join(' + ');
		const scenarioLabel = scenarios.find(s => s.id === scenarioId)?.label ?? '';
		const text = metric === 'Percent'
			? `Estimated share of local workforce affected (${effectLabel}) under Scenario ${scenarioId} (${scenarioLabel})`
			: `Estimated job loss from ${effectLabel} under Scenario ${scenarioId} (${scenarioLabel})`;

		return {
			fields,
			valueExpr,
			allNullExpr,
			metricType: metric,
			breaks,
			colours: graduated_col,
			size: graduated_siz,
			dataAvailable: true,
			text
		};
	}

	$: currentLayer = getScenarioLayer(selectedScenario, selectedEffects, metricType);

	// Helper for hover tooltip
	function getHoverDisplayValue(properties) {
		const fields = currentLayer.fields;
		// Loss is stored negative; take magnitude.
		const selectedLoss = Math.abs(
			fields.reduce((sum, f) => sum + (properties[f] ?? 0), 0)
		);

		if (metricType === 'Percent') {
			
			console.log('[updateMap] Percent mode – checking valueExpr:', currentLayer.valueExpr);
			// share of local workforce = loss / total employment (active geography)
			const g = GEO[geoType];
			const guid = properties[g.guid];
			const totalEmp = g.totals()[guid];
			if (!totalEmp || totalEmp <= 0) return "No data";
			return ((selectedLoss / totalEmp) * 100).toFixed(1) + '%';
		} else {
			if (selectedLoss === 0) return "0 jobs";
			return Math.round(selectedLoss).toLocaleString() + ' jobs';
		}
	}

	// ----------------------------------------
	// UPDATE MAP – with debug logging
	// ----------------------------------------
	function updateMap() {
		const g = GEO[geoType];
		if (
			!(map &&
			  map.isStyleLoaded() &&
			  map.getLayer(g.polyLayer) &&
			  map.getLayer(g.centLayer))
		) {
			return;
		}

		// All data layers across BOTH geographies -- so switching geoType hides
		// the other one.
		const everyDataLayer = [
			GEO.CSD.polyLayer, GEO.CSD.centLayer,
			GEO.ADA.polyLayer, GEO.ADA.centLayer,
		].filter(l => map.getLayer(l));

		if (selectedEffects.length === 0) {
			everyDataLayer.forEach(l => map.setLayoutProperty(l, 'visibility', 'none'));
			return;
		}

		const activePolygonLayer = g.polyLayer;
		const activeCentroidLayer = g.centLayer;

		// Clear hover highlight on the active geography.
		if (map.getLayer(g.hover)) {
			map.setFilter(g.hover, ['==', g.guid, '']);
		}

		if (metricType === "Percent") {
			everyDataLayer.forEach(l => map.setLayoutProperty(l, 'visibility', 'none'));
			map.setLayoutProperty(activePolygonLayer, 'visibility', 'visible');

			map.setPaintProperty(activePolygonLayer, "fill-opacity", 0.8);
			map.setPaintProperty(activePolygonLayer, "fill-color", [
				"case",
				currentLayer.allNullExpr, "#D0D1C9",
				["step", currentLayer.valueExpr,
				currentLayer.colours[0], currentLayer.breaks[0],
				currentLayer.colours[1], currentLayer.breaks[1],
				currentLayer.colours[2], currentLayer.breaks[2],
				currentLayer.colours[3], currentLayer.breaks[3],
				currentLayer.colours[4]],
			]);
		} else { // Count
			everyDataLayer.forEach(l => map.setLayoutProperty(l, 'visibility', 'none'));
			map.setLayoutProperty(activeCentroidLayer, 'visibility', 'visible');

				map.setPaintProperty(activeCentroidLayer, "circle-opacity", 0.5);
				map.setPaintProperty(activeCentroidLayer, "circle-stroke-width", 1);
				map.setPaintProperty(activeCentroidLayer, "circle-stroke-opacity", 0.75);

				const val = currentLayer.valueExpr;

				map.setPaintProperty(activeCentroidLayer, "circle-color", [
					"case",
					currentLayer.allNullExpr, "rgba(0,0,0,0)",
					["<", val, 1], "rgba(0,0,0,0)",
					[">", val, currentLayer.breaks[3]], currentLayer.colours[4],
					[">", val, currentLayer.breaks[2]], currentLayer.colours[3],
					[">", val, currentLayer.breaks[1]], currentLayer.colours[2],
					[">", val, currentLayer.breaks[0]], currentLayer.colours[1],
					currentLayer.colours[0],
				]);

				map.setPaintProperty(activeCentroidLayer, "circle-stroke-color", [
					"case",
					currentLayer.allNullExpr, "rgba(0,0,0,0)",
					["<", val, 1], "rgba(0,0,0,0)",
					[">", val, currentLayer.breaks[3]], currentLayer.colours[4],
					[">", val, currentLayer.breaks[2]], currentLayer.colours[3],
					[">", val, currentLayer.breaks[1]], currentLayer.colours[2],
					[">", val, currentLayer.breaks[0]], currentLayer.colours[1],
					currentLayer.colours[0],
				]);

				// Radius follows the original map's pattern: when ZOOMED OUT
				// (zoom < 8) only the two largest bands (>breaks[2]) render at
				// full size; the small bands (<5, <25) collapse to tiny 0.5-px
				// dots so the map isn't a wall of circles. At ZOOM >= 8 the full
				// five-band sizing kicks in. Sub-1-job (incl. 0) values draw nothing.
				const bigOnly = [
					"case",
					["<", val, 1], 0,
					[">", val, currentLayer.breaks[3]], currentLayer.size[4],
					[">", val, currentLayer.breaks[2]], currentLayer.size[3],
					0.5
				];
				const allBands = [
					"case",
					["<", val, 1], 0,
					[">", val, currentLayer.breaks[3]], currentLayer.size[4],
					[">", val, currentLayer.breaks[2]], currentLayer.size[3],
					[">", val, currentLayer.breaks[1]], currentLayer.size[2],
					[">", val, currentLayer.breaks[0]], currentLayer.size[1],
					currentLayer.size[0],
				];
				map.setPaintProperty(activeCentroidLayer, "circle-radius", [
					"interpolate", ["linear"], ["zoom"],
					3,      bigOnly,
					6.9999, bigOnly,
					7,      allBands,
				]);

				map.setLayoutProperty(
					activeCentroidLayer,
					"circle-sort-key",
					val
				);
			}
	}

	$: {
		currentLayer;
		map;
		geoType;
		updateMap();
	}

	let selectedZone = "";
	let selectedValue = "";
	let lastUpdate = "0";

	// After the function definition
	console.log('[emp] loadTotalEmployment function defined');


	onMount(async () => {

		// Load the Percent-mode denominator in parallel with map init.
		// applyEmploymentState() is called on every tile load once this resolves.
		try {
			console.log('[emp] about to call loadTotalEmployment');
			await loadTotalEmployment();
			console.log('[emp] loadTotalEmployment resolved successfully');
		} catch (err) {
			console.error('[emp] loadTotalEmployment threw an error:', err);
		}

		map = new maplibregl.Map({
			container: "map",
			style: {
				version: 8,
				glyphs: "https://schoolofcities.github.io/fonts/fonts/{fontstack}/{range}.pbf",
				sources: {
					osm: {
						type: 'vector',
						tiles: [
							'https://vector.openstreetmap.org/shortbread_v1/{z}/{x}/{y}.mvt'
						]
					}
				},
				layers: [
					{ id: 'background', type: 'background', paint: { 'background-color': '#fbfbfb' } },
					{ id: 'ocean', type: 'fill', source: 'osm', 'source-layer': 'ocean', paint: { 'fill-color': '#E3F4FB' } }
				]
			},
			center: [-95, 60],
			zoom: 3,
			bearing: 0,
			scrollZoom: true,
			minZoom: 1,
			maxZoom: 11.9,
			pitch: 5,
			projection: "globe",
			attributionControl: false,
		});

		window.debugMap = map;   // add this line

		map.on('load', async () => {

			map.addControl(new maplibregl.NavigationControl({
				visualizePitch: true,
				visualizeRoll: true,
				showZoom: true,
				showCompass: true
			}), 'bottom-left');

			// Add CSD and ADA sources. promoteId makes the GUID the feature id so
			// we can attach external per-geography data (total employment) via
			// setFeatureState for Percent-mode division.
			map.addSource('choropleth_csd',  { type: 'vector', url: 'pmtiles://' + choropleth_csd, promoteId: 'CSDDGUID' });
			map.addSource('centroids_csd',   { type: 'vector', url: 'pmtiles://' + centroids_csd, promoteId: 'CSDDGUID' });
			map.addSource('choropleth_ada',  { type: 'vector', url: 'pmtiles://' + choropleth_ada, promoteId: 'ADADGUID' });
			map.addSource('centroids_ada',   { type: 'vector', url: 'pmtiles://' + centroids_ada, promoteId: 'ADADGUID' });
			map.addSource('censusDivisions', { type: 'vector', url: 'pmtiles://' + censusDivisions });

			// Newly-loaded tiles start with empty feature-state, so re-apply the
			// employment denominator each time any CSD/ADA tile arrives (otherwise
			// Percent mode is blank on fresh tiles).
			const dataSources = new Set(['choropleth_csd', 'centroids_csd', 'choropleth_ada', 'centroids_ada']);
			map.on('data', (e) => {
				if (dataSources.has(e.sourceId) && e.tile) {
					applyEmploymentState();
				}
			});

			map.addSource('ne_water', {
				type: 'geojson',
				data: 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_lakes.geojson'
			});
			map.addSource('ne_provincelines', { type: 'geojson', data: './geojson/province-state-lines.geojson' });
			map.addSource('provincepoints', { type: 'geojson', data: './geojson/province-points.geojson' });
			map.addSource('city_names', { type: 'geojson', data: './geojson/populated-places-canada.geojson' });

			// CSD Polygon layer
			map.addLayer({
				id: 'polygons_csd',
				type: 'fill',
				source: 'choropleth_csd',
				'source-layer': POLY_LAYER,
				'layout': { 'visibility': 'none' }
			});

			// ADA Polygon layer (same slot; visibility toggled by geoType)
			map.addLayer({
				id: 'polygons_ada',
				type: 'fill',
				source: 'choropleth_ada',
				'source-layer': POLY_LAYER_ADA,
				'layout': { 'visibility': 'none' }
			});

			map.addLayer({
				id: 'land',
				type: 'fill',
				source: 'osm',
				'source-layer': 'land',
				'paint': { 'fill-color': 'black', 'fill-opacity': 0.02 }
			});

			map.addLayer({
				id: 'ne_water_fill',
				type: 'fill',
				source: 'ne_water',
				paint: { 'fill-color': '#E3F4FB' },
				minzoom: 0,
				maxzoom: 5
			});

			const CUTOFF = 30000000;
			map.addLayer({
				id: 'water_polygons_large',
				type: 'fill',
				source: 'osm',
				'source-layer': 'water_polygons',
				filter: ['all', ['==', 'kind', 'water'], ['>=', 'way_area', CUTOFF]],
				paint: { 'fill-color': '#E3F4FB' },
				minZoom: 5
			});
			map.addLayer({
				id: 'water_polygons_small',
				type: 'fill',
				source: 'osm',
				'source-layer': 'water_polygons',
				filter: ['all', ['==', 'kind', 'water'], ['<', 'way_area', CUTOFF]],
				paint: { 'fill-color': '#E3F4FB' },
				minzoom: 11
			});

			// CSD outline
			map.addLayer({
				id: 'outline-csd',
				type: 'line',
				source: 'choropleth_csd',
				'source-layer': POLY_LAYER,
				paint: {
					'line-color': '#808080',
					'line-width': ['interpolate', ['linear'], ['zoom'], 4, 0, 17, 3],
					'line-opacity': 0.4
				}
			});

			// ADA outline
			map.addLayer({
				id: 'outline-ada',
				type: 'line',
				source: 'choropleth_ada',
				'source-layer': POLY_LAYER_ADA,
				paint: {
					'line-color': '#808080',
					'line-width': ['interpolate', ['linear'], ['zoom'], 4, 0, 17, 3],
					'line-opacity': 0.4
				}
			});

			// Hover highlight (CSD)
			map.addLayer({
				id: 'outline-hover-csd',
				type: 'fill',
				source: 'choropleth_csd',
				'source-layer': POLY_LAYER,
				paint: { 'fill-color': '#1E3765', 'fill-opacity': 0.5 },
				'filter': ['==', 'CSDDGUID', '']
			});

			// Hover highlight (ADA)
			map.addLayer({
				id: 'outline-hover-ada',
				type: 'fill',
				source: 'choropleth_ada',
				'source-layer': POLY_LAYER_ADA,
				paint: { 'fill-color': '#1E3765', 'fill-opacity': 0.5 },
				'filter': ['==', 'ADADGUID', '']
			});

			map.addLayer({
				id: 'boundaries',
				type: 'line',
				source: 'osm',
				'source-layer': 'boundaries',
				paint: { 'line-color': '#D0D1C9', 'line-width': 1 }
			});
			map.addLayer({
				id: 'province_boundaries_case',
				type: 'line',
				source: 'ne_provincelines',
				paint: { 'line-color': '#ffffff', 'line-width': 3, 'line-opacity': 0.5 },
				maxzoom: 6
			});
			map.addLayer({ 
				id: 'censusDivisions', 
				type: 'line', 
				source: 'censusDivisions', 
				"source-layer": 'censusdivisions', 
				paint: { 
					'line-color': '#4d4d4d', 
					'line-width': 0.5 
				}, 
				minzoom: 6
			});
			map.addLayer({
				id: 'province_boundaries',
				type: 'line',
				source: 'ne_provincelines',
				paint: { 'line-color': '#D0D1C9', 'line-width': 1 },
				maxzoom: 6
			});

			// CSD Centroids
			map.addLayer({
				id: 'centroids_csd',
				type: 'circle',
				source: 'centroids_csd',
				'source-layer': CENTROID_LAYER,
				'layout': { 'visibility': 'none' }
			});

			// ADA Centroids
			map.addLayer({
				id: 'centroids_ada',
				type: 'circle',
				source: 'centroids_ada',
				'source-layer': CENTROID_LAYER_ADA,
				'layout': { 'visibility': 'none' }
			});

			// Label layers (unchanged)
			map.addLayer({
				id: "city_names_big",
				type: "symbol",
				source: "city_names",
				layout: {
					"text-field": ["get", "name"],
					"text-font": ["Open Sans Regular"],
					"text-size": ["interpolate", ["linear"], ["zoom"], 4, 10, 10, 13],
					"text-anchor": "center",
					"symbol-sort-key": ["get", "scalerank"]
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.8
				},
				filter: ["<", ["get", "scalerank"], 5],
				minzoom: 2,
				maxzoom: 6
			});
			map.addLayer({
				id: "city_names_all",
				type: "symbol",
				source: "city_names",
				layout: {
					"text-field": ["get", "name"],
					"text-font": ["Open Sans Regular"],
					"text-size": ["interpolate", ["linear"], ["zoom"], 4, 10, 10, 13],
					"text-anchor": "center",
					"symbol-sort-key": ["get", "scalerank"]
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.8
				},
				minzoom: 6,
				maxzoom: 8
			});
			map.addLayer({
				id: "place_labels_big",
				type: "symbol",
				source: "osm",
				"source-layer": "place_labels",
				layout: {
					"text-field": ["get", "name"],
					"text-font": ["Open Sans Regular"],
					"text-size": ["interpolate", ["linear"], ["zoom"], 4, 10, 10, 13],
					"text-anchor": "center"
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.8
				},
				filter: [
					"any",
					["==", ["get", "kind"], "city"],
					["==", ["get", "kind"], "state_capital"],
					["==", ["get", "kind"], "national capital"]
				],
				minzoom: 8
			});
			map.addLayer({
				id: "place_labels",
				type: "symbol",
				source: "osm",
				"source-layer": "place_labels",
				layout: {
					"text-field": ["get", "name"],
					"text-font": ["Open Sans Regular"],
					"text-size": ["interpolate", ["linear"], ["zoom"], 4, 9, 10, 11],
					"text-anchor": "center"
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.65
				},
				filter: [
					"all",
					["!=", ["get", "kind"], "city"],
					["!=", ["get", "kind"], "state_capital"],
					["!=", ["get", "kind"], "national capital"]
				],
				minzoom: 8
			});
			map.addLayer({
				id: "provincepoints",
				type: "symbol",
				source: "provincepoints",
				layout: {
					"text-field": ["get", "name"],
					"text-font": ["Open Sans Italic"],
					"text-size": ["interpolate", ["linear"], ["zoom"], 4, 14, 10, 16],
					"text-anchor": "center",
					"symbol-sort-key": ["get", "scalerank"]
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.8
				},
				minzoom: 2,
				maxzoom: 6
			});

			map.setLayerZoomRange('centroids_csd', 1, 12);
			map.setLayerZoomRange('centroids_ada', 1, 12);

			// ---- Wait for data and then call updateMap ----
			map.once('idle', () => {
				console.log('[map] idle, calling updateMap');
				updateMap();
			});

			// Also call after a delay in case idle doesn't fire
			setTimeout(() => {
				console.log('[map] timeout fallback, calling updateMap');
				updateMap();
			}, 5000);
		});

		map.on('style.load', () => {
			map.setProjection({ type: (map.getZoom() < 7) ? 'globe' : 'mercator' });
			map.on('zoom', () => {
				const zoom = map.getZoom();
				map.setProjection({ type: (zoom < 7) ? 'globe' : 'mercator' });
			});
		});

		// Hover handlers -- geography-aware via GEO[geoType].
		const handleZoneHover = (e) => {
			const now = performance.now();
			if (now - lastUpdate < 100) return;
			lastUpdate = now;

			map.getCanvas().style.cursor = 'pointer';
			if (!e.features.length) return;

			const g = GEO[geoType];
			const properties = e.features[0].properties;
			const currentZone = properties[g.guid];

			if (currentZone !== selectedZone) {
				selectedValue = getHoverDisplayValue(properties);
				selectedZone = currentZone;
				map.setFilter(g.hover, ['==', g.guid, selectedZone]);
			}
		};

		const handleZoneLeave = () => {
			const g = GEO[geoType];
			map.getCanvas().style.cursor = '';
			selectedZone = "";
			selectedValue = "";
			map.setFilter(g.hover, ['==', g.guid, '']);
		};

		// Bind to both geographies' polygon and centroid layers; the handler
		// reads the active geoType, and only the visible layer receives events.
		for (const lyr of ['polygons_csd', 'polygons_ada', 'centroids_csd', 'centroids_ada']) {
			map.on('mousemove', lyr, handleZoneHover);
			map.on('mouseleave', lyr, handleZoneLeave);
		}

	});

	// Geocoding
	const NOMINATIM_URL = "https://nominatim.openstreetmap.org/search?format=jsonv2&q=";
	const getResults = async () => {
		let inputQuery = addressQuery.endsWith("Canada") || addressQuery.endsWith("CA") || addressQuery.endsWith("Can")
			? addressQuery
			: addressQuery + ", Canada";

		addressResults = await fetch(NOMINATIM_URL + inputQuery).then((res) => res.json());

		if (addressResults.length > 0) {
			const { lat, lon } = addressResults[0];
			map.flyTo({ center: [lon, lat], zoom: 11, bearing: 0, speed: 2, curve: 1, easing(t) { return t; }, essential: true });
		}
	};

	let mouseX = 0;
	let mouseY = 0;

	function handleMouseMove(event) {
		const mapEl = document.getElementById("map");
		const rect = mapEl.getBoundingClientRect();
		let x = event.clientX - rect.left;
		let y = event.clientY - rect.top;

		const tooltipEl = document.getElementById("map-tooltip");
		const tooltipWidth = tooltipEl ? tooltipEl.offsetWidth : 150;
		const tooltipHeight = tooltipEl ? tooltipEl.offsetHeight : 30;

		mouseX = Math.min(x + 10, mapEl.clientWidth - tooltipWidth - 5);
		mouseY = Math.min(y + 10, mapEl.clientHeight - tooltipHeight - 5);
	}

	onMount(() => {
		const mapEl = document.getElementById("map");
		mapEl.addEventListener("mousemove", handleMouseMove);
		return () => mapEl.removeEventListener("mousemove", handleMouseMove);
	});
</script>

<!-- ============================================================ -->
<!-- HTML TEMPLATE – removed ADA toggle and simplified geoType     -->
<!-- ============================================================ -->
<div id="container">

	<div id="panel">

		<div class="logo-container">
			<a href="https://schoolofcities.utoronto.ca/" target="_blank" class="logo-link">
				<img src={logoBlueColour} alt="UofT and School of Cities logos" class="logo" />
			</a>
			<a href="./" target="_blank" class="research-link">Mapping Tariffs</a>
		</div>

		<h2>Mapping job-loss scenarios from U.S. tariffs in Canada</h2>
		<p style="font-size: 14px; margin-top: 25px; line-height: 20px;">
			By <a href="https://www.geography.utoronto.ca/people/directories/all-faculty/richard-difrancesco">Richard DiFrancesco</a>, <a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>, Clara Turner, <a href="https://www.linkedin.com/in/yihoi-jung-0b95351b5/" target="_blank">Yihoi Jung</a>.<br>
			<i>Last updated August 2026.</i>
		</p>

		<div id="select-wrapper">

			<p class = "summary">The following 5 job loss scenarios have been built using a <strong>Multiregional Input-Output model</strong> over Canadian provinces and territories, showing job losses by geographic unit using the model's provincial job losses as a multiplier.</p>
			<div id="destext">
				<p style="margin-bottom: -5px;">Select a scenario:</p>
			</div>
			<Select
				id="scenario-select"
				items={scenarioSelectList}
				value={scenarioSelectList.find((s) => s.value === selectedScenario)}
				clearable={false}
				showChevron={true}
				listAutoWidth={true}
				searchable={false}
				listOffset={10}
				on:change={scenarioSelect}
			/>
			<p class="scenario-description">
				{@html scenarios.find((s) => s.id === selectedScenario)?.description}
			</p>
		</div>

		<div id="destext">
			<p style="margin-bottom: -5px;">Select effects (multiple allowed — combined additively):</p>
		</div>
		<div class="button-group">
			{#each effectOptions as effect}
				<div
					class="toggle-button multiselect {selectedEffects.includes(effect.id) ? 'selected' : ''}"
					on:click={() => toggleEffect(effect.id)}
				>
					<!-- <span class="checkbox">{selectedEffects.includes(effect.id) ? '✓' : ''}</span> -->
					{effect.label}
				</div>
			{/each}
		</div>

		<div id="destext">
			<p style="margin-bottom: -5px;">Choose how to display this indicator:</p>
		</div>
		<div class="button-group">
			<div class="toggle-button {metricType === 'Percent' ? 'selected' : ''}" on:click={() => metricSelect("Percent")}>Percent</div>
			<div class="toggle-button {metricType === 'Count' ? 'selected' : ''}" on:click={() => metricSelect("Count")}>Total</div>
		</div>

		<div id="destext">
			<p style="margin-bottom: -5px;">Geographic unit:</p>
		</div>
		<div class="button-group">
			<div class="toggle-button {geoType === 'ADA' ? 'selected' : ''}" on:click={() => geoTypeSelect("ADA")}>Aggregate dissemination areas</div>
			<div class="toggle-button {geoType === 'CSD' ? 'selected' : ''}" on:click={() => geoTypeSelect("CSD")}>Census subdivisions (municipalities)</div>
		</div>

		<div class="des">
			{#if currentLayer.metricType === "Percent"}
				<div id="destext"><p>{currentLayer.text}</p></div>
				<div id="legend">
					<svg width='500' height='40'>
						<rect class="box" width="64" height="20" x="0" y="0" style="fill:{currentLayer.colours[0]};" />
						<rect class="box" width="64" height="20" x="65" y="0" style="fill:{currentLayer.colours[1]};" />
						<rect class="box" width="64" height="20" x="130" y="0" style="fill:{currentLayer.colours[2]};" />
						<rect class="box" width="64" height="20" x="195" y="0" style="fill:{currentLayer.colours[3]};" />
						<rect class="box" width="64" height="20" x="260" y="0" style="fill:{currentLayer.colours[4]};" />
						<rect class="box" width="64" height="20" x="340" y="0" style="fill:#D0D1C9;" />
						<text class="legend-label" text-anchor="middle" x="65" y="35">&lt;{currentLayer.breaks[0]}%</text>
						<text class="legend-label" text-anchor="middle" x="130" y="35">{currentLayer.breaks[1]}%</text>
						<text class="legend-label" text-anchor="middle" x="195" y="35">{currentLayer.breaks[2]}%</text>
						<text class="legend-label" text-anchor="middle" x="260" y="35">&gt;{currentLayer.breaks[3]}%</text>
						<text class="legend-label" text-anchor="middle" x="370" y="35">no data</text>
					</svg>
				</div>
			{:else if currentLayer.metricType === "Count"}
				<div id="destext"><p>{currentLayer.text}</p></div>
				<div id="legend">
					<svg width='350' height='200'>
						<circle class="box" cx="55" cy="35" r="{currentLayer.size[4]}" fill="{currentLayer.colours[4]}" fill-opacity="0.5" stroke="{currentLayer.colours[4]}" stroke-width="1px" />
						<circle class="box" cx="55" cy="96" r="{currentLayer.size[3]}" fill="{currentLayer.colours[3]}" fill-opacity="0.5" stroke="{currentLayer.colours[3]}" stroke-width="1px" />
						<circle class="box" cx="55" cy="137" r="{currentLayer.size[2]}" fill="{currentLayer.colours[2]}" fill-opacity="0.5" stroke="{currentLayer.colours[2]}" stroke-width="1px" />
						<circle class="box" cx="55" cy="164" r="{currentLayer.size[1]}" fill="{currentLayer.colours[1]}" fill-opacity="0.5" stroke="{currentLayer.colours[1]}" stroke-width="1px" />
						{#if currentLayer.breaks[0] !== 0}
							<circle class="box" cx="55" cy="182" r="{currentLayer.size[0]}" fill="{currentLayer.colours[0]}" fill-opacity="0.5" stroke="{currentLayer.colours[0]}" stroke-width="1px" />
						{/if}
						<text class="legend-label" x="100" y="35" dy="0.35em">&gt;{currentLayer.breaks[3]}</text>
						<text class="legend-label" x="100" y="96" dy="0.35em">{currentLayer.breaks[2] + 1} - {currentLayer.breaks[3]}</text>
						<text class="legend-label" x="100" y="137" dy="0.35em">{currentLayer.breaks[1] + 1} - {currentLayer.breaks[2]}</text>
						<text class="legend-label" x="100" y="160" dy="0.35em">{currentLayer.breaks[0] + 1} - {currentLayer.breaks[1]}</text>
						{#if currentLayer.breaks[0] !== 0}<text class="legend-label" x="100" y="182" dy="0.35em">&le;{currentLayer.breaks[0]}</text>{/if}
					</svg>
				</div>
			{/if}
		</div>

		<div id="hovered-zone">
			<i>Hovered zone</i>: {@html selectedValue ? '<strong>' + selectedValue + '</strong>' : 'No data available'}
		</div>

		<div class="datadetail">
			<p>
				Counts of employment (place of work) are based on estimates from the Canadian Business
				Register (December 2022) for Direct effects. Indirect and Induced effects are modeled
				using a provincial multi-regional input-output model (Statistics Canada Table 36-10-0113-01),
				allocated to this geography.
			</p>

			<h4 style="margin-bottom: 15px;">Data sources</h4>
			<ul>
				<li>Canadian Business Registry (Statistics Canada)</li>
				<li>Canadian Chamber of Commerce</li>
				<li>Canadian Census of Population (Statistics Canada)</li>
				<li>Canadian International Merchandise Trade Web Application (Statistics Canada Catalogue No. 71-607-X2021004)</li>
				<li>Harmonized Tariff Schedule of the United States (United States International Trade Commission)</li>
				<li>Statistics Canada Input-Output Multipliers, Provincial and Territorial, Detail Level (Table 36-10-0113-01)</li>
			</ul>
			<br />
			<br />
		</div>

	</div>

	<div id="map">
		<div id="searchbar">
			<input
				id="address-search"
				bind:value={addressQuery}
				placeholder="Search and fly to a location..."
				on:keydown={(e) => {
					if (e.key === 'Enter' && addressQuery.length > 0) { getResults(); }
				}}
			/>
			<button id="address-button" on:click={getResults} disabled={addressQuery.length < 1}>Search</button>

			{#if selectedValue}
				<div id="map-tooltip" style="top: {mouseY + 10}px; left: {mouseX + 10}px;">
					{selectedValue}
				</div>
			{/if}
		</div>
	</div>

</div>

<style>
	/* (styles unchanged) */
	#container {
		display: flex;
		min-width: 420px;
		flex-wrap: nowrap;
		height: 100dvh;
		overflow: auto;
		overflow-y: hidden;
		position: relative;
	}

	#panel {
		max-width: 450px;
		width: 100%;
		min-width: 350px;
		height: 100%;
		overflow-y: auto;
		background-color: #ffffff;
		padding: 20px;
		border-right: solid 1px var(--brandDarkBlue);
		flex-shrink: 0;
		overflow-x: hidden;
		box-sizing: border-box;
	}

	#map {
		flex: 1;
		height: 100%;
		min-width: 420px;
		overflow: hidden;
		background-color: #ffffff;
		z-index: 0;
		position: relative;
	}

	@media (max-width: 840px) {
		#container { flex-direction: column; }
		#map { order: -1; height: 50vh; border-bottom: solid 1px var(--brandDarkBlue); }
		#panel { max-width: 420px; min-width: 360px; width: 100%; height: 50vh; border-right: none; margin: 0 auto; }
	}

	.logo-container {
		display: flex;
		margin-top: 0px;
		margin-bottom: 40px;
		border-bottom: solid 1px var(--brandGray);
		padding: 0px;
	}

	.logo { width: 200px; height: 50px; padding: 0px; padding-left: 0px; margin-bottom: -5px; }
	.logo:hover { opacity: 0.75; }

	.research-link {
		position: sticky;
		top: 0px;
		padding-top: 18px;
		left: 380px;
		font-family: SourceSerifItalic, serif;
		font-size: 16px;
		text-decoration: underline;
		text-decoration-thickness: 1px;
		color: var(--brandDarkBlue);
	}
	.research-link:hover { color: var(--brandMedGreen); }

	#panel h2 { margin-top: 0px; font-size: 28px; line-height: 36px; }

	#select-wrapper {
		margin-top: 10px;
		border-top: solid 1px var(--brandGray);
		padding-top: 5px;
		margin-bottom: 10px;
		font-family: TradeGothicBold, sans-serif;
		font-size: 16px;
		font-weight: normal;
		color: var(--brandGray90);
	}

	.scenario-description {
		font-family: SourceSerif, sans-serif !important;
		font-size: 13px !important;
		font-weight: normal !important;
		color: var(--brandGray90);
		margin-top: 8px;
		line-height: 1.5; 
	}

	.summary {
		font-family: SourceSerif, sans-serif !important;
		font-size: 13px !important;
		font-weight: normal !important;
		color: var(--brandGray90);
		line-height: 1.5;   /* adjust this value as needed */
	}

	.data-pending-note {
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: #ab1368;
		background-color: #fdf0f6;
		border-radius: 4px;
		padding: 8px 10px;
		margin-top: 8px;
		line-height: 16px;
	}

	.button-group {
		display: flex;
		flex-wrap: wrap;
		margin-right: -10px;
	}

	.toggle-button {
		flex: 1 1 0;
		padding: 6px 12px;
		margin-right: 10px;
		margin-bottom: 8px;
		border: 1px solid var(--brandGray);
		border-radius: 5px;
		cursor: pointer;
		opacity: 0.5;
		background-color: var(--brandWhite);
		color: var(--brandDarkGray);
		user-select: none;
		font-family: TradeGothicBold, sans-serif;
		font-size: 14px;
		font-weight: normal;
		text-align: center;
	}

	.toggle-button.selected {
		opacity: 1.0;
		border: 2px solid var(--brandLightBlue);
	}

	.toggle-button:hover {
		opacity: 1;
		transition: opacity 0.2s ease;
		border: 2px solid var(--brandMedBlue);
	}

	.toggle-button.multiselect {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 6px;
	}

	.checkbox {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 14px;
		height: 14px;
		border: 1.5px solid var(--brandGray);
		border-radius: 3px;
		font-size: 11px;
		flex-shrink: 0;
	}

	.toggle-button.multiselect.selected .checkbox {
		border-color: var(--brandLightBlue);
		background-color: var(--brandLightBlue);
		color: var(--brandWhite);
	}

	#hovered-zone {
		margin-bottom: 10px;
		font-family: SourceSerif, sans-serif;
		font-size: 16px;
		font-weight: normal;
		color: var(--brandGray90);
		padding-top: 5px;
		padding-left: 0px;
		padding-right: 8px;
		padding-bottom: 20px;
		border-bottom: solid 1px var(--brandGray);
	}

	.des { margin-top: 20px; border-top: solid 1px var(--brandGray); }
	#destext { margin-bottom: 10px; margin-left: 0px; }
	#destext p { font-family: SourceSerif; font-size: 16px; line-height: 22px; font-weight: normal; color: var(--brandGray90); }
	.legend-label { font-size: 14px; fill: #000000; font: OpenSans; }

	.datadetail p {
		font-family: SourceSerif;
		font-weight: normal;
		color: var(--brandGray90);
		text-align: left;
		padding-top: 2px;
		padding-bottom: 2px;
		font-size: 14px;
		line-height: 20px;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-rendering: optimizeLegibility;
	}

	.datadetail ul { margin-top: -10px; margin-bottom: -10px; margin-left: -28px; list-style-type: circle; }
	.datadetail li {
		font-family: SourceSerif;
		font-weight: normal;
		color: var(--brandGray90);
		text-align: left;
		padding-top: 2px;
		padding-bottom: 2px;
		font-size: 14px;
		line-height: 18px;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-rendering: optimizeLegibility;
	}

	#searchbar { position: absolute; top: 10px; left: 10px; z-index: 999; }

	#address-search {
		width: 185px;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		border: 1.5px solid var(--brandGray);
		padding: 2px;
		padding-left: 6px;
		border-radius: 4px;
	}

	#address-button {
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		padding: 2px;
		padding-left: 5px;
		padding-right: 5px;
		margin-left: 0px;
		border: 1.5px solid var(--brandGray);
		border-radius: 4px;
		background-color: var(--brandWhite);
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	#address-button:hover:enabled { background-color: var(--brandLightBlue); }
	#address-button:disabled { opacity: 0.5; cursor: not-allowed; }

	#map-tooltip {
		position: absolute;
		background-color: var(--brandGray80);
		color: var(--brandWhite);
		border: 1px solid var(--brandGray);
		padding: 2px 6px;
		font-size: 12px;
		border-radius: 4px;
		pointer-events: none;
		box-shadow: 0 1px 4px rgba(0,0,0,0.3);
		white-space: nowrap;
		z-index: 999;
	}

	a { color: var(--brandBlack); text-decoration: underline; font-family: SourceSerif; }
	a:hover { color: var(--brandMedGreen); }
</style>