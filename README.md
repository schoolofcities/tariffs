# Mapping Tariffs

Maps, rankings, and reports on how U.S. tariffs could affect jobs, businesses and places across Canada. A [School of Cities](https://schoolofcities.utoronto.ca/) project at the University of Toronto.

Website: [mappingtariffs.org](https://mappingtariffs.org/mt/)  
About the project and research team: [mappingtariffs.org/mt/about](https://mappingtariffs.org/mt/about)

## Potential direct exposure

Where are the jobs and businesses that make goods subject to U.S. tariffs?

- Pages: [overview](https://mappingtariffs.org/mt/exposure) · [interactive map](https://mappingtariffs.org/mt/exposure/map) · [rankings](https://mappingtariffs.org/mt/exposure/rankings) · posts on [lumber](https://mappingtariffs.org/mt/exposure/lumber), [trucks](https://mappingtariffs.org/mt/exposure/trucks) and [Section 338](https://mappingtariffs.org/mt/exposure/section-338)
- Analysis: [`analysis/exposure/`](analysis/exposure/)
- Data downloads: [`static/downloads/exposure/`](static/downloads/exposure/)

## Job impact scenarios

How many jobs could be lost across Canadian cities and regions under five tariff scenarios?

- Pages: [overview](https://mappingtariffs.org/mt/scenarios) · [interactive map](https://mappingtariffs.org/mt/scenarios/map) · [rankings](https://mappingtariffs.org/mt/scenarios/rankings) · [summary report](https://mappingtariffs.org/mt/scenarios/summary-report) · [technical appendix (PDF)](static/documents/scenarios-appendix-a.pdf)
- Analysis: [`analysis/scenarios/`](analysis/scenarios/)
- Data downloads: [`static/downloads/scenarios/`](static/downloads/scenarios/)

## Canada–U.S. travel

How much has Canadian travel to U.S. cities declined?

- Page: [Canada–U.S. travel](https://mappingtariffs.org/mt/travel/canada-us-visits)
- Data download: [`static/data/travel/us_normalized_trips_daily.csv`](static/data/travel/us_normalized_trips_daily.csv)

## Other pages

[Current U.S. tariffs on Canada](https://mappingtariffs.org/mt/current-tariffs)

## Repo

- `src/` – the website ([SvelteKit](https://svelte.dev/docs/kit)); pages are in `src/routes/mt/`
- `static/` – data, map tiles, images and downloads served with the site
- `analysis/` – the data pipeline; see [`analysis/README.md`](analysis/README.md) for methods, data sources and how to update each tool

To run locally: `npm install`, then `npm run dev`. Pushes to `main` build and deploy to GitHub Pages (`.github/workflows/deploy.yml`).
