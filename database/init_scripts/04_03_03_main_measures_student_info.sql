-- This script creates the main.student_info table and populates it with data from the staging.studentInfo table
BEGIN;

CREATE TABLE main.student_info (
    student_id SERIAL PRIMARY KEY,
    orig_student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL REFERENCES main.module(module_id),
    presentation_id INTEGER NOT NULL REFERENCES main.presentation(presentation_id),
    age_band_id INTEGER NOT NULL REFERENCES main.age_band(age_band_id),
    imd_band_id INTEGER REFERENCES main.imd_band(imd_band_id),
    highest_education_id INTEGER NOT NULL REFERENCES main.highest_education(highest_education_id),
    region_id INTEGER NOT NULL REFERENCES main.region(region_id),
    final_result_id INTEGER NOT NULL REFERENCES main.final_result(final_result_id),
    is_female BOOLEAN,
    has_disability BOOLEAN,
    date_registration INTEGER,
    date_unregistration INTEGER,
    studied_credits INTEGER,
    num_of_prev_attempts INTEGER
);

COMMIT;

BEGIN;

WITH student_staging AS (
    SELECT
        student_id orig_student_id,
        module_code,
        presentation_code,
        COALESCE(age_band, 'Unknown Age Band') AS age_band,
        COALESCE(imd_band, 'Unknown IMD Band') AS imd_band,
        COALESCE(highest_education, 'Unknown Highest Education') AS highest_education,
        COALESCE(region, 'Unknown Region') AS region,
        COALESCE(final_result, 'Unknown Final Result') AS final_result,
        is_female::BOOLEAN AS is_female,
        has_disability::BOOLEAN AS has_disability,
        studied_credits,
        num_of_prev_attempts

    FROM staging.studentInfo
)

INSERT INTO main.student_info (
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
    s.orig_student_id,
    c.course_id,
    c.module_id,
    c.presentation_id,
    ab.age_band_id,
    i.imd_band_id,
    e.highest_education_id,
    r.region_id,
    f.final_result_id,
    s.is_female is_female,
    s.has_disability has_disability,
    sr.date_registration,
    sr.date_unregistration,
    s.studied_credits,
    s.num_of_prev_attempts
FROM student_staging s
JOIN main.highest_education e       ON e.highest_education = s.highest_education
JOIN main.region r                  ON r.region = s.region
JOIN main.imd_band i                ON i.imd_band = s.imd_band
JOIN main.age_band ab               ON ab.age_band = s.age_band
JOIN main.final_result f            ON f.final_result = s.final_result
JOIN main.course_info c             ON c.module_code = s.module_code 
                                    AND c.presentation_code = s.presentation_code
JOIN staging.studentRegistration sr ON sr.student_id = s.orig_student_id 
                                    AND sr.module_code = c.module_code 
                                    AND sr.presentation_code = c.presentation_code
;

COMMIT;