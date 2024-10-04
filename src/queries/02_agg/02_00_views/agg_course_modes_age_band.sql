select
    course_id
    , final_result_id
    , max((select age_band_id where age_band_top = 1)) age_band_top_1
    , max((select age_band_id where age_band_top = 2)) age_band_top_2
    , max((select age_band_id where age_band_top = 3)) age_band_top_3
    , max((select age_band_id where age_band_bot = 1)) age_band_bot_1
    , max((select age_band_id where age_band_bot = 2)) age_band_bot_2
    , max((select age_band_id where age_band_bot = 3)) age_band_bot_3
from (

    select
        row_number() over (
            partition by course_id, final_result_id
            order by count(*)
        ) age_band_bot
        , row_number() over (
            partition by course_id, final_result_id
            order by count(*) desc
        ) age_band_top
        , count(*) n_students
        , course_id
        , age_band_id
        , final_result_id
    from main.student_info
    group by
        course_id
        , age_band_id
        , final_result_id
) a
group by course_id, final_result_id
