CREATE TABLE IF NOT EXISTS dim_country (
    country_code VARCHAR(10) PRIMARY KEY,
    country_name VARCHAR(150) NOT NULL,
    region VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS fact_sustainability (
    country_code VARCHAR(10) NOT NULL,
    year INTEGER NOT NULL,
    co2_emissions DOUBLE PRECISION NOT NULL,
    population BIGINT NOT NULL,
    energy_per_capita DOUBLE PRECISION NOT NULL,

    PRIMARY KEY (country_code, year),

    CONSTRAINT fk_country
        FOREIGN KEY (country_code)
        REFERENCES dim_country(country_code)
);