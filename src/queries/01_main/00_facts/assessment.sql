select
    assessment_id
    , c.id course_id
    , c.module_id
    , c.presentation_id
    , at.id assessment_type_id
    , date
    , weight
from staging.assessments a
    join main.course_info c
        on
            c.module_code = a.code_module
            and c.presentation_code = a.code_presentation
    join main.assessment_types at on at.assessment_type = a.assessment_type
