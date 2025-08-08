<script>

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

	let work_side = "pmtiles/work_side.pmtiles";
	let ADA_cent = "pmtiles/ADA_centroids.pmtiles";
	let background = "pmtiles/background.pmtiles";
	
	let graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];
	let graduated_siz = [5, 7.5, 10, 20, 40];



	let metricType = "Percent"; // ["Percent", "Count"]
	function metricSelect(value) {
		metricType = value;
	};

	let impactType = "EmployeeWork" // ["EmployeeHome","EmployeeWork", "Business"] 
	function impactTypeSelect(value) {
		impactType = value;
	};

	let tariffType = "All" // see full list below
	function tariffTypeSelect(event) {
		tariffType = event.detail.value;
	}
	const selectTariffList = ["All tariffs", "Automobile tariffs", "Aluminum tariffs", "Steel tariffs", "Lumber tariffs", "Energy tariffs", "non-CUSMA tariffs"]; 

	let mapQuery;
	$: mapQuery = {
		metricType: metricType,
		impactType: impactType,
		tariffType: tariffType,
	};

	$: mapSelected = Object.entries(dataLayers).find(([key, layer]) =>
		Object.entries(mapQuery).every(([k, v]) => layer[k] === v)
	)?.[0];


	// dynamic update to map if any inputs are changed

	$: if (
		map &&
		map.isStyleLoaded() &&
		map.getLayer("polygons") &&
		map.getLayer("centroids")
	) {
		if (mapSelected) {
			if (mapQuery.metricType === "Percent") {
			
				map.setLayoutProperty('polygons', 'visibility', 'visible');
				map.setLayoutProperty('centroids', 'visibility', 'none');

				map.setPaintProperty("polygons", "fill-opacity", 0.8);

				map.setPaintProperty("polygons", "fill-color", [
					"case",
					["==", ["get", dataLayers[mapSelected].dataSource], null], "rgba(0,0,0,0)",
					["step", ["get", dataLayers[mapSelected].dataSource],
					dataLayers[mapSelected].colours[0], dataLayers[mapSelected].breaks[0],
					dataLayers[mapSelected].colours[1], dataLayers[mapSelected].breaks[1],
					dataLayers[mapSelected].colours[2], dataLayers[mapSelected].breaks[2],
					dataLayers[mapSelected].colours[3], dataLayers[mapSelected].breaks[3],
					dataLayers[mapSelected].colours[4]],
				]);

			} else if (mapQuery.metricType === "Count") {

				map.setLayoutProperty('polygons', 'visibility', 'none');
				map.setLayoutProperty('centroids', 'visibility', 'visible');

				map.setPaintProperty("centroids", "circle-opacity", 0.8);

				map.setPaintProperty("centroids", "circle-color", [
					"case",
					["==", ["get", dataLayers[mapSelected].dataSource], null], "rgba(0,0,0,0)",
					["==", ["get", dataLayers[mapSelected].dataSource], 0], "rgba(0,0,0,0)",
					[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].colours[4],
					[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].colours[3],
					[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[1]], dataLayers[mapSelected].colours[2],
					[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[0]], dataLayers[mapSelected].colours[1],
					dataLayers[mapSelected].colours[0],
				]);

				map.setPaintProperty("centroids", "circle-radius", [
					"interpolate", ["linear"], ["zoom"],
					3, [
						"case",
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].size[4],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].size[3],
						0
					],
					8, [
						"case",
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].size[4],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].size[3],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[1]], dataLayers[mapSelected].size[2],
						0
					],
					11, [
						"case",
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].size[4],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].size[3],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[1]], dataLayers[mapSelected].size[2],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[0]], dataLayers[mapSelected].size[1],
						dataLayers[mapSelected].size[0],
					],
				]);
			} else {
				console.log("no data")
			}
		} else {
			console.log("no matching data layer");
		}
	} else {
		console.log("map not loaded");
	}


	// all the data layers

	const dataLayers = {
		"Total_B_pc": {
			dataSource: "Total_B_pc",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "All tariffs",
			breaks: [0.0037, 0.0104, 0.0257, 0.0667],
			colours: graduated_col,
			text: "% of businesses directly affected by all types of US Administration's Tariffs on Canada",
		},
		"Total_E_pc": {
			dataSource: "Total_E_pc",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "All tariffs",
			breaks: [0.017, 0.057, 0.124, 0.26],
			colours: graduated_col,
			text: "Estimated % of employees directly affected by all types of US Administration's Tariffs on Canada",
		},
		"Auto_B_pct": {
			dataSource: "Auto_B_pct",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Automobile tariffs",
			breaks: [0.00017, 0.00076, 0.00146, 0.00322],
			colours: graduated_col,
			text: "% of businesses directly affected by US Administration's Automobile Tariffs on Canada",
		},
		"Auto_E_pct": {
			dataSource: "Auto_E_pct",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Automobile tariffs",
			breaks: [0.0012, 0.0086, 0.0505, 0.1012],
			colours: graduated_col,
			text: "Estimated % of employees directly affected by US Administration's Automobile Tariffs on Canada",
		},
		"Total_B": {
			dataSource: "Total_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "All tariffs",
			breaks: [127, 765, 1990, 7309],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly affected by all types of US Administration's Tariffs on Canada",
		},
		"Total_E": {
			dataSource: "Total_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "All tariffs",
			breaks: [5871, 27500, 82127, 211116],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees directly affected by all types of US Administration's Tariffs on Canada",
		},
	};


	// maps loading and hovering functions

	let selectedZone = "";
	let selectedValue = "";
	let lastUpdate = "0";

	onMount(async () => {
		
		map = new maplibregl.Map({
			container: "map",
			style: "https://api.protomaps.com/styles/v5/white/en.json?key=89c5d93843b4ca61",
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

		map.on('load', async () => {

			map.addSource('background', {
				type: 'vector',
				url: 'pmtiles://' + background,
			});
			
			map.addSource('work_side',{
				type: 'vector',
				url: 'pmtiles://' + work_side,
			});

			map.addSource('ADA_centroids', {
				type: 'vector',
				url: 'pmtiles://' + ADA_cent,
			});

			map.addLayer({
				'id': 'polygons',
				'type': 'fill',
				'source': 'work_side',
				'source-layer': 'ADA_aggregates',
				'layout': {
					'visibility': 'none',
				},
			});

			map.addLayer({
				'id': 'outline',
				'type': 'line',
				'source': 'background',
				'source-layer': 'background',
				'paint': {
					'line-color': '#808080',
					'line-width': 1,
					'line-opacity': 0.25,
				},
			});

			map.addLayer({
				'id': 'outline-hover',
				'type': 'fill',
				'source': 'background',
				'source-layer': 'background',
				'paint': {
					'fill-color': '#0000FF',
					'fill-opacity': 0.5,
				},
				'filter': ['==', 'DGUID', ''],
			});
			
			map.addLayer({
				'id': 'centroids',
				'type': 'circle',
				'source': 'ADA_centroids',
				'source-layer': 'ADA_centroids',
				'layout': {
					'visibility': 'none',
				},
			});
			
			map.setLayerZoomRange('centroids', 1, 12);


		});
		
		map.on('style.load', () => {

			map.setProjection({
				type: (map.getZoom() < 7) ? 'globe' : 'mercator'
			});
			
			map.on('zoom', () => {
				const zoom = map.getZoom();
				map.setProjection({
					type: (zoom < 7) ? 'globe' : 'mercator'
				});
			});

		});

		map.on('mousemove', 'polygons', (e) => {
			const now = performance.now();
			if (now - lastUpdate < 100) return; // Throttle updates to every 100ms
			lastUpdate = now;

			map.getCanvas().style.cursor = 'pointer';

			if (!e.features.length) return;

			const properties = e.features[0].properties;
			const currentZone = properties.ADADGUID;

			if (currentZone !== selectedZone) {

				const rawValue = properties[mapSelected];

				selectedValue = (rawValue != null && rawValue >= 0)
					? (rawValue * 100).toFixed(2) + '%'
					: "No Data";

				selectedZone = currentZone;

				map.setFilter('outline-hover', ['==', 'DGUID', selectedZone]);
			}
		});

		map.on('mouseleave', 'polygons', () => {
			map.getCanvas().style.cursor = '';
			selectedZone = "";
			selectedValue = "";
			map.setFilter('outline-hover', ['==', 'DGUID', '']);
		});

		map.on('mousemove', 'centroids', (e) => {
			const now = performance.now();
			if (now - lastUpdate < 100) return; // Throttle updates to every 100ms
			lastUpdate = now;

			map.getCanvas().style.cursor = 'pointer';

			if (!e.features.length) return;

			const properties = e.features[0].properties;
			
			const currentZone = properties.ADADGUID;

			if (currentZone !== selectedZone) {
				const rawValue = properties[mapSelected];
				selectedValue = (rawValue != null && rawValue >= 0)
					? Math.round(rawValue).toLocaleString()
					: "No Data";

				selectedZone = currentZone;

				map.setFilter('outline-hover', ['==', 'DGUID', selectedZone]);
			}
		});

		map.on('mouseleave', 'centroids', () => {
			map.getCanvas().style.cursor = '';
			selectedZone = "";
			selectedValue = "";
			map.setFilter('outline-hover', ['==', 'DGUID', '']);
		});

	});

</script>




<div id="container">

	<div id="panel">

		<div class="logo-container">

			<a href="https://schoolofcities.utoronto.ca/" target="_blank" class="logo-link">
				
				<img src={logoBlueColour} alt="UofT and School of Cities logos" class="logo" />

			</a>

			<a href="./" target="_blank" class="research-link">Canada-U.S. Tariff Research</a>

		</div>

		<h2>Maps of geographic impact of U.S. tariffs on Canada</h2>

		<div id = "select-wrapper">
			<Select
				id = 'select'
				items = {selectTariffList}
				value = {dataLayers[mapSelected]?.tariffType}
				clearable = {false}
				showChevron = {true}
				listAutoWidth = {true}
				searchable = {false}
				listOffset = {10}
				on:change = {tariffTypeSelect}
			/>
		</div>

		<div class="button-group">
			<div
				class="toggle-button {metricType === 'Percent' ? 'selected' : ''}"
				on:click={() => metricSelect("Percent")}
			>
				Percent
			</div>
			<div
				class="toggle-button {metricType === 'Count' ? 'selected' : ''}"
				on:click={() => metricSelect("Count")}
			>
				Count
			</div>
		</div>

		<div class="button-group" style="margin-top: 10px;">
			<div
				class="toggle-button {impactType === 'Business' ? 'selected' : ''}"
				on:click={() => impactTypeSelect("Business")}
			>
				Businesses
			</div>
			<div
				class="toggle-button {impactType === 'EmployeeWork' ? 'selected' : ''}"
				on:click={() => impactTypeSelect("EmployeeWork")}
			>
				Employees (place of work)
			</div>
			<div
				class="toggle-button {impactType === 'EmployeeHome' ? 'selected' : ''}"
				on:click={() => impactTypeSelect("EmployeeHome")}
			>
				Employees (home)
			</div>
		</div>

		<div class="des">

			{#if dataLayers[mapSelected]?.metricType === "Percent" && dataLayers[mapSelected]?.colours}

				<div id="destext">
					<p>
						{dataLayers[mapSelected]?.text}
					</p>
				</div>

				<div id="legend">
					<svg width='350' height='40'>
						<rect
						class = "box"
						width="64"
						height="20"
						x="20"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[0]};"
						/>
	
						<rect
						class = "box"
						width="64"
						height="20"
						x="85"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[1]};"
						/>
	
						<rect
						class = "box"
						width="64"
						height="20"
						x="150"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[2]};"
						/>
	
						<rect
						class = "box"
						width="64"
						height="20"
						x="215"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[3]};"
						/>
	
						<rect
						class = "box"
						width="64"
						height="20"
						x="280"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[4]};"
						/>
	
						<text class="legend-label" text-anchor="middle" x="85" y="35">&lt;{(dataLayers[mapSelected].breaks[0]*100).toFixed(2)}%</text>
						<text class="legend-label" text-anchor="middle" x="150" y="35">{(dataLayers[mapSelected].breaks[1]*100).toFixed(2)}%</text>
						<text class="legend-label" text-anchor="middle" x="215" y="35">{(dataLayers[mapSelected].breaks[2]*100).toFixed(2)}%</text>
						<text class="legend-label" text-anchor="middle" x="280" y="35">&gt{(dataLayers[mapSelected].breaks[3]*100).toFixed(2)}%</text>
					</svg>
				</div>

			{:else if dataLayers[mapSelected]?.metricType === "Count" && dataLayers[mapSelected]?.colours}
				<div id="destext">{dataLayers[mapSelected]?.text}</div>

				<div id="legend">
					<svg width='350' height='200'>
						<circle
						class = "box"
						cx="55"
						cy="10"
						r="{dataLayers[mapSelected].size[0]}"
						style="fill:{dataLayers[mapSelected].colours[0]};"
						/>

						<circle
						class = "box"
						cx="55"
						cy="32.5"
						r="{dataLayers[mapSelected].size[1]}"
						style="fill:{dataLayers[mapSelected].colours[1]};"
						/>

						<circle
						class = "box"
						cx="55"
						cy="55"
						r="{dataLayers[mapSelected].size[2]}"
						style="fill:{dataLayers[mapSelected].colours[2]};"
						/>

						<circle
						class = "box"
						cx="55"
						cy="90"
						r="{dataLayers[mapSelected].size[3]}"
						style="fill:{dataLayers[mapSelected].colours[3]};"
						/>

						<circle
						class = "box"
						cx="55"
						cy="150"
						r="35"
						style="fill:{dataLayers[mapSelected].colours[4]};"
						/>

						<text class="legend-label" x="100" y="10" dy="0.35em">&lt;{dataLayers[mapSelected].breaks[0]}</text>
						<text class="legend-label" x="100" y="32.5" dy="0.35em">{dataLayers[mapSelected].breaks[0]} - {dataLayers[mapSelected].breaks[1]}</text>
						<text class="legend-label" x="100" y="55" dy="0.35em">{dataLayers[mapSelected].breaks[1]} - {dataLayers[mapSelected].breaks[2]}</text>
						<text class="legend-label" x="100" y="90" dy="0.35em">{dataLayers[mapSelected].breaks[2]} - {dataLayers[mapSelected].breaks[3]}</text>
						<text class="legend-label" x="100" y="150" dy="0.35em">&gt;{dataLayers[mapSelected].breaks[3]}</text>
					</svg>
				</div>

			{/if}
		</div>

		<div id="hovered-zone" >
			<i>Hovered zone</i>: {@html selectedValue ? '<strong>' + selectedValue + '</strong>' : 'No data available'}
		</div>

		<div class="datadetail">
			<h4 style="margin-bottom: 0px;">Data & Methods</h4>
			<p>
				Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas consequat lacus eu dolor dapibus sodales. Aenean venenatis metus id eleifend tincidunt. Nulla ut lacus et urna finibus bibendum sit amet et ante. Aliquam tristique, ex sed porttitor hendrerit, ex odio accumsan ex, eu maximus leo quam quis nulla. 
			</p>

			<p>
				Fusce sed sem nulla. Praesent congue sapien pellentesque sodales fermentum. Pellentesque dapibus ultrices lacus consectetur laoreet. Integer imperdiet sed sapien sed pharetra. Praesent sodales nunc ut lorem venenatis laoreet vitae et neque. Etiam condimentum tincidunt dignissim. 
			</p>
		</div>
	
	</div>
	
	<div id="map"></div>

</div>


<style>

	#container {
		display: flex;
		height: 100vh;
		overflow: hidden;
	}

	#panel {
		max-width: 420px;
		width: 100%;
		min-width: 350px;
		height: calc(100dvh);
		overflow-y: auto;
		background-color: #ffffff;
		padding: 20px;
		border-right: solid 1px var(--brandDarkBlue);
		flex-shrink: 0;
	}

	.logo-container {
		display: flex;
		margin-top: 0px;
		margin-bottom: 40px;
		border-bottom: solid 1px var(--brandGray);
		padding: 0px;
	}

	.logo {
		width: 200px; 
		height: 50px;
		padding: 0px;
		padding-left: 0px;
		margin-bottom: -5px;
	}

	.logo:hover {
		opacity: 0.75;
	}

	.research-link {
		position: absolute;
		top: 40px;
		left: 252px;
		font-family: SourceSerifItalic, serif;
		font-size: 16px;
		text-decoration: underline;
		text-decoration-thickness: 1px;
		color: var(--brandDarkBlue);
	}

	.research-link:hover {
		color: var(--brandMedGreen);
	}


	#panel h2 {
		margin-top: 0px;
	}

	#map {
		flex: 1;
		height: 100vh;
		overflow: hidden;
	}

	#select-wrapper {
		margin-top: 10px;
		border-top: solid 1px var(--brandGray);
		padding-top: 20px;
		margin-bottom: 10px;
		font-family: TradeGothicBold, sans-serif;
		font-size: 16px;
		font-weight: normal;
		color: var(--brandGray90);
	}

	.button-group {
		display: flex;
		margin-right: -10px;
	}

	.toggle-button {
		width: 100%;
		padding: 6px 12px;
		margin-right: 10px;
		border: 1px solid var(--brandGray);
		border-radius: 5px;
		cursor: pointer;
		font-size: 14px;
		opacity: 0.5;
		background-color: var(--brandWhite);
		color: var(--brandDarkGray);
		user-select: none;
		font-family: TradeGothicBold, sans-serif;
		font-size: 16px;
		font-weight: normal;
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

	#destext {
		margin-bottom: 10px;
		margin-left: 0px;
	}

	#destext p {
		font-family: SourceSerif;
		font-size: 16px;
		line-height: 22px;
		font-weight: normal;
		color: var(--brandGray90);
	}

	.legend-label {
		font-size: 15px;
		fill: #000000;
	}

	.datadetail p {
		font-family: SourceSerif;
		font-weight: normal;
		color: var(--brandGray90);
		text-align: left;
		padding-top: 2px;
		padding-bottom: 2px;
		font-size: 16px;
		line-height: 24px;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-rendering: optimizeLegibility;
	}


</style>