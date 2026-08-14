<script>
    import { onDestroy, onMount } from 'svelte';
    import maplibregl from 'maplibre-gl';
    import 'maplibre-gl/dist/maplibre-gl.css';

    export let geojson = null;
    export let colorMode = 'exposure'; // 'exposure' | 'political'

    export let period = 'pre';   // 'pre' | 'post' | 'removed'
    $: field    = period === 'pre' ? 'pre_emp_pct'  : period === 'post' ? 'post_emp_pct'  : 'removed_emp_pct';
    $: empField = period === 'pre' ? 'pre_emp'      : period === 'post' ? 'post_emp'      : 'removed_emp';
    $: if (mapLoaded && (geojson || colorMode || period || field)) updateMap();

    let map, mapContainer, mapLoaded = false, popup;

    const SOURCE_ID = 'counties';
    const FILL_LAYER = 'county-fill';
    const LINE_LAYER = 'county-line';

    // Exposure: white → orange/red
    // Political: blue (Dem) → white → red (Rep)
    function fillColorExpression() {
        if (colorMode === 'political') {
            // Derive rep vote share: (1 + margin) / 2
            const repPct = ['/', ['+', 1, ['get', 'rep_margin']], 2];
            return [
                'case',
                ['==', ['get', 'rep_margin'], null], '#cccccc',
                ['interpolate', ['linear'], repPct,
                    0.0,  '#0055A4',   // 0% Rep (100% Dem)
                    0.35, '#89a9d1',   // 35% Rep
                    0.5,  '#f5f5f5',   // 50/50
                    0.65, '#d08080',   // 65% Rep
                    1.0,  '#E81B23'    // 100% Rep
                ]
            ];
        }
        return [
            'case',
            ['==', ['get', field], null], '#cccccc',
            ['==', ['get', field], 0],    '#cccccc',
            ['interpolate', ['linear'], ['get', field],
                0.001, '#fff7ec', 0.1, '#fdd49e', 0.3, '#fc8d59', 0.6, '#d7301f', 1.0, '#7f0000']
        ];
    }

    function updateMap() {
        if (!mapLoaded || !map) return;
        if (geojson) map.getSource(SOURCE_ID)?.setData(geojson);
        if (map.getLayer(FILL_LAYER)) {
            map.setPaintProperty(FILL_LAYER, 'fill-color', fillColorExpression());
        }
    }

    $: if (mapLoaded && (geojson || colorMode)) updateMap();

    onMount(() => {
        map = new maplibregl.Map({
            container: mapContainer,
            style: 'https://tiles.openfreemap.org/styles/positron',
            center: [-96, 38], zoom: 3.8,
            minZoom: 2, maxZoom: 10,
            attributionControl: false,
            projection: 'globe'
        });
        
        map.on('style.load', () => {
            map.setProjection({ type: 'globe' });
        });

        map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-left');

        map.on('load', () => {
            map.addSource(SOURCE_ID, {
                type: 'geojson',
                data: geojson || { type: 'FeatureCollection', features: [] }
            });
            map.addLayer({
                id: FILL_LAYER, type: 'fill', source: SOURCE_ID,
                paint: { 'fill-color': fillColorExpression(), 'fill-opacity': 0.8 }
            });
            map.addLayer({
                id: LINE_LAYER, type: 'line', source: SOURCE_ID,
                paint: { 'line-color': '#aaaaaa', 'line-width': 0.3, 'line-opacity': 0.5 }
            });


            // Replace the existing map.on('click') and mouseenter/mouseleave blocks with:

            // Shared hover tooltip for both modes
            const tip = document.createElement('div');
            tip.style.cssText = `
                position:absolute; pointer-events:none; opacity:0; transition:opacity 0.1s;
                background:rgba(255,255,255,0.95); border:1px solid #cccccc;
                border-radius:6px; padding:8px 10px; font-family:OpenSans,sans-serif;
                font-size:12px; line-height:1.6; box-shadow:0 2px 8px rgba(0,0,0,0.12);
                white-space:nowrap; z-index:10;
            `;
            mapContainer.appendChild(tip);

            map.on('mousemove', FILL_LAYER, (e) => {
                if (!e.features?.length) { tip.style.opacity = '0'; return; }
                const p = e.features[0].properties;

                if (colorMode === 'political') {
                    if (p.rep_margin == null) { tip.style.opacity = '0'; return; }
                    const repPct = ((1 + p.rep_margin) / 2 * 100).toFixed(1);
                    const demPct = (100 - parseFloat(repPct)).toFixed(1);
                    tip.innerHTML = `
                        <div style="font-weight:600;margin-bottom:4px;">${p.NAME} County</div>
                        <div style="color:#E81B23;">Republican: ${repPct}%</div>
                        <div style="color:#0055A4;">Democrat: ${demPct}%</div>
                    `;
                } else {
                    const rawPct = p[field];
                    const rawEmp = p[empField];
                    console.log(`${p.NAME} | period=${period} | ${field}=${rawPct} | ${empField}=${rawEmp} | all_emp=${p.all_emp}`);
                    const pct = rawPct != null ? (rawPct * 100).toFixed(1) + '%' : 'No data';
                    const exposed = rawEmp != null ? Number(rawEmp).toLocaleString() : 'N/A';
                    const total = p.all_emp != null && p.all_emp > 0 ? Number(p.all_emp).toLocaleString() : 'N/A';
                    tip.innerHTML = `
                        <div style="font-weight:600;margin-bottom:4px;">${p.NAME} County</div>
                        <div>Exposed employment: ${pct}</div>
                        <div>Jobs exposed: ${exposed}</div>
                        <div>Total jobs: ${total}</div>
                    `;
                }

                const rect = mapContainer.getBoundingClientRect();
                const x = e.originalEvent.clientX - rect.left + 14;
                const y = e.originalEvent.clientY - rect.top - 10;
                tip.style.left = `${x}px`;
                tip.style.top  = `${y}px`;
                tip.style.opacity = '1';
            });

            map.on('mouseleave', FILL_LAYER, () => {
                map.getCanvas().style.cursor = '';
                tip.style.opacity = '0';
            });

            map.on('mouseenter', FILL_LAYER, () => {
                map.getCanvas().style.cursor = 'pointer';
            });
            mapLoaded = true;
            updateMap();
        });
    });

    onDestroy(() => { if (popup) popup.remove(); if (map) map.remove(); });
</script>

<div class="map-wrapper">
    <div class="map" bind:this={mapContainer}></div>
    <div class="legend">
        {#if colorMode === 'exposure'}
            <div class="legend-title">Share of employment exposed</div>
            <div class="legend-ramp">
                <span>0%</span>
                <span class="ramp ramp-exposure"></span>
                <span>100%</span>
            </div>
            <div class="legend-note">Grey = no exposure</div>
        {:else}
            <div class="legend-title">2024 presidential vote share</div>
            <div class="legend-ramp">
                <span>0% Rep</span>
                <span class="ramp ramp-political"></span>
                <span>100% Rep</span>
            </div>
            <div class="legend-note">White = 50/50 split</div>
        {/if}
    </div>
</div>

<style>
    .map-wrapper { position: relative; width: 100%; max-width: 1080px; margin: 0 auto; height: 62vh; min-height: 460px; border: 1px solid var(--brandGray); }
    .map { width: 100%; height: 100%; }
    .legend {
        position: absolute; top: 12px; right: 12px;
        background: rgba(255,255,255,0.92); border: 1px solid var(--brandGray);
        border-radius: 6px; padding: 8px 12px; font-family: OpenSans; font-size: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }
    .legend-title { font-family: OpenSansBold; color: var(--brandGray90); margin-bottom: 4px; }
    .legend-ramp { display: flex; align-items: center; gap: 6px; }
    .ramp { display: inline-block; width: 120px; height: 10px; border-radius: 2px; border: 1px solid var(--brandGray); }
    .ramp-exposure { background: linear-gradient(to right, #fff7ec, #fdd49e, #fc8d59, #d7301f, #7f0000); }
    .ramp-political { background: linear-gradient(to right, #0055A4, #ffffff, #E81B23); }
    .legend-note { color: var(--brandGray70); margin-top: 4px; font-size: 11px; }
    :global(.maplibregl-popup-content) { border-radius: 8px; }
</style>