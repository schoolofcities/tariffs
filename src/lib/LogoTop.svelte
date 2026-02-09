<script>
	import "../assets/global-styles.css";
	import logoBlueColour from '../assets/sofc-uoft-logo-blue-colour.svg';
	import logoWhiteColour from '../assets/sofc-uoft-logo-white-colour.svg';
	import logoBlack from '../assets/sofc-uoft-logo-black.svg';
	import logoWhite from '../assets/sofc-uoft-logo-white.svg';

	export let logoType = 'Blue';
	export let backgroundColor = 'var(--brandWhite)';

	let menuOpen = false;

	const links = [
		{ name: "Homepage", url: "./" },
		{ name: "Background and findings", url: "./potential-local-impacts" },
		// { name: "Lumber and Trucks", url: "./lumber-trucks" },
		{ name: "National map", url: "./map" },
		{ name: "Metro area rankings", url: "./cma-ranking-charts" }
	];
</script>


<div class="logo-container" style="background-color: {backgroundColor}">
	<a href="https://schoolofcities.utoronto.ca/" target="_blank" class="logo-link">
		{#if logoType === 'Blue'}
			<img src={logoBlueColour} alt="UofT and School of Cities logos" class="logo" />
		{:else if logoType === 'White'}
			<img src={logoWhiteColour} alt="UofT and School of Cities logos" class="logo" />
		{:else if logoType === 'Black'}
			<img src={logoBlack} alt="UofT and School of Cities logos" class="logo" />
		{:else if logoType === 'WhiteOnly'}
			<img src={logoWhite} alt="UofT and School of Cities logos" class="logo" />
		{/if}
	</a>

	<div class="nav-area">
		<!-- <a href="./" class="research-link">Mapping Tariffs</a> -->
		<button class="menu-toggle" on:click={() => (menuOpen = !menuOpen)}>
			<span class="research-link">Mapping Tariffs</span> ▾
		</button>

		{#if menuOpen}
			<div class="dropdown">
				{#each links as link}
					<a href={link.url} class="dropdown-item">{link.name}</a>
				{/each}
			</div>
		{/if}
	</div>
</div>


<style>

	.logo-container {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: 0px;
		margin-bottom: 60px;
		border-bottom: solid 1px var(--brandDarkBlue);
		padding: 0px 35px;
		position: relative;
	}

	.logo {
		width: 300px;
		height: 60px;
	}

	.logo:hover {
		opacity: 0.75;
	}

	.nav-area {
		display: flex;
		align-items: center;
		position: relative;
	}

	.research-link {
		font-family: SourceSerifItalic, serif;
		font-size: 18px;
		text-decoration: underline;
		text-decoration-thickness: 1px;
		color: var(--brandDarkBlue);
		margin-right: 10px;
	}

	.research-link:hover {
		color: var(--brandMedGreen);
	}

	.menu-toggle {
		background: none;
		border: none;
		font-size: 18px;
		cursor: pointer;
		color: var(--brandDarkBlue);
		transform: translateY(-2px);
	}

	.menu-toggle:hover {
		color: var(--brandMedGreen);
	}

	.dropdown {
		position: absolute;
		top: 46px;
		right: 0;
		background: var(--brandWhite);
		border: 1px solid var(--brandDarkBlue);
		box-shadow: 0 2px 4px rgba(0,0,0,0.1);
		border-radius: 0px;
		display: flex;
		flex-direction: column;
		min-width: 150px;
		z-index: 5;
	}

	.dropdown-item {
		padding: 6px;
		padding-left: 10px;
		color: var(--brandDarkBlue);
		text-decoration: none;
		font-size: 14px;
	}

	.dropdown-item:hover {
		background: var(--brandLightGrey);
		color: var(--brandMedGreen);
	}

	@media (max-width: 730px) {
		.logo {
			width: 175px;
			padding-left: 0;
			/* margin-top: -8px; */
			/* margin-bottom: 0px; */
		}

		.logo-container {
			height: 60px;
			margin-bottom: 40px;
			padding-right: 15px;
			padding-left: 15px;
			padding-top: 0px;
			padding-bottom: 0px;
		}

		.research-link {
			font-size: 13px;
		}

		.menu-toggle {
			font-size: 13px;
			transform: none;
		}

		.dropdown {
			top: 30px;
			min-width: 120px;
		}
	}
</style>
