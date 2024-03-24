CREATE VIEW main.v_student_courses AS
SELECT

    si.id student_id
    , si.module_id
    , si.presentation_id
    , f.id final_result_id
    , a.id age_band_id
    , ib.id imd_band_id
    , he.id highest_education_id
    , r.id region_id
    , c.module_code
    , c.presentation_code
    , c.module_presentation_length
    , c.domain
    , c.start_month
    , c.presentation_year
    , f.final_result
    , a.age_band
    , si.num_of_prev_attempts
    , si.studied_credits
    , ib.imd_band
    , he.highest_education
    , r.region
    , si.is_female
    , si.has_disability

FROM main.student_info si
    JOIN main.course_info c
        ON
            c.module_id = si.module_id
            AND c.presentation_id = si.presentation_id
    JOIN main.final_result f ON f.id = si.final_result_id

    JOIN main.age_band a ON a.id = si.age_band_id
    JOIN main.imd_band ib ON ib.id = si.imd_band_id
    JOIN main.highest_education he ON he.id = si.highest_education_id
    JOIN main.region r ON r.id = si.region_id
