select cast(id_student as int) AS student_id,
    cast(code_module as varchar(3)) AS module_code,
    cast(code_presentation as varchar(5)) AS presentation_code,
    cast(
        case
            when gender = 'F' then '1'
            when gender = 'M' then '0'
            else NULL
        end as bit
    ) AS is_female,
    cast(imd_band as varchar(7)) AS imd_band,
    cast(highest_education as varchar(27)) AS highest_education,
    cast(age_band as varchar(5)) AS age_band,
    cast(num_of_prev_attempts as int) AS num_of_prev_attempts,
    cast(studied_credits as int) AS studied_credits,
    cast(region as varchar(20)) AS region,
    cast(
        case
            when disability = 'Y' then '1'
            when disability = 'N' then '0'
            else disability
        end as bit
    ) AS has_disability,
    cast(final_result as varchar(11)) AS final_result
from student_info