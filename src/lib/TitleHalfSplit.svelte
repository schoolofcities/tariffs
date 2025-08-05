<script>
	import "../assets/global-styles.css"
	import logoLight from '../assets/sofc-uoft-logo-blue-colour.svg';
	import logoDark from '../assets/sofc-uoft-logo-white-colour.svg';
	export let title = '';
	export let subtitle = '';
	export let image = '';
	export let imageAltText = '';
	export let imageCaption = '';
	export let imageSource = '';
	export let titleFontColour = 'var(--brandDarkBlue)';
	export let titleBorderColour = 'var(--brandDarkBlue)';
	export let subtitleFontColour = 'var(--brandDarkBlue)';
	export let backgroundColour = 'var(--brandWhite)';
	export let logoStyle = 'Light'; // 'Light' or 'Dark' or 'None'
</script>

<div class="container">
	<div class="left" style="background-color: {backgroundColour};">
		{#if logoStyle === 'Light'}
			<a href="https://schoolofcities.utoronto.ca/" target="_blank" class="logo-link">
				<img src={logoLight} alt="UofT and School of Cities logos" class="logo-top" />
			</a>
		{:else if logoStyle === 'Dark'}
			<a href="https://schoolofcities.utoronto.ca/" target="_blank" class="logo-link">
				<img src={logoDark} alt="UofT and School of Cities logos" class="logo-top" />
			</a>
		{/if}
		<div class="title-text-container">
			<h1 style="color: {titleFontColour}; border-bottom: solid 2px {titleBorderColour}">{title}</h1>
			<h2 style="color: {subtitleFontColour};">{subtitle}</h2>
		</div>
	</div>
	<div class="right">
		<img src={image} alt="{imageAltText}" />
	</div>
</div>


{#if imageCaption || imageSource}

	<p class="img-caption" >{@html imageCaption} <span id="image-source">{@html imageSource}</span></p>
	
{/if}

<div class="spacer"></div>



<style>
	.container {
		display: flex;
		height: 100vh;
		width: 100%;
		border-bottom: solid 1px var(--brandGray);
		margin-bottom: 0px;
		z-index: 20;
	}

	.left {
		flex: 1;
		/* background-color: var(--brandWhite); */
		border-right: solid 1px var(--brandGray);
		display: flex;
		justify-content: center;
		align-items: center;
		text-align: left;
		position: relative;
		z-index: inherit;
	}

	.logo-top {
		width: 300px;
		height: auto;
		position: absolute;
		top: 8px;
	}
	
	.logo-link {
		position: absolute;
		top: 0px;
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		justify-content: center;
		align-items: center;
		width: fit-content;
	}

	.logo-link:hover {
		opacity: 0.8;
	}

	.right {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		object-fit: cover;
		z-index: inherit;
	}

	.right img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.title-text-container {
		max-width: 680px;
		margin-left: 35px;
		margin-right: 35px;
	}

	.title-text-container h1 {
		text-align: left;
		font-family: TradeGothicBold;
		font-size: 54px;
		line-height: 62px;
		max-width: 720px;
		text-decoration: none;
		font-weight: normal;
		margin-top: 0px;
		margin-bottom: 0px;
		padding: 0px;
		padding-bottom: 10px;
	}

	.title-text-container h2 {
		text-align: left;
		font-family: SourceSerifItalic;
		font-weight: normal;
		font-size: 24px;
		margin-top: 8px;
		max-width: 720px;
	}

	/* Media Query for Tall Screens (Portrait Mode) */
	@media (max-aspect-ratio: 1/1) {
		.container {
			flex-direction: column; 
		}
		.left,
		.right {
			flex: none;
			width: 100%;
			height: 50%;
		}
		.left {
			border-bottom: solid 1px var(--brandLightBlue);
		}
		.right img {
			width: 100%; 
			height: 100%;
			border-bottom: solid 1px var(--brandLightBlue);
			object-fit: cover; 
		}
	}

	@media (max-width: 1930px) {
		.title-text-container h1 {
			font-size: 48px;
			line-height: 54px;
		}
		.title-text-container h2 {
			font-size: 22px; 
		}
	}

	@media (max-width: 800px) {
		.title-text-container h1 {
			font-size: 40px; 
			line-height: 46px;
		}

		.title-text-container h2 {
			font-size: 18px; 
		}
		.logo-top {
			width: 225px;
		}
	}

	@media (max-width: 600px) {
		.logo-top {
			width: 175px;
		}
	}

	@media screen and (max-width: 600px) and (max-height: 900px) {
		.container {
			height: calc(100vh + 200px);
		}
	}

	p {
		text-align: right;
		padding-right: 3px;
		margin: 0px;
		box-sizing: border-box;
		width: 100%;
		font-family: OpenSansBold;
		font-weight: normal;
		font-size: 12px;
		line-height: 18px;
	}

	.img-caption {
		font-family: OpenSansBold;
		font-weight: normal;
		color: var(--brandGray70);
		margin-top: 2px;
		margin-bottom: 0px;
		padding-top: 0px;
	}

	#image-source {
		font-family: OpenSans;
		font-weight: normal;
		color: var(--brandGray50);
	}

	.spacer {
		background-color: none;
		height: 50px;
	}

	@media (max-width: 500px) {
		p {
			font-size: 10px;
		}
	}


</style>
