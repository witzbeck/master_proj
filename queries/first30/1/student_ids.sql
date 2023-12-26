select
 si.id
into first30.student_ids
from main.student_info si
where (date_unregistration is null or date_unregistration > 30)