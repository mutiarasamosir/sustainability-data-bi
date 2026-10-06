# Global CO₂ & Energy Sustainability Dashboard

## Project Overview

This project develops an end-to-end data management and business intelligence workflow for analyzing global CO₂ emissions, population, and energy use.

The project integrates public datasets, performs data cleaning and validation using Python, stores the processed data in PostgreSQL, conducts analytical queries using SQL, and presents the results through an interactive Power BI dashboard.

The main objective is to transform raw sustainability data into structured information that can support descriptive and comparative analysis.

## Business Questions

This project addresses the following questions:

1. How have global CO₂ emissions changed over time?
2. Which countries contribute the largest CO₂ emissions?
3. How does CO₂ emissions per capita vary across countries?
4. How do CO₂ emissions differ across regions?
5. How is energy use per capita associated with CO₂ emissions per capita?
6. Which countries experienced the largest increase or decrease in CO₂ emissions between 2000 and 2023?

## Data Sources

The datasets are obtained from **Our World in Data (OWID)** and its underlying data sources.

The main datasets used are:

- Annual CO₂ emissions
- Population
- Primary energy use per capita
- UN M49 Level-1 regional classification

The final analytical dataset covers:

- Period: 2000–2023
- Countries: 205
- Records: 4,885

## Data Processing

The data processing workflow consists of:

1. Extracting data from public sources.
2. Standardizing column names and data types.
3. Filtering country-level records.
4. Checking missing values.
5. Checking duplicate country-year records.
6. Checking invalid negative values.
7. Integrating CO₂, population, and energy datasets.
8. Calculating CO₂ per capita.
9. Adding regional classification.
10. Validating the final analytical dataset.

## Data Quality

The final dataset contains:

- 4,885 records
- 205 countries
- 2000–2023 period
- 0 missing values
- 0 duplicate country-year records
- 0 negative values

Zero values in CO₂ emissions and energy use were retained because they are valid observations within the source data and were not treated as missing values.

Non-country aggregate entities were excluded from the final country-level analysis.

## Database Design

The processed data is stored in PostgreSQL using a simple relational structure.

### `dim_country`

Contains country-level reference information.

| Column | Description |
|---|---|
| `country_code` | Country identifier |
| `country_name` | Country name |
| `region` | Geographic region |

### `fact_sustainability`

Contains country-year sustainability indicators.

| Column | Description |
|---|---|
| `country_code` | Country identifier |
| `year` | Observation year |
| `co2_emissions` | Annual CO₂ emissions |
| `population` | Total population |
| `energy_per_capita` | Primary energy use per person |

A primary key is defined on `country_code` and `year`.

The `country_code` column in the fact table references `dim_country`.

## SQL Analysis

Several analytical queries were developed in PostgreSQL, including:

- Global CO₂ emissions trend by year
- Top 10 countries by total CO₂ emissions
- Top 10 countries by average CO₂ per capita
- CO₂ emissions by region and year
- Energy use per capita compared with CO₂ per capita
- Change in CO₂ emissions between 2000 and 2023

A SQL view named `vw_sustainability_analysis` is used to combine country information with country-year sustainability data and calculate CO₂ per capita.

## Power BI Dashboard

The processed data is connected to Power BI through PostgreSQL.

The dashboard provides:

- Global CO₂ emissions trend
- Top 10 countries by CO₂ emissions
- CO₂ emissions by region
- Top 10 countries by CO₂ per capita
- Energy use vs CO₂ per capita
- Countries with the largest increase in CO₂ emissions
- Interactive year and region filters
- KPI cards for total CO₂, average CO₂ per capita, and number of countries
