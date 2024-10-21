select
    s.id student_id,
    c.id course_id,
    f.id final_result_id,
    s.date_registration,
    s.date_unregistration,
    s.date_unregistration - s.date_registration reg_date_dif,
    f.final_result,
    s.studied_credits,
    s.num_of_prev_attempts,
    s.is_female,
    s.has_disability,
    c.module_id,
    c.module_code,
    c.presentation_id,
    c.presentation_code,
    c.module_presentation_length,
    c.start_month,
    c.presentation_year,
    c.start_date,
    c.domain
from main.student_info s
    join main.course_info c on c.id = s.course_id
    join main.final_result f on f.id = s.final_result_id
