const fs = require('fs');
const path = require('path');

const csvPath = path.join(__dirname, '..', 'docs', 'canada-us-visits', 'us_normalized_trips.csv');
const text = fs.readFileSync(csvPath, 'utf8');
const lines = text.split(/\r?\n/);

// stateToRegion mapping copied from +page.svelte
const stateToRegion = {
	'IL': 'Midwest', 'IN': 'Midwest', 'MI': 'Midwest', 'OH': 'Midwest', 'WI': 'Midwest',
	'IA': 'Midwest', 'KS': 'Midwest', 'MN': 'Midwest', 'MO': 'Midwest', 'NE': 'Midwest',
	'ND': 'Midwest', 'SD': 'Midwest',
	// Northeast
	'CT': 'Northeast', 'ME': 'Northeast', 'MA': 'Northeast', 'NH': 'Northeast', 'RI': 'Northeast',
	'VT': 'Northeast', 'NJ': 'Northeast', 'NY': 'Northeast', 'PA': 'Northeast',
	'DE': 'Northeast', 'MD': 'Northeast',
	// Southwest
	'AZ': 'Southwest', 'NM': 'Southwest', 'OK': 'Southwest', 'TX': 'Southwest',
	'CO': 'Southwest', 'NV': 'Southwest', 'UT': 'Southwest',
	// Southeast
	'AL': 'Southeast', 'AR': 'Southeast', 'FL': 'Southeast', 'GA': 'Southeast', 'KY': 'Southeast',
	'LA': 'Southeast', 'MS': 'Southeast', 'NC': 'Southeast', 'SC': 'Southeast', 'TN': 'Southeast',
	'VA': 'Southeast', 'WV': 'Southeast', 'DC': 'Southeast',
	// Pacific
	'AK': 'Pacific', 'CA': 'Pacific', 'HI': 'Pacific', 'OR': 'Pacific', 'WA': 'Pacific', 'ID': 'Pacific'
};

function getMetroRegion(metroName) {
	const stateMatch = metroName.match(/,\s*([A-Z]{2})/);
	if (stateMatch) {
		const state = stateMatch[1];
		return stateToRegion[state] || null;
	}
	const multiStateMatch = metroName.match(/,\s*([A-Z]{2}(?:-[A-Z]{2})+)/);
	if (multiStateMatch) {
		const firstState = multiStateMatch[1].split('-')[0];
		return stateToRegion[firstState] || null;
	}
	return null;
}

const startDate = new Date('2024-04-01');
const endDate = new Date('2026-03-31');
const period1Start = new Date('2024-04-01');
const period1End = new Date('2025-03-31');
const period2Start = new Date('2025-04-01');
const period2End = new Date('2026-03-31');

const metroRecords = new Map(); // metro -> array of {date, normalized}

for (let i = 1; i < lines.length; i++) {
	const line = lines[i].trim();
	if (!line) continue;
	let match = line.match(/^"([^"]+)",([0-9]{8}),(.+)$/);
	let metro, dateStr, normalized;
	if (match) {
		metro = match[1];
		dateStr = match[2];
		normalized = parseFloat(match[3]);
	} else {
		match = line.match(/^([^,]+),([0-9]{8}),(.+)$/);
		if (!match) continue;
		metro = match[1];
		dateStr = match[2];
		normalized = parseFloat(match[3]);
	}
	const year = parseInt(dateStr.substring(0,4), 10);
	const month = parseInt(dateStr.substring(4,6), 10) - 1;
	const day = parseInt(dateStr.substring(6,8), 10);
	const date = new Date(year, month, day);
	if (isNaN(date.getTime())) continue;
	if (date < startDate || date > endDate) continue;
	if (!metroRecords.has(metro)) metroRecords.set(metro, []);
	metroRecords.get(metro).push({date, normalized});
}

const totalUniqueMetros = metroRecords.size;
let passPeriodCounts = 0;
let failPeriodCounts = 0;
let regionNullCount = 0;
let finalCount = 0;
const metrosFailingPeriod = [];
const metrosRegionNull = [];

for (const [metro, recs] of metroRecords.entries()) {
	const period1Count = recs.filter(r => r.date >= period1Start && r.date <= period1End).length;
	const period2Count = recs.filter(r => r.date >= period2Start && r.date <= period2End).length;
	const region = getMetroRegion(metro);
	if (region === null) {
		regionNullCount++;
		metrosRegionNull.push(metro);
	}
	if (period1Count < 10 || period2Count < 10) {
		failPeriodCounts++;
		metrosFailingPeriod.push({metro, period1Count, period2Count, region});
	} else {
		passPeriodCounts++;
		if (region !== null) finalCount++;
	}
}

console.log('Total unique metros in date range:', totalUniqueMetros);
console.log('Metros with sufficient period counts (both >=10):', passPeriodCounts);
console.log('Metros failing period counts:', failPeriodCounts);
console.log('Metros with region=null:', regionNullCount);
console.log('Estimated frontend visible metros (passes period counts and has region):', finalCount);

// Print small lists for inspection
console.log('\nSample metros failing due to period counts (first 20):');
console.log(metrosFailingPeriod.slice(0,20));
console.log('\nSample metros with region null (first 20):');
console.log(metrosRegionNull.slice(0,20));
