select
    vcb.site_id,
    svb.student_id,
    c.module_id,
    c.presentation_id,
    at.id activity_type_id,
    c.module_code,
    c.presentation_code,
    at.activity_type,
    svb.date activity_date,
    svb.sum_click,
    case
        when week_from is null then 0
        else 1
    end has_date_range,
    vcb.week_from,
    vcb.week_to
from main.vle_course_bridge vcb
    join main.course_info c on c.id = vcb.course_id
    join main.student_vle_bridge svb on svb.site_id = vcb.site_id
    join main.activity_type at on at.id = vcb.activity_type_id
