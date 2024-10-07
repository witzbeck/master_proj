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
,sum(vibo.is_0_10_percent)  n_imd_0_10
,sum(vibo.is_10_20)         n_imd_10_20
,sum(vibo.is_20_30_percent) n_imd_20_30
,sum(vibo.is_30_40_percent) n_imd_30_40
,sum(vibo.is_40_50_percent) n_imd_40_50
,sum(vibo.is_50_60_percent) n_imd_50_60
,sum(vibo.is_60_70_percent) n_imd_60_70
,sum(vibo.is_70_80_percent) n_imd_70_80
,sum(vibo.is_80_90_percent) n_imd_80_90
,sum(vibo.is_90_100_percent)n_imd_90100




from main.student_info s
join main.onehot_imd_band vibo on vibo.id=s.imd_band_id
join main.final_result f on f.id=s.final_result_id

group by 
 s.course_id
,s.final_result_id
,f.final_result
