with activities_order as (
    select 
     row_number() over (partition by course_id order by sum(n_clicks) desc) order_by_clicks
    ,row_number() over (partition by course_id order by sum(n_visits) desc) order_by_visits
    ,sum(n_clicks) n_clicks
    ,sum(n_visits) n_visits
    ,course_id 
    ,activity_type_id
    ,site_id
    ,activity_type
    from first30.activities_by_frequency
    group by course_id, activity_type_id, site_id, activity_type
    )
select
 c.course_id
,c.activity_type_id
,c.site_id
,c.activity_type
,c.n_clicks
,c.n_visits
,c.order_by_visits
,c.order_by_clicks
,ceiling(((99 * cast(c.order_by_visits as float)) / max_by_visits)) + 1 activity_percentile_by_visits
,ceiling(((99 * cast(c.order_by_clicks as float)) / max_by_clicks)) + 1 activity_percentile_by_clicks
from activities_order c
join (
    select
    course_id
    ,max(order_by_clicks) max_by_clicks
    ,max(order_by_visits) max_by_visits
    from activities_order
    group by course_id
) na on na.course_id=c.course_id
group by  c.course_id
,c.activity_type_id
,c.site_id
,c.activity_type
,c.n_clicks
,c.n_visits
,c.order_by_visits
,c.order_by_clicks
,na.max_by_clicks
,na.max_by_visits

order by activity_percentile_by_clicks