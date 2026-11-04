<script>
	/** Address search (OpenStreetMap Nominatim), limited to Canada. */
	let { onselect } = $props();

	let query = $state('');
	let busy = $state(false);
	let message = $state('');

	const NOMINATIM = 'https://nominatim.openstreetmap.org/search?format=jsonv2&countrycodes=ca&limit=1&q=';

	async function search() {
		const q = query.trim();
		if (!q || busy) return;
		busy = true;
		message = '';
		try {
			const results = await fetch(NOMINATIM + encodeURIComponent(q)).then((r) => r.json());
			if (results.length) {
				onselect(Number(results[0].lon), Number(results[0].lat));
			} else {
				message = 'No match found';
			}
		} catch {
			message = 'Search unavailable';
		} finally {
			busy = false;
		}
	}
</script>

<form onsubmit={(e) => (e.preventDefault(), search())}>
	<input bind:value={query} placeholder="Search and fly to a location..." aria-label="Search for a location" />
	<button type="submit" disabled={!query.trim() || busy}>Search</button>
	{#if message}<span class="message">{message}</span>{/if}
</form>

<style>
	form {
		display: flex;
		align-items: center;
		gap: 2px;
		font-family: OpenSans, sans-serif;
		font-size: 12px;
	}

	input {
		width: 185px;
		font: inherit;
		border: 1.5px solid var(--brandGray);
		padding: 2px 6px;
		border-radius: 4px;
	}

	button {
		font: inherit;
		padding: 2px 5px;
		border: 1.5px solid var(--brandGray);
		border-radius: 4px;
		background-color: var(--brandWhite);
		cursor: pointer;
	}

	button:hover:enabled {
		background-color: var(--brandLightBlue);
	}

	button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.message {
		margin-left: 4px;
		padding: 1px 6px;
		border-radius: 4px;
		background: rgba(255, 255, 255, 0.9);
		color: var(--brandGray70);
	}
</style>
