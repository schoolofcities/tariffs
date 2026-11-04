// Report figures: which chart component draws each one. No regions are emphasised
// (the docx doesn't). Each chart's
// title is its caption as written in the report docx; data comes from the generated
// content (scripts/build_report_content.py -> figureData[n]).


export const FIGURES = {
	1: {
		type: 'timeline',
	},
	2: {
		type: 'paired'
	},
	3: {
		type: 'stacked'
	},
	4: {
		type: 'paired'
	},
	5: {
		type: 'grouped'
	},
	6: {
		type: 'stacked'
	},
	7: {
		type: 'ranked'
	},
	8: {
		type: 'grouped'
	},
	9: {
		type: 'stacked'
	},
	10: {
		type: 'ranked'
	},
	11: {
		type: 'grouped'
	},
	12: {
		type: 'ranked'
	},
	13: {
		type: 'grouped'
	},
	14: {
		type: 'industry',
	}
};
