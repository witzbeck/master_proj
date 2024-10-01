with freq as (
    select

        v.course_id
        , v.module_id
        , v.presentation_id
        , v.site_id
        , v.activity_type_id
        , count(distinct b.date) n_distinct_visits
        , count(*) n_total_visits
        , sum(b.sum_click) n_total_clicks
        , sum(cast(b.sum_click as float)) / count(distinct b.date) avg_clicks_per_day
        , sum(cast(b.sum_click as float)) / count(*) avg_clicks_per_visit
    from main.student_vle_bridge b
        join main.vle_course_bridge v on b.site_id = v.site_id

    group by
        v.course_id
        , v.module_id
        , v.presentation_id
        , v.site_id
        , v.activity_type_id

)

select
    f.course_id
    , f.module_id
    , f.presentation_id
    , f.site_id
    , f.activity_type_id
    , f.n_distinct_visits
    , f.n_total_visits
    , f.n_total_clicks
    , f.avg_clicks_per_day
    , f.avg_clicks_per_visit
    , ntile(100) over (order by f.n_distinct_visits) distinct_visits_percentile
    , ntile(100) over (order by f.n_total_visits) total_visits_percentile
    , ntile(100) over (order by f.n_total_clicks) total_clicks_percentile
    , ntile(100) over (order by f.avg_clicks_per_day) avg_clicks_per_day_percentile
    , ntile(100) over (order by f.avg_clicks_per_visit) avg_clicks_per_visit_percentile
from freq f
