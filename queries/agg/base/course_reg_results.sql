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
,sum(vabo.is_le_35)         n_le_35
,sum(vabo.is_35_55)         n_35_55
,sum(vabo.is_ge_55)         n_ge_55
,sum(vro.is_east_anglian)   n_east_anglian
,sum(vro.is_east_midlands)  n_east_midlands
,sum(vro.is_ireland)        n_ireland
,sum(vro.is_london)         n_london
,sum(vro.is_north)          n_north
,sum(vro.is_north_western)  n_north_western
,sum(vro.is_scotland)       n_scotland
,sum(vro.is_south_east)     n_south_east
,sum(vro.is_south)          n_south
,sum(vro.is_south_west)     n_south_west
,sum(vro.is_wales)          n_wales
,sum(vro.is_west_midlands)  n_west_midlands
,sum(vro.is_yorkshire)      n_yorkshire
,sum(vheo.is_a_level_or_equivalent)       n_a_level
,sum(vheo.is_he_qualification)            n_he_qual
,sum(vheo.is_lower_than_a_level)          n_lower_than_a_level
,sum(vheo.is_no_formal_quals)             n_no_formal_qual
,sum(vheo.is_post_graduate_qualification) n_post_grad_qual


into agg.course_reg_results
from main.student_info s
join main.v_imd_band_onehot vibo on vibo.id=s.imd_band_id
join main.v_age_band_onehot vabo on vabo.id=s.age_band_id
join main.v_region_onehot vro on vro.id=s.region_id
join main.v_highest_education_onehot vheo on vheo.id=s.highest_education_id
join main.final_result f on f.id=s.final_result_id

group by 
 s.course_id
,s.final_result_id
,f.final_result
