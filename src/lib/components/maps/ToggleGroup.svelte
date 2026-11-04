<script>
	/**
	 * Row of toggle buttons. options: [{ value, label }]
	 * Single-select by default; with `multiple`, `value` is an array and at
	 * least one option always stays selected.
	 */
	let { options, value = $bindable(), label, multiple = false } = $props();

	const isOn = (v) => (multiple ? value.includes(v) : value === v);

	function toggle(v) {
		if (!multiple) return (value = v);
		if (!value.includes(v)) return (value = [...value, v]);
		if (value.length > 1) value = value.filter((x) => x !== v);
	}
</script>

<div class="toggle-group" role="group" aria-label={label}>
	{#each options as option (option.value)}
		<button
			type="button"
			class:selected={isOn(option.value)}
			aria-pressed={isOn(option.value)}
			onclick={() => toggle(option.value)}
		>
			{option.label}
		</button>
	{/each}
</div>

<style>
	.toggle-group {
		display: flex;
		gap: 10px;
	}

	button {
		flex: 1;
		padding: 6px 12px;
		border: 1px solid var(--brandGray);
		border-radius: 5px;
		cursor: pointer;
		opacity: 0.5;
		background-color: var(--brandWhite);
		color: var(--brandGray80);
		font-family: TradeGothicBold, sans-serif;
		font-size: 16px;
		text-align: center;
		transition: opacity 0.2s ease;
	}

	button.selected {
		opacity: 1;
		border: 2px solid var(--brandLightBlue);
	}

	button:hover {
		opacity: 1;
		border: 2px solid var(--brandMedBlue);
	}
</style>
