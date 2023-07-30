select
 a.course_id
,f.student_id

,coalesce(sum(case 
    when activity_percentile_by_clicks < 6 then f.n_clicks 
    else 0 end),0)                                     n_total_clicks_by_top_5th_clicks
,coalesce(sum(case 
    when activity_percentile_by_clicks < 6 then f.n_visits 
    else 0 end),0)                                     n_total_clicks_by_top_5th_visits
,coalesce(sum(case 
    when activity_percentile_by_visits < 6 then f.n_clicks 
    else 0 end),0)                                     n_total_visits_by_top_5th_clicks
,coalesce(sum(case 
    when activity_percentile_by_visits < 6 then f.n_visits 
    else 0 end),0)                                     n_total_visits_by_top_5th_visits
,coalesce(sum(case when activity_percentile_by_visits < 6 then 1 else 0 end),0)                 n_distinct_top_5th_by_clicks
,coalesce(sum(case when activity_percentile_by_visits < 6 then 1 else 0 end),0)                 n_distinct_top_5th_by_visits
into first30.activities_top_5th_perc
from first30.activities_ordered a
join first30.activities_by_frequency f on f.course_id=a.course_id and f.site_id=a.site_id
where (activity_percentile_by_clicks < 6 or activity_percentile_by_visits < 6)
group by a.course_id, f.student_id
order by a.course_id, f.student_id
