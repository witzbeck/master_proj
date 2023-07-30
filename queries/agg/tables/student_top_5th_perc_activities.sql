with is_5th_perc as (select
 p.course_id
,p.site_id
,case when p.activity_percentile_by_visits < 6 then 1 else 0 end is_5th_perc_visits
,case when p.activity_percentile_by_clicks < 6 then 1 else 0 end is_5th_perc_clicks
from first30.course_activity_percentiles p
where (p.activity_percentile_by_clicks < 6 or p.activity_percentile_by_visits < 6))
select
 f.course_id
,f.student_id
,coalesce(sum(case 
    when is_5th_perc_clicks = 1 then f.n_clicks 
    else 0 end),0)                                     n_total_clicks_by_top_5th_clicks
,coalesce(sum(case 
    when is_5th_perc_clicks = 1 then f.n_visits 
    else 0 end),0)                                     n_total_clicks_by_top_5th_visits
,coalesce(sum(case 
    when is_5th_perc_visits = 1 then f.n_clicks 
    else 0 end),0)                                     n_total_visits_by_top_5th_clicks
,coalesce(sum(case 
    when is_5th_perc_visits = 1 then f.n_visits 
    else 0 end),0)                                     n_total_visits_by_top_5th_visits
,coalesce(sum(p.is_5th_perc_clicks),0)                 n_distinct_top_5th_by_clicks
,coalesce(sum(p.is_5th_perc_visits),0)                 n_distinct_top_5th_by_visits
into agg.course_activities_top_student_interactions
from agg.course_activities_by_frequency f
left join is_5th_perc p on p.course_id=f.course_id and p.site_id=f.site_id
group by f.course_id, f.student_id
order by f.course_id, f.student_id
