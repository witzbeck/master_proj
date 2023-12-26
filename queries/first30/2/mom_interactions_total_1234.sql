with act as (
select
 i.student_id
,i.n

,i.avg_clicks
,i.var_clicks
,i.stddev_clicks

,i.avg_date
,i.var_date
,i.stddev_date

,a.avg_n_activity_types
,a.var_n_activity_types
,a.stddev_n_activity_types

,a.avg_n_activities
,a.var_n_activities
,a.stddev_n_activities
from first30.mom_interactions_total_12 i
join first30.mom_activities_12 a on a.student_id=i.student_id
)
select
 v.student_id
,a.n

,a.avg_n_activity_types
,a.var_n_activity_types
,a.stddev_n_activity_types
,case when stddev_n_activity_types = 0 then 0 else (sum((v.n_activity_types - a.avg_n_activity_types)^3) / a.n) / (stddev_n_activity_types^3) end skew_n_activity_types
,case when stddev_n_activity_types = 0 then 0 else (sum((v.n_activity_types - a.avg_n_activity_types)^4) / a.n) / (stddev_n_activity_types^4) end kurt_n_activity_types

,a.avg_n_activities
,a.var_n_activities
,a.stddev_n_activities
,case when stddev_n_activities = 0 then 0 else (sum((v.n_activities - a.avg_n_activities)^3) / a.n) / (stddev_n_activities^3) end skew_n_activities
,case when stddev_n_activities = 0 then 0 else (sum((v.n_activities - a.avg_n_activities)^4) / a.n) / (stddev_n_activities^4) end kurt_n_activities

,a.avg_date
,a.var_date
,a.stddev_date
,case when stddev_date = 0 then 0 else (sum((v.date - a.avg_date)^3) / a.n) / (stddev_date^3) end skew_date
,case when stddev_date = 0 then 0 else (sum((v.date - a.avg_date)^4) / a.n) / (stddev_date^4) end kurt_date

,a.avg_clicks
,a.var_clicks
,a.stddev_clicks
,case when stddev_clicks = 0 then 0 else (sum((c.sum_click - a.avg_clicks)^3) / a.n) / (stddev_clicks^3) end skew_clicks
,case when stddev_clicks = 0 then 0 else (sum((c.sum_click - a.avg_clicks)^4) / a.n) / (stddev_clicks^4) end kurt_clicks
,case 
    when a.n > 2 then (|/(a.n * (a.n - 1)))/(a.n - 2) 
    else 1 end                                  fp_coeff

into first30.mom_interactions_total_1234
from agg.v_student_activities_per_day v
join agg.student_clicks_per_date c on c.student_id=v.student_id and c.date=v.date
join act a on a.student_id=v.student_id
where (c.date <= 30 or v.date <= 30)

--where stddev_clicks <> 0
--and stddev_date <> 0

group by 
 v.student_id
,a.n
,a.avg_n_activity_types
,a.var_n_activity_types
,a.stddev_n_activity_types
,a.avg_n_activities
,a.var_n_activities
,a.stddev_n_activities
,a.avg_date
,a.var_date
,a.stddev_date
,a.avg_clicks
,a.var_clicks
,a.stddev_clicks
