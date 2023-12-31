SELECT
 count(*)                           n_students
,s.course_id                        
,s.final_result_id                               final_result_id
,f.final_result
,sum(s.date_registration)           sum_date_reg
,sum(cast(s.date_registration as float)) 
    / count(*)                      avg_date_reg
,sum(s.date_unregistration)         sum_date_unreg
,sum(cast(s.date_unregistration as float)) 
    / count(*)                      avg_date_unreg
,sum(s.date_unregistration 
    - s.date_registration)          sum_reg_date_dif
,sum(cast(s.date_unregistration 
    - s.date_registration as float))
    / count(*)                      avg_reg_date_dif
,sum(s.studied_credits)             sum_studied_credits
,sum(cast(s.studied_credits as float))
    / count(*)                      avg_studied_credits
,sum(s.num_of_prev_attempts)        sum_prev_attempts
,sum(cast(s.num_of_prev_attempts as float))
    / count(*)                       avg_prev_attempts
,sum(case when s.is_female = '1' then 1 else 0 end)                   n_female
,count(*)  
    - sum(case when s.is_female = '1' then 1 else 0 end)              n_male
,sum(case when s.is_female = '1' then 1.00000000 else 0.00000000 end)
    / count(*)                      gender_ratio
,sum(case when s.has_disability = '1' then 1 else 0 end)              n_disabled
,sum(case when s.has_disability = '1' then 1.000000000 else 0.000000000 end)
    / count(*)                      disability_ratio
,sum(vibo.imd_band_00_10)  n_imd_00_10
,sum(vibo.imd_band_10_20)  n_imd_10_20
,sum(vibo.imd_band_20_30)  n_imd_20_30
,sum(vibo.imd_band_30_40)  n_imd_30_40
,sum(vibo.imd_band_40_50)  n_imd_40_50
,sum(vibo.imd_band_50_60)  n_imd_50_60
,sum(vibo.imd_band_60_70)  n_imd_60_70
,sum(vibo.imd_band_70_80)  n_imd_70_80
,sum(vibo.imd_band_80_90)  n_imd_80_90
,sum(vibo.imd_band_90_100) n_imd_90_100


into agg.course_reg_results
from main.student_info s
join main.v_imd_band_onehot vibo on vibo.id=s.imd_band_id
join main.final_result f on f.id=s.final_result_id

group by 
 s.course_id
,s.final_result_id
,f.final_result
