# Mapping Exposure to US Tariffs at Aggregate Dissemination Area Level

## OBJECTIVE
The objective of this visualisation is to map out the direct exposure of Canadian businesses, employees and residents to US President Donald Trump Second Administration’s Tariffs (Tariffs) at the Aggregate Dissemination Area (ADA) level.

As of July 2025, the Tariffs include the following:
1)	25% tariffs on all Canadian products not covered by CUSMA
2)	10% tariffs on potash, energy and natural resources
3)	25% tariffs on automobiles and auto parts
4)	25% tariffs on aluminum and derivative products
5)	25% tariffs on steel and derivative products
6)	Tariffs on lumber*
*Tariffs on lumber are included because it remains an economic measure that the US continues to impose on Canada.

Businesses are defined as the establishments that are recorded in the 20XX Establishment Counts by DA, excluding those with no employees.
Employees are defined from the employee ranges provided in the 20XX Establishment Counts by DA, which are as follows:
-	1 to 4  	3 employees
-	5 to 9 	7 employees
-	10 to 19 	15 employees
-	20 to 49 	35 employees
-	50 to 99 	75 employees
-	100 to 199 	150 employees
-	200 to 499 	350 employees
-	500 + 	550 employees
Residents are defined from Census 2021 data.

## DATA SOURCES
1)	List of HS Codes for products tariffed by the US from [HTS Chapter 99](https://hts.usitc.gov/reststop/file?release=currentRelease&filename=Chapter%2099)
2)	2025 US HS-NAICS Concordance Table [(_download the 2025 Import .xlsx file_)](https://www.census.gov/foreign-trade/reference/index.html)
3)	Province/Territory 2024 Annual Export Data to the World at HS6 level [(_toggle to HS6, click on 'Data Extraction', set start date as Jan 2024, set end date as Dec 2024, click on Annual data checkbox, set Country/State to 'World total' and download data for every province_)](https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/exp-eng.htm)
4)	Province/Territory 2024 Annual Export Data to the World at HS6 level [(_same setting as above, except to set Country/State to 'US total' instead_)](https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/exp-eng.htm)
5)	20XX Establishment Counts by Dissemination Area (DA) [(_to clarify later on which one needs to be downloaded_)](https://doi.org/10.5683/SP/FLLHOV)
6)	Census 2021 Geographic Boundary Files at Aggregate Dissemination Area (ADA) level [(_select the appropriate geographic level at the 'Statistical boundaries' section_)](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-eng.cfm?year=21)
7)	[Dissemination Geographies Relationship File](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/dguid-idugd/index2021-eng.cfm?year=21) to link DAs to ADAs
8)	Census 2021 Data – Aggregate Dissemination Area Level [(_data is found in the 'Comprehensive download files' section_)](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E&SearchText=canada&DGUIDlist=2021A000011124&GENDERlist=1,2,3&STATISTIClist=1,4&HEADERlist=0)

## STEPS
1)	Extract list of HS Codes for products that are tariffed by the US from Chapter 99 of US Harmonized Tariff Schedule (HTS)

       _Any new tariffs officially announced by the US International Trade Commission would result in an update of the HTS and changes to Chapter 99, which pertains to temporary legislation and amendments from the general HTS terms. HTS codes and HS codes are the same at the 6-digit level, thus it is safe to list the entire HTS code so long as they are later snipped to the first 6 digits during Python processing._
 
2)	Amend US HS-NAICS Concordance to ensure consistency between American and Canadian NAICS at the 5-digit (industry) level

       _American and Canadian NAICS codes are the same at the 5-digit (industry) level with the notable exception of oil and gas extracting industries. The American concordance table would classify oil and gas products under American NAICS codes for the oil and gas extracting industries (21112 and 21113). This needs to be amended appropriately into the Canadian-equivalent codes (21111 and 21114)._

3)	Clean up the Dissemination Geographies Relationship File

       _Only the IDs for Dissemination Areas (DADGUID_ADIDUGD) and Aggregate Dissemination Areas (ADADGUID_ADAIDUGD) are relevant. Ensure that duplicate Dissemination Area IDs are deleted._

4)	[Refer to Jupyter notebook] Connect the list of tariffed products with the concordance table to filter for the 5-digit NAICS codes of the industries directly exposed to US tariffs

5)	[Refer to Jupyter notebook] Use this new filter from Step 4 to find out the ratio of US to global exports for each NAICS code in every province/territory

6)	[Refer to Jupyter notebook] Also use this new filter from Step 4 onto the Establishment Counts dataset to find out the following from each DA:
7)	       _a.	How many businesses are directly exposed to tariffs_
  	    _b.	How many estimated employees are directly exposed to tariffs, after getting weighted for its province’s/territory’s NAICS US/Global export ratio (Step 5). This is also broken down by the type of tariffs_
  	    _c.	How many estimated employees working within each directly exposed industry_

8)	[Refer to Jupyter notebook] Each result (6a, 6b and 6c) will be aggregated from DA to ADA level using table created in Step 3

9)	[Refer to Jupyter notebook] Results 6a and 6b, after aggregated, will be used to create a choropleth map (showing percentage of exposure in each ADA) and centroid map (showing count of exposure in each ADA)

10)	[Refer to Jupyter notebook] Result 6c, after aggregated, will be used to create another weight of total jobs available within a 15km radius from each ADA to jobs with direct exposure to tariffs.

11)	[Refer to Jupyter notebook] Weight from Step 9 will be applied on Census 2021 Data on resident’s declared occupation industry, so as to estimate the number of residents in each ADA working in each affected 5-digit NAICS industry code

12)	[Refer to Jupyter notebook] This estimate is again multiplied by US/Global export ratio for each province (Step 5) in order to estimate the number of estimated residents that are directly exposed to tariffs

13)	[Refer to Jupter notebook] Results from Step 11 are then processed to be appended to the choropleth and centroid maps. They will both be saved as GeoJSON files.

14)	Convert the GeoJSON files into PMTiles via Windows Subsystem for Linux with the following codes:
15)	       _a.	For Choropleth Map: code to be added later_
   	    _b.	For Centroid Map: code to be added later_
