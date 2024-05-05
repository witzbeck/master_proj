-- Purpose: Load data into the main schema tables.
BEGIN;

-- Create the schema
INSERT INTO main.activity_type (activity_type)
SELECT activity_type
FROM staging.vle
GROUP BY activity_type
ORDER BY activity_type
;

INSERT INTO main.region (region)
SELECT region
FROM staging.studentInfo
GROUP BY region
ORDER BY region
;

INSERT INTO main.presentation (presentation_code)
SELECT presentation_code
FROM staging.courses
GROUP BY presentation_code
ORDER BY presentation_code
;

INSERT INTO main.module (module_code)
SELECT module_code
FROM staging.courses
GROUP BY module_code
ORDER BY module_code
;

INSERT INTO main.imd_band (imd_band)
SELECT imd_band
FROM staging.studentInfo
WHERE imd_band IS NOT NULL
GROUP BY imd_band
ORDER BY imd_band
;

INSERT INTO main.highest_education (highest_education)
SELECT highest_education
FROM staging.studentInfo
GROUP BY highest_education
ORDER BY highest_education
;

INSERT INTO main.final_result (final_result)
SELECT final_result
FROM staging.studentInfo
WHERE final_result IS NOT NULL
GROUP BY final_result
ORDER BY final_result
;

INSERT INTO main.assessment_type (assessment_type)
SELECT assessment_type
FROM staging.assessments
GROUP BY assessment_type
ORDER BY assessment_type
;

INSERT INTO main.age_band (age_band)
SELECT age_band
FROM staging.studentInfo
WHERE age_band IS NOT NULL
ORDER BY age_band
;

COMMIT;
