CREATE VIEW main.v_student_courses as
select

si.id student_id
,si.module_id
,si.presentation_id
,f.id                   final_result_id
,a.id                   age_band_id
,ib.id                  imd_band_id
,he.id                  highest_education_id
,r.id                   region_id
,c.module_code
,c.presentation_code
,c.module_presentation_length
,c.domain
,c.start_month
,c.presentation_year
,f.final_result
,a.age_band
,si.num_of_prev_attempts
,si.studied_credits
,ib.imd_band
,he.highest_education
,r.region
,si.is_female
,si.has_disability

from main.student_info si 
join main.course_info c on c.module_id=si.module_id
                        and c.presentation_id=si.presentation_id
join main.final_result f on f.id=si.final_result_id

join main.age_band a on a.id=si.age_band_id
join main.imd_band ib on ib.id=si.imd_band_id
join main.highest_education he on he.id=si.highest_education_id
join main.region r on r.id=si.region_id
