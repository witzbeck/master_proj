select
    cast(id_site as int) site_id,
    cast(id_student as int) student_id,
    cast(code_module as varchar(3)) module_code,
    cast(code_presentation as varchar(5)) presentation_code,
    cast(date as int) date,
    cast(sum_click as int) sum_click
from student_vle
