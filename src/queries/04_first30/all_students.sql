select
 a.student_id
,a.course_id
,c.module_id
,c.presentation_id

,vf.final_result
,a.final_result_id
,case when vf.is_distinction + vf.is_pass > 0 then 1 else 0 end is_pass_or_distinction
,case when vf.is_fail + vf.is_withdrawn > 0 then 1 else 0 end is_withdraw_or_fail
,vf.is_distinction
,vf.is_pass
,vf.is_fail
,vf.is_withdrawn

,c.module_presentation_length
,c.start_year
,c.start_month
,c.is_stem
,c.course_level

,a.num_of_prev_attempts
,a.studied_credits
,a.reg_date
,a.unreg_date
,a.reg_date_dif
,d.is_female
,d.has_disability
,case when va.age_band = '<=55' then '55+' else va.age_band end age_band
,d.age_band_id
,va.is_0_35                             is_age_0_to_35
,va.is_35_55                            is_age_35_to_55
,va.is_55_less_equal                    is_age_55_up
,d.highest_education_id
,vh.highest_education
,vh.is_a_level_or_equivalent            is_highest_ed_a_level_or_equivalent
,vh.is_he_qualification                 is_highest_ed_he_qualification
,vh.is_lower_than_a_level               is_highest_ed_lower_than_a_level
,vh.is_no_formal_quals                  is_highest_ed_no_formal_quals
,vh.is_post_graduate_qualification      is_highest_ed_post_graduate_qualification
,d.imd_band_id
,vi.imd_band
,vi.is_0_10_percent
,vi.is_10_20                            is_imd_10_20_percent
,vi.is_20_30_percent                    is_imd_20_30_percent
,vi.is_30_40_percent                    is_imd_30_40_percent
,vi.is_40_50_percent                    is_imd_40_50_percent
,vi.is_50_60_percent                    is_imd_50_60_percent
,vi.is_60_70_percent                    is_imd_60_70_percent
,vi.is_70_80_percent                    is_imd_70_80_percent
,vi.is_80_90_percent                    is_imd_80_90_percent
,vi.is_90_100_percent                   is_imd_90_100_percent
,d.region_id
,vr.region
,vr.is_east_anglian_region              is_region_east_anglian
,vr.is_east_midlands_region             is_region_east_midlands
,vr.is_ireland                          is_region_ireland
,vr.is_london_region                    is_region_london
,vr.is_north_region                     is_region_north
,vr.is_north_western_region             is_region_north_western
,vr.is_scotland                         is_region_scotland
,vr.is_south_east_region                is_region_south_east
,vr.is_south_region                     is_region_south
,vr.is_south_west_region                is_region_south_west
,vr.is_wales                            is_region_wales
,vr.is_west_midlands_region             is_region_west_midlands
,vr.is_yorkshire_region                 is_region_yorkshire

from first30.academic_info a
join feat.course_info c on c.course_id=a.course_id
join first30.demographic_info d on d.student_id=a.student_id
left join main.v_age_band_onehot va on va.id=d.age_band_id
left join main.v_final_result_onehot vf on vf.id=a.final_result_id
left join main.v_highest_education_onehot vh on vh.id=d.highest_education_id
left join main.v_imd_band_onehot vi on vi.id=d.imd_band_id
left join main.v_regions_onehot vr on vr.id=d.region_id
