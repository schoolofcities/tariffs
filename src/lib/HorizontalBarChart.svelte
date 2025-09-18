<script>
    import { onMount } from 'svelte';
    
    const GRADUATED_COLORS = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];
    
    let cmaPcts = [];
    let cmaCounts = [];
    
    onMount(async () => {
        const response = await fetch('json/cma_tariffs_percents_centroids.json');
        const pctData = await response.json();
        cmaPcts = pctData.filter(item => item.GEO_LEVEL === "Census metropolitan area");
        
        const countsResponse = await fetch('json/cma_tariffs_counts_centroids.json');
        const countsData = await countsResponse.json();
        cmaCounts = countsData.filter(item => item.GEO_LEVEL === "Census metropolitan area");
    });

    $: console.log(cmaPcts);
    $: console.log(cmaCounts);
    
</script>

<div>
    <!-- Chart markup will go here -->
</div>

<style>
</style>
