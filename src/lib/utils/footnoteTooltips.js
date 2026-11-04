// Svelte action: gives School of Cities footnote markers inside generated {@html}
// content the same hover tooltip as the <Footnote> component (same markup, classes
// and timing). Use on a container: <div use:footnoteTooltips={footnotes}>.
// footnotes: [{ id, text }]

export function footnoteTooltips(node, footnotes) {
	let notes = new Map(footnotes.map((f) => [String(f.id), f.text]));
	let tooltip = null;
	let hideTimeout;

	function remove() {
		tooltip?.remove();
		tooltip = null;
	}
	function scheduleHide() {
		clearTimeout(hideTimeout);
		hideTimeout = setTimeout(remove, 250);
	}
	function show(ref) {
		clearTimeout(hideTimeout);
		const id = ref.id.replace('footnote-ref-', '');
		if (tooltip?.dataset.id === id) return;
		remove();
		if (!notes.has(id)) return;
		tooltip = document.createElement('div');
		tooltip.className = 'footnoteTooltip';
		tooltip.setAttribute('role', 'tooltip');
		tooltip.dataset.id = id;
		tooltip.innerHTML = `<span class="footnoteNumber">[${id}]</span><p>${notes.get(id)}</p>`;
		tooltip.addEventListener('mouseenter', () => clearTimeout(hideTimeout));
		tooltip.addEventListener('mouseleave', scheduleHide);
		ref.parentElement.appendChild(tooltip);
	}

	function over(e) {
		const ref = e.target.closest?.('a.footnote-ref');
		if (ref && node.contains(ref)) show(ref);
	}
	function out(e) {
		const ref = e.target.closest?.('a.footnote-ref');
		if (ref && !ref.contains(e.relatedTarget)) scheduleHide();
	}
	function click(e) {
		const ref = e.target.closest?.('a.footnote-ref');
		if (!ref || !node.contains(ref)) return;
		const target = document.getElementById(ref.getAttribute('href').slice(1));
		if (!target) return;
		e.preventDefault();
		target.scrollIntoView({ behavior: 'auto', block: 'start' });
	}

	node.addEventListener('mouseover', over);
	node.addEventListener('mouseout', out);
	node.addEventListener('click', click);

	return {
		update(next) {
			notes = new Map(next.map((f) => [String(f.id), f.text]));
		},
		destroy() {
			clearTimeout(hideTimeout);
			remove();
			node.removeEventListener('mouseover', over);
			node.removeEventListener('mouseout', out);
			node.removeEventListener('click', click);
		}
	};
}
