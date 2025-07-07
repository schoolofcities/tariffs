<script>
    import { onMount } from "svelte";
    import maplibregl from "maplibre-gl";
    import "../assets/styles.css";
    import "maplibre-gl/dist/maplibre-gl.css";
    import * as pmtiles from "pmtiles";
    import Select from "svelte-select";

    const protocol = new pmtiles.Protocol();
    maplibregl.addProtocol("pmtiles", protocol.tile);

    let map;

    let polygon = "percentage.pmtiles";

    let centroid = "centroid.pmtiles";

    let graduated_col = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];

    let graduated_siz = [5, 7.5, 10, 20, 40];

    let mapSelected = "";

    const breaksDict = {
        // Counts - Businesses
        Auto_B: [0, 0, 0, 0],
        Alum_B: [1, 5, 15, 51],
        Steel_B: [0, 2, 7, 25],
        Lum_B: [0, 1, 3, 7],
        Ene_B: [0, 0, 1, 2],
        CUSMA_B: [0, 1, 3, 7],
        Total_B: [2, 8, 23, 61],

        // Counts - Employees
        Auto_E: [0, 3, 15, 35],
        Alum_E: [190, 646, 1385, 4336],
        Steel_E: [46, 177, 404, 1195],
        Lum_E: [17, 56, 117, 238],
        Ene_E: [27, 150, 287, 550],
        CUSMA_E: [22, 92, 242, 722],
        Total_E: [121, 459, 1101, 2601],

        // Counts - Residents
        Auto_C: [9, 37, 81, 166],
        Alum_C: [101, 271, 540, 1521],
        Steel_C: [33, 94, 187, 369],
        Lum_C: [34, 119, 286, 787],
        Ene_C: [12, 43, 106, 228],
        CUSMA_C: [27, 72, 144, 319],
        Total_C: [149, 392, 738, 2087],

        // Percentages - Businesses (_1)
        Auto_1: [0.000417, 0.0019569, 0.0033784, 0.0046729],
        Alum_1: [0.003344, 0.011628, 0.026316, 0.083333],
        Steel_1: [0.002188, 0.007194, 0.018868, 0.055556],
        Lum_1: [0.001712, 0.005464, 0.011364, 0.0625],
        Ene_1: [0.0002042, 0.0019802, 0.0046512, 0.010582],
        CUSMA_1: [0.001555, 0.00489, 0.010204, 0.023411],
        Total_1: [0.004866, 0.016393, 0.045732, 0.125],

        // Percentages - Employees (_2)
        Auto_2: [0.0003472, 0.0022838, 0.0077246, 0.0603004],
        Alum_2: [0.009575, 0.036215, 0.081901, 0.162557],
        Steel_2: [0.007246, 0.029827, 0.076109, 0.164044],
        Lum_2: [0.004723, 0.016598, 0.038231, 0.093552],
        Ene_2: [0.00693, 0.027958, 0.04579, 0.172277],
        CUSMA_2: [0.0045, 0.018514, 0.050558, 0.118035],
        Total_2: [0.01483, 0.05273, 0.13219, 0.31899],

        // Percentages - Residents (_3)
        Auto_3: [0.002372, 0.009226, 0.023469, 0.04595],
        Alum_3: [0.01709, 0.04565, 0.08209, 0.13921],
        Steel_3: [0.008247, 0.022198, 0.045257, 0.090705],
        Lum_3: [0.009451, 0.030769, 0.076923, 0.205152],
        Ene_3: [0.002586, 0.009032, 0.023484, 0.048214],
        CUSMA_3: [0.005556, 0.015102, 0.032965, 0.083333],
        Total_3: [0.02989, 0.07757, 0.13992, 0.32634],
    };

    const choropleths = {};
    const circleSize = {};

    for (const key in breaksDict) {
        const isPercentage =
            key.endsWith("_1") || key.endsWith("_2") || key.endsWith("_3");
        const isCount =
            key.endsWith("_B") || key.endsWith("_E") || key.endsWith("_C");

        const prefix = key.split("_")[0]; // e.g., "Auto"
        const suffix = key.split("_")[1]; // e.g., "1", "B", etc.

        const humanLabels = {
            Auto: "Tariffs on Automobiles",
            Alum: "Tariffs on Aluminum",
            Steel: "Tariffs on Steel",
            Lum: "Tariffs on Lumber",
            Ene: "Tariffs on Energy and Natural Resources",
            CUSMA: "Tariffs on non-CUSMA compliant goods",
            Total: "All Tariffs",
        };

        const targetLabels = {
            "1": "businesses",
            "2": "employees",
            "3": "residents",
            B: "businesses",
            E: "employees",
            C: "residents",
        };

        const fullKey = key;
        const breaks = breaksDict[fullKey];

        if (isPercentage) {
            choropleths[fullKey] = {
                dataSource: fullKey,
                breaks,
                colours: graduated_col,
                text: `Estimated % of ${targetLabels[suffix]} within the ADA that are directly affected by ${humanLabels[prefix]}`,
            };
        } else if (isCount) {
            circleSize[fullKey] = {
                dataSource: fullKey,
                breaks,
                size: graduated_siz,
                colours: graduated_col,
                text: `Estimated count of ${targetLabels[suffix]} within the ADA that are directly affected by ${humanLabels[prefix]}`,
            };
        }
    }

    function choroSet(layer) {
        let choropleth = choropleths[layer];
        console.log(choropleth);

        map.setPaintProperty("polygons_work", "fill-opacity", 0.8);

        map.setPaintProperty("polygons_work", "fill-color", [
            "case",
            ["==", ["get", choropleth.dataSource], null],
            "rgba(0,0,0,0)",
            ["==", ["get", choropleth.dataSource], 0],
            "rgba(0,0,0,0)",
            [
                "step",
                ["get", choropleth.dataSource],
                choropleth.colours[0],
                choropleth.breaks[0],
                choropleth.colours[1],
                choropleth.breaks[1],
                choropleth.colours[2],
                choropleth.breaks[2],
                choropleth.colours[3],
                choropleth.breaks[3],
                choropleth.colours[4],
            ],
        ]);
    }

    function circleSet(layer) {
        let circle = circleSize[layer];
        console.log(circle);

        map.setPaintProperty("centroids_work", "circle-opacity", 0.8);

        map.setPaintProperty("centroids_work", "circle-color", [
            "case",
            ["==", ["get", circle.dataSource], null],
            "rgba(0,0,0,0)",
            ["==", ["get", circle.dataSource], 0],
            "rgba(0,0,0,0)",
            [">", ["get", circle.dataSource], circle.breaks[3]],
            circle.colours[4],
            [">", ["get", circle.dataSource], circle.breaks[2]],
            circle.colours[3],
            [">", ["get", circle.dataSource], circle.breaks[1]],
            circle.colours[2],
            [">", ["get", circle.dataSource], circle.breaks[0]],
            circle.colours[1],
            circle.colours[0],
        ]);

        map.setPaintProperty("centroids_work", "circle-radius", [
            "interpolate",
            ["linear"],
            ["zoom"],
            3,
            [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]],
                circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]],
                circle.size[3],
                ["==", ["get", circle.dataSource], 0],
                0,
                0,
            ],
            8,
            [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]],
                circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]],
                circle.size[3],
                [">", ["get", circle.dataSource], circle.breaks[1]],
                circle.size[2],
                ["==", ["get", circle.dataSource], 0],
                0,
                0,
            ],
            11,
            [
                "case",
                [">", ["get", circle.dataSource], circle.breaks[3]],
                circle.size[4],
                [">", ["get", circle.dataSource], circle.breaks[2]],
                circle.size[3],
                [">", ["get", circle.dataSource], circle.breaks[1]],
                circle.size[2],
                [">", ["get", circle.dataSource], circle.breaks[0]],
                circle.size[1],
                ["==", ["get", circle.dataSource], 0],
                0,
                circle.size[0],
            ],
        ]);
    }

    function updateItems() {
        console.log("updateItems called", {
            estimatedPct,
            estimatedCount,
            selectedTarget,
        });

        if (!selectedTarget || (!estimatedPct && !estimatedCount)) {
            items = [];
            return;
        }

        // define suffix logic based on both checkboxes and target type
        let suffix = "";
        if (estimatedPct) {
            if (selectedTarget === "B") suffix = "_1";
            if (selectedTarget === "E") suffix = "_2";
            if (selectedTarget === "C") suffix = "_3";
        } else if (estimatedCount) {
            if (selectedTarget === "B") suffix = "_B";
            if (selectedTarget === "E") suffix = "_E";
            if (selectedTarget === "C") suffix = "_C";
        }

        const prefixList = [
            "Total",
            "Auto",
            "Alum",
            "Steel",
            "Lum",
            "Ene",
            "CUSMA",
        ];
        items = prefixList.map((prefix) => `${prefix}${suffix}`);
        mapSelected = items[0];

        if (estimatedPct) {
            map.setLayoutProperty("polygons_work", "visibility", "visible");
            map.setLayoutProperty("centroids_work", "visibility", "none");
            choroSet(mapSelected);
        } else if (estimatedCount) {
            map.setLayoutProperty("polygons_work", "visibility", "none");
            map.setLayoutProperty("centroids_work", "visibility", "visible");
            circleSet(mapSelected);
        }
    }

    let estimatedPct = false;
    let estimatedCount = false;
    let items;

    function toggleViz(event) {
        const id = event.target.id;
        if (id === "pctcheck" && estimatedPct) {
            estimatedCount = false;
        } else if (id === "countcheck" && estimatedCount) {
            estimatedPct = false;
        }

        updateItems(); // call new function
    }

    function layerSelect(e) {
        mapSelected = e.detail.value;
        if (estimatedPct) {
            choroSet(mapSelected);
        } else if (estimatedCount) {
            circleSet(mapSelected);
        }
    }

    let selectedZone = "";
    let selectedValue = "";
    let lastUpdate = "0";

    let selectedTarget = ""; // 'B', 'E', 'C'

    function setTarget(letter) {
        selectedTarget = letter;
        updateItems();
    }

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

        map.on("load", async () => {
            map.addSource("work_polygons", {
                type: "vector",
                url: "pmtiles://" + polygon,
            });

            map.addSource("work_centroids", {
                type: "vector",
                url: "pmtiles://" + centroid,
            });

            // to show choropleth
            map.addLayer({
                id: "polygons_work",
                type: "fill",
                source: "work_polygons",
                "source-layer": "choropleth",
                layout: {
                    visibility: "none",
                },
            });

            // to show outline of all ADAs. won't be affected by any change in checkboxes or buttons
            map.addLayer({
                id: "outline_work",
                type: "line",
                source: "work_polygons",
                "source-layer": "choropleth",
                paint: {
                    "line-color": "#808080",
                    "line-width": 1,
                    "line-opacity": 0.5,
                },
            });

            // to allow for the ADAs to be highlighted when hovered over when choropleth layer is put on
            map.addLayer({
                id: "outline-hover-work",
                type: "fill",
                source: "work_polygons",
                "source-layer": "choropleth",
                paint: {
                    "fill-color": "#0000FF",
                    "fill-opacity": 0.5,
                },
                filter: ["==", "ADADGUID", ""],
            });

            // to show centroids
            map.addLayer({
                id: "centroids_work",
                type: "circle",
                source: "work_centroids",
                "source-layer": "centroids",
                layout: {
                    visibility: "none",
                },
            });

            map.setLayerZoomRange("centroids_work", 1, 12);
        });

        map.on("style.load", () => {
            map.setProjection({
                type: map.getZoom() < 7 ? "globe" : "mercator",
            });

            map.on("zoom", () => {
                const zoom = map.getZoom();
                map.setProjection({
                    type: zoom < 7 ? "globe" : "mercator",
                });
            });
        });

        map.on("mousemove", "polygons_work", (e) => {
            const now = performance.now();
            if (now - lastUpdate < 100) return; // Throttle updates to every 100ms
            lastUpdate = now;

            map.getCanvas().style.cursor = "pointer";

            if (!e.features.length) return;

            const properties = e.features[0].properties;
            const currentZone = properties.ADADGUID;

            if (currentZone !== selectedZone) {
                const dataField = choropleths[mapSelected]?.dataSource;

                const rawValue = properties[dataField];

                if (rawValue == null) {
                    selectedValue = "No Data";
                    selectedZone = "";
                    map.setFilter("outline-hover-work", ["==", "ADADGUID", ""]);
                    return;
                }

                selectedValue = (rawValue * 100).toFixed(2) + "%";

                selectedZone = currentZone;

                map.setFilter("outline-hover-work", [
                    "==",
                    "ADADGUID",
                    selectedZone,
                ]);
            }
        });

        map.on("mouseleave", "polygons_work", () => {
            map.getCanvas().style.cursor = "";
            selectedZone = "";
            selectedValue = "";
            map.setFilter("outline-hover-work", ["==", "ADADGUID", ""]);
        });

        map.on("mousemove", "centroids_work", (e) => {
            const now = performance.now();
            if (now - lastUpdate < 100) return; // Throttle updates to every 100ms
            lastUpdate = now;

            map.getCanvas().style.cursor = "pointer";

            if (!e.features.length) return;

            const properties = e.features[0].properties;
            const currentZone = properties.ADADGUID;

            if (currentZone !== selectedZone) {
                const dataField = circleSize[mapSelected]?.dataSource;

                const rawValue = properties[dataField];

                selectedValue =
                    rawValue != null && rawValue >= 0
                        ? Math.round(rawValue).toLocaleString()
                        : "No Data";

                selectedZone = currentZone;

                map.setFilter("outline-hover-work", [
                    "==",
                    "ADADGUID",
                    selectedZone,
                ]);
            }
        });

        map.on("mouseleave", "centroids_work", () => {
            map.getCanvas().style.cursor = "";
            selectedZone = "";
            selectedValue = "";
            map.setFilter("outline-hover-work", ["==", "ADADGUID", ""]);
        });
    });
</script>

<div id="container">
    <div id="panel">
        <h1>Impact of US Administration's Tariffs on Canada</h1>

        <h2>
            Mapping information about the direct impacts of tariffs across
            Canada at the Aggregate Dissemination Area (ADA) level
        </h2>

        <div id="buttons">
            <button
                id="businessButton"
                class={selectedTarget === "B" ? "layerOn" : "layerOff"}
                on:click={() => setTarget("B")}
            >
                Businesses
            </button>

            <button
                id="employeeButton"
                class={selectedTarget === "E" ? "layerOn" : "layerOff"}
                on:click={() => setTarget("E")}
            >
                Employees
            </button>

            <button
                id="residentButton"
                class={selectedTarget === "C" ? "layerOn" : "layerOff"}
                on:click={() => setTarget("C")}
            >
                Residents
            </button>
        </div>

        <div id="checkbox" class="check-box">
            <label class="label-format"
                ><input
                    type="checkbox"
                    id="pctcheck"
                    class="check-box-item"
                    bind:checked={estimatedPct}
                    on:change={toggleViz}
                />
                Show estimated percentages
            </label>
            <br />
            <label class="label-format"
                ><input
                    type="checkbox"
                    id="countcheck"
                    class="check-box-item"
                    bind:checked={estimatedCount}
                    on:change={toggleViz}
                />
                Show estimated counts
            </label>
        </div>

        <div id="select-wrapper">
            <Select
                id="select"
                {items}
                value={mapSelected}
                clearable={false}
                showChevron={true}
                listAutoWidth={true}
                searchable={false}
                listOffset={10}
                on:change={layerSelect}
            />
        </div>

        <div>
            <div
                id="hovered-zone"
                style="padding: 4px; border: solid 1px #AB1368; font-weight: bold;"
            >
                Hovered zone: {selectedValue || "No data available"}
            </div>
        </div>

        <div class="des">
            {#if estimatedPct && choropleths[mapSelected]?.colours}
                <div id="destext">{choropleths[mapSelected]?.text}</div>

                <div id="legend">
                    <svg width="350" height="40">
                        <rect
                            class="box"
                            width="64"
                            height="20"
                            x="20"
                            y="0"
                            style="fill:{choropleths[mapSelected].colours[0]};"
                        />

                        <rect
                            class="box"
                            width="64"
                            height="20"
                            x="85"
                            y="0"
                            style="fill:{choropleths[mapSelected].colours[1]};"
                        />

                        <rect
                            class="box"
                            width="64"
                            height="20"
                            x="150"
                            y="0"
                            style="fill:{choropleths[mapSelected].colours[2]};"
                        />

                        <rect
                            class="box"
                            width="64"
                            height="20"
                            x="215"
                            y="0"
                            style="fill:{choropleths[mapSelected].colours[3]};"
                        />

                        <rect
                            class="box"
                            width="64"
                            height="20"
                            x="280"
                            y="0"
                            style="fill:{choropleths[mapSelected].colours[4]};"
                        />

                        <text
                            class="legend-label"
                            text-anchor="middle"
                            x="85"
                            y="35"
                            >&lt;{(
                                choropleths[mapSelected].breaks[0] * 100
                            ).toFixed(2)}%</text
                        >
                        <text
                            class="legend-label"
                            text-anchor="middle"
                            x="150"
                            y="35"
                            >{(
                                choropleths[mapSelected].breaks[1] * 100
                            ).toFixed(2)}%</text
                        >
                        <text
                            class="legend-label"
                            text-anchor="middle"
                            x="215"
                            y="35"
                            >{(
                                choropleths[mapSelected].breaks[2] * 100
                            ).toFixed(2)}%</text
                        >
                        <text
                            class="legend-label"
                            text-anchor="middle"
                            x="280"
                            y="35"
                            >&gt{(
                                choropleths[mapSelected].breaks[3] * 100
                            ).toFixed(2)}%</text
                        >
                    </svg>
                </div>
            {:else if estimatedCount && circleSize[mapSelected]?.colours}
                <div id="destext">{circleSize[mapSelected]?.text}</div>

                <div id="legend">
                    <svg width="350" height="200">
                        <circle
                            class="box"
                            cx="55"
                            cy="40"
                            r="35"
                            style="fill:{circleSize[mapSelected].colours[4]};"
                        />

                        {#if circleSize[mapSelected].breaks[3] !== 0}
                            <circle
                                class="box"
                                cx="55"
                                cy="100"
                                r={circleSize[mapSelected].size[3]}
                                style="fill:{circleSize[mapSelected]
                                    .colours[3]};"
                            />
                        {/if}

                        {#if circleSize[mapSelected].breaks[2] !== 0}
                            <circle
                                class="box"
                                cx="55"
                                cy="135"
                                r={circleSize[mapSelected].size[2]}
                                style="fill:{circleSize[mapSelected]
                                    .colours[2]};"
                            />
                        {/if}

                        {#if circleSize[mapSelected].breaks[1] !== 0}
                            <circle
                                class="box"
                                cx="55"
                                cy="157.5"
                                r={circleSize[mapSelected].size[1]}
                                style="fill:{circleSize[mapSelected]
                                    .colours[1]};"
                            />
                        {/if}

                        {#if circleSize[mapSelected].breaks[0] !== 0}
                            <circle
                                class="box"
                                cx="55"
                                cy="177"
                                r={circleSize[mapSelected].size[0]}
                                style="fill:{circleSize[mapSelected]
                                    .colours[0]};"
                            />
                        {/if}

                        <text class="legend-label" x="100" y="40" dy="0.35em"
                            >&gt;{circleSize[mapSelected].breaks[3]}</text
                        >
                        {#if circleSize[mapSelected].breaks[3] !== 0}<text
                                class="legend-label"
                                x="100"
                                y="100"
                                dy="0.35em"
                                >{circleSize[mapSelected].breaks[2] + 1} - {circleSize[
                                    mapSelected
                                ].breaks[3]}</text
                            >{/if}
                        {#if circleSize[mapSelected].breaks[2] !== 0}<text
                                class="legend-label"
                                x="100"
                                y="135"
                                dy="0.35em"
                                >{circleSize[mapSelected].breaks[1] + 1} - {circleSize[
                                    mapSelected
                                ].breaks[2]}</text
                            >{/if}
                        {#if circleSize[mapSelected].breaks[1] !== 0}<text
                                class="legend-label"
                                x="100"
                                y="157.5"
                                dy="0.35em"
                                >{circleSize[mapSelected].breaks[0] + 1} - {circleSize[
                                    mapSelected
                                ].breaks[1]}</text
                            >{/if}
                        {#if circleSize[mapSelected].breaks[0] !== 0}<text
                                class="legend-label"
                                x="100"
                                y="177"
                                dy="0.35em"
                                >&le;{circleSize[mapSelected].breaks[0]}</text
                            >{/if}
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
        border-right: solid 1px #dc4633;
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

    #buttons {
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .layerOn {
        background-color: #ab1368;
        color: white;
        font-weight: bold;
        border: none;
    }

    .layerOff {
        background-color: #f0f0f0;
        color: #333;
        border: 1px solid #ccc;
    }

    #checkbox {
        margin-top: 10px;
        margin-bottom: 10px;
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
