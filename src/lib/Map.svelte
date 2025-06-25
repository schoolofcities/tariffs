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

    let polygon = "work_pct.pmtiles";

    let centroid = "work_count.pmtiles";
    
    let graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];

    let graduated_siz = [5, 7.5, 10, 20, 40];

    let defaultMap = "All Tariffs (% of Businesses)";

    let mapSelected = defaultMap;

    const choropleths = {
        "All Tariffs (% of Businesses)": {
            dataSource: "Total_1",
            breaks: [0.003373, 0.009313, 0.024911, 0.058824],
            colours: graduated_col,
            text: "% of businesses within the ADA directly affected by all types of US Administration's Tariffs on Canada",
        },
        "All Tariffs (% of Employees)": {
            dataSource: "Total_2",
            breaks: [0.01593, 0.05325, 0.12301, 0.26468],
            colours: graduated_col,
            text: "Estimated % of employees working within the ADA that are directly affected by all types of US Administration's Tariffs on Canada",
        },
        "Tariffs on Automobiles (% of Businesses)": {
            dataSource: "Auto_1",
            breaks: [0.0002690, 0.0008795, 0.0015552, 0.0025907],
            colours: graduated_col,
            text: "% of businesses within the ADA directly affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Automobiles (% of Employees)": {
            dataSource: "Auto_2",
            breaks: [0.0007601, 0.0040214, 0.0408163, 0.0844206],
            colours: graduated_col,
            text: "Estimated % of employees working within the ADA that are directly affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Aluminum (% of Businesses)": {
            dataSource: "Alum_1",
            breaks: [0.001606, 0.004852, 0.010540, 0.023529],
            colours: graduated_col,
            text: "% of businesses within the ADA directly affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Aluminum (% of Employees)": {
            dataSource: "Alum_2",
            breaks: [0.01074, 0.03797, 0.08570, 0.17310],
            colours: graduated_col,
            text: "Estimated % of employees working within the ADA that are directly affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Steel (% of Businesses)": {
            dataSource: "Steel_1",
            breaks: [0.001008, 0.003396, 0.010204, 0.025210],
            colours: graduated_col,
            text: "% of businesses within the ADA directly affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Steel (% of Employees)": {
            dataSource: "Steel_2",
            breaks: [0.005952, 0.021349, 0.047185, 0.094637],
            colours: graduated_col,
            text: "Estimated % of employees working within the ADA that are directly affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Lumber (% of Businesses)": {
            dataSource: "Lumber_1",
            breaks: [0.001, 0.003663, 0.013699, 0.05],
            colours: graduated_col,
            text: "% of businesses within the ADA directly affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Lumber (% of Employees)": {
            dataSource: "Lumber_2",
            breaks: [0.005390, 0.019358, 0.048170, 0.155556],
            colours: graduated_col,
            text: "Estimated % of employees working within the ADA that are directly affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (% of Businesses)": {
            dataSource: "Energy_1",
            breaks: [0.0003789, 0.0012151, 0.002584, 0.0056818],
            colours: graduated_col,
            text: "% of businesses within the ADA directly affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (% of Employees)": {
            dataSource: "Energy_2",
            breaks: [0.01568, 0.05259, 0.11681, 0.22883],
            colours: graduated_col,
            text: "Estimated % of employees working within the ADA that are directly affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (% of Businesses)": {
            dataSource: "nonCUSMA_1",
            breaks: [0.0005841, 0.0019157, 0.0042918, 0.0196078],
            colours: graduated_col,
            text: "% of businesses within the ADA directly affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (% of Employees)": {
            dataSource: "nonCUSMA_2",
            breaks: [0.006887, 0.029499, 0.070126, 0.186407],
            colours: graduated_col,
            text: "Estimated % of employees working within the ADA that aredirectly affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
    };

    const circleSize = {
        "All Tariffs (Count of Businesses)": {
            dataSource: "Total_B",
            breaks: [4, 12, 36, 89],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses within the ADA directly affected by all types of US Administration's Tariffs on Canada",
        },
        "All Tariffs (Count of Employees)": {
            dataSource: "Total_E",
            breaks: [172, 583, 1365, 3271],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees working within the ADA that are directly affected by all types of US Administration's Tariffs on Canada",
        },
        "Tariffs on Automobiles (Count of Businesses)": {
            dataSource: "Auto_B",
            breaks: [0, 0, 0, 1],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses within the ADA directly affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Automobiles (Count of Employees)": {
            dataSource: "Auto_E",
            breaks: [0, 7, 150, 550],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees working within the ADA that are directly affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Aluminum (Count of Businesses)": {
            dataSource: "Aluminum_B",
            breaks: [2, 7, 22, 74],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses within the ADA directly affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Aluminum (Count of Employees)": {
            dataSource: "Aluminum_E",
            breaks: [129, 515, 1332, 2808],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees working within the ADA that are directly affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Steel (Count of Businesses)": {
            dataSource: "Steel_B",
            breaks: [0, 2, 7, 25],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses within the ADA directly affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Steel (Count of Employees)": {
            dataSource: "Steel_E",
            breaks: [51, 207, 438, 1250],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees working within the ADA that are directly affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Lumber (Count of Businesses)": {
            dataSource: "Lumber_B",
            breaks: [0, 1, 3, 10],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses within the ADA directly affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Lumber (Count of Employees)": {
            dataSource: "Lumber_E",
            breaks: [19, 60, 127, 265],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees working within the ADA that are directly affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (Count of Businesses)": {
            dataSource: "Energy_B",
            breaks: [0, 1, 2, 4],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses within the ADA directly affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (Count of Employees)": {
            dataSource: "Energy_E",
            breaks: [35, 192, 353, 1200],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees working within the ADA that are directly affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (Count of Businesses)": {
            dataSource: "nonCUSMA_B",
            breaks: [0, 1, 3, 7],
            size: graduated_siz,
            colours: graduated_col,
            text: "Count of businesses within the ADA directly affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (Count of Employees)": {
            dataSource: "nonCUSMA_E",
            breaks: [56, 225, 435, 700],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated count of employees working within the ADA that are directly affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
    };
    
    function choroSet(layer) {
        let choropleth = choropleths[layer];
        console.log(choropleth);

        map.setPaintProperty("polygons_work", "fill-opacity", 0.8);

        map.setPaintProperty("polygons_work", "fill-color", [
            "case",
            ["==", ["get", choropleth.dataSource], null], "rgba(0,0,0,0)",
            ["==", ["get", choropleth.dataSource], 0], "rgba(0,0,0,0)",
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

        map.setPaintProperty("centroids_work", "circle-opacity", 0.8);

        map.setPaintProperty("centroids_work", "circle-color", [
            "case",
            ["==", ["get", circle.dataSource], null], "rgba(0,0,0,0)",
            ["==", ["get", circle.dataSource], 0], "rgba(0,0,0,0)",
            [">", ["get", circle.dataSource], circle.breaks[3]], circle.colours[4],
            [">", ["get", circle.dataSource], circle.breaks[2]], circle.colours[3],
            [">", ["get", circle.dataSource], circle.breaks[1]], circle.colours[2],
            [">", ["get", circle.dataSource], circle.breaks[0]], circle.colours[1],
            circle.colours[0],
        ]);

        map.setPaintProperty("centroids_work", "circle-radius", [
            "interpolate", ["linear"], ["zoom"],
            3, [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]], circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]], circle.size[3],
                ["==", ["get", circle.dataSource], 0], 0,
                0
            ],
            8, [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]], circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]], circle.size[3],
                [">", ["get", circle.dataSource], circle.breaks[1]], circle.size[2],
                ["==", ["get", circle.dataSource], 0], 0,
                0
            ],
            11, [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]], circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]], circle.size[3],
                [">", ["get", circle.dataSource], circle.breaks[1]], circle.size[2],
                [">", ["get", circle.dataSource], circle.breaks[0]], circle.size[1],
                ["==", ["get", circle.dataSource], 0], 0,
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
            map.setLayoutProperty('polygons_work', 'visibility', 'visible');
            map.setLayoutProperty('centroids_work', 'visibility', 'none');
            choroSet(mapSelected);
        } else if (estimatedCount) {
            map.setLayoutProperty('polygons_work', 'visibility', 'none');
            map.setLayoutProperty('centroids_work', 'visibility', 'visible');
            circleSet(mapSelected);
        } else {
            map.setLayoutProperty('polygons_work', 'visibility', 'none');
            map.setLayoutProperty('centroids_work', 'visibility', 'none');
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
            //style: "https://demotiles.maplibre.org/style.json",
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
            
            map.addSource('work_polygons',{
                type: 'vector',
                url: 'pmtiles://' + polygon,
            });

            map.addSource('work_centroids', {
                type: 'vector',
                url: 'pmtiles://' + centroid,
            });

            map.addLayer({
                'id': 'polygons_work',
                'type': 'fill',
                'source': 'work_polygons',
                'source-layer': 'ADA_aggregates',
                'layout': {
                    'visibility': 'none',
                },
            });

            map.addLayer({
                'id': 'outline_work',
                'type': 'line',
                'source': 'work_polygons',
                'source-layer': 'ADA_aggregates',
                'paint': {
                    'line-color': '#808080',
                    'line-width': 1,
                    'line-opacity': 0.5,
                },
            });

            map.addLayer({
                'id': 'outline-hover-work',
                'type': 'fill',
                'source': 'work_polygons',
                'source-layer': 'ADA_aggregates',
                'paint': {
                    'fill-color': '#0000FF',
                    'fill-opacity': 0.5,
                },
                'filter': ['==', 'ADADGUID', ''],
            });
            
            map.addLayer({
                'id': 'centroids_work',
                'type': 'circle',
                'source': 'work_centroids',
                'source-layer': 'ADA_centroids',
                'layout': {
                    'visibility': 'none',
                },
            });
            
            map.setLayerZoomRange('centroids_work', 1, 12);

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
            layerSelect({ detail: { value: mapSelected } });
        });

        map.on('mousemove', 'polygons_work', (e) => {
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

                if (rawValue == null) {
                    selectedValue = "No Data";
                    selectedZone = "";
                    map.setFilter('outline-hover-work', ['==', 'ADADGUID', '']);
                    return;
                };

                selectedValue = (rawValue * 100).toFixed(2) + '%';

                selectedZone = currentZone;

                map.setFilter('outline-hover-work', ['==', 'ADADGUID', selectedZone]);
            }
        });

        map.on('mouseleave', 'polygons_work', () => {
            map.getCanvas().style.cursor = '';
            selectedZone = "";
            selectedValue = "";
            map.setFilter('outline-hover-work', ['==', 'ADADGUID', '']);
        });

        map.on('mousemove', 'centroids_work', (e) => {
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

                map.setFilter('outline-hover-work', ['==', 'ADADGUID', selectedZone]);
            }
        });

        map.on('mouseleave', 'centroids_work', () => {
            map.getCanvas().style.cursor = '';
            selectedZone = "";
            selectedValue = "";
            map.setFilter('outline-hover-work', ['==', 'ADADGUID', '']);
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
            <div id="hovered-zone" style="padding: 4px; border: solid 1px #AB1368; font-weight: bold;">
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
                        cy="40"
                        r="35"
                        style="fill:{circleSize[mapSelected].colours[4]};"
                        />

                        <circle
                        class = "box"
                        cx="55"
                        cy="100"
                        r="{circleSize[mapSelected].size[3]}"
                        style="fill:{circleSize[mapSelected].colours[3]};"
                        />

                        {#if circleSize[mapSelected].breaks[2] !== 0}
                            <circle
                            class = "box"
                            cx="55"
                            cy="135"
                            r="{circleSize[mapSelected].size[2]}"
                            style="fill:{circleSize[mapSelected].colours[2]};"
                            />
                        {/if}

                        {#if circleSize[mapSelected].breaks[1] !== 0}
                            <circle
                            class = "box"
                            cx="55"
                            cy="157.5"
                            r="{circleSize[mapSelected].size[1]}"
                            style="fill:{circleSize[mapSelected].colours[1]};"
                            />
                        {/if}

                        {#if circleSize[mapSelected].breaks[0] !== 0}
                            <circle
                            class = "box"
                            cx="55"
                            cy="177"
                            r="{circleSize[mapSelected].size[0]}"
                            style="fill:{circleSize[mapSelected].colours[0]};"
                            />
                        {/if}

                        <text class="legend-label" x="100" y="40" dy="0.35em">&gt;{circleSize[mapSelected].breaks[3]}</text>
                        <text class="legend-label" x="100" y="100" dy="0.35em">{circleSize[mapSelected].breaks[2]+ 1} - {circleSize[mapSelected].breaks[3]}</text>
                        {#if circleSize[mapSelected].breaks[2] !== 0}<text class="legend-label" x="100" y="135" dy="0.35em">{circleSize[mapSelected].breaks[1]+ 1} - {circleSize[mapSelected].breaks[2]}</text>{/if}
                        {#if circleSize[mapSelected].breaks[1] !== 0}<text class="legend-label" x="100" y="157.5" dy="0.35em">{circleSize[mapSelected].breaks[0] + 1} - {circleSize[mapSelected].breaks[1]}</text>{/if}
                        {#if circleSize[mapSelected].breaks[0] !== 0}<text class="legend-label" x="100" y="177" dy="0.35em">&le;{circleSize[mapSelected].breaks[0]}</text>{/if}
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