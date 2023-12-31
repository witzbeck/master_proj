SELECT

 f.student_id
,f.course_id
,f.module_id
,f.presentation_id
,f.n_days n_distinct_visits
,f.n_total_visits
,f.n_total_clicks
,f.avg_clicks_per_day
,f.avg_clicks_per_visit
,ntile(100) over (order by f.n_days) as distinct_visits_percentile
,ntile(100) over (order by f.n_total_visits) as total_visits_percentile
,ntile(100) over (order by f.n_total_clicks) as total_clicks_percentile
,ntile(100) over (order by f.avg_clicks_per_day) as avg_clicks_per_day_percentile
,ntile(100) over (order by f.avg_clicks_per_visit) as avg_clicks_per_visit_percentile
into agg.student_interaction_percentiles
FROM agg.mom_interactions_12 f
