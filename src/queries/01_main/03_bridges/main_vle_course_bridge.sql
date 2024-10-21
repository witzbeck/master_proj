select
    site_id,
    c.id course_id,
    c.module_id,
    c.presentation_id,
    a.id activity_type_id,
    week_from,
    week_to
from landing.vle v
    join main.course_info c
        on
            c.module_code = v.module_code
            and c.presentation_code = v.presentation_code
    join main.activity_type a on a.activity_type = v.activity_type
