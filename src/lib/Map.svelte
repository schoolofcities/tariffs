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

	let addressQuery="";
	let addressResults="";

	let choropleth = "pmtiles/choropleth.pmtiles";
	let centroids = "pmtiles/centroids.pmtiles";
	let censusDivisions = "pmtiles/census-divisions.pmtiles";
	
	let graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];
	let graduated_siz = [5, 7.5, 10, 20, 40];

	let metricType = "Percent"; // ["Percent", "Count"]
	function metricSelect(value) {
		metricType = value;
	};

	let impactType = "EmployeeHome" // ["EmployeeHome","EmployeeWork", "Business"] 
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
						["==", ["get", dataLayers[mapSelected].dataSource], 0], "rgba(0,0,0,0)",
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
			breaks: [0.04, 0.1, 0.2, 0.3],
			colours: graduated_col,
			text: "% of businesses directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_1": {
			dataSource: "Auto_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Automobile tariffs",
			breaks: [0.003, 0.01, 0.02, 0.06],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_1": {
			dataSource: "Alum_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Aluminum tariffs",
			breaks: [0.004, 0.01, 0.03, 0.05],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_1": {
			dataSource: "Steel_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Steel tariffs",
			breaks: [0.004, 0.01, 0.03, 0.07],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_1": {
			dataSource: "Cop_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Copper tariffs",
			breaks: [0.002, 0.006, 0.01, 0.03],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_1": {
			dataSource: "Lum_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Lumber tariffs",
			breaks: [0.004, 0.01, 0.07, 0.2],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_1": {
			dataSource: "Ene_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Energy tariffs",
			breaks: [0.004, 0.01, 0.03, 0.08],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_1": {
			dataSource: "CUSMA_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "non-CUSMA tariffs",
			breaks: [0.03, 0.09, 0.2, 0.3],
			colours: graduated_col,
			text: "% of businesses directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_2": {
			dataSource: "Total_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "All tariffs",
			breaks: [0.04, 0.1, 0.2, 0.6],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_2": {
			dataSource: "Auto_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Automobile tariffs",
			breaks: [0.01, 0.04, 0.1, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_2": {
			dataSource: "Alum_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Aluminum tariffs",
			breaks: [0.01, 0.05, 0.1, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_2": {
			dataSource: "Steel_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Steel tariffs",
			breaks: [0.02, 0.05, 0.1, 0.3],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_2": {
			dataSource: "Cop_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Copper tariffs",
			breaks: [0.004, 0.01, 0.03, 0.07],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_2": {
			dataSource: "Lum_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Lumber tariffs",
			breaks: [0.01, 0.04, 0.09, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_2": {
			dataSource: "Ene_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Energy tariffs",
			breaks: [0.01, 0.07, 0.2, 0.4],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_2": {
			dataSource: "CUSMA_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "non-CUSMA tariffs",
			breaks: [0.04, 0.1, 0.2, 0.5],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_3": {
			dataSource: "Total_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "All tariffs",
			breaks: [0.05, 0.1, 0.2, 0.6],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_3": {
			dataSource: "Auto_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Automobile tariffs",
			breaks: [0.01, 0.04, 0.09, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_3": {
			dataSource: "Alum_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Aluminum tariffs",
			breaks: [0.01, 0.03, 0.07, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_3": {
			dataSource: "Steel_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Steel tariffs",
			breaks: [0.01, 0.04, 0.2, 0.4],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_3": {
			dataSource: "Cop_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Copper tariffs",
			breaks: [0.001, 0.004, 0.01, 0.04],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_3": {
			dataSource: "Lum_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Lumber tariffs",
			breaks: [0.009, 0.03, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_3": {
			dataSource: "Ene_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Energy tariffs",
			breaks: [0.009, 0.03, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_3": {
			dataSource: "CUSMA_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "non-CUSMA tariffs",
			breaks: [0.04, 0.1, 0.2, 0.5],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_B": {
			dataSource: "Total_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "All tariffs",
			breaks: [14,40,90,200],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_B": {
			dataSource: "Auto_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Automobile tariffs",
			breaks: [1,5,10,50],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_B": {
			dataSource: "Alum_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Aluminum tariffs",
			breaks: [3,10,30,100],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_B": {
			dataSource: "Steel_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Steel tariffs",
			breaks: [2,10,30,80],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_B": {
			dataSource: "Cop_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Copper tariffs",
			breaks: [0,1,5,10],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_B": {
			dataSource: "Lum_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Lumber tariffs",
			breaks: [0,2,5,10],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_B": {
			dataSource: "Ene_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Energy tariffs",
			breaks: [1,10,20,70],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_B": {
			dataSource: "CUSMA_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "non-CUSMA tariffs",
			breaks: [13,40,80,200],
			size: graduated_siz,
			colours: graduated_col,
			text: "Count of businesses directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_E": {
			dataSource: "Total_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "All tariffs",
			breaks: [285,1000,3000,9000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_E": {
			dataSource: "Auto_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Automobile tariffs",
			breaks: [116,400,1000,4000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_E": {
			dataSource: "Alum_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Aluminum tariffs",
			breaks: [117,500,1000,3000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_E": {
			dataSource: "Steel_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Steel tariffs",
			breaks: [185,600,1000,4000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_E": {
			dataSource: "Cop_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Copper tariffs",
			breaks: [21,80,200,400],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_E": {
			dataSource: "Lum_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Lumber tariffs",
			breaks: [24,100,200,400],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_E": {
			dataSource: "Ene_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Energy tariffs",
			breaks: [99,400,900,2000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_E": {
			dataSource: "CUSMA_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "non-CUSMA tariffs",
			breaks: [244,800,2000,7000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_C": {
			dataSource: "Total_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "All tariffs",
			breaks: [138,300,500,900],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to all types of US Administration's Tariffs on Canada",
		},
		"Auto_C": {
			dataSource: "Auto_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Automobile tariffs",
			breaks: [28,80,200,300],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Automobile Tariffs on Canada",
		},
		"Alum_C": {
			dataSource: "Alum_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Aluminum tariffs",
			breaks: [43,100,200,400],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Aluminum Tariffs on Canada",
		},
		"Steel_C": {
			dataSource: "Steel_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Steel tariffs",
			breaks: [38,100,200,400],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Steel Tariffs on Canada",
		},
		"Cop_C": {
			dataSource: "Cop_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Copper tariffs",
			breaks: [4,10,20,60],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Copper Tariffs on Canada",
		},
		"Lum_C": {
			dataSource: "Lum_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Lumber tariffs",
			breaks: [15,50,100,300],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Lumber Tariffs on Canada",
		},
		"Ene_C": {
			dataSource: "Ene_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Energy tariffs",
			breaks: [36,100,300,600],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to US Administration's Energy Tariffs on Canada",
		},
		"CUSMA_C": {
			dataSource: "CUSMA_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "non-CUSMA tariffs",
			breaks: [136,300,500,900],
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
					{
						id: 'background',
						type: 'background',
						paint: {
							'background-color': '#fbfbfb'
						}
					},
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

			map.addControl(new maplibregl.NavigationControl({
				visualizePitch: true,
				visualizeRoll: true,
				showZoom: true,
				showCompass: true
			}));
			
			map.addSource('choropleth',{
				type: 'vector',
				url: 'pmtiles://' + choropleth,
			});

			map.addSource('centroids', {
				type: 'vector',
				url: 'pmtiles://' + centroids,
			});

			map.addSource('censusDivisions', {
				type: 'vector',
				url: 'pmtiles://' + censusDivisions,
			});

			map.addSource('ne_water', {
				type: 'geojson',
				data: 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_lakes.geojson'
			});

			map.addSource('ne_provincelines', {
				type: 'geojson',
				data: './geojson/province-state-lines.geojson'
			});

			map.addSource('provincepoints', {
				type: 'geojson',
				data: './geojson/province-points.geojson'
			});

			map.addSource('city_names', {
				type: 'geojson',
				data: './geojson/populated-places-canada.geojson'
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
				'id': 'land',
				'type': 'fill',
				'source': 'osm',
				'source-layer': 'land',
				'paint': {
					'fill-color': 'black',
					'fill-opacity': 0.02
				}
			});

			map.addLayer({
				'id': 'streets',
				'type': 'line',
				'source': 'osm',
				'source-layer': 'streets',
				'paint': {
					'line-color': 'black',
					'line-width': 1,
					'line-opacity': 0.04
				}
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

			const CUTOFF = 30000000; 

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
				minzoom: 11
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
					'fill-color': '#1E3765',
					'fill-opacity': 0.5,
				},
				'filter': ['==', 'ADADGUID', ''],
			});

			map.addLayer({
				id: 'boundaries',
				type: 'line',
				source: 'osm',
				'source-layer': 'boundaries',
				paint: {
					'line-color': '#D0D1C9',
					'line-width': 1
				}
			});

			map.addLayer({
				id: 'province_boundaries_case',
				type: 'line',
				source: 'ne_provincelines',
				paint: {
					'line-color': '#ffffff',
					'line-width': 3,
					'line-opacity': 0.5
				},
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
				paint: {
					'line-color': '#D0D1C9',
					'line-width': 1
				},
				maxzoom: 6
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

			

			map.addLayer({
				id: "city_names_big",
				type: "symbol",
				source: "city_names",
				layout: {
					"text-field": ["get", "name"],
					"text-font": ["Open Sans Regular"],
					
					"text-size": [
					"interpolate", ["linear"], ["zoom"],
						4, 10, 	
						10, 13  
					],
					"text-anchor": "center",
					"symbol-sort-key": ["get", "scalerank"]
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.8,
				},
				filter: ["<", ["get", "scalerank"], 5],
				minzoom: 2,
				maxzoom: 6,
			});

			map.addLayer({
				id: "city_names_all",
				type: "symbol",
				source: "city_names",
				layout: {
					"text-field": ["get", "name"],
					"text-font": ["Open Sans Regular"],
					
					"text-size": [
					"interpolate", ["linear"], ["zoom"],
						4, 10, 	
						10, 13  
					],
					"text-anchor": "center",
					"symbol-sort-key": ["get", "scalerank"]
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.8,
				},
				minzoom: 6,
				maxzoom: 8,
			});

			

			map.addLayer({
				id: "place_labels_big",
				type: "symbol",
				source: "osm",
				"source-layer": "place_labels",
				layout: {
					"text-field": ["get", "name"],
					"text-font": ["Open Sans Regular"],
					
					"text-size": [
					"interpolate", ["linear"], ["zoom"],
						4, 10, 	
						10, 13  
					],
					"text-anchor": "center"
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.8,
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
					
					"text-size": [
					"interpolate", ["linear"], ["zoom"],
						4, 9, 	
						10, 11  
					],
					"text-anchor": "center"
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.65,
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
					"text-size": [
					"interpolate", ["linear"], ["zoom"],
						4, 14, 	
						10, 16  
					],
					"text-anchor": "center",
					"symbol-sort-key": ["get", "scalerank"]
				},
				paint: {
					"text-color": "#333333",
					"text-halo-color": "#fff",
					"text-halo-width": 1.5,
					"text-opacity": 0.8,
				},
				minzoom: 2,
				maxzoom: 6,
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


	const NOMINATIM_URL = "https://nominatim.openstreetmap.org/search?format=jsonv2&q=";
	const getResults = async () => {
		let inputQuery = addressQuery.endsWith("Canada") || addressQuery.endsWith("CA") || addressQuery.endsWith("Can") 
			? addressQuery 
			: addressQuery + ", Canada";

		addressResults = await fetch(NOMINATIM_URL + inputQuery).then((res) => res.json());

		if (addressResults.length > 0) {

			const { lat, lon } = addressResults[0];

			map.flyTo({
				center: [lon, lat],
				zoom: 11,
				bearing: 0,
				speed: 2,
				curve: 1,
				easing(t) { return t; },
				essential: true,
			});

		}

	}


	let mouseX = 0;
	let mouseY = 0;

	function handleMouseMove(event) {
		const mapEl = document.getElementById("map");
		const rect = mapEl.getBoundingClientRect();

		// Mouse coordinates relative to the map
		let x = event.clientX - rect.left;
		let y = event.clientY - rect.top;

		const tooltipEl = document.getElementById("map-tooltip");
		const tooltipWidth = tooltipEl ? tooltipEl.offsetWidth : 150; // fallback width
		const tooltipHeight = tooltipEl ? tooltipEl.offsetHeight : 30;

		// Clamp tooltip inside map bounds
		mouseX = Math.min(x + 10, mapEl.clientWidth - tooltipWidth - 5);
		mouseY = Math.min(y + 10, mapEl.clientHeight - tooltipHeight - 5);
	}

	onMount(() => {
		const mapEl = document.getElementById("map");
		mapEl.addEventListener("mousemove", handleMouseMove);

		return () => mapEl.removeEventListener("mousemove", handleMouseMove);
	});

</script>



<div id="container">

	<div id="panel">

		<div class="logo-container">

			<a href="https://schoolofcities.utoronto.ca/" target="_blank" class="logo-link">
				
				<img src={logoBlueColour} alt="UofT and School of Cities logos" class="logo" />

			</a>

			<a href="./" target="_blank" class="research-link">Mapping Tariffs</a>

		</div>

		<h2>Mapping potential direct exposure of U.S. tariffs in Canada</h2>
		<p style="font-size: 14px; margin-top: -0px;"><i>August 2025</i></p>
		

		<div id = "select-wrapper">
			<div id="destext">
				<p style="margin-bottom: -5px;">Select the tariff industry:</p>
			</div>
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

		<div id="destext">
		<p style="margin-bottom: -5px;">
			Show exposure by the number of businesses, employees based on where they work, or employees based on their home location:
		</p>
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

		<div id="destext">
		<p style="margin-bottom: -5px;">
			Show exposure as the total businesses or employees, or as a percent of all within the area:
		</p>
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
				Total
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
	
						<text class="legend-label" text-anchor="middle" x="85" y="35">&lt;{(dataLayers[mapSelected].breaks[0]*100).toFixed(1)}%</text>
						<text class="legend-label" text-anchor="middle" x="150" y="35">{(dataLayers[mapSelected].breaks[1]*100).toFixed(0)}%</text>
						<text class="legend-label" text-anchor="middle" x="215" y="35">{(dataLayers[mapSelected].breaks[2]*100).toFixed(0)}%</text>
						<text class="legend-label" text-anchor="middle" x="280" y="35">&gt{(dataLayers[mapSelected].breaks[3]*100).toFixed(0)}%</text>
					</svg>
				</div>

			{:else if dataLayers[mapSelected]?.metricType === "Count" && dataLayers[mapSelected]?.colours}
				<div id="destext">
					<p>
						{dataLayers[mapSelected]?.text}
					</p></div>

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
			<h4 style="margin-bottom: 0px;">Data Sources</h4>
			<p>
				Layers on this map were created via combinding source data from
				the list of HS Codes for products tariffed by the US from HTS Chapter 98, HTS Chapter 99 and US Federal Register for Duties on Softwood Lumber (from August 2025). 2025 Canadian HS8-NAICS Concordance Table (Statistics Canada). Province/Territory 2024 Annual Export Data to the World at HS6 level (Statistics Canada). Canadian Business Registry (Statistics Canada, December 2022). And the 2021 Canadian Census (Statistics Canada). 
			</p>
			<p>
				For detailed data descriptions, download links, and processing steps, please read our <a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file" target="_blank">data and methodology page</a>. The data processing and geospatial analysis was led by <a href="https://mkbs-mkbs2000.github.io/Personal-Portfolio/">Muhammad Khalis Bin Samion</a> and design of this interactive map was led by <a href="https://jamaps.github.io/" target="_blank">Jeff Allen</a>.
			</p>
			<br>
			<br>
		</div>
		
	
	</div>
	
	<div id="map">

		<div id="searchbar">

			<input 
				id="address-search" 
				bind:value={addressQuery} 
				placeholder="Search and fly to a location..." 
				on:keydown={(e) => {
					if (e.key === 'Enter' && addressQuery.length > 0) {
					getResults();
					}
				}}
			/>
			
			<button 
				id="address-button" 
				on:click={getResults} 
				disabled={addressQuery.length < 1}
			>
				Search
			</button>

			{#if selectedValue}
				<div
				id="map-tooltip"
				style="top: {mouseY + 10}px; left: {mouseX + 10}px;"
				>
				{selectedValue}
				</div>
			{/if}

		</div>

	</div>

	

</div>


<style>

	#container {
		display: flex;
		height: 100vh;
		overflow: hidden;
		position: relative;
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

	.research-link:hover {
		color: var(--brandMedGreen);
	}


	#panel h2 {
		margin-top: 0px;
		font-size: 28px;
		line-height: 36px;
	}

	

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

	.des {
		margin-top: 20px;
		border-top: solid 1px var(--brandGray);
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
		font-size: 14px;
		fill: #000000;
		font: OpenSans;
	}

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


	#map {
		flex: 1;
		height: 100vh;
		overflow: hidden;
		background-color: #ffffff;
		z-index: 0;
		position: relative;
	}

	#searchbar {
		position: absolute;
		top: 10px;
		left: 10px;
		z-index: 999;
	}

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

	#address-button:hover:enabled {
		background-color: var(--brandLightBlue);
	}

	#address-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

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

</style>