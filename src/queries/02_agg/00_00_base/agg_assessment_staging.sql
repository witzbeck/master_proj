select distinct
    s.id student_id,
    b.student_id orig_student_id,
    a.course_id,
    b.assessment_id,
    a.assessment_type_id,
    t.assessment_type,
    b.score,
    a.assessment_weight,
    case
        when a.assessment_weight > 0 then 1
        else 0
    end is_weighted,
    b.is_banked,
    b.date_submitted,
    a.assessment_date - b.date_submitted days_before_due_submitted,
    a.assessment_date date_due
from main.student_assessment_bridge b
    join (
        select
            id,
            orig_student_id
        from main.student_info
        group by
            id,
            orig_student_id
    ) s on s.orig_student_id = b.student_id
    join main.assessment a on a.assessment_id = b.assessment_id
    join main.assessment_type t on t.id = a.assessment_type_id

