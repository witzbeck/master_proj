select
--count(*) n
v.id
--,v.orig_student_id
--,v.course_id
,v.module_code
,v.presentation_code
,v.age_band
,v.imd_band
,v.highest_education
,v.region
,v.is_female
,v.has_disability
--,v.num_of_prev_attempts
--,v.studied_credits
,v.final_result

--,v.date_registration
--,v.date_unregistration
--,v.presentation_year
--,v.start_month
--,v.module_presentation_length
--,v.domain
--,v.level
,'main' source
from main.v_student_info v
/*
group by 
 v.module_code
,v.presentation_code
,v.age_band
,v.imd_band
,v.highest_education
,v.region
,v.is_female
,v.has_disability
--,v.num_of_prev_attempts
--,v.studied_credits
,v.final_result
*/
union all 

select
 --count(*) n
 s.student_id
,s.code_module
,s.code_presentation
,s.age_band
,s.imd_band
,s.highest_education
,s.region
,s.is_female
,s.has_disability
--,s.num_of_prev_attempts
--,s.studied_credits
,s.final_result

,'staging' source
from staging."studentInfo" s
/*
group by s.code_module
,s.code_presentation
,s.age_band
,s.imd_band
,s.highest_education
,s.region
,s.is_female
,s.has_disability
--,s.num_of_prev_attempts
--,s.studied_credits
,s.final_result
*/