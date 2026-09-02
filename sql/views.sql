CREATE OR REPLACE VIEW vw_sustainability_analysis AS
SELECT
    f.country_code,
    c.country_name,
    c.region,
    f.year,
    f.co2_emissions,
    f.population,
    f.energy_per_capita,
    CASE
        WHEN f.population > 0
        THEN f.co2_emissions / f.population
        ELSE NULL
    END AS co2_per_capita
FROM fact_sustainability f
JOIN dim_country c
    ON f.country_code = c.country_code;