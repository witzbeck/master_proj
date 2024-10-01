select
    cast(id_student as int) student_id,
    cast(id_assessment as int) assessment_id,
    cast(date_submitted as int) date_submitted,
    cast(is_banked as bit) is_banked,
    cast(score as smallint) score
from studentassessment
