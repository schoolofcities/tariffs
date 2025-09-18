<script>
    import { onMount } from 'svelte';
    import Select from "svelte-select";
    
    const GRADUATED_COLORS = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];
    const TARIFF_LIST = ["All goods subject to tariffs", "Automobiles", "Aluminum", "Steel", "Copper", "Lumber", "Energy and natural resources", "Non-CUSMA-Compliant"];
    
    const TARIFF_NAME_CODES = {
        "All goods subject to tariffs": 'Total', 
        "Automobiles": 'Auto', 
        "Aluminum": 'Alum', 
        "Steel": 'Steel', 
        "Copper": 'Cop', 
        "Lumber": 'Lum', 
        "Energy and natural resources": 'Ene', 
        "Non-CUSMA-Compliant": 'CUSMA',
    }
    const TARIFF_IMPACT_CODES_PCT = {
        'Business': "_1",
        'EmployeeWork': "_2",
        'EmployeeHome': "_3",
    }
    const TARIFF_IMPACT_CODES_COUNT = {
        'Business': "_B",
        'EmployeeWork': "_E",
        'EmployeeHome': "_C",
    }

    let cmaPcts = $state([]);
    let cmaCounts = $state([]);

    let metricType = $state("Percent"); // ["Percent", "Count"]
    let impactType = $state("EmployeeHome"); // ["EmployeeHome","EmployeeWork", "Business"] 
    let tariffType = $state("All goods subject to tariffs"); // see full list in TARIFF_LIST

    function sortCmaData(data, metric) {
        const tariffKey = TARIFF_NAME_CODES[tariffType] + (metric === "Percent" ? TARIFF_IMPACT_CODES_PCT[impactType] : TARIFF_IMPACT_CODES_COUNT[impactType]);
        return data
            ?.filter(item => item[tariffKey])
            .sort(function(a,b) {return b[tariffKey] - a[tariffKey]})
    }

    let cmaPctsSorted = $derived(sortCmaData(cmaPcts, "Percent"));
    let cmaCountsSorted = $derived(sortCmaData(cmaCounts, "Count"));

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

    function impactTypeSelect(value) {
        impactType = value;
    }

    function tariffTypeSelect(event) {
        tariffType = event.detail.value;
    }

    $effect(() => {
        // console.log($state.snapshot(cmaPcts));
        // console.log(cmaCounts);
    });

    $effect(() => {
        // metricType, impactType, tariffType;
        // console.log(`changed state!! ${metricType}, ${impactType}, ${tariffType}`);
        console.log($state.snapshot(cmaPctsSorted));
        
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
            Choose how to display this indicator:
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
    </div>

    <div class='chart-wrapper'>

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
</style>
