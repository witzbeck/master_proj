create view feat.minmax_scaled_student_info as 
with courses as (
    select
     max(id) - min(id) course_id_range
    ,max(module_id) - min(module_id) module_id_range
    ,max(presentation_id) - min(presentation_id) presentation_id_range
    from main.course_info
),
reg as (
    select
     max(date_registration) - min(date_registration) reg_date_range
    ,max(studied_credits) - min(studied_credits) studied_credits_range
    ,max(num_of_prev_attempts) - min(num_of_prev_attempts) n_prev_attempts_range
    from main.student_info
),
age   as (select max(id) - min(id) age_id_range from main.age_band),
imd   as (select max(id) - min(id) imd_id_range from main.imd_band),
ed   as (select max(id) - min(id) ed_id_range from main.highest_education),
region   as (select max(id) - min(id) region_id_range from main.regions)

select
 si.id                  student_id
,si.course_id
,si.course_id / cast(course_id_range as float) scaled_course_id
,si.module_id
,si.module_id / cast(module_id_range as float) scaled_module_id
,si.presentation_id
,si.presentation_id / cast(presentation_id_range as float) scaled_presentation_id
,si.age_band_id
,si.age_band_id / cast(age_id_range as float) scaled_age_id
,si.imd_band_id
,si.imd_band_id / cast(imd_id_range as float) scaled_imd_id
,si.highest_education_id
,si.highest_education_id / cast(ed_id_range as float) scaled_ed_id
,si.region_id
,si.region_id / cast(region_id_range as float) scaled_region_id
,si.final_result_id
,f.final_result
,si.is_female
,si.has_disability
,si.date_registration
,si.date_registration / cast(reg_date_range as float) scaled_reg_date
,si.studied_credits
,si.studied_credits / cast(studied_credits_range as float) scaled_studied_credits
,si.num_of_prev_attempts
,si.num_of_prev_attempts / cast(n_prev_attempts_range as float) scaled_n_prev_attempts
from main.student_info si
join main.final_result f on f.id=si.final_result_id
join courses on true
join reg on true
join age on true
join imd on true
join ed on true
join region on true