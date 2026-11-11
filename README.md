# Mapping Tariffs

Maps, rankings, and reports on how U.S. tariffs could affect jobs, businesses, and places across Canada. A [School of Cities](https://schoolofcities.utoronto.ca/) project at the University of Toronto.

Website: [mappingtariffs.org](https://mappingtariffs.org/mt/)  
About the project and research team: [mappingtariffs.org/mt/about](https://mappingtariffs.org/mt/about)  
Methods, data sources, and how to update the data: [`analysis/README.md`](analysis/README.md)

## Potential direct exposure

Where are the jobs and businesses that make goods subject to U.S. tariffs?

- Pages: [overview](https://mappingtariffs.org/mt/exposure) · [interactive map](https://mappingtariffs.org/mt/exposure/map) · [rankings](https://mappingtariffs.org/mt/exposure/rankings) · posts on [lumber](https://mappingtariffs.org/mt/exposure/lumber), [trucks](https://mappingtariffs.org/mt/exposure/trucks), and [Section 338](https://mappingtariffs.org/mt/exposure/section-338)
- Analysis: [`analysis/exposure/`](analysis/exposure/)
- Data downloads: [`static/downloads/exposure/`](static/downloads/exposure/)
  - [`ada_counts_and_percents.xlsx`](static/downloads/exposure/ada_counts_and_percents.xlsx) – businesses, employees (place of work), and employees (place of residence) exposed to each tariff, for every aggregate dissemination area (ADA, neighbourhood level). Counts and percentages are on separate sheets.
  - [`csd_counts_and_percents.xlsx`](static/downloads/exposure/csd_counts_and_percents.xlsx) – the same measures for every census subdivision (CSD, roughly municipalities).
  - [`cma_tariffs_counts_and_percents.xlsx`](static/downloads/exposure/cma_tariffs_counts_and_percents.xlsx) – the same measures for each census metropolitan area (CMA), as shown in the rankings, with 2021 population.
  - [`tariff_hs_codes_9_29_2026.csv`](static/downloads/exposure/tariff_hs_codes_9_29_2026.csv) – the Harmonized System (HS) product codes subject to U.S. tariffs (as of September 29, 2026), which are matched to industries (NAICS) in the analysis.
  - [`section_338.xlsx`](static/downloads/exposure/section_338.xlsx) – the HS codes covered by the Section 338 dairy, alcohol, and motor vehicle orders, with tariffed and excluded (banned) items marked.

## Job impact scenarios

How many jobs could be lost across Canadian cities and regions under five tariff scenarios?

- Pages: [overview](https://mappingtariffs.org/mt/scenarios) · [interactive map](https://mappingtariffs.org/mt/scenarios/map) · [rankings](https://mappingtariffs.org/mt/scenarios/rankings) · [summary report](https://mappingtariffs.org/mt/scenarios/summary-report) · [technical appendix (PDF)](static/documents/scenarios-appendix-a.pdf)
- Analysis: [`analysis/scenarios/`](analysis/scenarios/)
- Data downloads: [`static/downloads/scenarios/`](static/downloads/scenarios/)
  - [`all_scenarios_ada.csv`](static/downloads/scenarios/all_scenarios_ada.csv) / [`all_scenarios_csd.csv`](static/downloads/scenarios/all_scenarios_csd.csv) – estimated job losses for each aggregate dissemination area / census subdivision under each scenario, split into direct, indirect, and induced effects. Job losses are negative numbers.
  - [`all_scenarios_cma.csv`](static/downloads/scenarios/all_scenarios_cma.csv) / [`all_scenarios_province.csv`](static/downloads/scenarios/all_scenarios_province.csv) – the same rolled up to census metropolitan areas / provinces and territories, with totals and job losses as a share of employment, as shown in the rankings.
  - [`ada_total_emp.csv`](static/downloads/scenarios/ada_total_emp.csv) / [`csd_total_emp.csv`](static/downloads/scenarios/csd_total_emp.csv) – total employment in each area, used as the denominator for the percentages on the scenarios map.

## Canada–U.S. travel

How much has Canadian travel to U.S. cities declined?

- Page: [Canada–U.S. travel](https://mappingtariffs.org/mt/travel/canada-us-visits)
- Data download: [`static/data/travel/us_normalized_trips_daily.csv`](static/data/travel/us_normalized_trips_daily.csv) – daily trips by Canadian devices to each U.S. metropolitan area, normalized by the number of Canadian devices observed that day (from Cuebiq mobile data).

## Other pages

[Current U.S. tariffs on Canada](https://mappingtariffs.org/mt/current-tariffs)

## Repo

- `src/` – the website ([SvelteKit](https://svelte.dev/docs/kit)); pages are in `src/routes/mt/`
- `static/` – data, map tiles, images, and downloads served with the site
- `analysis/` – the data pipeline; see [`analysis/README.md`](analysis/README.md) for methods, data sources, and how to update each tool

To run locally: `npm install`, then `npm run dev`. Pushes to `main` build and deploy to GitHub Pages (`.github/workflows/deploy.yml`).
