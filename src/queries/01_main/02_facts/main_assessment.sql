select
    assessment_id,
    c.id course_id,
    c.module_id,
    c.presentation_id,
    at.id assessment_type_id,
    a.assessment_date,
    a.assessment_weight
from landing.assessments a
    join main.course_info c
        on
            c.module_code = a.module_code
            and c.presentation_code = a.presentation_code
    join main.assessment_type at on at.assessment_type = a.assessment_type
