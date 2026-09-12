<script>
    export let correlations = [];  // from industryCorrelations.js
    export let model = null;       // from RegressionView's fitted model (optional)

    // Top negative correlation with p < 0.1
    $: topNeg = correlations
        .filter(d => d.correlation !== null && d.pValue !== null && d.pValue < 0.1 && d.correlation < 0)
        .sort((a, b) => a.correlation - b.correlation)[0];

    // Top positive correlation with p < 0.1
    $: topPos = correlations
        .filter(d => d.correlation !== null && d.pValue !== null && d.pValue < 0.1 && d.correlation > 0)
        .sort((a, b) => b.correlation - a.correlation)[0];

    // Count industries with p < 0.1
    $: sigCount = correlations.filter(d => d.pValue !== null && d.pValue < 0.1).length;
    $: negCount = correlations.filter(d => d.pValue !== null && d.pValue < 0.1 && d.correlation < 0).length;

    function fmt(v) {
        if (v === null || v === undefined) return '—';
        return (v > 0 ? '+' : '') + v.toFixed(3);
    }
    function fmtPct(v) {
        if (v === null || v === undefined) return '—';
        return (v * 100).toFixed(1) + '%';
    }
</script>

<div class="cards-row">
    {#if topNeg}
        <div class="card card--negative">
            <div class="card-eyebrow">Strongest negative predictor</div>
            <div class="card-industry">{topNeg.industry}</div>
            <div class="card-stat">{fmt(topNeg.correlation)}</div>
            <div class="card-sublabel">correlation with visit change</div>
            <div class="card-pvalue">p = {topNeg.pValue < 0.001 ? '<0.001' : topNeg.pValue.toFixed(3)}</div>
        </div>
    {/if}

    {#if topPos}
        <div class="card card--positive">
            <div class="card-eyebrow">Strongest positive predictor</div>
            <div class="card-industry">{topPos.industry}</div>
            <div class="card-stat">{fmt(topPos.correlation)}</div>
            <div class="card-sublabel">correlation with visit change</div>
            <div class="card-pvalue">p = {topPos.pValue < 0.001 ? '<0.001' : topPos.pValue.toFixed(3)}</div>
        </div>
    {:else}
        <div class="card card--neutral">
            <div class="card-eyebrow">Significant industries</div>
            <div class="card-industry">{sigCount} of {correlations.length}</div>
            <div class="card-stat">{negCount}</div>
            <div class="card-sublabel">industries negatively correlated (p &lt; 0.1)</div>
            <div class="card-pvalue">at 10% significance level</div>
        </div>
    {/if}

    <div class="card card--neutral">
        <div class="card-eyebrow">Industries measured</div>
        <div class="card-industry">{correlations.length} sectors</div>
        <div class="card-stat">{sigCount}</div>
        <div class="card-sublabel">with significant correlation to visit decline</div>
        <div class="card-pvalue">at p &lt; 0.10 threshold</div>
    </div>
</div>

<style>
    .cards-row {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        max-width: 680px;
        margin: 24px auto;
    }

    .card {
        flex: 1 1 180px;
        min-width: 160px;
        border-radius: 6px;
        padding: 16px 18px;
        border-left: 4px solid transparent;
        background: var(--brandWhite);
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }

    .card--negative {
        border-left-color: var(--brandRed, #DC4633);
        background: rgba(220, 70, 51, 0.04);
    }

    .card--positive {
        border-left-color: var(--brandMedBlue, #007FA3);
        background: rgba(0, 127, 163, 0.04);
    }

    .card--neutral {
        border-left-color: var(--brandGray, #cccccc);
        background: rgba(0,0,0,0.02);
    }

    .card-eyebrow {
        font-family: OpenSansBold, sans-serif;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--brandGray70, #666);
        margin-bottom: 6px;
    }

    .card-industry {
        font-family: OpenSansBold, sans-serif;
        font-size: 14px;
        color: var(--brandGray90);
        margin-bottom: 8px;
        line-height: 1.3;
    }

    .card-stat {
        font-family: TradeGothicBold, sans-serif;
        font-size: 28px;
        line-height: 1;
        margin-bottom: 4px;
    }

    .card--negative .card-stat { color: var(--brandRed, #DC4633); }
    .card--positive .card-stat { color: var(--brandMedBlue, #007FA3); }
    .card--neutral  .card-stat { color: var(--brandGray90); }

    .card-sublabel {
        font-family: OpenSans, sans-serif;
        font-size: 11px;
        color: var(--brandGray70, #666);
        line-height: 1.4;
    }

    .card-pvalue {
        font-family: OpenSans, sans-serif;
        font-size: 11px;
        color: var(--brandGray70, #666);
        margin-top: 6px;
        opacity: 0.8;
    }
</style>
