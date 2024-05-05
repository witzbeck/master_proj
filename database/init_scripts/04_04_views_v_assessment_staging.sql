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
