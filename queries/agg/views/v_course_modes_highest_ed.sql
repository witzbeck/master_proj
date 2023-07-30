create view agg.course_modes_result_highest_ed as
select 

course_id
,final_result_id
,max((select highest_education_id where highest_ed_top = 1)) highest_ed_top_1
,max((select highest_education_id where highest_ed_top = 2)) highest_ed_top_2
,max((select highest_education_id where highest_ed_top = 3)) highest_ed_top_3
,max((select highest_education_id where highest_ed_bot = 1)) highest_ed_bot_1
,max((select highest_education_id where highest_ed_bot = 2)) highest_ed_bot_2
,max((select highest_education_id where highest_ed_bot = 3)) highest_ed_bot_3
from (

select 
 row_number() over (partition by course_id, final_result_id
                    order by count(*))      highest_ed_bot
,row_number() over (partition by course_id, final_result_id
                    order by count(*) desc) highest_ed_top
,count(*) n_students
,course_id
,highest_education_id
,final_result_id
from main.student_info
GROUP BY 
course_id
,highest_education_id
,final_result_id
) a
group by course_id
,final_result_id

