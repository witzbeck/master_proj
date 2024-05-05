-- This script creates the main.student_assessment_bridge table and populates it with data from the staging.studentAssessment table.
BEGIN;

CREATE TABLE main.student_assessment_bridge (
    student_assessment_bridge_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES main.student_info(id),
    assessment_id INTEGER NOT NULL REFERENCES main.assessment_info(id),
    course_id INTEGER NOT NULL REFERENCES main.course_info(id),
    assessment_type_id INTEGER NOT NULL REFERENCES main.assessment_type(id),
    date_submitted DATE,
    is_banked BOOLEAN,
    score DECIMAL,
    date DATE,
    weight DECIMAL
);

COMMIT;

BEGIN;
INSERT INTO main.student_assessment_bridge (
    student_id,
    assessment_id,
    course_id,
    assessment_type_id,
    date_submitted,
    is_banked,
    score,
    date,
    weight
)
SELECT
    si.student_id,
    ai.assessment_id,
    ai.course_id,
    ai.assessment_type_id,
    sa.date_submitted,
    sa.is_banked,
    sa.score,
    ai.date,
    ai.weight

FROM staging.studentAssessment sa
JOIN main.assessment_info ai ON sa.assessment_id = ai.id
JOIN main.student_info si ON sa.student_id = si.orig_student_id and ai.course_id = si.course_id
;

COMMIT;
