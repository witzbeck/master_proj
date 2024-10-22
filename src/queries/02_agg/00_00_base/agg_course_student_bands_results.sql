SELECT s.course_id,
    s.final_result_id,
    count(*) n_students,
    sum(
        CASE
            WHEN s.is_female = '1' THEN 1
            ELSE 0
        END
    ) n_female,
    sum(
        CASE
            WHEN s.has_disability = '1' THEN 1
            ELSE 0
        END
    ) n_disabled,
    sum(vro.is_east_anglian) n_in_east_anglian,
    sum(vro.is_east_midlands) n_in_east_midlands,
    sum(vro.is_ireland) n_in_ireland,
    sum(vro.is_london) n_in_london,
    sum(vro.is_north) n_in_north,
    sum(vro.is_north_western) n_in_north_western,
    sum(vro.is_scotland) n_in_scotland,
    sum(vro.is_south_east) n_in_south_east,
    sum(vro.is_south_west) n_in_south_west,
    sum(vro.is_wales) n_in_wales,
    sum(vro.is_west_midlands) n_in_west_midlands,
    sum(vro.is_yorkshire) n_in_yorkshire,
    sum(vabo.is_le_35) n_age_le_35,
    sum(vabo.is_35_55) n_age_35_55,
    sum(vabo.is_ge_55) n_age_ge_55,
    sum(vh.is_a_level_or_equivalent) n_a_level_or_eq,
    sum(vh.is_he_qualification) n_he_quals,
    sum(vh.is_lower_than_a_level) n_lower_than_a_level,
    sum(vh.is_no_formal_quals) n_no_formal_quals,
    sum(vh.is_post_graduate_qualification) n_post_grad_quals,
    sum(vibo.imd_band_00_10) n_imd_00_10,
    sum(vibo.imd_band_10_20) n_imd_10_20,
    sum(vibo.imd_band_20_30) n_imd_20_30,
    sum(vibo.imd_band_30_40) n_imd_30_40,
    sum(vibo.imd_band_40_50) n_imd_40_50,
    sum(vibo.imd_band_50_60) n_imd_50_60,
    sum(vibo.imd_band_60_70) n_imd_60_70,
    sum(vibo.imd_band_70_80) n_imd_70_80,
    sum(vibo.imd_band_80_90) n_imd_80_90,
    sum(vibo.imd_band_90_100) n_imd_90_100
FROM main.student_info s
    JOIN main.onehot_region vro ON vro.id = s.region_id
    JOIN main.onehot_age_band vabo ON vabo.id = s.age_band_id
    JOIN main.onehot_highest_education vh ON vh.id = s.highest_education_id
    JOIN main.onehot_imd_band vibo ON vibo.id = s.imd_band_id
GROUP BY s.course_id,
    s.final_result_id