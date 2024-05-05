SELECT

    f.student_id
    , f.course_id
    , f.module_id
    , f.presentation_id
    , f.n_days n_distinct_visits
    , f.n_total_visits
    , f.n_total_clicks
    , f.avg_clicks_per_day
    , f.avg_clicks_per_visit
    , ntile(100) OVER (ORDER BY f.n_days) distinct_visits_percentile
    , ntile(100) OVER (ORDER BY f.n_total_visits) total_visits_percentile
    , ntile(100) OVER (ORDER BY f.n_total_clicks) total_clicks_percentile
    , ntile(100) OVER (ORDER BY f.avg_clicks_per_day) avg_clicks_per_day_percentile
    , ntile(100) OVER (ORDER BY f.avg_clicks_per_visit) avg_clicks_per_visit_percentile
FROM agg.mom_interactions_12 f
