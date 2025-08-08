# Mapping Potential Direct Exposure to US Tariffs at Aggregate Dissemination Area Level

## OBJECTIVE
The objective of this visualisation is to map out the direct exposure of Canadian businesses and employees (by work location and primary residence) to US President Donald Trump Second Administration’s Tariffs (Tariffs) at the Aggregate Dissemination Area (ADA) level.

As of August 2025, the Tariffs include the following:
1)	10% tariffs on energy and natural resources [(HTS 9903.01.13)](https://content.govdelivery.com/bulletins/gd/USDHSCBP-3d7c46d?wgt_ref=USDHSCBP_WIDGET_2) and potash [(HTS 9903.01.15)](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/3d5b0a5)
2)	50% tariffs on iron and steel, and their derivative products (HTS 9903.81.87, 9903.81.88, 9903.81.89, 9903.81.90, 9903.81.91, 9903.81.93)
3)	50% tariffs on aluminum, and its derivative products (HTS 9903.85.02, 9903.85.04, 9903.85.07, 9903.85.08)
4)	25% tariffs on automobiles, and its parts (HTS 9903.94.01, 9903.94.03, 9903.94.05)
5)	50% tariffs on semi-finished copper and intensive copper derivative products (HTS 9903.78.01)
6)	35% tariffs on all Canadian products not covered by CUSMA (focusing on goods that the US maintains Tariff-Rate Quotas as found in HTS Chapter 98 Subchapter XXIII)
7)	Duties on softwood lumber (This is included because it remains an economic measure that the US continues to impose on Canada, even if it has not been explicitly threatened as a tariff as of July 2025.)

Data on employees (by primary residence) are derived from Census 2021 data

Businesses are defined as the establishments that are recorded in the December 2022 Establishment Counts by DA, excluding those with no employees.
Employees (by work location) are defined from the employee ranges provided in the December 2022 Establishment Counts by DA, which are as follows:
-	1 to 4 --> 	3 employees
-	5 to 9 -->	7 employees
-	10 to 19 -->	15 employees
-	20 to 49 -->	35 employees
-	50 to 99 -->	75 employees
-	100 to 199 -->	150 employees
-	200 to 499 -->	350 employees
-	500 + -->	550 employees

## DATA SOURCES
1)	List of HS Codes for products tariffed by the US from [HTS Chapter 98](https://hts.usitc.gov/reststop/file?release=currentRelease&filename=Chapter%2098), [HTS Chapter 99](https://hts.usitc.gov/reststop/file?release=currentRelease&filename=Chapter%2099) and US Federal Register for [Duties on Softwood Lumber](https://www.federalregister.gov/documents/2018/01/03/2017-28484/certain-softwood-lumber-products-from-canada-antidumping-duty-order-and-partial-amended-final)
2)	2025 Canadian HS8-NAICS Concordance Table (_requested directly from StatsCan_)
3)	Province/Territory 2024 Annual Export Data to the World at HS6 level [(_toggle to HS6, click on 'Data Extraction', set start date as Jan 2024, set end date as Dec 2024, click on Annual data checkbox, set Country/State to 'World total' and download data for every province_)](https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/exp-eng.htm)
4)	Province/Territory 2024 Annual Export Data to the World at HS6 level [(_same setting as above, except to set Country/State to 'US total' instead_)](https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/exp-eng.htm)
5)	December 2022 Establishment Counts by Dissemination Area (DA) [(_downloaded from Borealis_)](https://borealisdata.ca/file.xhtml?fileId=442841&version=5.1)
6)	Census 2021 Geographic Boundary Files at Aggregate Dissemination Area (ADA) level [(_select the appropriate geographic level at the 'Statistical boundaries' section_)](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-eng.cfm?year=21)
7)	[Dissemination Geographies Relationship File](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/dguid-idugd/index2021-eng.cfm?year=21) to link DAs to ADAs
8)	Census 2021 Data – Aggregate Dissemination Area Level [(_data is found in the 'Comprehensive download files' section_)](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E&SearchText=canada&DGUIDlist=2021A000011124&GENDERlist=1,2,3&STATISTIClist=1,4&HEADERlist=0)

## STEPS
1)	Extract list of HS Codes for products that are subject to tariffs and duties

       _Any new tariffs officially announced by the US International Trade Commission would result in an update of the HTS and changes to Chapter 99, which pertains to temporary legislation and amendments from the general HTS terms. HTS codes and HS codes are the same at the 6-digit level, thus it is safe to list the entire HTS code so long as they are later snipped to the first 6 digits during Python processing._

2)	Clean up the Dissemination Geographies Relationship File

       _Only the IDs for Dissemination Areas (DADGUID_ADIDUGD) and Aggregate Dissemination Areas (ADADGUID_ADAIDUGD) are relevant. Ensure that duplicate Dissemination Area IDs are deleted._

3)	[Refer to Jupyter notebook] Connect the list of tariffed products with the concordance table to filter for the NAICS codes of the industries directly exposed to US tariffs

4)	[Refer to Jupyter notebook] Use this new filter from Step 3 to find out the ratio of US to global exports for each NAICS code in every province/territory

5)	[Refer to Jupyter notebook] Also use this new filter from Step 3 onto the Establishment Counts dataset to find out the following from each DA:
   
	  _a.	How many businesses are directly exposed to tariffs_
  	
  	  _b.	How many estimated employees are directly exposed to tariffs, after getting weighted for its province’s/territory’s NAICS US/Global export ratio (Step 5). This is also broken down by the type of tariffs_
  	
  	  _c.	How many estimated employees working within each directly exposed industry_

6)	[Refer to Jupyter notebook] Each result (5a, 5b and 5c) will be aggregated from DA to ADA level using table created in Step 2

7)	[Refer to Jupyter notebook] Results 5a and 5b, after aggregated, will be used to create a choropleth map (showing percentage of exposure in each ADA) and centroid map (showing count of exposure in each ADA)

8)	[Refer to Jupyter notebook] Result 5c, after aggregated, will be used to create another weight of total jobs available within a 15km radius from each ADA to jobs with direct exposure to tariffs.

9)	[Refer to Jupyter notebook] Weight from Step 8 will be applied on Census 2021 Data on resident’s declared occupation industry, so as to estimate the number of residents in each ADA working in each affected NAICS industry code

10)	[Refer to Jupyter notebook] This estimate is again multiplied by US/Global export ratio for each province (Step 4) in order to estimate the number of estimated residents that are directly exposed to tariffs

11)	[Refer to Jupter notebook] Results from Step 10 are then processed to be appended to the choropleth and centroid maps. They will both be saved as GeoJSON files.

12)	Convert the GeoJSON files into PMTiles via Windows Subsystem for Linux with the following codes:
    
	  _a.	For Choropleth Map: code to be added later_

	  _b.	For Centroid Map: code to be added later_
