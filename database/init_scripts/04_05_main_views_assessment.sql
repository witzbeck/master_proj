create view main.v_assessment_staging as
select
    b.student_id
    , a.course_id
    , b.assessment_id
    , b.date_submitted
    , b.is_banked
    , b.score
    , a.assessment_type_id
    , a.date date_due
    , a.weight
    , case when a.weight > 0 then 1 else 0 end is_weighted
    , a.date - b.date_submitted days_before_due_submitted
from main.student_assessment_bridge b
    join main.assessment_info a on a.assessment_id = b.assessment_id

;

create view main.v_course_assessments as
select
    a.assessment_id
    , c.module_id
    , c.presentation_id
    , t.id assessment_type_id
    , c.module_code
    , c.presentation_code
    , t.assessment_type
    , a.date assessment_date
    , a.weight assessment_weight
from main.assessment_info a
    join main.course_info c on c.course_id = a.course_id
    join main.assessment_types t on t.assessment_type_id = a.assessment_type_id
