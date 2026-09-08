<script>
    import { onMount } from 'svelte';
    import Select from "svelte-select";
    import { scaleLinear, scalePow } from 'd3-scale';
    import { GRADUATED_COLORS } from './constantsv2.js';

    /*
      Data comes straight from roll_up_to_cma_prov.py:
        json/all_scenarios_cma.json
        json/all_scenarios_province.json
        json/rollup_breaks.json
      Each record: GEO_LEVEL, GEO_UID, GEO_NAME, CSD_COUNT, TOTAL_EMP,
                   S{n}_{DIR|INDIR|INDCD|TOT}_Jobs, S{n}_{...}_Pct
    */

    // Scenario codes are read from the data; give the ones you have real names here.
    // Keys must match the S{n} codes in the rollup output. Your data has
    // S1, S3, S4, S5, S6 — there is no S2. Replace these with the real
    // tariff descriptions; unlisted codes fall back to "Scenario n".
    const SCENARIO_LABELS = {
        S1: "Household Consumption",
        S3: "Agri-food & Seafood",
        S4: "Steel & Aluminum",
        S5: "Softwood Lumber",
        S6: "Autos & Parts"
    };
    
    const EFFECTS = [
        { code: "TOT",   label: "All effects" },
        { code: "DIR",   label: "Direct" },
        { code: "INDIR", label: "Indirect" },
        { code: "INDCD", label: "Induced" }
    ];

    const EFFECT_TEXT = {
        TOT:   "Total job losses — direct, indirect and induced combined.",
        DIR:   "Direct job losses in the industries facing the tariff.",
        INDIR: "Indirect job losses in supplier industries.",
        INDCD: "Induced job losses from reduced household spending."
    };

    let cmaData = $state([]);
    let provData = $state([]);
    let breaks = $state({});

    let geoType = $state("CMA");            // ["CMA", "Province"]
    let scenario = $state("S1");
    let effectType = $state("TOT");         // ["TOT","DIR","INDIR","INDCD"]
    let metricType = $state("Count");       // ["Percent", "Count"]
    // Percent fields only exist once the rollup is run with --employment-col.
    let hasPercent = $derived.by(() => {
        const source = geoType === "CMA" ? cmaData : provData;
        return Boolean(source.length && pctKey in source[0]);
    });
    let scaleType = $state("Linear");       // ["Linear", "Power-0.2"]
    let excludeResidual = $state(true);     // hide the Non-CMA / Unassigned bucket

    let scenarioList = $derived.by(() => {
        const source = cmaData.length ? cmaData : provData;
        if (!source.length) return [];
        const codes = new Set();
        for (const key of Object.keys(source[0])) {
            const m = key.match(/^(S\d+)_(?:DIR|INDIR|INDCD|TOT)_Jobs$/);
            if (m) codes.add(m[1]);
        }
        return [...codes]
            .sort((a, b) => +a.slice(1) - +b.slice(1))
            .map(code => ({ value: code, label: SCENARIO_LABELS[code] ?? `Scenario ${code.slice(1)}` }));
    });

    let scenarioLabel = $derived(SCENARIO_LABELS[scenario] ?? `Scenario ${scenario.slice(1)}`);
    let countKey = $derived(`${scenario}_${effectType}_Jobs`);
    let pctKey = $derived(`${scenario}_${effectType}_Pct`);
    let sortKey = $derived(metricType === "Percent" && hasPercent ? pctKey : countKey);

    let rows = $derived.by(() => {
        const source = geoType === "CMA" ? cmaData : provData;
        if (!source.length) return [];
        return source
            .filter(d => !(excludeResidual && (d.GEO_UID === "Non-CMA" || d.GEO_UID === "Unassigned")))
            .filter(d => d[sortKey] != null && Number.isFinite(+d[sortKey]))
            .map(d => ({ ...d, __value: +d[sortKey] }))
            .sort((a, b) => b.__value - a.__value);
    });

    // Percentage-box class breaks: precomputed by the script, quantiles as fallback.
    let pctBreaks = $derived.by(() => {
        const level = geoType === "CMA" ? "cma" : "province";
        const supplied = breaks?.[level]?.[pctKey];
        if (supplied?.length) return supplied;
        const vals = rows.map(d => +d[pctKey]).filter(Number.isFinite).sort((a, b) => a - b);
        if (vals.length < 5) return [];
        return [0.2, 0.4, 0.6, 0.8].map(q => {
            const v = vals[Math.floor(q * (vals.length - 1))];
            return Math.round(v * 10) / 10;
        });
    });

    // Chart geometry — same conventions as HorizontalBarChartv2
    let chartWidth = $state(0);
    let legendWidth = $state(0);
    let chartHeight = $derived(24 * rows.length + 40);

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

    let plotWidth = $derived(
        Math.max(0, chartWidth - CHART_PARAMS.xAxisStart - CHART_PARAMS.chartEndGap)
    );

    // Domain is rescaled per selection, because scenarios and geo levels differ
    // by orders of magnitude. That is what the scale note below warns about.
    let maxValue = $derived(rows.length ? niceCeiling(rows[0].__value) : 0);

    function niceCeiling(v) {
        if (!(v > 0)) return 1;
        const mag = Math.pow(10, Math.floor(Math.log10(v)));
        return Math.ceil(v / mag) * mag;
    }

    let xScale = $derived.by(() =>
        scaleType === "Linear"
            ? scaleLinear().domain([0, maxValue]).range([0, plotWidth])
            : scalePow().exponent(0.2).domain([0, maxValue]).range([0, plotWidth])
    );

    let gridBreaks = $derived.by(() => {
        if (!maxValue) return [0];
        if (scaleType === "Linear") {
            return [0, 0.25, 0.5, 0.75, 1].map(f => maxValue * f);
        }
        return [0, 0.02, 0.1, 0.3, 0.6, 1].map(f => maxValue * f);
    });

    function numberWithCommas(n) {
        const parts = n.toString().split(".");
        return parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",") + (parts[1] ? "." + parts[1] : "");
    }

    function formatAxis(n) {
        if (metricType === "Percent") return `${Math.round(n * 10) / 10}%`;
        if (n >= 1000) return `${Math.round(n / 100) / 10}K`;
        return Math.round(n).toString();
    }

    function formatValue(n) {
        if (n == null || !Number.isFinite(+n)) return "n/a";
        return metricType === "Percent"
            ? `${(+n).toFixed(1)}%`
            : numberWithCommas(Math.round(+n));
    }

    function getColorForPercentage(pctValue, breakpoints) {
        if (!breakpoints || breakpoints.length === 0) return GRADUATED_COLORS[0];
        for (let i = 0; i < breakpoints.length; i++) {
            if (pctValue <= breakpoints[i]) return GRADUATED_COLORS[i];
        }
        return GRADUATED_COLORS[breakpoints.length];
    }

    onMount(async () => {
        const [cmaRes, provRes, breaksRes] = await Promise.all([
            fetch('json/all_scenarios_cma.json'),
            fetch('json/all_scenarios_province.json'),
            fetch('json/rollup_breaks.json')
        ]);
        cmaData = await cmaRes.json();
        provData = await provRes.json();
        breaks = await breaksRes.json();
    });

    function geoTypeSelect(value) { geoType = value; }
    function effectSelect(value) { effectType = value; }
    function metricSelect(value) { metricType = value; }
    function scaleSelect(value) { scaleType = value; }

    function scenarioSelect(event) {
        const next = event.detail?.value;
        if (next) scenario = next;
    }
</script>

<div class="text">
    <div>
        <div id="select-wrapper">
            <div id="destext">
                <p style="margin-bottom: -5px;">Select a tariff scenario:</p>
            </div>
            <Select
                id='select'
                items={scenarioList}
                value={scenario}
                clearable={false}
                showChevron={true}
                listAutoWidth={true}
                searchable={false}
                listOffset={10}
                on:change={scenarioSelect}
            />
        </div>

        <div id="destext">
            <p style="margin-bottom: -5px;">Select a geographic level:</p>
        </div>
        <div class="button-group" style="margin-top: 10px;">
            <button
                class="toggle-button {geoType === 'CMA' ? 'selected' : ''}"
                type="button"
                onclick={() => geoTypeSelect("CMA")}
            >
                Census metropolitan areas
            </button>
            <button
                class="toggle-button {geoType === 'Province' ? 'selected' : ''}"
                type="button"
                onclick={() => geoTypeSelect("Province")}
            >
                Provinces and territories
            </button>
        </div>

        <div id="destext">
            <p style="margin-bottom: -5px;">Select which job losses to show:</p>
        </div>
        <div class="button-group" style="margin-top: 10px;">
            {#each EFFECTS as effect}
                <button
                    class="toggle-button {effectType === effect.code ? 'selected' : ''}"
                    type="button"
                    onclick={() => effectSelect(effect.code)}
                >
                    {effect.label}
                </button>
            {/each}
        </div>

        <div id="destext">
            <p style="margin-bottom: -5px;">Choose how to rank this indicator:</p>
        </div>
        <div class="button-group">
            <button
                class="toggle-button {metricType === 'Percent' ? 'selected' : ''}"
                type="button"
                disabled={!hasPercent}
                title={hasPercent ? "" : "Rerun the rollup with --employment-col to enable"}
                onclick={() => metricSelect("Percent")}
            >
                Share of employment
            </button>
            <button
                class="toggle-button {metricType === 'Count' ? 'selected' : ''}"
                type="button"
                onclick={() => metricSelect("Count")}
            >
                Total jobs
            </button>
        </div>

        <div id="destext">
            <p style="margin-bottom: -5px;">Choose the scale you want to use:</p>
        </div>
        <div class="button-group">
            <button
                class="toggle-button {scaleType === 'Linear' ? 'selected' : ''}"
                type="button"
                onclick={() => scaleSelect("Linear")}
            >
                Linear scale
            </button>
            <button
                class="toggle-button {scaleType === 'Power-0.2' ? 'selected' : ''}"
                type="button"
                onclick={() => scaleSelect("Power-0.2")}
            >
                Power scale
            </button>
        </div>
    </div>

    <!-- Legend section -->
    <div class="legend-section">
        <div id="destext">
            <p style="margin-bottom: -5px;">
                {scenarioLabel}: {EFFECT_TEXT[effectType]}
                Bars show {metricType === "Percent" ? "job losses as a share of employment" : "the number of jobs lost"};
                the coloured box shows {metricType === "Percent" ? "the job count" : "the share of employment"}.
            </p>
        </div>

        <div id="legend" bind:offsetWidth={legendWidth}>
            <svg width='100%' height='25'>
                {#if legendWidth && pctBreaks.length === 4}
                    {@const boxWidth = legendWidth / 7.1}
                    {#each GRADUATED_COLORS.slice(0, 5) as color, i}
                        <rect
                            class="box"
                            width={boxWidth}
                            height="12"
                            x={boxWidth * i}
                            y="0"
                            stroke="white" stroke-width="1"
                            style="fill:{color};"
                        />
                    {/each}
                    <text class="legend-label" text-anchor="middle" x={boxWidth} y="25">&lt;{pctBreaks[0]}%</text>
                    <text class="legend-label" text-anchor="middle" x={boxWidth * 2} y="25">{pctBreaks[1]}%</text>
                    <text class="legend-label" text-anchor="middle" x={boxWidth * 3} y="25">{pctBreaks[2]}%</text>
                    <text class="legend-label" text-anchor="middle" x={boxWidth * 4} y="25">&gt;{pctBreaks[3]}%</text>
                {/if}
            </svg>
        </div>
    </div>

    <div class='chart-wrapper' bind:offsetWidth={chartWidth}>
        <svg height={chartHeight} width={chartWidth} id="chart">
            <!-- Grid lines -->
            {#each gridBreaks as gridValue}
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
                    {formatAxis(gridValue)}
                </text>
            {/each}

            <!-- Data bars, ranked high to low -->
            {#each rows as row, i}
                {@const barWidth = xScale(row.__value)}
                {@const pctValue = +row[pctKey] || 0}
                {@const boxValue = metricType === "Percent" ? +row[countKey] : pctValue}
                {@const boxColor = getColorForPercentage(pctValue, pctBreaks)}
                {@const yPosition = CHART_PARAMS.barTop + (i * CHART_PARAMS.barGap)}

                <g>
                <title>{row.GEO_NAME}: {formatValue(row.__value)} ({row.CSD_COUNT} census subdivisions)</title>

                <line class="bar-data"
                    x1={barStart}
                    y1={yPosition}
                    x2={barStart + barWidth}
                    y2={yPosition}
                    stroke-width={CHART_PARAMS.barStrokeWidth}
                ></line>

                <!-- Complementary-metric box -->
                <rect class="bar-classifier-box"
                    x={CHART_PARAMS.regionStart}
                    y={yPosition - (CHART_PARAMS.percentageBoxHeight / 2)}
                    width={CHART_PARAMS.percentageBoxWidth}
                    height={CHART_PARAMS.percentageBoxHeight}
                    fill={boxColor}
                    stroke={boxColor}
                ></rect>

                <text class="bar-classifier-text"
                    x={CHART_PARAMS.regionStart + (CHART_PARAMS.percentageBoxWidth / 2)}
                    y={yPosition + 4}
                    text-anchor="middle"
                    fill="white"
                >
                    {metricType === "Percent"
                        ? (boxValue >= 1000 ? `${Math.round(boxValue / 100) / 10}K` : Math.round(boxValue))
                        : `${pctValue.toFixed(1)}%`}
                </text>

                <!-- Region name -->
                <text class="bar-label"
                    x={barLabelStart}
                    y={barLabelTop + (i * CHART_PARAMS.barGap) + 1}
                >{row.GEO_NAME}</text>
                </g>
            {/each}
        </svg>

        <div id="destext">
            <p>
                Note: each figure is the sum of the census subdivisions in that region.
                {geoType === 'CMA'
                    ? 'Census metropolitan areas exclude the parts of the country outside their boundaries, so they do not add to the national total.'
                    : 'Provinces and territories cover the whole country, so they add to the national total.'}
                The scale is rescaled for each selection — check the axis before comparing scenarios.
            </p>
        </div>
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

    .toggle-button:disabled {
        opacity: 0.25;
        cursor: not-allowed;
    }

    .toggle-button:focus-visible {
        outline: 2px solid var(--brandMedBlue);
        outline-offset: 2px;
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
        margin: 0px;
        margin-top: -20px;
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
        stroke: var(--brandGray);
        stroke-width: 0.5px;
    }

    .axis-label {
        fill: var(--brandBlack);
        font-size: 12px;
        font-family: OpenSans;
    }

    .bar-data {
        stroke: var(--brandGray);
        stroke-opacity: 1;
    }

    .bar-classifier-box {
        stroke-width: 1;
        stroke-opacity: 1;
    }

    .bar-classifier-text {
        font-size: 12px;
        font-family: OpenSans;
        font-weight: bold;
    }

    .bar-label {
        fill: var(--brandGray70);
        font-size: 14px;
        font-family: OpenSans;
    }

    .legend-section {
        margin: 10px 0;
        padding-top: 5px;
    }

    .legend-label {
        font-size: 14px;
        fill: #000000;
        font-family: OpenSans;
    }
</style>