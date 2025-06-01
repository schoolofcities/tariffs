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
    
    let colours_yellowred = ["#ADADAD", "#B198B4", "#C97CA3", "#DD5C76", "#DC4633"];

    const defaultMap = "Est % of All Employees Affected";

    const choropleths = {
        "Est % of All Employees Affected": {
            dataSource: "Total_E_pc",
            breaks: [0.017, 0.057, 0.124, 0.26],
            colours: colours_yellowred,
            text: "Estimated % of All Employees affected by US Administration's Tariffs on Canada",
        },
    };

    function layerSet(layer) {
        let choropleth = choropleths[layer];
        console.log(choropleth);

        map.setPaintProperty("work_side", "fill-opacity", 0.9);
        map.setPaintProperty("work_side", "fill-color", [
            "case",
            ["==", ["get", choropleth.dataSource], null], "#FFFFFF",
            ["step", ["get", choropleth.dataSource],
            choropleth.colours[0], choropleth.breaks[0],
            choropleth.colours[1], choropleth.breaks[1],
            choropleth.colours[2], choropleth.breaks[2],
            choropleth.colours[3], choropleth.breaks[3],
            choropleth.colours[4]],
        ]);
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
            maxZoom: 12,
            pitch: 5,
            projection: "globe",
            attributionControl: false,
        });

        map.on('load', async () => {

            map.addSource('work_side',{
                type: 'vector',
                url: 'pmtiles://' + work_side,
            });

            map.addLayer({
                'id': 'work_side',
                'type': 'fill',
                'source': 'work_side',
                'source-layer': 'ADA_aggregates',
            });

            layerSet(defaultMap);

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

            layerSet(defaultMap);

        });

    });

</script>


<div id="map-container">
    <div id="map"></div>
</div>


<style>

    #map-container {
        position: relative;
        width: 100%;
        height: 100vh;
    }

    #map {
        position: absolute;
        width: 100%;
        height: 100%;
    }

</style>
