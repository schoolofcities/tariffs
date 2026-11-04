// Loads the per-geography lookup files written by scripts/build_*_data.py.
//
// Each file is loaded at most once per page (the promise is cached), so
// switching back and forth between geographies never re-fetches, and a slow
// response can never overwrite a newer one: results are stored by geography,
// and the map always renders whatever the *current* selection points at.

const cache = new Map(); // url -> Promise<AreaData>

/**
 * @typedef {Object} AreaData
 * @property {string[]} ids
 * @property {(string|null)[]|undefined} names
 * @property {Map<string, number>} index           id -> row
 * @property {Record<string, (number|null)[]>} cols column -> values by row
 * @property {(i: number) => [number, number] | null} point
 */

/** @returns {Promise<AreaData>} */
export function loadAreaData(url) {
	if (!cache.has(url)) {
		const p = fetch(url)
			.then((r) => {
				if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
				return r.json();
			})
			.then(prepare);
		// Don't cache failures, so a later attempt can retry.
		p.catch(() => cache.delete(url));
		cache.set(url, p);
	}
	return cache.get(url);
}

function prepare(raw) {
	const index = new Map(raw.ids.map((id, i) => [id, i]));
	return {
		ids: raw.ids,
		names: raw.names,
		cols: raw.cols,
		index,
		point: (i) => (raw.lon?.[i] == null ? null : [raw.lon[i], raw.lat[i]])
	};
}

/** Value for one area + column, or null when missing. */
export function valueOf(data, id, column) {
	const i = data.index.get(id);
	if (i === undefined) return null;
	const v = data.cols[column]?.[i];
	return v == null || Number.isNaN(v) ? null : v;
}
