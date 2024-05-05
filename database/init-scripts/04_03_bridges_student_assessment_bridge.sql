select
    student_id
    , assessment_id
    , date_submitted
    , is_banked
    , score
into main.student_assessment_bridge
from staging."studentAssessment"
;
