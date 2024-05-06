-- Purpose: Create the main dimensions tables and populate them with data from the staging tables.
--
-- This script creates the following tables in the main schema:
-- - activity_types
-- - region
-- - presentations
-- - modules
-- - imd_band
-- - highest_education
-- - final_result
-- - assessment_types
-- - age_band

BEGIN;

-- Create the schema
CREATE SCHEMA main;

CREATE TABLE main.activity_type (
    activity_type_id SERIAL PRIMARY KEY,
    activity_type VARCHAR(25) NOT NULL
);
CREATE TABLE main.region (
    region_id SERIAL primary key,
    region VARCHAR(25) not null
);
CREATE TABLE main.presentation (
    presentation_id SERIAL primary key,
    presentation_code VARCHAR(5) not null
);
CREATE TABLE main.module (
    module_id SERIAL primary key,
    module_code VARCHAR(3) not null
);
CREATE TABLE main.imd_band (
    imd_band_id SERIAL PRIMARY KEY,
    imd_band VARCHAR(25) NOT NULL
);
CREATE TABLE main.highest_education (
    highest_education_id SERIAL primary key,
    highest_education VARCHAR(27) not null
);
CREATE TABLE main.final_result (
    final_result_id SERIAL PRIMARY KEY,
    final_result VARCHAR(25) NOT NULL
);
CREATE TABLE main.assessment_type (
    assessment_type_id SERIAL PRIMARY KEY,
    assessment_type VARCHAR(25) NOT NULL
);
CREATE TABLE main.age_band (
    age_band_id SERIAL PRIMARY KEY,
    age_band VARCHAR(25) NOT NULL
);

COMMIT;