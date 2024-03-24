select
    ci.id course_id
    , ci.module_id
    , ci.presentation_id
    , ci.module_presentation_length
    , cast(presentation_year as int) start_year
    , case when start_month = 'February' then 2 else 10 end start_month
    , case when ci.domain = 'STEM' then 1 else 0 end is_stem
    , ci.level course_level
into feat.course_info
from main.course_info ci
