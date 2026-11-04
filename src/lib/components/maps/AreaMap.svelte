<!--
	AreaMap: the shared engine behind the tariff maps.

	The parent owns all UI state and passes it down as one `view` object:
	    { geo, mode: 'fill' | 'circle', column, breaks, colours, sizes }
	Everything the map shows is derived from `view` in a single render(), which
	re-runs whenever `view` or the loaded data changes. There are no other code
	paths that touch layers, so the UI and the map can't drift apart.

	Design rules (each fixes a bug in the old maps):
	  - Layers are added once on load; switching only flips visibility + paint.
	  - Readiness is a flag we set ourselves (mapReady), never isStyleLoaded(),
	    which is false whenever any tile is in flight and made toggles get dropped.
	  - Values come from the per-geography lookup (areaData.js), not from tile
	    attributes. Fill colours (feature-state), circles (our own GeoJSON) and
	    the tooltip all read that same lookup, so they always agree.
	  - Only the active geography's layers are visible, so the hidden one
	    doesn't load tiles.
	  - Hover is read in one rAF-throttled handler that looks at the *current*
	    view each time, and is cleared on every render.
-->
<script module>
	let pmtilesRegistered = false;
</script>

<script>
	import 'maplibre-gl/dist/maplibre-gl.css';
	import { onMount } from 'svelte';
	import { ANCHORS, INITIAL_VIEW, GLOBE_MAX_ZOOM, baseStyle, addBasemapLayers } from '$lib/maps/basemap.js';
	import { loadAreaData, valueOf } from '$lib/maps/areaData.js';
	import { NO_DATA_COLOUR, fillColour, circleColour, circleRadius, stateValue, propValue } from '$lib/maps/styleExpressions.js';
	import LocationSearch from './LocationSearch.svelte';

	/**
	 * @typedef {Object} Geography
	 * @property {string} tiles         URL of the polygon .pmtiles (geometry + id only)
	 * @property {string} sourceLayer   layer name inside the pmtiles
	 * @property {string} idField       feature id property (e.g. ADADGUID)
	 * @property {string} data          URL of the lookup JSON
	 * @property {object} [linePaint]   paint for the boundary lines
	 */

	let {
		/** @type {Record<string, Geography>} */
		geographies,
		/** @type {{geo: string, mode: 'fill'|'circle', column: string, breaks: number[], colours: string[], sizes?: number[]}} */
		view,
		/** (value|null, view) => string, used by the tooltip */
		format = (v) => (v == null ? 'No data' : String(v)),
		/** Current hover, readable by the parent: { id, name, value } | null */
		hovered = $bindable(null),
		/**
		 * Optional: compute a column that isn't in the lookup file, e.g. a sum of
		 * several columns or a share of employment. (data, column) => values[] | null.
		 * Results are cached on the dataset, and colours, circles and the tooltip
		 * all read the cached array, so they can't disagree.
		 */
		derive = null
	} = $props();

	let container;
	let map;
	let mapReady = $state(false);
	let datasets = $state.raw({}); // geo -> AreaData (raw: large arrays, no deep proxy)
	let loadError = $state(null);
	let tooltip = $state(null); // { x, y, name, text }

	// Plain bookkeeping, not reactive.
	const requested = new Set();
	const fillColumnsApplied = {}; // geo -> Set(column)
	const circleColumnShown = {}; // geo -> column
	let hoverTarget = null; // { source, sourceLayer, id }
	let pendingMouse = null;
	let hoverFrame = 0;

	const isLoading = $derived(!datasets[view.geo] && !loadError);

	const ids = (g) => ({
		areas: `${g}-areas`,
		points: `${g}-points`,
		fill: `${g}-fill`,
		line: `${g}-line`,
		hover: `${g}-hover`,
		circle: `${g}-circle`
	});

	// ---------------------------------------------------------------- data

	function requestData(geo) {
		if (requested.has(geo)) return;
		requested.add(geo);
		loadAreaData(geographies[geo].data)
			.then((d) => (datasets = { ...datasets, [geo]: d }))
			.catch((err) => {
				requested.delete(geo);
				loadError = `Couldn't load map data (${err.message}).`;
			});
	}

	/** Values for a column: from the lookup file, or computed once via `derive`. */
	function columnValues(data, column) {
		if (!data.cols[column] && derive) {
			const values = derive(data, column);
			if (values) data.cols[column] = values;
		}
		return data.cols[column];
	}

	function applyFillColumn(geo, data, column) {
		const applied = (fillColumnsApplied[geo] ??= new Set());
		if (applied.has(column)) return;
		const values = columnValues(data, column);
		if (!values) return console.warn(`[AreaMap] no column ${column} for ${geo}`);
		const target = { source: ids(geo).areas, sourceLayer: geographies[geo].sourceLayer };
		for (let i = 0; i < data.ids.length; i++) {
			if (values[i] != null) map.setFeatureState({ ...target, id: data.ids[i] }, { [column]: values[i] });
		}
		applied.add(column);
	}

	function showCircleColumn(geo, data, column) {
		if (circleColumnShown[geo] === column) return;
		const values = columnValues(data, column);
		if (!values) return console.warn(`[AreaMap] no column ${column} for ${geo}`);
		// Only positive values get a circle; ascending order draws big ones on top.
		const rows = [];
		for (let i = 0; i < data.ids.length; i++) {
			if (values[i] > 0 && data.point(i)) rows.push(i);
		}
		rows.sort((a, b) => values[a] - values[b]);
		map.getSource(ids(geo).points).setData({
			type: 'FeatureCollection',
			features: rows.map((i) => ({
				type: 'Feature',
				properties: { id: data.ids[i], v: values[i] },
				geometry: { type: 'Point', coordinates: data.point(i) }
			}))
		});
		circleColumnShown[geo] = column;
	}

	// ---------------------------------------------------------------- render

	function setVisible(layerId, visible) {
		const next = visible ? 'visible' : 'none';
		if (map.getLayoutProperty(layerId, 'visibility') !== next) {
			map.setLayoutProperty(layerId, 'visibility', next);
		}
	}

	function render() {
		const { geo, mode, column, breaks, colours, sizes } = view;
		if (!mapReady) return;

		const data = datasets[geo];
		if (!data) requestData(geo);

		for (const g of Object.keys(geographies)) {
			const L = ids(g);
			const active = g === geo;
			setVisible(L.line, active);
			setVisible(L.hover, active);
			// Data layers only show once their values are in, so a loading
			// geography never flashes as all-grey "no data".
			setVisible(L.fill, active && mode === 'fill' && !!data);
			setVisible(L.circle, active && mode === 'circle' && !!data);
		}
		clearHover();
		if (!data) return;

		const L = ids(geo);
		if (mode === 'fill') {
			applyFillColumn(geo, data, column);
			map.setPaintProperty(L.fill, 'fill-color', fillColour(stateValue(column), breaks, colours));
		} else {
			showCircleColumn(geo, data, column);
			const colour = circleColour(propValue(), breaks, colours);
			map.setPaintProperty(L.circle, 'circle-color', colour);
			map.setPaintProperty(L.circle, 'circle-stroke-color', colour);
			map.setPaintProperty(L.circle, 'circle-radius', circleRadius(propValue(), breaks, sizes));
		}
	}

	$effect(render);

	// ---------------------------------------------------------------- hover

	function clearHover() {
		if (hoverTarget) map?.setFeatureState(hoverTarget, { hover: false });
		hoverTarget = null;
		tooltip = null;
		hovered = null;
	}

	function processHover() {
		hoverFrame = 0;
		const e = pendingMouse;
		const { geo, mode, column } = view;
		const data = datasets[geo];
		const L = ids(geo);
		const layer = mode === 'fill' ? L.fill : L.circle;
		if (!e || !data || map.getLayoutProperty(layer, 'visibility') !== 'visible') return clearHover();

		const feature = map.queryRenderedFeatures(e.point, { layers: [layer] })[0];
		if (!feature) return clearHover();
		const id = mode === 'fill' ? feature.id : feature.properties.id;

		const target = { source: L.areas, sourceLayer: geographies[geo].sourceLayer, id };
		if (hoverTarget?.id !== id || hoverTarget?.source !== target.source) {
			if (hoverTarget) map.setFeatureState(hoverTarget, { hover: false });
			map.setFeatureState(target, { hover: true });
			hoverTarget = target;
		}

		const i = data.index.get(id);
		columnValues(data, column);
		const value = valueOf(data, id, column);
		const name = i === undefined ? null : (data.names?.[i] ?? null);
		hovered = { id, name, value };
		tooltip = { x: e.point.x, y: e.point.y, name, text: format(value, view), flip: e.point.x > container.clientWidth - 200 };
	}

	// ---------------------------------------------------------------- setup

	function addDataLayers() {
		for (const [g, cfg] of Object.entries(geographies)) {
			const L = ids(g);
			const src = { source: L.areas, 'source-layer': cfg.sourceLayer };
			map.addSource(L.areas, {
				type: 'vector',
				url: `pmtiles://${cfg.tiles}`,
				promoteId: { [cfg.sourceLayer]: cfg.idField }
			});
			map.addSource(L.points, { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });

			const hidden = { visibility: 'none' };
			map.addLayer({ id: L.fill, type: 'fill', ...src, layout: hidden, paint: { 'fill-color': NO_DATA_COLOUR, 'fill-opacity': 0.8 } }, ANCHORS.fills);
			map.addLayer({ id: L.line, type: 'line', ...src, layout: hidden, paint: cfg.linePaint ?? { 'line-color': '#808080', 'line-width': 1, 'line-opacity': 0.2 } }, ANCHORS.lines);
			map.addLayer(
				{
					id: L.hover, type: 'fill', ...src, layout: hidden,
					paint: { 'fill-color': '#1E3765', 'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], 0.5, 0] }
				},
				ANCHORS.lines
			);
			map.addLayer(
				{
					id: L.circle, type: 'circle', source: L.points, layout: hidden, maxzoom: 12,
					paint: { 'circle-opacity': 0.5, 'circle-stroke-width': 1, 'circle-stroke-opacity': 0.75 }
				},
				ANCHORS.circles
			);
		}
	}

	export function flyTo(lon, lat, zoom = 11) {
		map?.flyTo({ center: [lon, lat], zoom, speed: 2, curve: 1, essential: true });
	}

	onMount(() => {
		let destroyed = false;
		requestData(view.geo); // start fetching values while the map boots

		(async () => {
			const [{ default: maplibregl }, { Protocol }] = await Promise.all([import('maplibre-gl'), import('pmtiles')]);
			if (destroyed) return;
			if (!pmtilesRegistered) {
				maplibregl.addProtocol('pmtiles', new Protocol().tile);
				pmtilesRegistered = true;
			}

			map = new maplibregl.Map({
				container,
				style: baseStyle(),
				...INITIAL_VIEW,
				attributionControl: { compact: true, customAttribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors' }
			});
			map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'bottom-left');

			// Globe when zoomed out, flat when zoomed in. Only touch the
			// projection when crossing the threshold, not on every zoom tick.
			let globe = null;
			const syncProjection = () => {
				const want = map.getZoom() < GLOBE_MAX_ZOOM;
				if (want !== globe) {
					globe = want;
					map.setProjection({ type: want ? 'globe' : 'mercator' });
				}
			};
			map.on('style.load', () => {
				globe = null;
				syncProjection();
			});
			map.on('zoom', syncProjection);

			map.on('load', () => {
				addBasemapLayers(map);
				addDataLayers();

				map.on('mousemove', (e) => {
					pendingMouse = e;
					if (!hoverFrame) hoverFrame = requestAnimationFrame(processHover);
				});
				map.on('mouseout', () => {
					pendingMouse = null;
					clearHover();
				});
				// Once the first view has settled, warm the other geographies so
				// switching to them is instant.
				map.once('idle', () => Object.keys(geographies).forEach(requestData));

				mapReady = true;
				if (import.meta.env.DEV) window.__areaMap = { map, datasets: () => datasets, view: () => view };
			});
		})();

		return () => {
			destroyed = true;
			cancelAnimationFrame(hoverFrame);
			map?.remove();
		};
	});
</script>

<div class="area-map">
	<div class="canvas" bind:this={container}></div>

	<div class="search">
		<LocationSearch onselect={(lon, lat) => flyTo(lon, lat)} />
	</div>

	{#if isLoading}
		<div class="status">Loading map data…</div>
	{:else if loadError}
		<div class="status error">{loadError}</div>
	{/if}

	{#if tooltip}
		<div class="tooltip" class:flip={tooltip.flip} style="left: {tooltip.x}px; top: {tooltip.y}px;">
			{#if tooltip.name}<span class="name">{tooltip.name}</span>{/if}
			<span>{tooltip.text}</span>
		</div>
	{/if}
</div>

<style>
	.area-map {
		position: relative;
		width: 100%;
		height: 100%;
	}

	.canvas {
		position: absolute;
		inset: 0;
	}

	.search {
		position: absolute;
		top: 10px;
		left: 10px;
		z-index: 2;
	}

	.status {
		position: absolute;
		top: 10px;
		left: 50%;
		transform: translateX(-50%);
		z-index: 2;
		padding: 4px 10px;
		border-radius: 4px;
		background: rgba(255, 255, 255, 0.9);
		border: 1px solid var(--brandGray);
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		color: var(--brandGray80);
	}

	.status.error {
		border-color: var(--brandRed);
		color: var(--brandRed);
	}

	.tooltip {
		position: absolute;
		z-index: 3;
		pointer-events: none;
		transform: translate(12px, 12px);
		display: flex;
		flex-direction: column;
		gap: 1px;
		max-width: 220px;
		padding: 3px 7px;
		border-radius: 4px;
		background-color: var(--brandGray80);
		color: var(--brandWhite);
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
		font-family: OpenSans, sans-serif;
		font-size: 12px;
		line-height: 16px;
	}

	.tooltip.flip {
		transform: translate(calc(-100% - 12px), 12px);
	}

	.tooltip .name {
		font-family: OpenSansBold, sans-serif;
	}
</style>
