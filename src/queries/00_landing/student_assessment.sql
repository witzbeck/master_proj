select cast(id_student as int) AS student_id,
    cast(id_assessment as int) AS assessment_id,
    cast(date_submitted as int) AS date_submitted,
    cast(is_banked as bit) AS is_banked,
    cast(score as smallint) AS score
from student_assessment