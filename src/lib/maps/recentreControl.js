// MapLibre control: one button (styled like the zoom buttons) that flies back to a view,
// e.g. the starting view of Canada. Add it right after the NavigationControl in the same
// corner so it stacks under the zoom buttons:
//
//   map.addControl(new RecentreControl(INITIAL_VIEW), 'top-right');

// crosshair / "re-centre" icon, drawn in the button's text colour
const ICON = `<svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round">
	<circle cx="10" cy="10" r="5.2" />
	<circle cx="10" cy="10" r="1.4" fill="currentColor" stroke="none" />
	<path d="M10 1.8v3M10 15.2v3M1.8 10h3M15.2 10h3" />
</svg>`;

export class RecentreControl {
	/** @param {{ center: [number, number], zoom: number, pitch?: number, bearing?: number }} view */
	constructor(view) {
		this.view = view;
	}

	onAdd(map) {
		this.map = map;
		this.container = document.createElement('div');
		this.container.className = 'maplibregl-ctrl maplibregl-ctrl-group';

		const button = document.createElement('button');
		button.type = 'button';
		button.className = 'recentre-button';
		button.title = 'Re-centre map';
		button.setAttribute('aria-label', 'Re-centre map');
		button.innerHTML = ICON;
		button.addEventListener('click', () => {
			const { center, zoom, pitch = 0, bearing = 0 } = this.view;
			map.flyTo({ center, zoom, pitch, bearing, essential: true });
		});

		this.container.appendChild(button);
		return this.container;
	}

	onRemove() {
		this.container.remove();
		this.map = undefined;
	}
}
