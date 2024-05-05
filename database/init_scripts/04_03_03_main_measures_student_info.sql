-- This script creates the main.student_info table and populates it with data from the staging.studentInfo table
BEGIN;

CREATE TABLE main.student_info (
    student_id SERIAL PRIMARY KEY,
    orig_student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL REFERENCES main.course_info(module_id),
    presentation_id INTEGER NOT NULL REFERENCES main.course_info(presentation_id),
    age_band_id INTEGER NOT NULL REFERENCES main.age_band(id),
    imd_band_id INTEGER REFERENCES main.imd_band(id), -- Assuming it can be null
    highest_education_id INTEGER NOT NULL REFERENCES main.highest_education(id),
    region_id INTEGER NOT NULL REFERENCES main.region(id),
    final_result_id INTEGER NOT NULL REFERENCES main.final_result(id),
    is_female BOOLEAN,
    has_disability BOOLEAN,
    date_registration DATE,
    date_unregistration DATE,
    studied_credits INTEGER,
    num_of_prev_attempts INTEGER
);

COMMIT;

BEGIN;

INSERT INTO main.student_info (
    student_id,
    orig_student_id,
    course_id,
    module_id,
    presentation_id,
    age_band_id,
    imd_band_id,
    highest_education_id,
    region_id,
    final_result_id,
    is_female,
    has_disability,
    date_registration,
    date_unregistration,
    studied_credits,
    num_of_prev_attempts
)
SELECT DISTINCT 
    s.student_id AS orig_student_id,
    c.course_id,
    c.module_id,
    c.presentation_id,
    ab.age_band_id,
    i.imd_band_id,
    e.highest_education_id,
    r.region_id,
    f.final_result_id,
    s.is_female,
    s.has_disability,
    sr.date_registration,
    sr.date_unregistration,
    s.studied_credits,
    s.num_of_prev_attempts
FROM staging.studentInfo s
JOIN main.highest_education e ON e.highest_education = s.highest_education
JOIN main.region r ON r.region = s.region
JOIN main.course_info c ON c.module_code = s.module_code AND c.presentation_code = s.presentation_code
LEFT JOIN main.imd_band i ON i.imd_band = s.imd_band
JOIN main.course_info c ON c.module_code = s.module_code AND c.presentation_code = s.presentation_code
JOIN staging.studentRegistration sr ON sr.student_id = s.student_id AND sr.module_code = c.module_code AND sr.presentation_code = c.presentation_code
JOIN main.age_band ab ON ab.age_band = s.age_band
JOIN main.final_result f ON f.final_result = s.final_result
;

COMMIT;