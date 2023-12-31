with freq as (
SELECT

 v.course_id
,v.module_id
,v.presentation_id
,v.site_id
,v.activity_type_id
,count(DISTINCT b.date)                                     n_distinct_visits
,count(*)                                                   n_total_visits
,sum(b.sum_click)                                           n_total_clicks
,sum(cast(b.sum_click as float)) / count(DISTINCT b.date)   avg_clicks_per_day
,sum(cast(b.sum_click as float)) / count(*)                 avg_clicks_per_visit
FROM main.student_vle_bridge b
JOIN main.vle_course_bridge v on b.site_id=v.site_id

group by   v.course_id
,v.module_id
,v.presentation_id
,v.site_id
,v.activity_type_id

)
SELECT
 f.course_id
,f.module_id
,f.presentation_id
,f.site_id
,f.activity_type_id
,f.n_distinct_visits
,f.n_total_visits
,f.n_total_clicks
,f.avg_clicks_per_day
,f.avg_clicks_per_visit
,ntile(100) over (order by f.n_distinct_visits) as distinct_visits_percentile
,ntile(100) over (order by f.n_total_visits) as total_visits_percentile
,ntile(100) over (order by f.n_total_clicks) as total_clicks_percentile
,ntile(100) over (order by f.avg_clicks_per_day) as avg_clicks_per_day_percentile
,ntile(100) over (order by f.avg_clicks_per_visit) as avg_clicks_per_visit_percentile
into agg.activity_interaction_percentiles
FROM freq f
