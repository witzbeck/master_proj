select
    course_id
    , is_stem
    , n_students
    , n_females
    , n_disabled
    , cast(n_females as float) / cast(n_students as float) female_ratio
    , cast(n_disabled as float) / cast(n_students as float) disabled_ratio
from (
    select
        ac.course_id
        , ac.is_stem
        , count(*) n_students
        , sum(cast(ac.is_female as int)) n_females
        , sum(cast(ac.has_disability as int)) n_disabled
    from first30.all_classes ac
    group by
        ac.course_id
        , ac.is_stem
) a
