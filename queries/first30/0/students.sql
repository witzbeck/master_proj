select
 si.id
into first30.students
from main.student_info si
where (date_unregistration is null or date_unregistration > 30)