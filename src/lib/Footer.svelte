<script>

	import "../assets/global-styles.css"
	import logos from '../assets/sofc-uoft-logo-white-colour.svg';

</script>


<div class="footer">

	<div class="footer-content">

		<a href="https://schoolofcities.utoronto.ca/" target="_blank" class="logo-link">
			
			<img src={logos} alt="University of Toronto and School of Cities logos" class="logos"/>

		</a>

	</div>

</div>


<style>

.footer {
	width: 100%;
	background-color: var(--brandDarkBlue);
	margin-top: 100px;
	padding-top: 25px;
	padding-bottom: 25px;
	text-align: center; 
	border-top: solid 1px var(--brandGray);
}

.footer-content {
	max-width: 700px;
	margin: 0 auto;
}

.logos {
	width: 300px;
	height: auto;
	display: block;
	margin: 0 auto;
}

.logos:hover {
	opacity: 0.75;
}

@media (max-width: 800px) {
	.footer {
		margin-top: 25px;
		padding-top: 15px;
		padding-bottom: 15px;
	}
	.logos {
		width: 250px;
	}
}

@media (max-width: 500px) {
	.logos {
		width: 225px;
	}
}

</style>