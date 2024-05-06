-- This script creates the assessment_info table and populates it with data from the staging.assessments table.
BEGIN;

CREATE TABLE main.assessment_info (
    assessment_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES main.course_info(course_id),
    module_id INTEGER NOT NULL REFERENCES main.module(module_id),
    presentation_id INTEGER NOT NULL REFERENCES main.presentation(presentation_id),
    assessment_type_id INTEGER NOT NULL REFERENCES main.assessment_type(assessment_type_id),
    assessment_date INTEGER,
    assessment_weight DECIMAL
);

COMMIT;

BEGIN;

INSERT INTO main.assessment_info (
    assessment_id,
    course_id,
    module_id,
    presentation_id,
    assessment_type_id,
    assessment_date,
    assessment_weight
)
SELECT DISTINCT
    a.assessment_id,
    c.course_id,
    c.module_id,
    c.presentation_id,
    at.assessment_type_id,
    a.assessment_date,
    a.assessment_weight
FROM staging.assessments a
JOIN main.course_info c ON c.module_code = a.module_code AND c.presentation_code = a.presentation_code
JOIN main.assessment_type at ON at.assessment_type = a.assessment_type;

COMMIT;