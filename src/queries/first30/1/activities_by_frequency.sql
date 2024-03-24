select
    a.course_id
    , a.student_id
    , a.activity_type_id
    , a.site_id
    , a.activity_type
    , a.n_clicks
    , a.n_visits
    , row_number() over (partition by
        a.course_id
        , a.student_id
    order by a.n_visits desc) top_student_activity_by_visits
    , row_number() over (partition by
        a.course_id
        , a.student_id
    order by a.n_clicks desc) top_student_activity_by_clicks
    , row_number() over (partition by
        a.course_id
        , a.student_id
    order by a.n_visits) bot_student_activity_by_visits
    , row_number() over (partition by
        a.course_id
        , a.student_id
    order by a.n_clicks) bot_student_activity_by_clicks
into first30.activities_by_frequency

from (
    select
        vis.course_id
        , vis.student_id
        , vis.activity_type_id
        , vis.site_id
        , vis.activity_type
        , sum(vis.sum_click) n_clicks
        , count(*) n_visits
    from first30.interaction_types_staging vis
    where date <= 30
    group by
        vis.course_id
        , vis.student_id
        , vis.activity_type_id
        , vis.site_id
        , vis.activity_type
) a
order by course_id, top_student_activity_by_visits
