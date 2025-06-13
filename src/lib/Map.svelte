<script>
    import { onMount } from "svelte";
    import maplibregl from "maplibre-gl";
    import "../assets/styles.css";
    import "maplibre-gl/dist/maplibre-gl.css";
    import * as pmtiles from "pmtiles";
    import Select from "svelte-select";

    const protocol = new pmtiles.Protocol();
    maplibregl.addProtocol('pmtiles', protocol.tile);

    let map;

    let work_side = "work_side.pmtiles";

    let ADA_cent = "ADA_centroids.pmtiles";

    let background = "background.pmtiles";
    
    let graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];

    let graduated_siz = [5, 7.5, 10, 20, 40];

    let defaultMap = "All Tariffs (% of Businesses)";

    let mapSelected = defaultMap;

    const choropleths = {
        "All Tariffs (% of Businesses)": {
            dataSource: "Total_B_pc",
            breaks: [0.0037, 0.0104, 0.0257, 0.0667],
            colours: graduated_col,
            text: "% of businesses directly affected by all types of US Administration's Tariffs on Canada",
        },
        "All Tariffs (% of Employees)": {
            dataSource: "Total_E_pc",
            breaks: [0.017, 0.057, 0.124, 0.26],
            colours: graduated_col,
            text: "Estimated % of employees directly affected by all types of US Administration's Tariffs on Canada",
        },
        "Tariffs on Automobiles (% of Businesses)": {
            dataSource: "Auto_B_pct",
            breaks: [0.00017, 0.00076, 0.00146, 0.00322],
            colours: graduated_col,
            text: "% of businesses directly affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Automobiles (% of Employees)": {
            dataSource: "Auto_E_pct",
            breaks: [0.0012, 0.0086, 0.0505, 0.1012],
            colours: graduated_col,
            text: "Estimated % of employees directly affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Aluminum (% of Businesses)": {
            dataSource: "Aluminum_1",
            breaks: [0.002, 0.006, 0.0131, 0.0287],
            colours: graduated_col,
            text: "% of businesses directly affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Aluminum (% of Employees)": {
            dataSource: "Aluminum_2",
            breaks: [0.012, 0.045, 0.103, 0.207],
            colours: graduated_col,
            text: "Estimated % of employees directly affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Steel (% of Businesses)": {
            dataSource: "Steel_B_pc",
            breaks: [0.0011, 0.0037, 0.0092, 0.0357],
            colours: graduated_col,
            text: "% of businesses directly affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Steel (% of Employees)": {
            dataSource: "Steel_E_pc",
            breaks: [0.0064, 0.0246, 0.0671, 0.2244],
            colours: graduated_col,
            text: "Estimated % of employees directly affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Lumber (% of Businesses)": {
            dataSource: "Lumber_B_p",
            breaks: [0.0013, 0.0045, 0.0156, 0.0556],
            colours: graduated_col,
            text: "% of businesses directly affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Lumber (% of Employees)": {
            dataSource: "Lumber_E_p",
            breaks: [0.0061, 0.0226, 0.057, 0.1834],
            colours: graduated_col,
            text: "Estimated % of employees directly affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (% of Businesses)": {
            dataSource: "Energy_B_p",
            breaks: [0.0004, 0.00128, 0.00257, 0.00614],
            colours: graduated_col,
            text: "% of businesses directly affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (% of Employees)": {
            dataSource: "Energy_E_p",
            breaks: [0.0056, 0.0296, 0.0696, 0.3205],
            colours: graduated_col,
            text: "Estimated % of employees directly affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (% of Businesses)": {
            dataSource: "nonCUSMA_1",
            breaks: [0.00064, 0.00206, 0.00457, 0.01283],
            colours: graduated_col,
            text: "% of businesses directly affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (% of Employees)": {
            dataSource: "nonCUSMA_2",
            breaks: [0.0086, 0.0349, 0.0856, 0.1958],
            colours: graduated_col,
            text: "Estimated % of employees directly affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
    };

    const circleSize = {
        "All Tariffs (Count of Businesses)": {
            dataSource: "Total_B",
            breaks: [127, 765, 1990, 7309],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses directly affected by all types of US Administration's Tariffs on Canada",
        },
        "All Tariffs (Count of Employees)": {
            dataSource: "Total_E",
            breaks: [5871, 27500, 82127, 211116],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees directly affected by all types of US Administration's Tariffs on Canada",
        },
        "Tariffs on Automobiles (Count of Businesses)": {
            dataSource: "Auto_B",
            breaks: [5, 16, 31, 142],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses directly affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Automobiles (Count of Employees)": {
            dataSource: "Auto_E",
            breaks: [30, 805, 4400, 7700],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees directly affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Aluminum (Count of Businesses)": {
            dataSource: "Aluminum_B",
            breaks: [85, 558, 1672, 5061],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses directly affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Aluminum (Count of Employees)": {
            dataSource: "Aluminum_E",
            breaks: [6439, 32663, 75072, 146906],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees directly affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Steel (Count of Businesses)": {
            dataSource: "Steel_B",
            breaks: [48, 271, 806, 2586],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses directly affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Steel (Count of Employees)": {
            dataSource: "Steel_E",
            breaks: [1284, 5867, 17711, 51468],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees directly affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Lumber (Count of Businesses)": {
            dataSource: "Lumber_B",
            breaks: [16, 61, 195, 858],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses directly affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Lumber (Count of Employees)": {
            dataSource: "Lumber_E",
            breaks: [875, 3300, 7162, 19095],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees directly affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (Count of Businesses)": {
            dataSource: "Energy_B",
            breaks: [5, 19, 46, 131],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses directly affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (Count of Employees)": {
            dataSource: "Energy_E",
            breaks: [1440, 5250, 12000, 26620],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees directly affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (Count of Businesses)": {
            dataSource: "nonCUSMA_B",
            breaks: [20, 96, 277, 910],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses directly affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (Count of Employees)": {
            dataSource: "nonCUSMA_E",
            breaks: [2100, 9426, 26875, 55160],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees directly affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
    };
    
    function choroSet(layer) {
        let choropleth = choropleths[layer];
        console.log(choropleth);

        map.setPaintProperty("polygons", "fill-opacity", 0.8);

        map.setPaintProperty("polygons", "fill-color", [
            "case",
            ["==", ["get", choropleth.dataSource], null], "rgba(0,0,0,0)",
            ["step", ["get", choropleth.dataSource],
            choropleth.colours[0], choropleth.breaks[0],
            choropleth.colours[1], choropleth.breaks[1],
            choropleth.colours[2], choropleth.breaks[2],
            choropleth.colours[3], choropleth.breaks[3],
            choropleth.colours[4]],
        ]);
    };

    function circleSet(layer) {
        let circle = circleSize[layer];
        console.log(circle);

        map.setPaintProperty("centroids", "circle-opacity", 0.8);

        map.setPaintProperty("centroids", "circle-color", [
            "case",
            ["==", ["get", circle.dataSource], null], "rgba(0,0,0,0)",
            ["==", ["get", circle.dataSource], 0], "rgba(0,0,0,0)",
            [">", ["get", circle.dataSource], circle.breaks[3]], circle.colours[4],
            [">", ["get", circle.dataSource], circle.breaks[2]], circle.colours[3],
            [">", ["get", circle.dataSource], circle.breaks[1]], circle.colours[2],
            [">", ["get", circle.dataSource], circle.breaks[0]], circle.colours[1],
            circle.colours[0],
        ]);

        map.setPaintProperty("centroids", "circle-radius", [
            "interpolate", ["linear"], ["zoom"],
            3, [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]], circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]], circle.size[3],
                0
            ],
            8, [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]], circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]], circle.size[3],
                [">", ["get", circle.dataSource], circle.breaks[1]], circle.size[2],
                0
            ],
            11, [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]], circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]], circle.size[3],
                [">", ["get", circle.dataSource], circle.breaks[1]], circle.size[2],
                [">", ["get", circle.dataSource], circle.breaks[0]], circle.size[1],
                circle.size[0],
            ],
        ]);
    };

    let estimatedPct = false;
    let estimatedCount = false;
    let items;

    function toggleViz(event) {
        const id = event.target.id;
        if (id === 'pctcheck' && estimatedPct) {
            estimatedCount = false;
            items = Object.keys(choropleths);
            mapSelected = items[0];
        } else if (id === 'countcheck' && estimatedCount) {
            estimatedPct = false;
            items = Object.keys(circleSize);
            mapSelected = items[0];
        }

        if (estimatedPct) {
            map.setLayoutProperty('polygons', 'visibility', 'visible');
            map.setLayoutProperty('centroids', 'visibility', 'none');
            choroSet(mapSelected);
        } else if (estimatedCount) {
            map.setLayoutProperty('polygons', 'visibility', 'none');
            map.setLayoutProperty('centroids', 'visibility', 'visible');
            circleSet(mapSelected);
        } else {
            map.setLayoutProperty('polygons', 'visibility', 'none');
            map.setLayoutProperty('centroids', 'visibility', 'none');
        }
    };

    function layerSelect(e) {
        mapSelected = e.detail.value;
        if (estimatedPct) {
            choroSet(mapSelected);
        } else if (estimatedCount) {
            circleSet(mapSelected);
        };
    };

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
                    'line-opacity': 0.5,
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

        map.once('styledata', () => {
            layerSelect();
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
                const dataField = choropleths[mapSelected]?.dataSource;

                const rawValue = properties[dataField];

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
                const dataField = circleSize[mapSelected]?.dataSource;

                const rawValue = properties[dataField];

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

        <h1>Impact of US Administration's Tariffs on Canada</h1>
        
        <h2>Mapping information about the direct impacts of tariffs across Canada at the aggregate dissemination area level</h2>

        <div id="checkbox" class="check-box">
			<label class="label-format"><input type="checkbox" id="pctcheck" class="check-box-item" bind:checked={estimatedPct} on:change={toggleViz}/> 
				Show estimated percentages
			</label>
			<br>
			<label class="label-format"><input type="checkbox" id="countcheck" class="check-box-item" bind:checked={estimatedCount} on:change={toggleViz}/> 
				Show estimated counts
			</label>
        </div>

        <div id = "select-wrapper">
            <Select
            id = 'select'
            items = {items}
            value = {mapSelected}
            clearable = {false}
            showChevron = {true}
            listAutoWidth = {true}
            searchable = {false}
            listOffset = {10}
            on:change = {layerSelect}
            />
        </div>

        <div>
            <div id="hovered-zone" style="padding: 4px; border: solid 1px #AB1368;">
                Hovered zone: {selectedValue || 'No data available'}
	        </div>
        </div>

        <div class="des">
            {#if estimatedPct && choropleths[mapSelected]?.colours}
                <div id="destext">{choropleths[mapSelected]?.text}</div>

                <div id="legend">
                    <svg width='350' height='40'>
			            <rect
			            class = "box"
			            width="64"
			            height="20"
			            x="20"
			            y="0"
			            style="fill:{choropleths[mapSelected].colours[0]};"
			            />
	
			            <rect
			            class = "box"
			            width="64"
			            height="20"
			            x="85"
			            y="0"
			            style="fill:{choropleths[mapSelected].colours[1]};"
			            />
	
			            <rect
			            class = "box"
			            width="64"
			            height="20"
			            x="150"
			            y="0"
			            style="fill:{choropleths[mapSelected].colours[2]};"
			            />
	
			            <rect
			            class = "box"
			            width="64"
			            height="20"
			            x="215"
			            y="0"
			            style="fill:{choropleths[mapSelected].colours[3]};"
			            />
	
			            <rect
			            class = "box"
			            width="64"
			            height="20"
			            x="280"
			            y="0"
			            style="fill:{choropleths[mapSelected].colours[4]};"
			            />
	
			            <text class="legend-label" text-anchor="middle" x="85" y="35">&lt;{(choropleths[mapSelected].breaks[0]*100).toFixed(2)}%</text>
			            <text class="legend-label" text-anchor="middle" x="150" y="35">{(choropleths[mapSelected].breaks[1]*100).toFixed(2)}%</text>
			            <text class="legend-label" text-anchor="middle" x="215" y="35">{(choropleths[mapSelected].breaks[2]*100).toFixed(2)}%</text>
			            <text class="legend-label" text-anchor="middle" x="280" y="35">&gt{(choropleths[mapSelected].breaks[3]*100).toFixed(2)}%</text>
		            </svg>
                </div>

            {:else if estimatedCount && circleSize[mapSelected]?.colours}
                <div id="destext">{circleSize[mapSelected]?.text}</div>

                <div id="legend">
                    <svg width='350' height='200'>
                        <circle
                        class = "box"
                        cx="55"
                        cy="10"
                        r="{circleSize[mapSelected].size[0]}"
                        style="fill:{circleSize[mapSelected].colours[0]};"
                        />

                        <circle
                        class = "box"
                        cx="55"
                        cy="32.5"
                        r="{circleSize[mapSelected].size[1]}"
                        style="fill:{circleSize[mapSelected].colours[1]};"
                        />

                        <circle
                        class = "box"
                        cx="55"
                        cy="55"
                        r="{circleSize[mapSelected].size[2]}"
                        style="fill:{circleSize[mapSelected].colours[2]};"
                        />

                        <circle
                        class = "box"
                        cx="55"
                        cy="90"
                        r="{circleSize[mapSelected].size[3]}"
                        style="fill:{circleSize[mapSelected].colours[3]};"
                        />

                        <circle
                        class = "box"
                        cx="55"
                        cy="150"
                        r="35"
                        style="fill:{circleSize[mapSelected].colours[4]};"
                        />

                        <text class="legend-label" x="100" y="10" dy="0.35em">&lt;{circleSize[mapSelected].breaks[0]}</text>
                        <text class="legend-label" x="100" y="32.5" dy="0.35em">{circleSize[mapSelected].breaks[0]} - {circleSize[mapSelected].breaks[1]}</text>
                        <text class="legend-label" x="100" y="55" dy="0.35em">{circleSize[mapSelected].breaks[1]} - {circleSize[mapSelected].breaks[2]}</text>
                        <text class="legend-label" x="100" y="90" dy="0.35em">{circleSize[mapSelected].breaks[2]} - {circleSize[mapSelected].breaks[3]}</text>
                        <text class="legend-label" x="100" y="150" dy="0.35em">&gt;{circleSize[mapSelected].breaks[3]}</text>
                    </svg>
                </div>

            {/if}
        </div>
    
    </div>
    
    <div id="map"></div>
</div>


<style>

    #panel {
		max-width: 420px;
		width: 100%;
		min-width: 350px;
		height: calc(100vh - 15px);
		overflow-y: auto;
		background-color: #ffffff;
		padding: 15px;
		border-right: solid 1px #DC4633;
		flex-shrink: 0;
	}

    #container {
        display: flex;
        height: 100vh;
        overflow: hidden;
    }

    #map {
        flex: 1;
        height: 100vh;
        overflow: hidden;
    }

    #select-wrapper {
        margin-top: 10px;
        margin-bottom: 10px;
    }

    #hovered-zone {
        margin-bottom: 10px;
    }

    #destext {
        margin-bottom: 10px;
    }

    .legend-label {
        font-size: 15px;
        fill: #000000;
    }

</style>