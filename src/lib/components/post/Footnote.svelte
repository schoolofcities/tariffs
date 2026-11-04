<script>
	/**
	 * Inline footnote marker with hover tooltip (School of Cities, from
	 * schoolofcities.github.io/src/lib/footnotes). id = [n, html] as returned by
	 * createFootnoteStore().addFootnote(). Styles are global (global.css) so the same
	 * markup also works in generated {@html} content; see footnoteTooltips.js.
	 */
	let { id } = $props();
	const n = $derived(id[0]);
	const footnoteText = $derived(id[1]);

	let isHovered = $state(false);
	let hideTimeout;

	// A short grace period before hiding, cancelled if the mouse re-enters (either
	// the reference or the tooltip) in time, so the tooltip's text can be selected.
	function show() {
		clearTimeout(hideTimeout);
		isHovered = true;
	}
	function scheduleHide() {
		clearTimeout(hideTimeout);
		hideTimeout = setTimeout(() => (isHovered = false), 250);
	}
	function jump(e) {
		e.preventDefault();
		document.getElementById(`footnote-${n}`)?.scrollIntoView({ behavior: 'auto', block: 'start' });
	}
</script>

<span class="footnote-ref-wrapper"
	><a id="footnote-ref-{n}" href="#footnote-{n}" class="footnote-ref" onclick={jump} onmouseenter={show} onmouseleave={scheduleHide}
		><span>[{n}]</span></a
	>{#if isHovered}<div class="footnoteTooltip" role="tooltip" onmouseenter={show} onmouseleave={scheduleHide}>
			<span class="footnoteNumber">[{n}]</span>
			<p>{@html footnoteText}</p>
		</div>{/if}</span
>
