SELECT s.course_id,
    s.final_result_id,
    count(*) n_students,
    sum(
        case
            when s.is_female = '1' then 1
            else 0
        end
    ) n_female,
    sum(
        case
            when s.has_disability = '1' then 1
            else 0
        end
    ) n_disabled,
    sum(vro.is_east_anglian_region) n_in_east_anglian_region,
    sum(vro.is_east_midlands_region) n_in_east_midlands_region,
    sum(vro.is_ireland) n_in_ireland,
    sum(vro.is_london_region) n_in_london_region,
    sum(vro.is_north_region) n_in_north_region,
    sum(vro.is_north_western_region) n_in_north_western_region,
    sum(vro.is_scotland) n_in_scotland,
    sum(vro.is_south_east_region) n_in_south_east_region,
    sum(vro.is_south_region) n_in_south_region,
    sum(vro.is_south_west_region) n_in_south_west_region,
    sum(vro.is_wales) n_in_wales,
    sum(vro.is_west_midlands_region) n_in_west_midlands_region,
    sum(vro.is_yorkshire_region) n_in_yorkshire_region,
    sum(vabo.is_0_35) n_age_0_35,
    sum(vabo.is_35_55) n_age_35_55,
    sum(vabo.is_55_less_equal) n_age_55_up,
    sum(vh.is_a_level_or_equivalent) n_a_level_or_eq,
    sum(vh.is_he_qualification) n_he_quals,
    sum(vh.is_lower_than_a_level) n_lower_than_a_level,
    sum(vh.is_no_formal_quals) n_no_formal_quals,
    sum(vh.is_post_graduate_qualification) n_post_grad_quals,
    sum(vibo.is_0_10_percent) n_imd_0_10,
    sum(vibo.is_10_20) n_imd_10_20,
    sum(vibo.is_20_30_percent) n_imd_20_30,
    sum(vibo.is_30_40_percent) n_imd_30_40,
    sum(vibo.is_40_50_percent) n_imd_40_50,
    sum(vibo.is_50_60_percent) n_imd_50_60,
    sum(vibo.is_60_70_percent) n_imd_60_70,
    sum(vibo.is_70_80_percent) n_imd_70_80,
    sum(vibo.is_80_90_percent) n_imd_80_90,
    sum(vibo.is_90_100_percent) n_imd_90_100
from main.student_info s
    join main.onehot_region vro on vro.id = s.region_id
    join main.onehot_age_band vabo on vabo.id = s.age_band_id
    join main.onehot_highest_education vh on vh.id = s.highest_education_id
    join main.onehot_imd_band vibo on vibo.id = s.imd_band_id
group by s.course_id,
    s.final_result_id