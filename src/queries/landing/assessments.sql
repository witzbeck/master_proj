select
    cast(id_assessment as int) assessment_id
    , cast(code_module as varchar(3)) code_module
    , cast(code_presentation as varchar(5)) code_presentation
    , cast(assessment_type as varchar(4)) assessment_type
    , cast(date as int) assessment_date
    , cast(weight as int) assessment_weight
into staging.assessments
from landing.assessments
