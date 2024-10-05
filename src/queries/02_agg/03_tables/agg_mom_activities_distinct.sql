with avg as (
    select v.student_id,
        count(*) n,
        cast(sum(v.n_activity_types) as float) / count(*) n_activity_types,
        cast(sum(v.n_activities) as float) / count(*) n_activities
    from agg.v_student_activities_per_day v
    where v.date <= 30
    group by student_id
)
select avg.student_id,
    avg.n n,
    avg.n_activity_types avg_n_activity_types,
    sum((v.n_activity_types - avg.n_activity_types) ^ 2) / avg.n var_n_activity_types,
    sqrt(
        sum((v.n_activity_types - avg.n_activity_types) ^ 2) / avg.n
    ) stddev_n_activity_types,
    avg.n_activities avg_n_activities,
    sum((v.n_activities - avg.n_activities) ^ 2) / avg.n var_n_activities,
    sqrt(
        sum((v.n_activities - avg.n_activities) ^ 2) / avg.n
    ) stddev_n_activities into first30.mom_activities_12
from agg.v_student_activities_per_day v
    join avg on avg.student_id = v.student_id
where v.date <= 30
group by avg.student_id,
    avg.n,
    avg.n_activity_types,
    avg.n_activities