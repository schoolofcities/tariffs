<script>
	import { onMount, onDestroy } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';

	export let filteredMetroMetrics = [];
	export let globalMaxNormalized = 0.001;
	export let legendSizeBins = [];

	const negativeColor = '#DC4633';
	const positiveColor = '#007FA3';

	let map;
	let mapContainer;
	let mapLoaded = false;
	let mapClickBound = false;
	let currentPopup = null;

	let usMetroCoords = {};

	const metroNameAliases = {
		"Louisville, KY-IN": "Louisville/Jefferson County, KY-IN"
	};

	function findMetroCoords(metroName) {
		if (usMetroCoords[metroName]) return usMetroCoords[metroName];

		const normalizedMetro = metroName.replace(' Micro Area', '').trim();
		const aliasedMetro = metroNameAliases[normalizedMetro] || normalizedMetro;
		if (usMetroCoords[aliasedMetro]) return usMetroCoords[aliasedMetro];

		const metroStateMatch = aliasedMetro.match(/,\s*([A-Z]{2})/);
		const metroState = metroStateMatch ? metroStateMatch[1] : null;
		const shortName = aliasedMetro.split(',')[0].trim();

		const stateMatched = [];
		for (const [key, coords] of Object.entries(usMetroCoords)) {
			const keyShort = key.split(',')[0].trim();
			if (keyShort !== shortName) continue;
			if (!metroState) {
				stateMatched.push(coords);
				continue;
			}
			const keyStateMatch = key.match(/,\s*([A-Z]{2})(?:-|$)/);
			const keyState = keyStateMatch ? keyStateMatch[1] : null;
			if (keyState === metroState) stateMatched.push(coords);
		}

		if (stateMatched.length === 1) return stateMatched[0];
		if (metroState) return null;

		for (const [key, coords] of Object.entries(usMetroCoords)) {
			if (key.startsWith(shortName + ',')) return coords;
		}

		return null;
	}

	function updateMapData() {
		if (!map || !mapLoaded) return;

		if (map.getLayer('metro-circles')) map.removeLayer('metro-circles');
		if (map.getSource('metros')) map.removeSource('metros');

		if (filteredMetroMetrics.length === 0) return;

		const maxNormalized = globalMaxNormalized;
		const sizeBin1 = maxNormalized * 0.2;
		const sizeBin2 = maxNormalized * 0.4;
		const sizeBin3 = maxNormalized * 0.6;
		const sizeBin4 = maxNormalized * 0.8;

		const geojson = {
			type: 'FeatureCollection',
			features: filteredMetroMetrics
				.filter(m => findMetroCoords(m.metro) !== null)
				.map(m => ({
					type: 'Feature',
					geometry: { type: 'Point', coordinates: findMetroCoords(m.metro) },
					properties: {
						metro: m.metro,
						avg1: m.avg1,
						avg2: m.avg2,
						percentChange: m.percentChange,
						total1: m.total1,
						total2: m.total2
					}
				}))
		};

		map.addSource('metros', { type: 'geojson', data: geojson });

		map.addLayer({
			id: 'metro-circles',
			type: 'circle',
			source: 'metros',
			paint: {
				'circle-radius': [
					'step', ['get', 'avg2'],
					5, sizeBin1, 10, sizeBin2, 20, sizeBin3, 27, sizeBin4, 30
				],
				'circle-color': [
					'interpolate', ['linear'], ['get', 'percentChange'],
					-70, '#DC4633',
					-35, '#EEA298',
					-15, '#F1C500',
					0, '#FFFFFF',
					15, '#A5D5E3',
					30, '#007FA3'
				],
				'circle-opacity': 0.9,
				'circle-stroke-width': 1,
				'circle-stroke-color': '#1E3765'
			}
		});

		if (!mapClickBound) {
			map.on('click', 'metro-circles', (e) => {
				if (currentPopup) currentPopup.remove();

				const props = e.features[0].properties;
				const change = parseFloat(props.percentChange).toFixed(2);
				const changeColor = change >= 0 ? positiveColor : negativeColor;

				currentPopup = new maplibregl.Popup()
					.setLngLat(e.lngLat)
					.setHTML(`
						<div style="color: #333; font-family: Roboto, sans-serif;">
							<strong>${props.metro}</strong><br>
							<span style="color: ${changeColor}; font-weight: bold;">${change >= 0 ? '+' : ''}${change}%</span> YoY change<br>
						</div>
					`)
					.addTo(map);

				currentPopup.on('close', () => { currentPopup = null; });
			});

			map.on('mouseenter', 'metro-circles', () => {
				map.getCanvas().style.cursor = 'pointer';
			});
			map.on('mouseleave', 'metro-circles', () => {
				map.getCanvas().style.cursor = '';
			});
			mapClickBound = true;
		}
	}

	$: if (mapLoaded && filteredMetroMetrics) {
		updateMapData();
	}

	onMount(async () => {
		const coordsRes = await fetch('/geojson/us-metro-coords.geojson');
		const coordsGeoJSON = await coordsRes.json();
		usMetroCoords = Object.fromEntries(
			coordsGeoJSON.features.map(f => [f.properties.name, f.geometry.coordinates])
		);

		map = new maplibregl.Map({
			container: mapContainer,
			style: {
				version: 8,
				glyphs: "https://schoolofcities.github.io/fonts/fonts/{fontstack}/{range}.pbf",
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
			center: [-98, 40],
			zoom: 2.8,
			bearing: 0,
			scrollZoom: true,
			minZoom: 2.3,
			maxZoom: 6,
			pitch: 5,
			projection: "globe",
			attributionControl: false,
		});

		map.on('load', () => {
			map.addControl(new maplibregl.NavigationControl({
				visualizePitch: true,
				visualizeRoll: true,
				showZoom: true,
				showCompass: true
			}), 'bottom-left');

			map.addSource('ne_water', {
				type: 'geojson',
				data: '/geojson/ne_50m_lakes.geojson'
			});

			map.addSource('ne_provincelines', {
				type: 'geojson',
				data: '/geojson/province-state-lines.geojson'
			});

			map.addSource('city_names', {
				type: 'geojson',
				data: '/geojson/populated-places-us.json'
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
				minzoom: 5
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
				paint: { 'line-color': '#ffffff', 'line-width': 3, 'line-opacity': 0.5 }
			});
			map.addLayer({
				id: 'province_boundaries',
				type: 'line',
				source: 'ne_provincelines',
				paint: { 'line-color': '#D0D1C9', 'line-width': 1 }
			});

			map.addLayer({
				id: 'city_names_big',
				type: 'symbol',
				source: 'city_names',
				layout: {
					'text-field': ['get', 'name'],
					'text-font': ['Open Sans Regular'],
					'text-size': ['interpolate', ['linear'], ['zoom'], 4, 10, 10, 13],
					'text-anchor': 'center',
					'symbol-sort-key': ['get', 'scalerank']
				},
				paint: { 'text-color': '#333333', 'text-halo-color': '#fff', 'text-halo-width': 1.5, 'text-opacity': 0.8 },
				filter: ['<', ['get', 'scalerank'], 5],
				minzoom: 2,
				maxzoom: 6
			});

			map.addLayer({
				id: 'city_names_all',
				type: 'symbol',
				source: 'city_names',
				layout: {
					'text-field': ['get', 'name'],
					'text-font': ['Open Sans Regular'],
					'text-size': ['interpolate', ['linear'], ['zoom'], 4, 10, 10, 13],
					'text-anchor': 'center',
					'symbol-sort-key': ['get', 'scalerank']
				},
				paint: { 'text-color': '#333333', 'text-halo-color': '#fff', 'text-halo-width': 1.5, 'text-opacity': 0.8 },
				minzoom: 6,
				maxzoom: 8
			});

			map.addLayer({
				id: 'place_labels_big',
				type: 'symbol',
				source: 'osm',
				'source-layer': 'place_labels',
				layout: {
					'text-field': ['get', 'name'],
					'text-font': ['Open Sans Regular'],
					'text-size': ['interpolate', ['linear'], ['zoom'], 4, 10, 10, 13],
					'text-anchor': 'center'
				},
				paint: { 'text-color': '#333333', 'text-halo-color': '#fff', 'text-halo-width': 1.5, 'text-opacity': 0.8 },
				filter: ['any', ['==', ['get', 'kind'], 'city'], ['==', ['get', 'kind'], 'state_capital'], ['==', ['get', 'kind'], 'national capital']],
				minzoom: 8
			});

			map.addLayer({
				id: 'place_labels',
				type: 'symbol',
				source: 'osm',
				'source-layer': 'place_labels',
				layout: {
					'text-field': ['get', 'name'],
					'text-font': ['Open Sans Regular'],
					'text-size': ['interpolate', ['linear'], ['zoom'], 4, 9, 10, 11],
					'text-anchor': 'center'
				},
				paint: { 'text-color': '#333333', 'text-halo-color': '#fff', 'text-halo-width': 1.5, 'text-opacity': 0.65 },
				filter: ['all', ['!=', ['get', 'kind'], 'city'], ['!=', ['get', 'kind'], 'state_capital'], ['!=', ['get', 'kind'], 'national capital']],
				minzoom: 8
			});

			map.addLayer({
				id: 'state_province_labels',
				type: 'symbol',
				source: 'osm',
				'source-layer': 'boundary_labels',
				filter: ['==', ['get', 'admin_level'], 4],
				layout: {
					'text-field': ['get', 'name'],
					'text-font': ['Open Sans Regular'],
					'text-size': ['interpolate', ['linear'], ['zoom'], 2, 9, 5, 11],
					'text-anchor': 'center',
					'text-letter-spacing': 0.1,
					'text-transform': 'uppercase'
				},
				paint: {
					'text-color': '#aaaaaa',
					'text-halo-color': '#ffffff',
					'text-halo-width': 1,
					'text-opacity': 0.75
				},
				minzoom: 2,
				maxzoom: 7
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
					'text-anchor': 'center',
					'text-letter-spacing': 0.15,
					'text-transform': 'uppercase'
				},
				paint: {
					'text-color': '#999999',
					'text-halo-color': '#ffffff',
					'text-halo-width': 1.5,
					'text-opacity': 0.45
				},
				minzoom: 2,
				maxzoom: 7
			});

			mapLoaded = true;
			updateMapData();
		});

		map.on('style.load', () => {
			map.setProjection({ type: (map.getZoom() < 7) ? 'globe' : 'mercator' });
			map.on('zoom', () => {
				map.setProjection({ type: (map.getZoom() < 7) ? 'globe' : 'mercator' });
			});
		});

		map.dragRotate.disable();
		map.touchZoomRotate.disableRotation();
	});

	onDestroy(() => {
		if (map) {
			map.remove();
			map = null;
		}
	});
</script>

<div class="map-section">

	<div class="color-legend">
		<span>Percent change Canadians visiting U.S. metros</span>
		<div class="legend-bar">
			<div class="legend-gradient"></div>
		</div>
		<div class="legend-labels">
			<span class="legend-left">-70%</span>
			<!-- <span class="legend-mid">-20%</span> -->
			<span class="legend-zero">0%</span>
			<span class="legend-right">+30%</span>
		</div>
		<!-- <div class="size-legend">
			<div class="size-items">
				<div class="size-item">
					<span class="legend-circle" style={`width:${legendCircleDiameterPx(7)}px;height:${legendCircleDiameterPx(7)}px;`}></span>
					<span>mall trip volume</span>
				</div>
				<div class="size-item">
					<span class="legend-circle" style={`width:${legendCircleDiameterPx(25)}px;height:${legendCircleDiameterPx(25)}px;`}></span>
					<span>medium trip volume</span>
				</div>
				<div class="size-item">
					<span class="legend-circle" style={`width:${legendCircleDiameterPx(55)}px;height:${legendCircleDiameterPx(55)}px;`}></span>
					<span>large trip volume</span>
				</div>
			</div>
		</div> -->

		<p class="map-legend-text">
			The larger the circle size, the greater the total volume of trips from 04/2025 to 03/2026. 
			<br><br>
			Click on a metro to display its statistics.
		</p>
	</div>
	<div class="map-container" bind:this={mapContainer}></div>
</div>

<style>
	.map-section {
		max-width: 1080px;
		margin: 0 auto 0px auto;
	}

	.map-container {
		width: 100%;
		height: 600px;
		max-height: 90dvh;
		border: 1px solid var(--brandGray);
		border-radius: 0px;
	}

	.map-legend-text {
		font-size: 13px;
		line-height: 17px;
		font-family: OpenSans;
		color: var(--brandGray90);
		margin-bottom: 10px;
	}

	:global(.maplibregl-popup-content) {
		background: rgba(255,255,255,0.95);
		padding: 10px 40px 10px 15px;
		border-radius: 4px;
	}

	:global(.maplibregl-popup-close-button) {
		font-size: 16px;
		color: #333;
		width: 28px;
		height: 28px;
		padding: 0;
		right: 4px;
		top: 4px;
		position: absolute;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		background: transparent;
		border: 0;
		line-height: 1;
	}

	:global(.maplibregl-popup-close-button:hover) {
		background-color: rgba(0, 0, 0, 0.05);
	}

	.color-legend {
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		font-weight: normal;
		margin: 15px auto;
		max-width: 680px;
	}

	.legend-bar {
		width: 100%;
		height: 10px;
		border: 1px solid var(--brandGray);
		border-radius: 3px;
		overflow: hidden;
		justify-content: center;
		margin-top: 5px;
	}

	.legend-gradient {
		width: 100%;
		height: 100%;
		background: linear-gradient(to right, #DC4633 0%, #F1C500 55%, #FFFFFF 70%, #007FA3 100%);
	}

	.legend-labels {
		position: relative;
		margin-top: 5px;
		font-size: 12px;
		color: var(--brandGray90);
		height: 18px;
	}

	.legend-labels span {
		position: absolute;
		transform: translateX(-50%);
		white-space: nowrap;
	}

	.legend-left { left: 2%; transform: none; }
	.legend-mid { left: 50%; }
	.legend-zero { left: 70%; }
	.legend-right { left: 98%; transform: translateX(-100%); }

	.size-legend {
		margin-top: 10px;
		font-size: 12px;
		color: var(--brandGray90);
	}

	.size-items {
		display: flex;
		gap: 12px;
		flex-wrap: wrap;
		margin-top: 6px;
	}

	.size-item {
		display: inline-flex;
		align-items: center;
		gap: 6px;
	}

	.legend-circle {
		display: inline-block;
		border-radius: 50%;
		background: rgba(255, 255, 255, 0.85);
		border: 1.5px solid #4d5d7a;
		flex: 0 0 auto;
	}

	@media (max-width: 720px) {
		.color-legend {
			padding-left: 20px;
			padding-right: 20px;
			box-sizing: border-box;
		}
	}
</style>
