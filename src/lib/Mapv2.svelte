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

	let addressQuery="";
	let addressResults="";

	// **Change these to have the .gz extension after .pmtiles for deployment**

	// ADA pmtiles (ada_all contains both LumOld and LumNew data)
	let choropleth_ada = "/pmtiles/ada_all/v2/choropleth_z11.pmtiles";
	let centroids_ada = "/pmtiles/ada_all/v2/centroids.pmtiles";

	// CSD pmtiles (csd_all contains both LumOld and LumNew data)
	let choropleth_csd = "/pmtiles/csd_all/v2/choropleth_csd.pmtiles";
	let centroids_csd = "/pmtiles/csd_all/v2/centroids_csd.pmtiles";
	let censusDivisions = "/pmtiles/census-divisions.pmtiles";

	let graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];
	let graduated_siz = [5, 9, 15, 24, 34];

	let metricType = "Percent"; // ["Percent", "Count"]
	function metricSelect(value) {
		metricType = value;
	}

	let geoType = "ADA"; // ["ADA", "CSD"]
	function geoTypeSelect(value) {
		geoType = value;
	}

	let impactType = "Business" // ["EmployeeHome","EmployeeWork", "Business"] 
	function impactTypeSelect(value) {
		impactType = value;
	}

	let tariffType = "All goods subject to tariffs" // see full list below
	function tariffTypeSelect(event) {
		const raw = event.detail.value;
		if (raw === "Motorcycles and broader auto parts") {
			tariffType = "Motor";
		} else {
			tariffType = raw;
		}
	}

	// Maps the internal dataLayers tariffType value to the label shown in the dropdown
	const tariffLabelMap = {
		"Motor": "Motorcycles and broader auto parts"
	};

	// Reactive: what the Select component should display, given the current internal tariffType
	$: selectedTariffLabel = tariffLabelMap[tariffType] ?? tariffType;


	const selectTariffList = ["All goods subject to tariffs", "Automobiles", "Aluminum", "Steel", "Copper", "Lumber (before Oct 14)", "Lumber (after Oct 14)", "Trucks (Medium & Heavy Duty Vehicles)", "Dairy", "Alcohol", "Motorcycles and broader auto parts", "Energy and natural resources", "Non-CUSMA-Compliant"]; 

	

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
			map.getLayer("polygons_csd") &&
			map.getLayer("centroids") &&
			map.getLayer("centroids_csd")
		) {
			if (mapSelected) {
				const useCSD = geoType === "CSD";
				
				// Determine active layers based on geoType
				let activePolygonLayer, activeCentroidLayer, activeOutlineLayer;
				if (useCSD) {
					activePolygonLayer = 'polygons_csd';
					activeCentroidLayer = 'centroids_csd';
					activeOutlineLayer = 'outline-hover-csd';
					map.setPaintProperty('outline', 'line-opacity', 0.05); // changes appearance of ADA boundaries
				} else {
					activePolygonLayer = 'polygons';
					activeCentroidLayer = 'centroids';
					activeOutlineLayer = 'outline-hover';
					map.setPaintProperty('outline', 'line-opacity', 0.2);  // changes appearance of ADA boundaries
				}
				
				// All polygon/centroid layers
				const allPolygonLayers = ['polygons', 'polygons_csd'];
				const allCentroidLayers = ['centroids', 'centroids_csd'];
				const allOutlineLayers = ['outline-hover', 'outline-hover-csd'];
				const guidField = useCSD ? 'CSDDGUID' : 'ADADGUID';

				// Hide all outline layers
				allOutlineLayers.forEach(layer => {
					if (map.getLayer(layer)) {
						const field = layer.includes('csd') ? 'CSDDGUID' : 'ADADGUID';
						map.setFilter(layer, ['==', field, '']);
					}
				});

				if (mapQuery.metricType === "Percent") {
					// Hide all polygon/centroid layers, then show active
					allPolygonLayers.forEach(layer => map.setLayoutProperty(layer, 'visibility', 'none'));
					allCentroidLayers.forEach(layer => map.setLayoutProperty(layer, 'visibility', 'none'));
					map.setLayoutProperty(activePolygonLayer, 'visibility', 'visible');

				map.setPaintProperty(activePolygonLayer, "fill-opacity", 0.8);					map.setPaintProperty(activePolygonLayer, "fill-color", [
						"case",
						["==", ["get", dataLayers[mapSelected].dataSource], null], "#D0D1C9",
						["step", ["get", dataLayers[mapSelected].dataSource],
						dataLayers[mapSelected].colours[0], dataLayers[mapSelected].breaks[0],
						dataLayers[mapSelected].colours[1], dataLayers[mapSelected].breaks[1],
						dataLayers[mapSelected].colours[2], dataLayers[mapSelected].breaks[2],
						dataLayers[mapSelected].colours[3], dataLayers[mapSelected].breaks[3],
						dataLayers[mapSelected].colours[4]],
					]);

				} else if (mapQuery.metricType === "Count") {
					// Hide all polygon/centroid layers, then show active
					allPolygonLayers.forEach(layer => map.setLayoutProperty(layer, 'visibility', 'none'));
					allCentroidLayers.forEach(layer => map.setLayoutProperty(layer, 'visibility', 'none'));
					map.setLayoutProperty(activeCentroidLayer, 'visibility', 'visible');

					map.setPaintProperty(activeCentroidLayer, "circle-opacity", 0.5);
					map.setPaintProperty(activeCentroidLayer, "circle-stroke-width", 1);
					map.setPaintProperty(activeCentroidLayer, "circle-stroke-opacity", 0.75);

					map.setPaintProperty(activeCentroidLayer, "circle-color", [
						"case",
						["==", ["get", dataLayers[mapSelected].dataSource], null], "rgba(0,0,0,0)",
						["==", ["get", dataLayers[mapSelected].dataSource], 0], "rgba(0,0,0,0)",
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].colours[4],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].colours[3],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[1]], dataLayers[mapSelected].colours[2],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[0]], dataLayers[mapSelected].colours[1],
						dataLayers[mapSelected].colours[0],
					]);

					map.setPaintProperty(activeCentroidLayer, "circle-stroke-color", [
						"case",
						["==", ["get", dataLayers[mapSelected].dataSource], null], "rgba(0,0,0,0)",
						["==", ["get", dataLayers[mapSelected].dataSource], 0], "rgba(0,0,0,0)",
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].colours[4],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].colours[3],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[1]], dataLayers[mapSelected].colours[2],
						[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[0]], dataLayers[mapSelected].colours[1],
						dataLayers[mapSelected].colours[0],
					]);

					map.setPaintProperty(activeCentroidLayer, "circle-radius", [
						"interpolate", ["linear"], ["zoom"],
						3, [
							"case",
							[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].size[4],
							[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].size[3],
							0.5
						],
						7.9999, [
							"case",
							[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].size[4],
							[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].size[3],
							0.5
						],
						8, [
							"case",
							[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[3]], dataLayers[mapSelected].size[4],
							[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[2]], dataLayers[mapSelected].size[3],
							[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[1]], dataLayers[mapSelected].size[2],
							[">", ["get", dataLayers[mapSelected].dataSource], dataLayers[mapSelected].breaks[0]], dataLayers[mapSelected].size[1],
							dataLayers[mapSelected].size[0],
						],
					]);

					map.setLayoutProperty(
						activeCentroidLayer,
						"circle-sort-key",
						["get", dataLayers[mapSelected].dataSource]
					);
					

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
		geoType;
		updateMap();
	}



	// all the data layers

	const dataLayers = {
		"Total_1": {
			dataSource: "Total_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "All goods subject to tariffs",
			breaks: [0.05, 0.1, 0.2, 0.3],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to all types of U.S. Administration's Tariffs on Canada",
		},
		"Auto_1": {
			dataSource: "Auto_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Automobiles",
			breaks: [0.01, 0.02, 0.03, 0.06],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Automobile Tariffs on Canada",
		},
		"Alum_1": {
			dataSource: "Alum_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Aluminum",
			breaks: [0.01, 0.02, 0.03, 0.05],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Aluminum Tariffs on Canada",
		},
		"Steel_1": {
			dataSource: "Steel_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Steel",
			breaks: [0.01, 0.02, 0.03, 0.07],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Steel Tariffs on Canada",
		},
		"Cop_1": {
			dataSource: "Cop_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Copper",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Copper Tariffs on Canada",
		},
		"LumOld_1": {
			dataSource: "LumOld_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Lumber (before Oct 14)",
			breaks: [0.01, 0.02, 0.07, 0.15],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
		},
		"LumNew_1": {
			dataSource: "LumNew_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Lumber (after Oct 14)",
			breaks: [0.01, 0.02, 0.07, 0.15],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
		},
		"MHDV_1": {
			dataSource: "MHDV_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Trucks (Medium & Heavy Duty Vehicles)",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Medium Heavy Duty Vehicles Tariffs on Canada",
		},
		"Dairy_1": {
			dataSource: "Dairy_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Dairy",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Dairy Tariffs on Canada",
		},
		"Alcohol_1": {
			dataSource: "Alcohol_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Alcohol",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Alcohol Tariffs on Canada",
		},
		"Motor_1": {
			dataSource: "Motor_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Motor",
			breaks: [0.01, 0.04, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Motor Tariffs on Canada",
		},
		"Ene_1": {
			dataSource: "Ene_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Energy and natural resources",
			breaks: [0.01, 0.02, 0.03, 0.08],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's Energy and natural resources tariffs on Canada",
		},
		"CUSMA_1": {
			dataSource: "CUSMA_1",
			metricType: "Percent",
			impactType: "Business",
			tariffType: "Non-CUSMA-Compliant",
			breaks: [0.05, 0.1, 0.2, 0.3],
			colours: graduated_col,
			text: "Estimated % of businesses directly exposed to U.S. Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_2": {
			dataSource: "Total_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "All goods subject to tariffs",
			breaks: [0.04, 0.1, 0.2, 0.4],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to all types of U.S. Administration's Tariffs on Canada",
		},
		"Auto_2": {
			dataSource: "Auto_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Automobiles",
			breaks: [0.01, 0.04, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Automobile Tariffs on Canada",
		},
		"Alum_2": {
			dataSource: "Alum_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Aluminum",
			breaks: [0.01, 0.05, 0.1, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Aluminum Tariffs on Canada",
		},
		"Steel_2": {
			dataSource: "Steel_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Steel",
			breaks: [0.01, 0.05, 0.1, 0.3],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Steel Tariffs on Canada",
		},
		"Cop_2": {
			dataSource: "Cop_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Copper",
			breaks: [0.01, 0.02, 0.04, 0.08],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Copper Tariffs on Canada",
		},
		"LumOld_2": {
			dataSource: "LumOld_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Lumber (before Oct 14)",
			breaks: [0.01, 0.05, 0.1, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
		},
		"LumNew_2": {
			dataSource: "LumNew_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Lumber (after Oct 14)",
			breaks: [0.01, 0.05, 0.1, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
		},
		"MHDV_2": {
			dataSource: "MHDV_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Trucks (Medium & Heavy Duty Vehicles)",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Medium Heavy Duty Vehicles Tariffs on Canada",
		},
		"Dairy_2": {
			dataSource: "Dairy_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Dairy",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Dairy Tariffs on Canada",
		},
		"Alcohol_2": {
			dataSource: "Alcohol_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Alcohol",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Alcohol Tariffs on Canada",
		},
		"Motor_2": {
			dataSource: "Motor_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Motor",
			breaks: [0.01, 0.04, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Motor Tariffs on Canada",
		},
		"Ene_2": {
			dataSource: "Ene_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Energy and natural resources",
			breaks: [0.01, 0.05, 0.1, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's Energy and natural resources tariffs on Canada",
		},
		"CUSMA_2": {
			dataSource: "CUSMA_2",
			metricType: "Percent",
			impactType: "EmployeeWork",
			tariffType: "Non-CUSMA-Compliant",
			breaks: [0.05, 0.1, 0.2, 0.4],
			colours: graduated_col,
			text: "Estimated % of employees (by work location) directly exposed to U.S. Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_3": {
			dataSource: "Total_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "All goods subject to tariffs",
			breaks: [0.05, 0.1, 0.2, 0.5],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to all types of U.S. Administration's Tariffs on Canada",
		},
		"Auto_3": {
			dataSource: "Auto_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Automobiles",
			breaks: [0.01, 0.02, 0.05, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Automobile Tariffs on Canada",
		},
		"Alum_3": {
			dataSource: "Alum_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Aluminum",
			breaks: [0.01, 0.03, 0.07, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Aluminum Tariffs on Canada",
		},
		"Steel_3": {
			dataSource: "Steel_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Steel",
			breaks: [0.01, 0.05, 0.1, 0.25],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Steel Tariffs on Canada",
		},
		"Cop_3": {
			dataSource: "Cop_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Copper",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Copper Tariffs on Canada",
		},
		"LumOld_3": {
			dataSource: "LumOld_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Lumber (before Oct 14)",
			breaks: [0.01, 0.03, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
		},
		"LumNew_3": {
			dataSource: "LumNew_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Lumber (after Oct 14)",
			breaks: [0.01, 0.03, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
		},
		"MHDV_3": {
			dataSource: "MHDV_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Trucks (Medium & Heavy Duty Vehicles)",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Medium Heavy Duty Vehicles Tariffs on Canada",
		},
		"Dairy_3": {
			dataSource: "Dairy_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Dairy",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Dairy Tariffs on Canada",
		},
		"Alcohol_3": {
			dataSource: "Alcohol_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Alcohol",
			breaks: [0.01, 0.02, 0.03, 0.04],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Alcohol Tariffs on Canada",
		},
		"Motor_3": {
			dataSource: "Motor_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Motor",
			breaks: [0.01, 0.04, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Motor Tariffs on Canada",
		},
		"Ene_3": {
			dataSource: "Ene_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Energy and natural resources",
			breaks: [0.01, 0.03, 0.08, 0.2],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's Energy and natural resources tariffs on Canada",
		},
		"CUSMA_3": {
			dataSource: "CUSMA_3",
			metricType: "Percent",
			impactType: "EmployeeHome",
			tariffType: "Non-CUSMA-Compliant",
			breaks: [0.05, 0.1, 0.2, 0.5],
			colours: graduated_col,
			text: "Estimated % of employees (by primary residence) directly exposed to U.S. Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_B": {
			dataSource: "Total_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "All goods subject to tariffs",
			breaks: [10,50,100,200],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to all types of U.S. Administration's Tariffs on Canada",
		},
		"Auto_B": {
			dataSource: "Auto_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Automobiles",
			breaks: [5,10,20,50],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Automobile Tariffs on Canada",
		},
		"Alum_B": {
			dataSource: "Alum_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Aluminum",
			breaks: [5,10,20,50],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Aluminum Tariffs on Canada",
		},
		"Steel_B": {
			dataSource: "Steel_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Steel",
			breaks: [5,10,20,50],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Steel Tariffs on Canada",
		},
		"Cop_B": {
			dataSource: "Cop_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Copper",
			breaks: [2,5,10,20],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Copper Tariffs on Canada",
		},
		"LumOld_B": {
			dataSource: "LumOld_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Lumber (before Oct 14)",
			breaks: [2,5,10,20],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
		},
		"LumNew_B": {
			dataSource: "LumNew_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Lumber (after Oct 14)",
			breaks: [2,5,10,20],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
		},
		"MHDV_B": {
			dataSource: "MHDV_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Trucks (Medium & Heavy Duty Vehicles)",
			breaks: [2,5,10,20],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Medium Heavy Duty Vehicles Tariffs on Canada",
		},
		"Dairy_B": {
			dataSource: "Dairy_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Dairy",
			breaks: [2,5,10,20],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Dairy Tariffs on Canada",
		},
		"Alcohol_B": {
			dataSource: "Alcohol_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Alcohol",
			breaks: [2,5,10,20],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Alcohol Tariffs on Canada",
		},
		"Motor_B": {
			dataSource: "Motor_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Motor",
			breaks: [10,50,100,200],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Motor Tariffs on Canada",
		},
		"Ene_B": {
			dataSource: "Ene_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Energy and natural resources",
			breaks: [5,10,20,50],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's Energy and natural resources tariffs on Canada",
		},
		"CUSMA_B": {
			dataSource: "CUSMA_B",
			metricType: "Count",
			impactType: "Business",
			tariffType: "Non-CUSMA-Compliant",
			breaks: [10,50,100,200],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of businesses directly exposed to U.S. Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_E": {
			dataSource: "Total_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "All goods subject to tariffs",
			breaks: [500,1000,2500,5000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to all types of U.S. Administration's Tariffs on Canada",
		},
		"Auto_E": {
			dataSource: "Auto_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Automobiles",
			breaks: [200,500,1000,2000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Automobile Tariffs on Canada",
		},
		"Alum_E": {
			dataSource: "Alum_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Aluminum",
			breaks:  [200,500,1000,2000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Aluminum Tariffs on Canada",
		},
		"Steel_E": {
			dataSource: "Steel_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Steel",
			breaks:  [200,500,1000,2000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Steel Tariffs on Canada",
		},
		"Cop_E": {
			dataSource: "Cop_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Copper",
			breaks:  [200,500,1000,2000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Copper Tariffs on Canada",
		},
		"LumOld_E": {
			dataSource: "LumOld_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Lumber (before Oct 14)",
			breaks: [25,100,250,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
		},
		"LumNew_E": {
			dataSource: "LumNew_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Lumber (after Oct 14)",
			breaks: [25,100,250,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
		},
		"MHDV_E": {
			dataSource: "MHDV_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Trucks (Medium & Heavy Duty Vehicles)",
			breaks: [50,100,250,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Medium Heavy Duty Vehicles Tariffs on Canada",
		},
		"Dairy_E": {
			dataSource: "Dairy_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Dairy",
			breaks: [25,100,250,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Dairy Tariffs on Canada",
		},
		"Alcohol_E": {
			dataSource: "Alcohol_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Alcohol",
			breaks: [25,100,250,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Alcohol Tariffs on Canada",
		},
		"Motor_E": {
			dataSource: "Motor_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Motor",
			breaks: [200,500,1000,2000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Motor Tariffs on Canada",
		},
		"Ene_E": {
			dataSource: "Ene_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Energy and natural resources",
			breaks: [50,100,250,1000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's Energy and natural resources tariffs on Canada",
		},
		"CUSMA_E": {
			dataSource: "CUSMA_E",
			metricType: "Count",
			impactType: "EmployeeWork",
			tariffType: "Non-CUSMA-Compliant",
			breaks: [500,1000,2500,5000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by work location) directly exposed to U.S. Administration's non-CUSMA Compliant Tariffs on Canada",
		},
		"Total_C": {
			dataSource: "Total_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "All goods subject to tariffs",
			breaks: [400,700,1000,1500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to all types of U.S. Administration's Tariffs on Canada",
		},
		"Auto_C": {
			dataSource: "Auto_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Automobiles",
			breaks: [50,100,250,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Automobile Tariffs on Canada",
		},
		"Alum_C": {
			dataSource: "Alum_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Aluminum",
			breaks: [50,100,250,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Aluminum Tariffs on Canada",
		},
		"Steel_C": {
			dataSource: "Steel_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Steel",
			breaks: [50,100,250,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Steel Tariffs on Canada",
		},
		"Cop_C": {
			dataSource: "Cop_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Copper",
			breaks: [10,25,50,100],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Copper Tariffs on Canada",
		},
		"LumOld_C": {
			dataSource: "LumOld_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Lumber (before Oct 14)",
			breaks: [25,100,200,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
		},
		"LumNew_C": {
			dataSource: "LumNew_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Lumber (after Oct 14)",
			breaks: [25,100,200,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
		},
		"MHDV_C": {
			dataSource: "MHDV_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Trucks (Medium & Heavy Duty Vehicles)",
			breaks: [25,100,200,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Medium Heavy Duty Vehicles Tariffs on Canada",
		},
		"Dairy_C": {
			dataSource: "Dairy_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Dairy",
			breaks: [25,100,200,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Dairy Tariffs on Canada",
		},
		"Alcohol_C": {
			dataSource: "Alcohol_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Alcohol",
			breaks: [25,100,200,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Alcohol Tariffs on Canada",
		},
		"Motor_C": {
			dataSource: "Motor_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Motor",
			breaks: [200,500,1000,2000],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Motor Tariffs on Canada",
		},
		"Ene_C": {
			dataSource: "Ene_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Energy and natural resources",
			breaks: [25,100,200,500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's Energy and natural resources tariffs on Canada",
		},
		"CUSMA_C": {
			dataSource: "CUSMA_C",
			metricType: "Count",
			impactType: "EmployeeHome",
			tariffType: "Non-CUSMA-Compliant",
			breaks: [400,700,1000,1500],
			size: graduated_siz,
			colours: graduated_col,
			text: "Estimated count of employees (by primary residence) directly exposed to U.S. Administration's non-CUSMA Compliant Tariffs on Canada",
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
			}),
  			'bottom-left');
			
			// ADA sources (ada_all - contains both LumOld and LumNew)
			map.addSource('choropleth',{
				type: 'vector',
				url: 'pmtiles://' + choropleth_ada,
			});

			map.addSource('centroids', {
				type: 'vector',
				url: 'pmtiles://' + centroids_ada,
			});

			// CSD sources (csd_all - contains both LumOld and LumNew)
			map.addSource('choropleth_csd',{
				type: 'vector',
				url: 'pmtiles://' + choropleth_csd,
			});

			map.addSource('centroids_csd', {
				type: 'vector',
				url: 'pmtiles://' + centroids_csd,
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
				'id': 'polygons_csd',
				'type': 'fill',
				'source': 'choropleth_csd',
				'source-layer': 'choropleth_csd',
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

			// map.addLayer({
			// 	'id': 'streets',
			// 	'type': 'line',
			// 	'source': 'osm',
			// 	'source-layer': 'streets',
			// 	'paint': {
			// 		'line-color': 'black',
			// 		'line-width': 1,
			// 		'line-opacity': 0.04
			// 	}
			// });

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
					'line-opacity': 0.15
				}
			});

			map.addLayer({
				id: 'outline-csd',
				type: 'line',
				source: 'choropleth_csd',
				'source-layer': 'choropleth_csd',
				paint: {
					'line-color': '#808080',
					'line-width': [
						'interpolate', ['linear'], ['zoom'],
						4, 0,  
						17, 3
					],
					'line-opacity': 0.4
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
				'id': 'outline-hover-csd',
				'type': 'fill',
				'source': 'choropleth_csd',
				'source-layer': 'choropleth_csd',
				'paint': {
					'fill-color': '#1E3765',
					'fill-opacity': 0.5,
				},
				'filter': ['==', 'CSDDGUID', ''],
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
					// "circle-sort-key": ["get", "Total_C"]
				}
			});

			map.addLayer({
				'id': 'centroids_csd',
				'type': 'circle',
				'source': 'centroids_csd',
				'source-layer': 'centroids_csd',
				'layout': {
					'visibility': 'none',
				}
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
			map.setLayerZoomRange('centroids_csd', 1, 12);

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

		const handlePolygonHover = (e) => {
			const now = performance.now();
			if (now - lastUpdate < 100) return; // Throttle updates to every 100ms
			lastUpdate = now;

			map.getCanvas().style.cursor = 'pointer';

			if (!e.features.length) return;

			const properties = e.features[0].properties;
			const useCSD = geoType === "CSD";
			const guidField = useCSD ? 'CSDDGUID' : 'ADADGUID';
			const currentZone = properties[guidField];

			if (currentZone !== selectedZone) {

				const dataSourceField = mapSelected && dataLayers[mapSelected] ? dataLayers[mapSelected].dataSource : null;
				const rawValue = dataSourceField ? properties[dataSourceField] : null;

				selectedValue = (rawValue != null && rawValue >= 0)
					? (rawValue * 100).toFixed(1) + '%'
					: "No Data";

				selectedZone = currentZone;

				// Clear all outline layers
				map.setFilter('outline-hover', ['==', 'ADADGUID', '']);
				map.setFilter('outline-hover-csd', ['==', 'CSDDGUID', '']);
				// Set active outline
				if (useCSD) {
					map.setFilter('outline-hover-csd', ['==', 'CSDDGUID', selectedZone]);
				} else {
					map.setFilter('outline-hover', ['==', 'ADADGUID', selectedZone]);
				}
			}
		};

		const handlePolygonLeave = () => {
			map.getCanvas().style.cursor = '';
			selectedZone = "";
			selectedValue = "";
			map.setFilter('outline-hover', ['==', 'ADADGUID', '']);
			map.setFilter('outline-hover-csd', ['==', 'CSDDGUID', '']);
		};

		map.on('mousemove', 'polygons', handlePolygonHover);
		map.on('mousemove', 'polygons_csd', handlePolygonHover);

		map.on('mouseleave', 'polygons', handlePolygonLeave);
		map.on('mouseleave', 'polygons_csd', handlePolygonLeave);

		const handleCentroidHover = (e) => {
			const now = performance.now();
			if (now - lastUpdate < 100) return; // Throttle updates to every 100ms
			lastUpdate = now;

			map.getCanvas().style.cursor = 'pointer';

			if (!e.features.length) return;

			const properties = e.features[0].properties;
			const useCSD = geoType === "CSD";
			const guidField = useCSD ? 'CSDDGUID' : 'ADADGUID';
			const currentZone = properties[guidField];

			if (currentZone !== selectedZone) {
				const dataSourceField = mapSelected && dataLayers[mapSelected] ? dataLayers[mapSelected].dataSource : null;
				const rawValue = dataSourceField ? properties[dataSourceField] : null;
				selectedValue = (rawValue != null && rawValue >= 0)
					? Math.round(rawValue).toLocaleString()
					: "No Data";

				selectedZone = currentZone;

				// Clear all outline layers
				map.setFilter('outline-hover', ['==', 'ADADGUID', '']);
				map.setFilter('outline-hover-csd', ['==', 'CSDDGUID', '']);
				// Set active outline
				if (useCSD) {
					map.setFilter('outline-hover-csd', ['==', 'CSDDGUID', selectedZone]);
				} else {
					map.setFilter('outline-hover', ['==', 'ADADGUID', selectedZone]);
				}
			}
		};

		map.on('mousemove', 'centroids', handleCentroidHover);
		map.on('mousemove', 'centroids_csd', handleCentroidHover);

		const handleCentroidLeave = () => {
			map.getCanvas().style.cursor = '';
			selectedZone = "";
			selectedValue = "";
			map.setFilter('outline-hover', ['==', 'ADADGUID', '']);
			map.setFilter('outline-hover-csd', ['==', 'CSDDGUID', '']);
		};

		map.on('mouseleave', 'centroids', handleCentroidLeave);
		map.on('mouseleave', 'centroids_csd', handleCentroidLeave);

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
		<p style="font-size: 14px; margin-top: 25px; line-height: 20px;">
			By <a href='https://mkbs-mkbs2000.github.io/Personal-Portfolio/' target='_blank'>Muhammad Khalis Bin Samion</a>, <a href='https://jamaps.github.io/' target='_blank'> Jeff Allen</a>, <a href="https://www.linkedin.com/in/yihoi-jung-0b95351b5/" target="_blank">Yihoi Jung</a>, <a href='https://discover.research.utoronto.ca/8035-tara-vinodrai' target='_blank'>Tara Vinodrai</a>, <a href='https://schoolofcities.utoronto.ca/people/karen-chapple/' target='_blank'>Karen Chapple</a>.<br>
			<i>First published October 2025. Updated August 2026.</i>
		</p>

		<div id = "select-wrapper">
			<div id="destext">
				<p style="margin-bottom: -5px;">Select the good/product subject to U.S. tariffs:</p>
			</div>
			<Select
				id = 'select'
				items = {selectTariffList}
				value = {selectedTariffLabel}
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
			Select an indicator:
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
			Choose how to display this indicator:
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

		<div id="destext">
		<p style="margin-bottom: -5px;">
			Choose geographic unit:
		</p>
		</div>
		<div class="button-group">
			<div
				class="toggle-button {geoType === 'ADA' ? 'selected' : ''}"
				on:click={() => geoTypeSelect("ADA")}
			>
				Aggregate dissemination areas
			</div>
			<div
				class="toggle-button {geoType === 'CSD' ? 'selected' : ''}"
				on:click={() => geoTypeSelect("CSD")}
			>
				Census subdivisions (municipalities)
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
					<svg width='500' height='40'>
						<rect
						class = "box"
						width="64"
						height="20"
						x="0"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[0]};"
						/>
	
						<rect
						class = "box"
						width="64"
						height="20"
						x="65"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[1]};"
						/>
	
						<rect
						class = "box"
						width="64"
						height="20"
						x="130"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[2]};"
						/>
	
						<rect
						class = "box"
						width="64"
						height="20"
						x="195"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[3]};"
						/>
	
						<rect
						class = "box"
						width="64"
						height="20"
						x="260"
						y="0"
						style="fill:{dataLayers[mapSelected].colours[4]};"
						/>

						<rect
							class = "box"
							width="64"
							height="20"
							x="340"
							y="0"
							style="fill:#D0D1C9;"
						/>
	
						<text class="legend-label" text-anchor="middle" x="65" y="35">&lt;{(dataLayers[mapSelected].breaks[0]*100).toFixed(0)}%</text>
						<text class="legend-label" text-anchor="middle" x="130" y="35">{(dataLayers[mapSelected].breaks[1]*100).toFixed(0)}%</text>
						<text class="legend-label" text-anchor="middle" x="195" y="35">{(dataLayers[mapSelected].breaks[2]*100).toFixed(0)}%</text>
						<text class="legend-label" text-anchor="middle" x="260" y="35">&gt{(dataLayers[mapSelected].breaks[3]*100).toFixed(0)}%</text>

						<text class="legend-label" text-anchor="middle" x="370" y="35">no data</text>
					</svg>
				</div>

			{:else if dataLayers[mapSelected]?.metricType === "Count" && dataLayers[mapSelected]?.colours}
				<div id="destext">
					<p>
						{dataLayers[mapSelected]?.text} (as of September 1, 2025)
					</p></div>

				<!--5, 7.5, 10, 20, 40--> 

				<div id="legend">
					<svg width='350' height='200'>
						<circle
							class="box"
							cx="55"
							cy="35"
							r="{dataLayers[mapSelected].size[4]}"
							fill="{dataLayers[mapSelected].colours[4]}"
							fill-opacity="0.5"
							stroke="{dataLayers[mapSelected].colours[4]}"
							stroke-width="1px"
						/>
						<circle
							class = "box"
							cx="55"
							cy="96"
							r="{dataLayers[mapSelected].size[3]}"
							fill="{dataLayers[mapSelected].colours[3]}"
							fill-opacity="0.5"
							stroke="{dataLayers[mapSelected].colours[3]}"
							stroke-width="1px"
						/>

						<circle
							class = "box"
							cx="55"
							cy="137"
							r="{dataLayers[mapSelected].size[2]}"
							fill="{dataLayers[mapSelected].colours[2]}"
							fill-opacity="0.5"
							stroke="{dataLayers[mapSelected].colours[2]}"
							stroke-width="1px"
						/>

						<circle
							class = "box"
							cx="55"
							cy="164"
							r="{dataLayers[mapSelected].size[1]}"
							fill="{dataLayers[mapSelected].colours[1]}"
							fill-opacity="0.5"
							stroke="{dataLayers[mapSelected].colours[1]}"
							stroke-width="1px"
						/>

						{#if dataLayers[mapSelected].breaks[0] !== 0}
						<circle
							class = "box"
							cx="55"
							cy="182"
							r="{dataLayers[mapSelected].size[0]}"
							fill="{dataLayers[mapSelected].colours[0]}"
							fill-opacity="0.5"
							stroke="{dataLayers[mapSelected].colours[0]}"
							stroke-width="1px"
						/>
						{/if}

						<text class="legend-label" x="100" y="35" dy="0.35em">&gt;{dataLayers[mapSelected].breaks[3]}</text>
						<text class="legend-label" x="100" y="96" dy="0.35em">{dataLayers[mapSelected].breaks[2] + 1} - {dataLayers[mapSelected].breaks[3]}</text>
						<text class="legend-label" x="100" y="137" dy="0.35em">{dataLayers[mapSelected].breaks[1] + 1} - {dataLayers[mapSelected].breaks[2]}</text>
						<text class="legend-label" x="100" y="160" dy="0.35em">{dataLayers[mapSelected].breaks[0] + 1} - {dataLayers[mapSelected].breaks[1]}</text>
						{#if dataLayers[mapSelected].breaks[0] !== 0}<text class="legend-label" x="100" y="182" dy="0.35em">&le;{dataLayers[mapSelected].breaks[0]}</text>{/if}
					</svg>
				</div>

			{/if}
		</div>

		<div id="hovered-zone" >
			<i>Hovered zone</i>: {@html selectedValue ? '<strong>' + selectedValue + '</strong>' : 'No data available'}
		</div>


		<div class="datadetail">

			<p>
				Counts of Employment (home) data are based on estimates from the 2021 Census of Population. Counts of Businesses and Employment (place of work) and are based on estimates from the Canadian Business Register (December 2022).
			</p>
			
			<h4 style="margin-bottom: 0px;">Data sources</h4>
			<p>
				All layers on this map are based on tariffs as of September 1, 2025, except for the Lumber and Medium  layers, which were updated in November 25, 2025.
			</p>
			<p>
				Layers on this map were created by combining data from the following sources:
			</p>
			<ul>
				<li>Canadian Business Registry (Statistics Canada)</li>
				<li>Canadian Chamber of Commerce</li>
				<li>Canadian Census of Population (Statistics Canada)</li>
				<li>Canadian International Merchandise Trade Web Application (Statistics Canada Catalogue No. 71-607-X2021004)</li>
				<li>Cargo Systems Messaging Service (United States Customs and Border Protection)</li>
				<li>Harmonized Tariff Schedule of the United States (United States International Trade Commission )</li>
				<li>International Trade and Development Division (Statistics Canada)</li>
				<li>U.S. Department of Commerce</li>
				<li>U.S. Census Bureau</li>
			</ul>
			<p>
				For detailed data descriptions, download links, and processing steps, please read our <a href="https://github.com/schoolofcities/tariffs?tab=readme-ov-file" target="_blank">data and methodology page</a>
			</p>
			<!-- <h4 style="margin-bottom: 0px;">
				Project team:
			</h4>
			<p>
				- Data processing and analysis: <a href="https://mkbs-mkbs2000.github.io/Personal-Portfolio/">Muhammad Khalis Bin Samion</a>.
				<br>
				- Interactive map and website design: <a href="https://jamaps.github.io/" target="_blank">Jeff Allen</a>.
				<br>
				- Data modelling scenarios: Rick DiFrancesco and Eli Easton
				<br>
				- Scientific direction: Karen Chapple and Tara Vinodrai
			</p> -->
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
		#container {
			flex-direction: column; 
		}

		#map {
			order: -1; 
			height: 50vh; 
			border-bottom: solid 1px var(--brandDarkBlue);
		}

		#panel {
			max-width: 420px;
			min-width: 360px; 
			width: 100%; 
			height: 50vh;
			border-right: none;
			margin: 0 auto;
		}
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

	.datadetail ul {
		margin-top: -10px;
		margin-bottom: -10px;
		margin-left: -28px;
		list-style-type: circle;
	}

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

	a {
		color: var(--brandBlack);
		text-decoration: underline;
		font-family: SourceSerif;
	}

		a:hover {
		color: var(--brandMedGreen);
	}

</style>