select cast(code_module as varchar(3)) AS module_code,
    cast(code_presentation as varchar(5)) AS presentation_code,
    cast(id_student as int) AS student_id,
    cast(date_registration as int) AS date_registration,
    cast(date_unregistration as int) AS date_unregistration
from student_registration