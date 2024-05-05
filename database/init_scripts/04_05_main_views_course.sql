create view main.v_course_registrations as
select
    s.id student_id
    , c.course_id
    , f.final_result_id
    , s.date_registration
    , s.date_unregistration
    , s.date_unregistration - s.date_registration reg_date_dif
    , f.final_result
    , s.studied_credits
    , s.num_of_prev_attempts
    , s.is_female
    , s.has_disability
    , c.module_id
    , c.module_code
    , c.presentation_id
    , c.presentation_code
    , c.module_presentation_length
    , c.start_month
    , c.presentation_year
    , c.start_date
    , c.domain
from main.student_info s
    join main.course_info c on c.course_id = s.course_id
    join main.final_result f on f.final_result_id = s.final_result_id

create view main.v_registrations as
select
    module_code
    , presentation_code
    , count(distinct student_id) n_student_ids
    , cast(sum(n_registrations) as int) n_registrations
    , cast(sum(n_unregistrations) as int) n_unregistrations
    , cast(sum(n_records) as int) n_records
from (
    select
        m.module_code
        , p.presentation_code
        , sr.id student_id
        , sr.date_registration
        , sr.date_unregistration
        , count(*) n_records
        , sum(case
            when sr.date_registration is not null
            then 1 else 0
        end) n_registrations
        , sum(case
            when sr.date_unregistration is not null
            then 1 else 0
        end) n_unregistrations
    from main.student_info sr
        join main.module m on m.module_id = sr.module_id
        join main.presentation p on p.presentation_id = sr.presentation_id

    group by
        module_code
        , presentation_code
        , sr.student_id
        , sr.date_registration
        , sr.date_unregistration
) a
group by
    module_code, presentation_code
