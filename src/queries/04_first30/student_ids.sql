select
 si.id
from main.student_info si
where (date_unregistration is null or date_unregistration > 30)