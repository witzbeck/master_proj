select cast(id_site as int) AS site_id,
    cast(id_student as int) AS student_id,
    cast(code_module as varchar(3)) AS module_code,
    cast(code_presentation as varchar(5)) AS presentation_code,
    cast(date as int) date,
    cast(sum_click as int) AS sum_click
from student_vle