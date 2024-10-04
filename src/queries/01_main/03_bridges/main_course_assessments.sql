select
    a.assessment_id,
    c.module_id,
    c.presentation_id,
    t.id assessment_type_id,
    c.module_code,
    c.presentation_code,
    t.assessment_type,
    a.assessment_date,
    a.assessment_weight
from main.assessment a
    join main.course_info c on c.id = a.course_id
    join main.assessment_type t on t.id = a.assessment_type_id
