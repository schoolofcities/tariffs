<script>
	import PageTitle from '$lib/components/layout/PageTitle.svelte';
	import Seo from '$lib/components/post/Seo.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import ToolCards from '$lib/components/layout/ToolCards.svelte';
	import CanadaIcon from '$lib/components/icons/CanadaIcon.svelte';
	import BarChartIcon from '$lib/components/icons/BarChartIcon.svelte';
	import DocumentIcon from '$lib/components/icons/DocumentIcon.svelte';
	import { PUBLISHED } from '$lib/components/maps/scenarios/config.js';

	// the report gets its own card above the tools
	const report = [
		{
			href: '/scenarios/report',
			icon: DocumentIcon,
			published: PUBLISHED,
			title: 'Report',
			text: 'Modeling potential economic impacts of U.S. tariffs on Canada’s regions and industries: context, methods, and the regional and industry effects of each scenario.'
		}
	];

	const tools = [
		{
			href: '/scenarios/map',
			icon: CanadaIcon,
			published: PUBLISHED,
			title: 'Interactive map',
			text: 'Explore modelled job losses under each scenario for neighbourhoods and municipalities, as a number of jobs or as a share of local employment, combining direct, indirect and induced effects.'
		},
		{
			href: '/scenarios/rankings',
			icon: BarChartIcon,
			published: PUBLISHED,
			title: 'Rankings',
			text: 'Compare job losses across Canada’s census metropolitan areas and provinces for each scenario and type of effect.'
		}
	];
</script>

<Seo
	title="Job-loss scenarios from U.S. tariffs"
	description="Modelled job losses across Canadian cities and regions under five U.S. tariff scenarios, from a multi-regional input-output model."
/>

<main>
	<div class="two-col">
		<div class="intro">
			<PageTitle
				title="Job-loss scenarios from U.S. tariffs"
				subtitle="How many jobs could be lost across Canadian cities and regions under different tariff scenarios?"
			/>

			<!-- TODO: placeholder text, to be written -->
			<p>
				Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas consequat lacus eu dolor dapibus sodales. Aenean venenatis metus id eleifend tincidunt. Nulla ut lacus et urna finibus bibendum sit amet et ante. Aliquam tristique, ex sed porttitor hendrerit, ex odio accumsan ex, eu maximus leo quam quis nulla.
			</p>

			<p>
				Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.
			</p>

			<p>
				Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur.
			</p>

			<p>
				Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur. At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident.
			</p>

			<p>
				Similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.
			</p>

			<p>
				Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.
			</p>

			<p>
				Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris. Integer in mauris eu nibh euismod gravida. Duis ac tellus et risus vulputate vehicula. Donec lobortis risus a elit. Etiam tempor.
			</p>

			<p>
				Ut ullamcorper, ligula eu tempor congue, eros est euismod turpis, id tincidunt sapien risus a quam. Maecenas fermentum consequat mi. Donec fermentum. Pellentesque malesuada nulla a mi. Duis sapien sem, aliquet nec, commodo eget, consequat quis, neque. Aliquam faucibus, elit ut dictum aliquet, felis nisl adipiscing sapien, sed malesuada diam lacus eget erat.
			</p>
		</div>

		<aside class="sidebar">
			<ToolCards tools={report} />
			<h2 class="side-heading">Tools</h2>
			<ToolCards {tools} />
		</aside>
	</div>

	<Footer />
</main>
