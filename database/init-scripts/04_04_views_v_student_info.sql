create view main.v_student_info as
select
    si.id
    , si.orig_student_id
    , si.course_id
    , a.age_band
    , i.imd_band
    , h.highest_education
    , r.region
    , f.final_result
    , si.is_female
    , si.has_disability
    , si.date_registration
    , si.date_unregistration
    , si.studied_credits
    , si.num_of_prev_attempts
    , c.module_code
    , c.presentation_code
    , c.presentation_year
    , c.start_month
    , c.module_presentation_length
    , c.domain
    , c.level
from main.student_info si
    join main.final_result f on f.id = si.final_result_id
    join main.region r on r.id = si.region_id
    join main.highest_education h on h.id = si.highest_education_id
    join main.imd_band i on i.id = si.imd_band_id
    join main.age_band a on a.id = si.age_band_id
    join main.course_info c on c.id = si.course_id
