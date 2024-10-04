select
    c.id course_id
    , a.final_result_id
    , a.age_band_top_1
    , a.age_band_top_2
    , a.age_band_top_3
    , a.age_band_bot_1
    , a.age_band_bot_2
    , a.age_band_bot_3
    , i.imd_top_1
    , i.imd_top_2
    , i.imd_top_3
    , i.imd_bot_1
    , i.imd_bot_2
    , i.imd_bot_3
    , r.region_top_1
    , r.region_top_2
    , r.region_top_3
    , r.region_bot_1
    , r.region_bot_2
    , r.region_bot_3
    , e.highest_ed_top_1
    , e.highest_ed_top_2
    , e.highest_ed_top_3
    , e.highest_ed_bot_1
    , e.highest_ed_bot_2
    , e.highest_ed_bot_3
from main.course_info c
    left join agg.v_course_modes_age_band a on c.id = a.course_id and a.final_result_id = a.final_result_id
    left join agg.v_course_modes_imd_band i on c.id = i.course_id and i.final_result_id = a.final_result_id
    left join agg.v_course_modes_region r on c.id = r.course_id and r.final_result_id = a.final_result_id
    left join agg.v_course_modes_highest_ed e on c.id = e.course_id and e.final_result_id = a.final_result_id
