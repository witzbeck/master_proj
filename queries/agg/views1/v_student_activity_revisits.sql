create view agg.v_student_activity_revists as
select
 student_id
,max(r.n_days)              n_max_revists
,min(r.n_days)              n_min_revists
,sum(r.n_days)              n_sum_top_5_revists
,sum(r.n_days) / count(*)   avg_top_5_revists
,count(*)                   n_top_days

from (
select
 vis.student_id
,vis.site_id
,count(distinct vis.date) n_days
,row_number() over (partition by student_id 
                    order by count(distinct vis.date) desc) top_order
from agg.interaction_types_staging vis
where activity_type_id not in (7,4) -- not homepage, folder
group by vis.student_id, site_id
) r
where top_order < 6
group by student_id
