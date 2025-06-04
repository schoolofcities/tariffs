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

    let ADA_cent = "ADA_centroids.pmtiles"
    
    let graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];

    let graduated_siz = [5, 7.5, 10, 20, 40];

    const defaultMap = "All Tariffs (% of Employees)";

    let mapSelected = defaultMap;

    const choropleths = {
        "All Tariffs (% of Employees)": {
            dataSource: "Total_E_pc",
            breaks: [0.017, 0.057, 0.124, 0.26],
            colours: graduated_col,
            text: "Estimated % of employees affected by all types of US Administration's Tariffs on Canada",
        },
        "All Tariffs (% of Businesses)": {
            dataSource: "Total_B_pc",
            breaks: [0.0037, 0.0104, 0.0257, 0.0667],
            colours: graduated_col,
            text: "Estimated % of businesses affected by all types of US Administration's Tariffs on Canada",
        },
        "Tariffs on Automobiles (% of Employees)": {
            dataSource: "Auto_E_pc",
            breaks: [0.0012, 0.0086, 0.0505, 0.1012],
            colours: graduated_col,
            text: "Estimated % of employees affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Automobiles (% of Businesses)": {
            dataSource: "Auto_B_pc",
            breaks: [0.00017, 0.00076, 0.00146, 0.00322],
            colours: graduated_col,
            text: "Estimated % of businesses affected by US Administration's Automobile Tariffs on Canada",
        },
        "Tariffs on Aluminum (% of Businesses)": {
            dataSource: "Aluminum_1",
            breaks: [0.002, 0.006, 0.0131, 0.0287],
            colours: graduated_col,
            text: "Estimated % of businesses affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Aluminum (% of Employees)": {
            dataSource: "Aluminum_2",
            breaks: [0.012, 0.045, 0.103, 0.207],
            colours: graduated_col,
            text: "Estimated % of employees affected by US Administration's Aluminum Tariffs on Canada",
        },
        "Tariffs on Steel (% of Businesses)": {
            dataSource: "Steel_B_pc",
            breaks: [0.0011, 0.0037, 0.0092, 0.0357],
            colours: graduated_col,
            text: "Estimated % of businesses affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Steel (% of Employees)": {
            dataSource: "Steel_E_pc",
            breaks: [0.0064, 0.0246, 0.0671, 0.2244],
            colours: graduated_col,
            text: "Estimated % of employees affected by US Administration's Steel Tariffs on Canada",
        },
        "Tariffs on Lumber (% of Businesses)": {
            dataSource: "Lumber_B_p",
            breaks: [0.0013, 0.0045, 0.0156, 0.0556],
            colours: graduated_col,
            text: "Estimated % of businesses affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Lumber (% of Employees)": {
            dataSource: "Lumber_E_p",
            breaks: [0.0061, 0.0226, 0.057, 0.1834],
            colours: graduated_col,
            text: "Estimated % of employees affected by US Administration's Lumber Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (% of Businesses)": {
            dataSource: "Energy_B_p",
            breaks: [0.0004, 0.00128, 0.00257, 0.00614],
            colours: graduated_col,
            text: "Estimated % of businesses affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on Energy and Natural Resources (% of Employees)": {
            dataSource: "Energy_E_p",
            breaks: [0.0056, 0.0296, 0.0696, 0.3205],
            colours: graduated_col,
            text: "Estimated % of employees affected by US Administration's Energy and Natural Resources Tariffs on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (% of Businesses)": {
            dataSource: "nonCUSMA_1",
            breaks: [0.00064, 0.00206, 0.00457, 0.01283],
            colours: graduated_col,
            text: "Estimated % of businesses affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
        "Tariffs on non-CUSMA compliant goods (% of Employees)": {
            dataSource: "nonCUSMA_2",
            breaks: [0.0086, 0.0349, 0.0856, 0.1958],
            colours: graduated_col,
            text: "Estimated % of employees affected by US Administration's Tariffs for non-CUSMA compliant goods on Canada",
        },
    };

    const circleSize = {
        "Est Count of All Employees Affected": {
            dataSource: "Total_E",
            breaks: [5871, 27500, 82127, 211116],
            size: graduated_siz,
            colours: graduated_col,
            text: "Estimated Count of All Employees affected by US Administration's Tariffs on Canada",
        },
    };
    
    const items = Object.keys(choropleths);
    //const items = Object.keys(choropleths).concat(Object.keys(circleSize)); later once you have the circle data ready

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

    function layerSelect(e) {
        mapSelected = e.detail.value;
        choroSet(mapSelected);
    }

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
            });

            /*map.addLayer({
                'id': 'centroids',
                'type': 'circle',
                'source': 'ADA_centroids',
                'source-layer': 'ADA_centroids',
            });*/

            map.setLayerZoomRange('centroids', 1, 12);

            choroSet(defaultMap);
            //circleSet(defaultMap);

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

            //choroSet(defaultMap);
            //circleSet(defaultMap);

        });

        map.once('styledata', () => {
            layerSelect();
        });

    });

</script>


<div id="container">

    <div id="panel">

        <h1>Impact of US Administration's Tariffs on Canada</h1>
        
        <h2>Mapping information about the direct impacts of tariffs across Canada at the aggregate dissemination area level</h2>

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
        flex-direction: row;
    }

    #map {
        flex: 1;
        height: 100vh;
        overflow: hidden;
    }

</style>
