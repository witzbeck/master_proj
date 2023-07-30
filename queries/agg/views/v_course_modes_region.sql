create view agg.course_modes_result_region as
select 

course_id
,final_result_id
,max((select region_id where region_top = 1)) region_top_1
,max((select region_id where region_top = 2)) region_top_2
,max((select region_id where region_top = 3)) region_top_3
,max((select region_id where region_bot = 1)) region_bot_1
,max((select region_id where region_bot = 2)) region_bot_2
,max((select region_id where region_bot = 3)) region_bot_3
from (

select 
 row_number() over (partition by course_id, final_result_id
                    order by count(*)) region_bot
,row_number() over (partition by course_id, final_result_id
                    order by count(*) desc) region_top
,count(*) n_students
,course_id
,region_id
,final_result_id
from main.student_info
GROUP BY 
course_id
,region_id
,final_result_id
) a
group by course_id, final_result_id

