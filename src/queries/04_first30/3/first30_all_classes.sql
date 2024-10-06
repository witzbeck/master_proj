select
    a.id student_id
    , a.course_id
    , c.module_id
    , c.presentation_id

    , vf.final_result
    , a.final_result_id
    , case when vf.is_distinction + vf.is_pass > 0 then 1 else 0 end is_pass_or_distinction
    , case when vf.is_fail + vf.is_withdrawn > 0 then 1 else 0 end is_withdraw_or_fail
    , vf.is_distinction
    , vf.is_pass
    , vf.is_fail
    , vf.is_withdrawn

    , c.module_presentation_length
    , c.presentation_year start_year
    , c.start_month
    , case when domain = 'STEM' then 1 else 0 end is_stem
    , c.level course_level

    , a.num_of_prev_attempts
    , a.studied_credits
    , a.date_registration reg_date
    , a.date_unregistration unreg_date
    , a.date_unregistration - a.date_registration reg_date_dif
    , a.is_female
    , a.has_disability
    , case when va.age_band = '<=55' then '55+' else va.age_band end age_band
    , a.age_band_id
    , va.is_le_35
    , va.is_35_55
    , va.is_ge_55
    , a.highest_education_id
    , vh.highest_education
    , vh.is_no_formal_quals
    , vh.is_lower_than_a_level
    , vh.is_a_level_or_equivalent
    , vh.is_he_qualification
    , vh.is_post_graduate_qualification
    , a.imd_band_id
    , vi.imd_band
    , vi.imd_band_00_10
    , vi.imd_band_10_20
    , vi.imd_band_20_30
    , vi.imd_band_30_40
    , vi.imd_band_40_50
    , vi.imd_band_50_60
    , vi.imd_band_60_70
    , vi.imd_band_70_80
    , vi.imd_band_80_90
    , vi.imd_band_90_100
    , a.region_id
    , vr.region
    , vr.is_east_anglian
    , vr.is_east_midlands
    , vr.is_ireland
    , vr.is_london
    , vr.is_north
    , vr.is_north_western
    , vr.is_scotland
    , vr.is_south_east
    , vr.is_south_west
    , vr.is_west_midlands
    , vr.is_yorkshire
    , vr.is_south
    , vr.is_wales

from main.student_info a
    join main.course_info c on c.id = a.course_id
    join first30.students s on s.id = a.id
    left join main.v_age_band_onehot va on va.id = a.age_band_id
    left join main.v_final_result_onehot vf on vf.id = a.final_result_id
    left join main.v_highest_education_onehot vh on vh.id = a.highest_education_id
    left join main.v_imd_band_onehot vi on vi.id = a.imd_band_id
    left join main.v_region_onehot vr on vr.id = a.region_id
