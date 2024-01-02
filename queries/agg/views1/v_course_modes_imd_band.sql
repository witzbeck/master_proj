create view agg.v_course_modes_imd_band as
select
 course_id
,final_result_id
,max((select imd_band_id where imd_top = 1)) imd_top_1
,max((select imd_band_id where imd_top = 2)) imd_top_2
,max((select imd_band_id where imd_top = 3)) imd_top_3
,max((select imd_band_id where imd_bot = 1)) imd_bot_1
,max((select imd_band_id where imd_bot = 2)) imd_bot_2
,max((select imd_band_id where imd_bot = 3)) imd_bot_3
from (

select 
 row_number() over (partition by course_id, final_result_id
                    order by count(*)) imd_bot
,row_number() over (partition by course_id, final_result_id
                    order by count(*) desc) imd_top
,count(*) n_students
,course_id
,imd_band_id
,final_result_id
from main.student_info
GROUP BY 
course_id
,imd_band_id
,final_result_id
) a
group by course_id, final_result_id

