select
    site_id
    , si.id student_id
    , si.course_id
    , m.id module_id
    , p.id presentation_id
    , date
    , sum_click
into main.student_vle_bridge
from staging."studentVle" s
    join main.modules m on m.module_code = s.code_module
    join main.presentations p on p.presentation_code = s.code_presentation
    join main.student_info si on
        si.orig_student_id = s.student_id
        and si.module_id = m.id
        and si.presentation_id = p.id
;
