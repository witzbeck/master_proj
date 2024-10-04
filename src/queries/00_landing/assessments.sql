select
    cast(id_assessment as int) assessment_id,
    cast(code_module as varchar(3)) module_code,
    cast(code_presentation as varchar(5)) presentation_code,
    cast(assessment_type as varchar(4)) assessment_type,
    cast(date as int) assessment_date,
    cast(weight as int) assessment_weight
from assessments
