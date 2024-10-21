select
    b.student_id,
    a.course_id,
    b.assessment_id,
    b.date_submitted,
    b.is_banked,
    b.score,
    a.assessment_type_id,
    a.assessment_date date_due,
    a.assessment_weight,
    case
        when a.assessment_weight > 0 then 1
        else 0
    end is_weighted,
    a.assessment_date - b.date_submitted days_before_due_submitted
from main.student_assessment_bridge b
    join main.assessment a on a.assessment_id = b.assessment_id;
