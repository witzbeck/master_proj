select cast(id_assessment as int) AS assessment_id,
    cast(code_module as varchar(3)) AS module_code,
    cast(code_presentation as varchar(5)) AS presentation_code,
    cast(assessment_type as varchar(4)) AS assessment_type,
    cast(date as int) AS assessment_date,
    cast(weight as int) AS assessment_weight
from assessments