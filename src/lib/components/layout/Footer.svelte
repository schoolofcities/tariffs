<script>
	import logo from '$assets/logos/sofc-uoft-logo-white-colour.svg';
</script>

<footer class="footer">
	<a href="https://schoolofcities.utoronto.ca/" target="_blank" rel="noopener">
		<img src={logo} alt="University of Toronto School of Cities" class="logo" />
	</a>
</footer>

<style>
	.footer {
		width: 100%;
		margin-top: 100px;
		padding: 25px 0;
		background-color: var(--brandDarkBlue);
		border-top: 1px solid var(--brandGray);
		text-align: center;
	}

	.logo {
		display: block;
		width: 300px;
		height: auto;
		margin: 0 auto;
	}

	.logo:hover {
		opacity: 0.75;
	}

	@media (max-width: 800px) {
		.footer {
			margin-top: 25px;
			padding: 15px 0;
		}
		.logo {
			width: 250px;
		}
	}

	@media (max-width: 500px) {
		.logo {
			width: 225px;
		}
	}
</style>
