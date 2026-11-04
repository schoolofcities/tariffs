<script>
	import '$lib/styles/global.css';
	import SiteHeader from '$lib/components/layout/SiteHeader.svelte';
	import PasswordGate from '$lib/components/layout/PasswordGate.svelte';

	let { children } = $props();
</script>

<!-- while in development: one password for the whole site, remembered per browser -->
<PasswordGate />

<SiteHeader />

{@render children()}
