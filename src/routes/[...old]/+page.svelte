<script>
	import Redirect from '$lib/components/layout/Redirect.svelte';

	let { data } = $props();
</script>

<Redirect to={data.to} />
