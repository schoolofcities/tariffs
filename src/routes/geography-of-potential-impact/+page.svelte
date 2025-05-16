<script>
    import { onMount } from "svelte";
    import maplibregl from "maplibre-gl";
    import "../../assets/styles.css";
    import "maplibre-gl/dist/maplibre-gl.css";
    import * as pmtiles from "pmtiles";

    let map;
    
    onMount(() => {
        
        map = new maplibregl.Map({
            container: "map",
            style: "https://api.protomaps.com/styles/v5/white/en.json?key=89c5d93843b4ca61",
            center: [-95, 60],
            zoom: 3,
            bearing: 0,
            scrollZoom: true,
            minZoom: 1,
            pitch: 5,
            projection: "globe",
            attributionControl: false,
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

    });

</script>



<div id="map"></div>



<style>

    #map {
        position: absolute;
        width: 100%;
        height: 100%;
    }

</style>
