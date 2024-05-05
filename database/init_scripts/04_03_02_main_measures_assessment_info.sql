-- This script creates the assessment_info table and populates it with data from the staging.assessments table.
BEGIN;

CREATE TABLE main.assessment_info (
    assessment_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES main.course_info(course_id),
    module_id INTEGER NOT NULL REFERENCES main.module(module_id),
    presentation_id INTEGER NOT NULL REFERENCES main.presentation(presentation_id),
    assessment_type_id INTEGER NOT NULL REFERENCES main.assessment_types(assessment_type_id),
    date DATE,
    weight DECIMAL
);

COMMIT;

BEGIN;

INSERT INTO main.assessment_info (
    assessment_id,
    course_id,
    module_id,
    presentation_id,
    assessment_type_id,
    date,
    weight
)
SELECT DISTINCT
    a.assessment_id,
    c.course_id,
    c.module_id,
    c.presentation_id,
    at.assessment_type_id,
    a.date,
    a.weight
FROM staging.assessments a
JOIN main.course_info c ON c.module_code = a.code_module AND c.presentation_code = a.code_presentation
JOIN main.assessment_types at ON at.assessment_type = a.assessment_type;

COMMIT;