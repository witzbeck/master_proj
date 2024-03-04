select
    cast(id_student as int) student_id
    , cast(code_module as varchar(3)) code_module
    , cast(code_presentation as varchar(5)) code_presentation
    , cast(case
        when gender = 'F' then '1'
        when gender = 'M' then '0'
        else NULL
    end as bit) is_female
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
    end as bit) has_disability
    , cast(final_result as varchar(11)) final_result
into staging."studentInfo"
from landing."studentInfo"
