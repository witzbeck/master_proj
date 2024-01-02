create view agg.v_course_details as
select 

 c.*
,cr.final_result_id
,fr.n_students
,fr.n_distinction
,fr.n_fail
,fr.n_pass
,fr.n_withdrawn
,cr.sum_date_reg
,cr.avg_date_reg
,cr.sum_date_unreg
,cr.avg_date_unreg
,cr.sum_reg_date_dif
,cr.avg_reg_date_dif
,cr.sum_studied_credits
,cr.avg_studied_credits
,cr.sum_prev_attempts
,cr.avg_prev_attempts
,cr.n_female
,cr.n_male
,cr.gender_ratio
,cr.n_disabled
,cr.disability_ratio
,cr.n_east_anglian
,cr.n_east_midlands
,cr.n_ireland
,cr.n_london
,cr.n_north
,cr.n_north_western
,cr.n_scotland
,cr.n_south_east
,cr.n_south
,cr.n_south_west
,cr.n_wales
,cr.n_west_midlands
,cr.n_yorkshire
,cr.n_le_35
,cr.n_35_55
,cr.n_ge_55
,cr.n_a_level
,cr.n_he_qual
,cr.n_lower_than_a_level
,cr.n_no_formal_qual
,cr.n_post_grad_qual
,cr.n_imd_00_10
,cr.n_imd_10_20
,cr.n_imd_20_30
,cr.n_imd_30_40
,cr.n_imd_40_50
,cr.n_imd_50_60
,cr.n_imd_60_70
,cr.n_imd_70_80
,cr.n_imd_80_90
,cr.n_imd_90_100
,cm.age_band_top_1
,cm.age_band_top_2
,cm.age_band_top_3
,cm.age_band_bot_1
,cm.age_band_bot_2
,cm.age_band_bot_3
,cm.imd_top_1
,cm.imd_top_2
,cm.imd_top_3
,cm.imd_bot_1
,cm.imd_bot_2
,cm.imd_bot_3
,cm.region_top_1
,cm.region_top_2
,cm.region_top_3
,cm.region_bot_1
,cm.region_bot_2
,cm.region_bot_3
,cm.highest_ed_top_1
,cm.highest_ed_top_2
,cm.highest_ed_top_3
,cm.highest_ed_bot_1
,cm.highest_ed_bot_2
,cm.highest_ed_bot_3

from agg.course_info c
join agg.course_reg_results cr on cr.course_id=c.course_id
join agg.v_course_modes cm on cm.course_id=c.course_id and cm.final_result_id=cr.final_result_id
join (select
 s.course_id
,s.final_result_id
,sum(vfro.is_distinction)   n_distinction
,sum(vfro.is_fail)          n_fail
,sum(vfro.is_pass)          n_pass
,sum(vfro.is_withdrawn)     n_withdrawn
,count(*)                   n_students
from main.student_info s
join main.v_final_result_onehot vfro on vfro.id=s.final_result_id
group by s.course_id
,s.final_result_id
) fr on fr.course_id=c.course_id and fr.final_result_id=cr.final_result_id