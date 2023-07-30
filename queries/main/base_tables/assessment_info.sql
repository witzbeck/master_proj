drop table if exists main.assessments cascade;
select
     assessment_id
    ,c.id               course_id
    ,at.id              assessment_type_id
    ,date
    ,weight
into main.assessment_info
from staging.assessments a 
join main.course_info c on c.module_code=a.code_module
                     and c.presentation_code=a.code_presentation
join main.assessment_types at on at.assessment_type=a.assessment_type