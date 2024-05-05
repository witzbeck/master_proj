CREATE TABLE main.assessment_types (
    id SERIAL PRIMARY KEY,
    assessment_type VARCHAR(4) NOT NULL
);
INSERT INTO main.assessment_types (assessment_type)
SELECT DISTINCT
    assessment_type
FROM staging.assessments
ORDER BY assessment_type;
