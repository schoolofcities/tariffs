<!--
	Page title (h1) with an optional subtitle, used by every page except the homepage.
	Styles are global (.page-heading, .page-title, .page-subtitle in global.css), along
	with the square beside the title.

	id: optional id on the h1 (e.g. a table-of-contents target).
-->
<script>
	let { title, subtitle = '', id = undefined } = $props();
</script>

<header class="page-heading">
	<h1 class="page-title" {id}>{title}</h1>
	{#if subtitle}<p class="page-subtitle">{subtitle}</p>{/if}
</header>
