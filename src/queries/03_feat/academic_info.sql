drop table if exists first30.academic_info;
select
 si.id                                          student_id
,course_id
,si.num_of_prev_attempts
,si.final_result_id
,si.studied_credits
,si.date_registration                           reg_date
,si.date_unregistration                         unreg_date
,si.date_unregistration - si.date_registration  reg_date_dif
into first30.academic_info
from main.student_info si
where (date_unregistration is null or date_unregistration > 30)