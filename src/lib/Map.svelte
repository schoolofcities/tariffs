<script>
    import { onMount } from "svelte";
    import maplibregl from "maplibre-gl";
    import "../assets/styles.css";
    import "maplibre-gl/dist/maplibre-gl.css";
    import * as pmtiles from "pmtiles";

    const protocol = new pmtiles.Protocol();
    maplibregl.addProtocol('pmtiles', protocol.tile);

    let map;

    let work_side = "work_side.pmtiles";

    let ADA_cent = "ADA_centroids.pmtiles"
    
    let graduated_col = ["#ADADAD", "#B198B4", "#C97CA3", "#DD5C76", "#DC4633"];

    let graduated_siz = [10, 20, 30, 40, 50];

    const defaultMap = "Est Count of All Employees Affected";

    const choropleths = {
        "Est % of All Employees Affected": {
            dataSource: "Total_E_pc",
            breaks: [0.017, 0.057, 0.124, 0.26],
            colours: graduated_col,
            text: "Estimated % of All Employees affected by US Administration's Tariffs on Canada",
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

        /*map.setPaintProperty("centroids", "circle-radius",[
            'step', ['get', circle.dataSource],
            circle.size[0], circle.breaks[0], 
            circle.size[1], circle.breaks[1], 
            circle.size[2], circle.breaks[2], 
            circle.size[3], circle.breaks[3], 
            circle.size[4],
        ]);*/

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

        /*map.setPaintProperty("centroids", "circle-radius", [
            "case",
            ["==", ["get", circle.dataSource], null], 0,
            ["==", ["get", circle.dataSource], 0], 0,
            [">", ["get", circle.dataSource], circle.breaks[3]], circle.size[4],
            [">", ["get", circle.dataSource], circle.breaks[2]], circle.size[3],
            [">", ["get", circle.dataSource], circle.breaks[1]], circle.size[2],
            [">", ["get", circle.dataSource], circle.breaks[0]], circle.size[1],
            circle.size[0],
        ]);*/
    };

    onMount(async () => {
        
        map = new maplibregl.Map({
            container: "map",
            style: "https://api.protomaps.com/styles/v5/white/en.json?key=89c5d93843b4ca61",
            center: [-95, 60],
            zoom: 3,
            bearing: 0,
            scrollZoom: true,
            minZoom: 1,
            maxZoom: 11.75,
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

            /*map.addLayer({
                'id': 'polygons',
                'type': 'fill',
                'source': 'work_side',
                'source-layer': 'ADA_aggregates',
            });*/

            map.addLayer({
                'id': 'centroids',
                'type': 'circle',
                'source': 'ADA_centroids',
                'source-layer': 'ADA_centroids',
            });

            map.setLayerZoomRange('centroids', 1, 12);

            // choroSet(defaultMap);
            circleSet(defaultMap);

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
            circleSet(defaultMap);

        });

    });

</script>


<div id="map-container">
    <div id="panel">
        <h1>Impact of US Administration's Tariffs on Canada</h1>
        <h2>Mapping information about the direct impacts of tariffs across Canada at the aggregate dissemination area level</h2>
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
		padding-top: 15px;
		border-right: solid 1px #DC4633;
		flex-shrink: 0;
	}

    #map-container {
        display: flex;
        flex-direction: row;
    }

    #map {
        flex: 1;
        height: 100vh;
        overflow: hidden;
    }

</style>
