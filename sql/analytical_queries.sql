-- 1. Global CO2 emissions trend
SELECT
    year,
    SUM(co2_emissions) AS total_co2_emissions
FROM vw_sustainability_analysis
GROUP BY year
ORDER BY year;


-- 2. Top 10 countries by total CO2 emissions
SELECT
    country_name,
    SUM(co2_emissions) AS total_co2_emissions
FROM vw_sustainability_analysis
GROUP BY country_name
ORDER BY total_co2_emissions DESC
LIMIT 10;


-- 3. Top 10 countries by CO2 per capita
-- Average across 2000-2023
SELECT
    country_name,
    AVG(co2_per_capita) AS avg_co2_per_capita
FROM vw_sustainability_analysis
GROUP BY country_name
ORDER BY avg_co2_per_capita DESC
LIMIT 10;


-- 4. CO2 emissions by region and year
SELECT
    region,
    year,
    SUM(co2_emissions) AS total_co2_emissions
FROM vw_sustainability_analysis
GROUP BY region, year
ORDER BY year, total_co2_emissions DESC;


-- 5. Energy use and CO2 per capita
SELECT
    country_name,
    year,
    energy_per_capita,
    co2_per_capita
FROM vw_sustainability_analysis
ORDER BY year, country_name;


-- 6. Change in CO2 emissions from 2000 to 2023
SELECT
    country_name,
    SUM(CASE WHEN year = 2000 THEN co2_emissions ELSE 0 END) AS co2_2000,
    SUM(CASE WHEN year = 2023 THEN co2_emissions ELSE 0 END) AS co2_2023,
    SUM(CASE WHEN year = 2023 THEN co2_emissions ELSE 0 END)
    -
    SUM(CASE WHEN year = 2000 THEN co2_emissions ELSE 0 END)
    AS absolute_change
FROM vw_sustainability_analysis
GROUP BY country_name
ORDER BY absolute_change DESC;