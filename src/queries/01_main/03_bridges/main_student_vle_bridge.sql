select
    site_id,
    si.id student_id,
    si.course_id,
    m.id module_id,
    p.id presentation_id,
    date,
    sum_click
from landing.student_vle s
    join main.module m on m.module_code = s.module_code
    join main.presentation p on p.presentation_code = s.presentation_code
    join main.student_info si on
        si.orig_student_id = s.student_id
        and si.module_id = m.id
        and si.presentation_id = p.id;
