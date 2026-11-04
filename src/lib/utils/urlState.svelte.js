// Mirror a component's selection state to the URL query string, so any view
// can be shared as a link. Call during component init:
//
//   let sel = $state({ ...DEFAULTS });
//   syncUrlState(sel, {
//     tariff:  { values: ['ScenAfter', 'Steel', ...] },
//     effects: { values: ['DIR', 'INDIR', 'INDCD'], multiple: true },
//   }, DEFAULTS);
//
// Only allowed values are read back; defaults are left out of the URL.

import { afterNavigate, replaceState } from '$app/navigation';

const serialize = (v) => (Array.isArray(v) ? v.join(',') : String(v));

export function syncUrlState(state, spec, defaults) {
	let ready = $state(false);

	// afterNavigate (not onMount): replaceState needs the router to be started.
	afterNavigate(() => {
		if (ready) return;
		const q = new URLSearchParams(window.location.search);
		for (const [key, { values, multiple }] of Object.entries(spec)) {
			const raw = q.get(key);
			if (raw == null) continue;
			if (multiple) {
				const picked = raw.split(',').filter((v) => values.includes(v));
				if (picked.length) state[key] = picked;
			} else if (values.includes(raw)) {
				state[key] = raw;
			}
		}
		ready = true;
	});

	$effect(() => {
		const current = Object.keys(spec).map((key) => [key, serialize(state[key]), serialize(defaults[key])]);
		if (!ready) return;
		const q = new URLSearchParams();
		for (const [key, value, fallback] of current) if (value !== fallback) q.set(key, value);
		const qs = q.toString();
		replaceState(qs ? `?${qs}` : window.location.pathname, {});
	});
}
