BEGIN;

CREATE SCHEMA staging;

select
    cast(id_assessment as int) assessment_id
    , cast(code_module as varchar(3)) module_code
    , cast(code_presentation as varchar(5)) presentation_code
    , cast(assessment_type as varchar(4)) assessment_type
    , cast(NULLIF(date, '') as int) assessment_date
    , cast(NULLIF(weight, '') as float) assessment_weight
into staging.assessments
from landing.assessments
;

select
    cast(id_site as int) site_id
    , cast(code_module as varchar(3)) module_code
    , cast(code_presentation as varchar(5)) presentation_code
    , cast(activity_type as varchar(14)) activity_type
    , cast(NULLIF(week_from, '') as smallint) week_from
    , cast(NULLIF(week_to, '') as smallint) week_to
into staging.vle
from landing.vle
;

select
    cast(id_site as int) site_id
    , cast(id_student as int) student_id
    , cast(code_module as varchar(3)) module_code
    , cast(code_presentation as varchar(5)) presentation_code
    , cast(date as int) date
    , cast(sum_click as int) sum_click
into staging.studentVle
from landing.studentVle
;

select
    cast(code_module as varchar(3)) module_code
    , cast(code_presentation as varchar(5)) presentation_code
    , cast(id_student as int) student_id
    , cast(NULLIF(date_registration, '') as int) date_registration
    , cast(NULLIF(date_unregistration, '') as int) date_unregistration
into staging.studentRegistration
from landing.studentRegistration
;

select
    cast(id_student as int) student_id
    , cast(code_module as varchar(3)) module_code
    , cast(code_presentation as varchar(5)) presentation_code
    , cast(case
        when gender = 'F' then '1'
        when gender = 'M' then '0'
        else NULL
    end as smallint) is_female
    , cast(imd_band as varchar(7)) imd_band
    , cast(highest_education as varchar(27)) highest_education
    , cast(age_band as varchar(5)) age_band
    , cast(num_of_prev_attempts as int) num_of_prev_attempts
    , cast(studied_credits as int) studied_credits
    , cast(region as varchar(20)) region
    , cast(case
        when disability = 'Y' then '1'
        when disability = 'N' then '0'
        else disability
    end as smallint) has_disability
    , cast(final_result as varchar(11)) final_result
into staging.studentInfo
from landing.studentInfo
;

select
    cast(id_student as int) student_id
    , cast(id_assessment as int) assessment_id
    , cast(date_submitted as int) date_submitted
    , cast(is_banked as smallint) is_banked
    , cast(NULLIF(score, '') as smallint) score
into staging.studentAssessment
from landing.studentAssessment
;

select
    cast(code_module as varchar(3)) module_code
    , cast(code_presentation as varchar(5)) presentation_code
    , cast(module_presentation_length as int) module_presentation_length
into staging.courses
from landing.courses
;

COMMIT;