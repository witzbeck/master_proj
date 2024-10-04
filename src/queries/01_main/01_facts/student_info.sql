select distinct
    row_number() over () id
    , s.student_id orig_student_id
    , c.id course_id
    , c.module_id
    , c.presentation_id
    , ab.id age_band_id
    , i.id imd_band_id
    , e.id highest_education_id
    , r.id region_id
    , f.id final_result_id
    , is_female
    , has_disability
    , sr.date_registration
    , sr.date_unregistration
    , studied_credits
    , num_of_prev_attempts

from staging.studentinfo s
    join main.highest_education e on e.highest_education = s.highest_education
    join main.region r on r.region = s.region
    join main.course_info c on c.module_code = s.code_module and c.presentation_code = s.code_presentation
    left join main.imd_band i on i.imd_band = s.imd_band
    join staging.studentregistration sr
        on
            sr.student_id = s.student_id
            and sr.code_module = c.module_code
            and sr.code_presentation = c.presentation_code
    join main.age_band ab on ab.age_band = s.age_band
    join main.final_result f on f.final_result = s.final_result
order by s.student_id, c.id, region_id, imd_band_id, highest_education_id
;
