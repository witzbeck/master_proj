create view agg.v_course_details as
select 

 c.*
,csb.n_students
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
,cmr.n_in_east_anglian_region
,cmr.n_in_east_midlands_region
,cmr.n_in_ireland
,cmr.n_in_london_region
,cmr.n_in_north_region
,cmr.n_in_north_western_region
,cmr.n_in_scotland
,cmr.n_in_south_east_region
,cmr.n_in_south_region
,cmr.n_in_south_west_region
,cmr.n_in_wales
,cmr.n_in_west_midlands_region
,cmr.n_in_yorkshire_region
,cma.n_age_0_35
,cma.n_age_35_55
,cma.n_age_55_up
,cmh.n_a_level_or_eq
,cmh.n_he_quals
,cmh.n_lower_than_a_level
,cmh.n_no_formal_quals
,cmh.n_post_grad_quals
,cmi.n_imd_0_10
,cmi.n_imd_10_20
,cmi.n_imd_20_30
,cmi.n_imd_30_40
,cmi.n_imd_40_50
,cmi.n_imd_50_60
,cmi.n_imd_60_70
,cmi.n_imd_70_80
,cmi.n_imd_80_90
,cmi.n_imd_90_100
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
join agg.v_course_modes cm on cm.course_id=c.course_id
join agg.v_course_modes_age_band cma on cma.course_id=c.course_id 
join agg.v_course_modes_highest_ed cmh on cmh.course_id=c.course_id 
join agg.v_course_modes_imd_band cmi on cmi.course_id=c.course_id 
join agg.v_course_modes_region cmr on cmr.course_id=c.course_id 
join (select
 s.course_id
,sum(vfro.is_distinction)   n_distinction
,sum(vfro.is_fail)          n_fail
,sum(vfro.is_pass)          n_pass
,sum(vfro.is_withdrawn)     n_withdrawn
from main.student_info s
join main.v_final_result_onehot vfro on vfro.id=s.final_result_id
group by s.course_id) fr on fr.course_id=c.course_id