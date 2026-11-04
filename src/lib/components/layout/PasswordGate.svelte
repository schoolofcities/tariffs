<!--
	Site-wide password screen while the new site is in development. Once the password
	is entered, the browser remembers it (localStorage), so every other page, and later
	visits, open straight away.

	Note: this keeps casual visitors out; it isn't real security. On a static site the
	pages' content still ships to the browser.

	To change the password, replace PASSWORD_HASH with the SHA-256 of the new one, e.g.
	  printf '%s' 'new-password' | sha256sum
-->
<script>
	import { onMount } from 'svelte';

	const PASSWORD_HASH = 'a8f8a96834959c2dc070fd2607a18411d4c390c126a2006e2fb770412795cb74';
	const KEY = 'mt-unlocked';

	let unlocked = $state(false);
	let checked = $state(false);
	let password = $state('');
	let wrong = $state(false);

	onMount(() => {
		try {
			unlocked = localStorage.getItem(KEY) === PASSWORD_HASH;
		} catch {
			unlocked = false;
		}
		checked = true;
	});

	async function sha256(text) {
		const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
		return [...new Uint8Array(bytes)].map((b) => b.toString(16).padStart(2, '0')).join('');
	}

	async function submit(event) {
		event.preventDefault();
		if ((await sha256(password.trim())) === PASSWORD_HASH) {
			try {
				localStorage.setItem(KEY, PASSWORD_HASH);
			} catch {
				// storage blocked: stays unlocked for this visit only
			}
			unlocked = true;
			document.documentElement.classList.add(KEY);
		} else {
			wrong = true;
		}
	}

	// before the page paints: hide the screen straight away for browsers already unlocked
	const headScript = `<script>try{if(localStorage.getItem(${JSON.stringify(KEY)})===${JSON.stringify(PASSWORD_HASH)})document.documentElement.classList.add(${JSON.stringify(KEY)})}catch(e){}</` + `script>`;
</script>

<svelte:head>
	{@html headScript}
</svelte:head>

{#if !unlocked}
	<div class="gate" class:checked role="dialog" aria-modal="true" aria-labelledby="gate-title">
		<form class="box" onsubmit={submit}>
			<p class="wordmark">Mapping Tariffs</p>
			<h2 id="gate-title">This site is under development</h2>
			<p class="note">Please do not share without permission.</p>
			<div class="row">
				<input
					type="password"
					bind:value={password}
					oninput={() => (wrong = false)}
					placeholder="Password"
					aria-label="Password"
					aria-invalid={wrong}
					autocomplete="current-password"
				/>
				<button type="submit">Enter</button>
			</div>
			{#if wrong}<p class="error" role="alert">Incorrect password</p>{/if}
		</form>
	</div>
{/if}

<style>
	/* opaque cover over the whole site, above the header */
	.gate {
		position: fixed;
		inset: 0;
		z-index: 10000;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 16px;
		background: var(--brandWhite);
	}

	/* already unlocked (set by the head script before paint): never show it */
	:global(html.mt-unlocked) .gate {
		display: none;
	}

	/* square, flat */
	.box {
		width: 100%;
		max-width: 400px;
		padding: 28px 28px 24px;
		border: 1px solid var(--brandGray);
	}

	.wordmark {
		display: inline-block;
		margin: 0 0 18px;
		padding: 2px 10px;
		background: var(--brandDarkBlue);
		font-family: TradeGothicBold, sans-serif;
		font-size: 18px;
		line-height: 28px;
		color: var(--brandWhite);
	}

	h2 {
		margin: 0 0 6px;
		font-size: 22px;
		color: var(--brandBlack);
	}

	.note {
		margin: 0 0 18px;
		font-family: OpenSans, sans-serif;
		font-size: 14px;
		line-height: 20px;
		color: var(--brandGray70);
	}

	.row {
		display: flex;
		gap: 8px;
	}

	input {
		flex: 1;
		min-width: 0;
		padding: 8px 10px;
		border: 1px solid var(--brandGray);
		border-radius: 0;
		font-family: OpenSans, sans-serif;
		font-size: 15px;
	}

	input:focus {
		outline: none;
		border-color: var(--brandDarkBlue);
	}

	input[aria-invalid='true'] {
		border-color: var(--brandRed, #dc4633);
	}

	button {
		padding: 8px 16px;
		border: none;
		border-radius: 0;
		background: var(--brandDarkBlue);
		font-family: OpenSansBold, sans-serif;
		font-size: 14px;
		color: var(--brandWhite);
		cursor: pointer;
	}

	button:hover {
		background: var(--brandMedBlue);
	}

	.error {
		margin: 10px 0 0;
		font-family: OpenSans, sans-serif;
		font-size: 13px;
		color: var(--brandRed, #dc4633);
	}
</style>
