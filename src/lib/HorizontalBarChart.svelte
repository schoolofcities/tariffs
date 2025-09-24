<script>
    import { onMount } from 'svelte';
    import Select from "svelte-select";
    import { scaleLinear, scalePow } from 'd3-scale';
    import { 
        GRADUATED_COLORS, 
        TARIFF_LIST, 
        TARIFF_NAME_CODES, 
        TARIFF_IMPACT_TEXT,
        TARIFF_IMPACT_CODES_PCT, 
        TARIFF_IMPACT_CODES_COUNT,
        TARIFF_CMA_BREAKS_PCT,
        TARIFF_CMA_BREAKS_COUNT_LINEAR,
        TARIFF_CMA_BREAKS_COUNT_POW,
    } from './constants.js';
    
    let cmaPcts = $state([]);
    let cmaCounts = $state([]);
    let cmaData = $derived.by(() => {  // Merge datasets once when data loads
        if (!cmaPcts.length || !cmaCounts.length) return [];
        return mergeDatasets(cmaPcts, cmaCounts);
    });

    // Sort merged data based on user selections
    let cmaSorted = $derived.by(() => {
        if (!cmaData.length) return [];
        
        const sortKey = metricType === "Percent" ? tariffKeyPct : tariffKeyCount;
        return sortByMetric(cmaData, sortKey);
    });

    let metricType = $state("Count"); // ["Percent", "Count"]
    let scaleType = $state("Linear"); // ["Linear", "Power-0.2"]
    let impactType = $state("EmployeeHome"); // ["EmployeeHome","EmployeeWork", "Business"] 
    let tariffType = $state("All goods subject to tariffs"); // see full list in TARIFF_LIST

    let tariffKeyPct = $derived(TARIFF_NAME_CODES[tariffType] + TARIFF_IMPACT_CODES_PCT[impactType]);
    let tariffKeyCount = $derived(TARIFF_NAME_CODES[tariffType] + TARIFF_IMPACT_CODES_COUNT[impactType]);

    // Helper function to copy non-shared properties
    function copyUniqueProperties(source, excludeKeys) {
        const result = {};
        for (const [key, value] of Object.entries(source)) {
            if (!excludeKeys.includes(key)) {
                result[key] = value;
            }
        }
        return result;
    }

    // Function to merge percentage and count datasets
    function mergeDatasets(pctData, countData) {
        const sharedKeys = ['CMADGUID', 'GEO_LEVEL', 'GEO_NAME', 'CHAR_POP21', 'geometry'];
        
        return pctData.map(pctItem => {
            const countItem = countData.find(c => c.CMADGUID === pctItem.CMADGUID);
            if (!countItem) return null;
            
            return {
                // Keep shared attributes
                CMADGUID: pctItem.CMADGUID,
                GEO_LEVEL: pctItem.GEO_LEVEL,
                GEO_NAME: pctItem.GEO_NAME,
                CHAR_POP21: pctItem.CHAR_POP21,
                geometry: pctItem.geometry,
                // Add unique properties from both datasets
                ...copyUniqueProperties(pctItem, sharedKeys),
                ...copyUniqueProperties(countItem, sharedKeys)
            };
        }).filter(item => item !== null);
    }

    // Function to sort merged data by selected metric
    function sortByMetric(mergedData, sortKey) {
        return mergedData
            .filter(item => item[sortKey] != null)
            .sort((a, b) => b[sortKey] - a[sortKey]);
    }

    // Chart variables
    let chartWidth = $state(0);
    let chartHeight = $derived(24 * cmaSorted.length + 40);
    let legendWidth = $state(0);

    // Chart parameters
    const CHART_PARAMS = {
        xAxisTop: 34,
        xAxisStart: 60,
        regionStart: 0,
        barTop: 52,
        barGap: 24,
        chartEndGap: 60,
        percentageBoxWidth: 50,
        percentageBoxHeight: 16,
        barStrokeWidth: 16
    };

    const barStart = CHART_PARAMS.xAxisStart + 1;
    const barLabelStart = CHART_PARAMS.xAxisStart + 5;
    const barLabelTop = CHART_PARAMS.barTop + 4;

    // D3 scale setup
    let gridBreaks = $derived.by(() => {
        const breaks = scaleType === "Linear" 
            ? TARIFF_CMA_BREAKS_COUNT_LINEAR[tariffKeyCount]
            : TARIFF_CMA_BREAKS_COUNT_POW[tariffKeyCount];
        if (!breaks) return [0];
        return [0, ...breaks];
    });

    let xScale = $derived.by(() => {
        const maxValue = gridBreaks[gridBreaks.length - 1];
        if (scaleType === "Linear") {
            return scaleLinear()
                .domain([0, maxValue])
                .range([0, chartWidth - CHART_PARAMS.xAxisStart - CHART_PARAMS.chartEndGap]);
        } else {
            return scalePow().exponent(0.2)
                .domain([0, maxValue])
                .range([0, chartWidth - CHART_PARAMS.xAxisStart - CHART_PARAMS.chartEndGap]);
        }
    });

    function numberWithCommas(n) {
        var parts = n.toString().split(".");
        return parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",") + (parts[1] ? "." + parts[1] : "");
    }

    function formatNumberK(n) {
        if (n >= 1000) {
            return (n / 1000) + 'K';
        }
        return n.toString();
    }

    function getColorForPercentage(pctValue, breakpoints) {
        if (!breakpoints || breakpoints.length === 0) return GRADUATED_COLORS[0];
        for (let i = 0; i < breakpoints.length; i++) {
            if (pctValue <= breakpoints[i]) {
                return GRADUATED_COLORS[i];
            }
        }
        return GRADUATED_COLORS[breakpoints.length];
    }

    onMount(async () => {
        const response = await fetch('json/cma_tariffs_percents_centroids.json');
        const pctData = await response.json();
        cmaPcts = pctData.filter(item => item.GEO_LEVEL === "Census metropolitan area");
        
        const countsResponse = await fetch('json/cma_tariffs_counts_centroids.json');
        const countsData = await countsResponse.json();
        cmaCounts = countsData.filter(item => item.GEO_LEVEL === "Census metropolitan area");
    });

    function metricSelect(value) {
        metricType = value;
    }

    function scaleSelect(value) {
        scaleType = value;
    }

    function impactTypeSelect(value) {
        impactType = value;
    }

    function tariffTypeSelect(event) {
        tariffType = event.detail.value;
    }

    $effect(() => {
        // metricType, impactType, tariffType;
        // console.log(`changed state!! ${metricType, impactType, tariffType}`);
        // console.log($state.snapshot(cmaSorted));
        
    })
</script>

<div class="text">
    <div>
        <div id = "select-wrapper">
            <div id="destext">
                <p style="margin-bottom: -5px;">Select the good/product subject to US tariffs:</p>
            </div>
            <Select
                id = 'select'
                items = {TARIFF_LIST}
                value = {tariffType}
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
            <button
                class="toggle-button {impactType === 'Business' ? 'selected' : ''}"
                type="button"
                onclick={() => impactTypeSelect("Business")}
            >
                Businesses
            </button>
            <button
                class="toggle-button {impactType === 'EmployeeWork' ? 'selected' : ''}"
                type="button"
                onclick={() => impactTypeSelect("EmployeeWork")}
            >
                Employees (place of work)
            </button>
            <button
                class="toggle-button {impactType === 'EmployeeHome' ? 'selected' : ''}"
                type="button"
                onclick={() => impactTypeSelect("EmployeeHome")}
            >
                Employees (home)
            </button>
        </div>
    
        <div id="destext">
            <p style="margin-bottom: -5px;">
                Choose how to rank this indicator:
            </p>
        </div>
        <div class="button-group">
            <button
                class="toggle-button {metricType === 'Percent' ? 'selected' : ''}"
                type="button"
                onclick={() => metricSelect("Percent")}
            >
                Percent
            </button>
            <button
                class="toggle-button {metricType === 'Count' ? 'selected' : ''}"
                type="button"
                onclick={() => metricSelect("Count")}
            >
                Total
            </button>
        </div>

        <div id="destext">
            <p style="margin-bottom: -5px;">
                Choose the scale you want to use: 
            </p>
        </div>
        <div class="button-group">
            <button
                class="toggle-button {scaleType === 'Linear' ? 'selected' : ''}"
                type="button"
                onclick={() => scaleSelect("Linear")}
            >
                Linear
            </button>
            <button
                class="toggle-button {scaleType === 'Power-0.2' ? 'selected' : ''}"
                type="button"
                onclick={() => scaleSelect("Power-0.2")}
            >
                Power-0.2
            </button>
        </div>
    </div>

    <!-- Legend section -->
    <div class="legend-section">
        <div id="destext">
            <p style="margin-bottom: -5px;">
                {TARIFF_IMPACT_TEXT[tariffKeyPct]}
            </p>
        </div>
        
        <div id="legend" bind:offsetWidth={legendWidth}>
            <svg width='100%' height='40'>
                {#if legendWidth}
                    {@const currentBreakpoints = TARIFF_CMA_BREAKS_PCT[tariffKeyPct]}
                    {@const boxWidth = legendWidth / 5}
                    <rect
                        class="box"
                        width={boxWidth}
                        height="20"
                        x="0"
                        y="0"
                        style="fill:{GRADUATED_COLORS[0]};"
                    />

                    <rect
                        class="box"
                        width={boxWidth}
                        height="20"
                        x={boxWidth}
                        y="0"
                        style="fill:{GRADUATED_COLORS[1]};"
                    />

                    <rect
                        class="box"
                        width={boxWidth}
                        height="20"
                        x={boxWidth * 2}
                        y="0"
                        style="fill:{GRADUATED_COLORS[2]};"
                    />

                    <rect
                        class="box"
                        width={boxWidth}
                        height="20"
                        x={boxWidth * 3}
                        y="0"
                        style="fill:{GRADUATED_COLORS[3]};"
                    />

                    <rect
                        class="box"
                        width={boxWidth}
                        height="20"
                        x={boxWidth * 4}
                        y="0"
                        style="fill:{GRADUATED_COLORS[4]};"
                    />

                    <text class="legend-label" text-anchor="middle" x={boxWidth} y="35">&lt;{currentBreakpoints[0]}%</text>
                    <text class="legend-label" text-anchor="middle" x={boxWidth * 2} y="35">{currentBreakpoints[1]}%</text>
                    <text class="legend-label" text-anchor="middle" x={boxWidth * 3} y="35">{currentBreakpoints[2]}%</text>
                    <text class="legend-label" text-anchor="middle" x={boxWidth * 4} y="35">&gt{currentBreakpoints[3]}%</text>
                {/if}
            </svg>
        </div>
    </div>

    <div class='chart-wrapper' bind:offsetWidth={chartWidth}>
        <svg height={chartHeight} width={chartWidth} id="chart">
            <!-- Grid lines -->
            {#each gridBreaks as gridValue, i}
                <line class="grid-primary"
                    x1={CHART_PARAMS.xAxisStart + xScale(gridValue)}
                    y1={CHART_PARAMS.xAxisTop}
                    x2={CHART_PARAMS.xAxisStart + xScale(gridValue)}
                    y2={chartHeight}
                ></line>

                <text class="axis-label"
                    x={CHART_PARAMS.xAxisStart + xScale(gridValue)}
                    y={CHART_PARAMS.xAxisTop - 4}
                    text-anchor="middle"
                >
                    {formatNumberK(gridValue)}
                </text>
            {/each}

            <!-- Data bars -->
            {#each cmaSorted as cmaData, i}
                {@const countValue = cmaData[tariffKeyCount]}
                {@const barWidth = xScale(countValue)}
                {@const pctValue = cmaData[tariffKeyPct] || 0}
                {@const currentBreakpoints = TARIFF_CMA_BREAKS_PCT[tariffKeyPct] || []}
                {@const boxColor = getColorForPercentage(pctValue, currentBreakpoints)}
                {@const yPosition = CHART_PARAMS.barTop + (i * CHART_PARAMS.barGap)}
                
                <!-- Main data bar (always shows count data) -->
                <line class="bar-data"
                    x1={barStart}
                    y1={yPosition}
                    x2={barStart + barWidth}
                    y2={yPosition}
                    stroke-width={CHART_PARAMS.barStrokeWidth}
                ></line>

                <!-- Percentage box -->
                <rect class="bar-classifier-box"
                    x={CHART_PARAMS.regionStart}
                    y={yPosition - (CHART_PARAMS.percentageBoxHeight / 2)}
                    width={CHART_PARAMS.percentageBoxWidth}
                    height={CHART_PARAMS.percentageBoxHeight}
                    fill={boxColor}
                    stroke={boxColor}
                ></rect>

                <!-- Percentage text -->
                <text class="bar-classifier-text"
                    x={CHART_PARAMS.regionStart + (CHART_PARAMS.percentageBoxWidth / 2)}
                    y={yPosition + 4}
                    text-anchor="middle"
                    fill="white"
                >
                    {(pctValue).toFixed(1)}%
                </text>

                <!-- City name -->
                <text class="bar-label"
                    x={barLabelStart}
                    y={barLabelTop + (i * CHART_PARAMS.barGap) + 1}
                >{cmaData.GEO_NAME}</text>
            {/each}
        </svg>
    </div>
</div>

<style>
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

    .chart-wrapper {
        margin: 20px 0;
        min-width: 250px;
        max-width: 100%;
        width: 100%;
        overflow-x: auto;
    }

    #chart {
        margin-top: 10px;
        margin-bottom: 10px;
        background-color: var(--brandWhite);
    }

    .grid-primary {
        stroke: var(--brandDarkBlue);
        stroke-width: 0.5px;
    }

    .axis-label {
        fill: var(--brandBlack);
        font-size: 12px;
        font-family: TradeGothicLTLight;
    }

    .bar-data {
        stroke: var(--brandLightBlue);
        stroke-opacity: 0.6;
    }

    .bar-classifier-box {
        stroke-width: 1;
        stroke-opacity: 1;
    }

    .bar-classifier-text {
        font-size: 12px;
        font-family: TradeGothicLTLight;
        font-weight: bold;
    }

    .bar-label {
        fill: var(--brandBlack);
        font-size: 14px;
        font-family: TradeGothicLTLight;
    }

    .legend-section {
        margin: 10px 0;
        padding-top: 5px;
    }

    .legend-label {
        font-size: 14px;
        fill: #000000;
        font-family: TradeGothicLTLight;
    }
</style>
