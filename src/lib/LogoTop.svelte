<script>

	import "../assets/global-styles.css";
	import logoBlueColour from '../assets/sofc-uoft-logo-blue-colour.svg';
	import logoWhiteColour from '../assets/sofc-uoft-logo-white-colour.svg';
	import logoBlack from '../assets/sofc-uoft-logo-black.svg';
	import logoWhite from '../assets/sofc-uoft-logo-white.svg';

	export let logoType = 'Blue'; // 'Blue', 'White', 'Black', 'WhiteOnly'
	export let backgroundColor = 'var(--brandWhite)'; 

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

</div>


<style>

	.logo-container {
		display: flex;
		/* justify-content: center; */
		/* align-items: center; */
		margin-top: 0px;
		margin-bottom: 60px;
		border-bottom: solid 1px var(--brandDarkBlue);
		padding: 0px;
	}

	.logo {
		width: 300px; 
		height: 60px;
		padding: 0px;
		padding-left: 35px;
		margin-bottom: -5px;
	}

	.logo:hover {
		opacity: 0.75;
	}

	@media (max-width: 730px) {
		.logo {
			width: 175px;
			padding-left: 15px;
			margin-top: -8px
		}
		.logo-container {
			height: 40px;
			margin-bottom: 40px;
		}
	}

</style>