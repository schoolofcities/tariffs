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

	let choropleth = "pmtiles/choropleth.pmtiles";
	let centroids = "pmtiles/centroids.pmtiles";
	
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

	let tariffType = "All tariffs" // see full list below
	function tariffTypeSelect(event) {
		tariffType = event.detail.value;
	}
	const selectTariffList = ["All tariffs", "Automobile tariffs", "Aluminum tariffs", "Steel tariffs", "Copper tariffs", "Lumber tariffs", "Energy tariffs", "non-CUSMA tariffs"]; 

	let mapQuery;
	$: mapQuery = {
		metricType: metricType,
		impactType: impactType,
		tariffType: tariffType,
	};

	let mapSelected;
	$: mapSelected = Object.entries(dataLayers).find(([key, layer]) =>
		Object.entries(mapQuery).every(([k, v]) => layer[k] === v)
	)?.[0];


	// dynamic update to map if any inputs are changed

	function updateMap() {
		if (
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
						["==", ["get", dataLayers[mapSelected].dataSource], 0], "#f1c500",
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
	};

	$: {
		mapQuery;   // track metricType, impactType, tariffType
		mapSelected;
		map;
		updateMap();
	}



	// all the data layers

	const dataLayers = {
		"Total_1": {
			dataSource: "Total_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "All tariffs",
			breaks: [0.012, 0.037, 0.077, 0.219],
			colours: graduated_col,
			text: "% of businesses directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_1": {
			dataSource: "Auto_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Automobile tariffs",
			breaks: [0.003, 0.0099, 0.0212, 0.0625],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_1": {
			dataSource: "Alum_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Aluminum tariffs",
			breaks: [0.0039, 0.0124, 0.0254, 0.0473],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_1": {
			dataSource: "Steel_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Steel tariffs",
			breaks: [0.005, 0.0159, 0.0344, 0.087],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_1": {
			dataSource: "Cop_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Copper tariffs",
			breaks: [0.0019, 0.0062, 0.0133, 0.0333],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_1": {
			dataSource: "Lum_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Lumber tariffs",
			breaks: [0.0037, 0.0147, 0.0667, 0.1667],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_1": {
			dataSource: "Ene_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Energy tariffs",
			breaks: [0.0037, 0.0123, 0.0279, 0.0833],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_1": {
			dataSource: "CUSMA_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "non-CUSMA tariffs",
			breaks: [0.0051, 0.0162, 0.0366, 0.087],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_2": {
			dataSource: "Total_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "All tariffs",
			breaks: [0.027, 0.082, 0.161, 0.296],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_2": {
			dataSource: "Auto_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Automobile tariffs",
			breaks: [0.013, 0.047, 0.108, 0.211],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_2": {
			dataSource: "Alum_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Aluminum tariffs",
			breaks: [0.015, 0.053, 0.119, 0.217],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_2": {
			dataSource: "Steel_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Steel tariffs",
			breaks: [0.017, 0.056, 0.125, 0.317],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_2": {
			dataSource: "Cop_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Copper tariffs",
			breaks: [0.0046, 0.0175, 0.0421, 0.0915],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_2": {
			dataSource: "Lum_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Lumber tariffs",
			breaks: [0.011, 0.04, 0.097, 0.243],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_2": {
			dataSource: "Ene_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Energy tariffs",
			breaks: [0.012, 0.048, 0.125, 0.319],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_2": {
			dataSource: "CUSMA_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "non-CUSMA tariffs",
			breaks: [0.012, 0.043, 0.103, 0.265],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_3": {
			dataSource: "Total_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "All tariffs",
			breaks: [0.044, 0.11, 0.205, 0.5],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_3": {
			dataSource: "Auto_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Automobile tariffs",
			breaks: [0.012, 0.035, 0.081, 0.233],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_3": {
			dataSource: "Alum_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Aluminum tariffs",
			breaks: [0.018, 0.046, 0.092, 0.24],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_3": {
			dataSource: "Steel_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Steel tariffs",
			breaks: [0.016, 0.041, 0.079, 0.223],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_3": {
			dataSource: "Cop_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Copper tariffs",
			breaks: [0.0019, 0.0057, 0.0156, 0.0448],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_3": {
			dataSource: "Lum_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Lumber tariffs",
			breaks: [0.013, 0.043, 0.109, 0.333],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_3": {
			dataSource: "Ene_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Energy tariffs",
			breaks: [0.01, 0.027, 0.063, 0.173],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_3": {
			dataSource: "CUSMA_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "non-CUSMA tariffs",
			breaks: [0.016, 0.046, 0.097, 0.189],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_B": {
			dataSource: "Total_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "All tariffs",
			breaks: [6,21,58,148],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_B": {
			dataSource: "Auto_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Automobile tariffs",
			breaks: [1,5,17,51],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_B": {
			dataSource: "Alum_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Aluminum tariffs",
			breaks: [2,10,30,74],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_B": {
			dataSource: "Steel_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Steel tariffs",
			breaks: [2,9,29,81],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_B": {
			dataSource: "Cop_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Copper tariffs",
			breaks: [0,2,7,20],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_B": {
			dataSource: "Lum_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Lumber tariffs",
			breaks: [0,2,5,11],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_B": {
			dataSource: "Ene_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Energy tariffs",
			breaks: [1,5,14,38],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_B": {
			dataSource: "CUSMA_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "non-CUSMA tariffs",
			breaks: [2,8,19,41],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_E": {
			dataSource: "Total_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "All tariffs",
			breaks: [274,959,2356,7195],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_E": {
			dataSource: "Auto_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Automobile tariffs",
			breaks: [123,456,1219,5235],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_E": {
			dataSource: "Alum_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Aluminum tariffs",
			breaks: [242,880,1874,3519],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_E": {
			dataSource: "Steel_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Steel tariffs",
			breaks: [161,587,1358,3474],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_E": {
			dataSource: "Cop_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Copper tariffs",
			breaks: [22,85,213,393],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_E": {
			dataSource: "Lum_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Lumber tariffs",
			breaks: [28,112,275,555],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_E": {
			dataSource: "Ene_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Energy tariffs",
			breaks: [67,271,634,1405],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_E": {
			dataSource: "CUSMA_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "non-CUSMA tariffs",
			breaks: [86,211,744,1919],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_C": {
			dataSource: "Total_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "All tariffs",
			breaks: [147,375,657,1197],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_C": {
			dataSource: "Auto_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Automobile tariffs",
			breaks: [45,124,263,541],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_C": {
			dataSource: "Alum_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Aluminum tariffs",
			breaks: [69,183,357,771],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_C": {
			dataSource: "Steel_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Steel tariffs",
			breaks: [61,159,311,696],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_C": {
			dataSource: "Cop_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Copper tariffs",
			breaks: [8,24,60,192],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_C": {
			dataSource: "Lum_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Lumber tariffs",
			breaks: [23,73,167,352],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_C": {
			dataSource: "Ene_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Energy tariffs",
			breaks: [34,94,186,415],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_C": {
			dataSource: "CUSMA_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "non-CUSMA tariffs",
			breaks: [56,157,350,726],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
	};


	// maps loading and hovering functions

	let selectedZone = "";
	let selectedValue = "";
	let lastUpdate = "0";

	onMount(async () => {
		
		map = new maplibregl.Map({
			container: "map",
			// style: "https://api.protomaps.com/styles/v5/white/en.json?key=89c5d93843b4ca61",
			style: {
				version: 8,
				sources: {
					osm: {
						type: 'vector',
						tiles: [
						'https://vector.openstreetmap.org/shortbread_v1/{z}/{x}/{y}.mvt'
						]
					}
					},
				layers: [
					{
						id: 'ocean',
						type: 'fill',
						source: 'osm',
						'source-layer': 'ocean',
						paint: {
							'fill-color': '#E3F4FB'
						}
					}
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

		map.on('load', async () => {
			
			map.addSource('choropleth',{
				type: 'vector',
				url: 'pmtiles://' + choropleth,
			});

			map.addSource('centroids', {
				type: 'vector',
				url: 'pmtiles://' + centroids,
			});

			map.addSource('ne_water', {
				type: 'geojson',
				data: 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_lakes.geojson'
			});

			
			map.addLayer({
				'id': 'polygons',
				'type': 'fill',
				'source': 'choropleth',
				'source-layer': 'choropleth',
				'layout': {
					'visibility': 'none',
				},
			});

			map.addLayer({
				id: 'ne_water_fill',
				type: 'fill',
				source: 'ne_water',
				paint: {
					'fill-color': '#E3F4FB'
				},
				minzoom: 0,
				maxzoom: 5
			});

			const CUTOFF = 50000000; 

			// Large lakes: show at all zooms
			map.addLayer({
				id: 'water_polygons_large',
				type: 'fill',
				source: 'osm',
				'source-layer': 'water_polygons',
				filter: ['all', ['==', 'kind', 'water'], ['>=', 'way_area', CUTOFF]],
				paint: { 'fill-color': '#E3F4FB' },
				minZoom: 5
			});

			// Small lakes: only from z>=10
			map.addLayer({
				id: 'water_polygons_small',
				type: 'fill',
				source: 'osm',
				'source-layer': 'water_polygons',
				filter: ['all', ['==', 'kind', 'water'], ['<', 'way_area', CUTOFF]],
				paint: { 'fill-color': '#E3F4FB' },
				minzoom: 9.6
			});

			map.addLayer({
				id: 'outline',
				type: 'line',
				source: 'choropleth',
				'source-layer': 'choropleth',
				paint: {
					'line-color': '#808080',
					'line-width': [
						'interpolate', ['linear'], ['zoom'],
						3, 1,  
						16, 2
					],
					'line-opacity': 0.25
				}
			});

			map.addLayer({
				'id': 'outline-hover',
				'type': 'fill',
				'source': 'choropleth',
				'source-layer': 'choropleth',
				'paint': {
					'fill-color': '#0000FF',
					'fill-opacity': 0.5,
				},
				'filter': ['==', 'ADADGUID', ''],
			});
			
			map.addLayer({
				'id': 'centroids',
				'type': 'circle',
				'source': 'centroids',
				'source-layer': 'centroids',
				'layout': {
					'visibility': 'none',
				},
			});
			
			map.setLayerZoomRange('centroids', 1, 12);

			mapQuery = {
				metricType: metricType,
				impactType: impactType,
				tariffType: tariffType,
			};

			mapSelected = Object.entries(dataLayers).find(([key, layer]) =>
				Object.entries(mapQuery).every(([k, v]) => layer[k] === v)
			)?.[0];

			map.once('idle', () => {
				updateMap();
			});

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

				map.setFilter('outline-hover', ['==', 'ADADGUID', selectedZone]);
			}
		});

		map.on('mouseleave', 'polygons', () => {
			map.getCanvas().style.cursor = '';
			selectedZone = "";
			selectedValue = "";
			map.setFilter('outline-hover', ['==', 'ADADGUID', '']);
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

				map.setFilter('outline-hover', ['==', 'ADADGUID', selectedZone]);
			}
		});

		map.on('mouseleave', 'centroids', () => {
			map.getCanvas().style.cursor = '';
			selectedZone = "";
			selectedValue = "";
			map.setFilter('outline-hover', ['==', 'ADADGUID', '']);
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
			<p>Select the tariff industry:</p>
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

		<p>Show exposure by the number of businesses, employees based on where they work, or employees based on their home location.</p>
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

		<p>Show exposure as the total businesses or employees, or as a percent of all within the area.</p>
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

				<!--5, 7.5, 10, 20, 40--> 

				<div id="legend">
					<svg width='350' height='200'>
						<circle
						class = "box"
						cx="55"
						cy="40"
						r="35"
						style="fill:{dataLayers[mapSelected].colours[4]};"
						/>

						<circle
						class = "box"
						cx="55"
						cy="100"
						r="{dataLayers[mapSelected].size[3]}"
						style="fill:{dataLayers[mapSelected].colours[3]};"
						/>

						<circle
						class = "box"
						cx="55"
						cy="135"
						r="{dataLayers[mapSelected].size[2]}"
						style="fill:{dataLayers[mapSelected].colours[2]};"
						/>

						<circle
						class = "box"
						cx="55"
						cy="157.5"
						r="{dataLayers[mapSelected].size[1]}"
						style="fill:{dataLayers[mapSelected].colours[1]};"
						/>

						{#if dataLayers[mapSelected].breaks[0] !== 0}
						<circle
						class = "box"
						cx="55"
						cy="180"
						r="{dataLayers[mapSelected].size[0]}"
						style="fill:{dataLayers[mapSelected].colours[0]};"
						/>
						{/if}

						<text class="legend-label" x="100" y="40" dy="0.35em">&gt;{dataLayers[mapSelected].breaks[3]}</text>
						<text class="legend-label" x="100" y="100" dy="0.35em">{dataLayers[mapSelected].breaks[2] + 1} - {dataLayers[mapSelected].breaks[3]}</text>
						<text class="legend-label" x="100" y="135" dy="0.35em">{dataLayers[mapSelected].breaks[1] + 1} - {dataLayers[mapSelected].breaks[2]}</text>
						<text class="legend-label" x="100" y="157.5" dy="0.35em">{dataLayers[mapSelected].breaks[0] + 1} - {dataLayers[mapSelected].breaks[1]}</text>
						{#if dataLayers[mapSelected].breaks[0] !== 0}<text class="legend-label" x="100" y="180" dy="0.35em">&le;{dataLayers[mapSelected].breaks[0]}</text>{/if}
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