// School of Cities footnote helpers (from schoolofcities.github.io/src/lib/footnotes).

export function parseMarkdown(text) {
	return text
		.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') // bold
		.replace(/\*(?!\*)(.+?)\*/g, '<em>$1</em>') // italics
		.replace(/\[([^\]]+)]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>') // links
		.replace(/\n\n/g, '<span class="footnote-gap"></span>') // blank line between references
		.replace(/\n/g, '<br>'); // line breaks
}

export function createFootnoteStore() {
	let footnotes = [];

	function addFootnote(text) {
		const id = footnotes.length + 1;
		const parsed = parseMarkdown(text);
		footnotes.push({ id, text: parsed });
		return [id, parsed];
	}

	return {
		get footnotes() {
			return footnotes;
		},
		addFootnote
	};
}
