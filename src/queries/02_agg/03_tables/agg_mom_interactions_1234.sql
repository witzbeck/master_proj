with act as (
    select mc1.student_id,
        mc1.n,
        mc1.avg_clicks,
        mc1.var_clicks,
        mc1.stddev_clicks,
        md1.avg_date,
        md1.var_date,
        md1.stddev_date,
        mda1.avg_n_activity_types,
        mda1.var_n_activity_types,
        mda1.stddev_n_activity_types,
        mda1.avg_n_activities,
        mda1.var_n_activities,
        mda1.stddev_n_activities
    from agg.mom_dates_12 md1
        join agg.mom_clicks_12 mc1 on mc1.student_id = md1.student_id
        join agg.mom_distinct_activities_12 mda1 on mda1.student_id = md1.student_id
)
select v.student_id,
    a.n,
    a.avg_n_activity_types,
    a.var_n_activity_types,
    a.stddev_n_activity_types,
    case
        when stddev_n_activity_types = 0 then 0
        else (
            sum(
                (v.n_activity_types - a.avg_n_activity_types) ^ 3
            ) / a.n
        ) / (stddev_n_activity_types ^ 3)
    end skew_n_activity_types,
    case
        when stddev_n_activity_types = 0 then 0
        else (
            sum(
                (v.n_activity_types - a.avg_n_activity_types) ^ 4
            ) / a.n
        ) / (stddev_n_activity_types ^ 4)
    end kurt_n_activity_types,
    a.avg_n_activities,
    a.var_n_activities,
    a.stddev_n_activities,
    case
        when stddev_n_activities = 0 then 0
        else (
            sum((v.n_activities - a.avg_n_activities) ^ 3) / a.n
        ) / (stddev_n_activities ^ 3)
    end skew_n_activities,
    case
        when stddev_n_activities = 0 then 0
        else (
            sum((v.n_activities - a.avg_n_activities) ^ 4) / a.n
        ) / (stddev_n_activities ^ 4)
    end kurt_n_activities,
    a.avg_date,
    a.var_date,
    a.stddev_date,
    case
        when stddev_date = 0 then 0
        else (sum((v.date - a.avg_date) ^ 3) / a.n) / (stddev_date ^ 3)
    end skew_date,
    case
        when stddev_date = 0 then 0
        else (sum((v.date - a.avg_date) ^ 4) / a.n) / (stddev_date ^ 4)
    end kurt_date,
    a.avg_clicks,
    a.var_clicks,
    a.stddev_clicks,
    case
        when stddev_clicks = 0 then 0
        else (sum((c.sum_click - a.avg_clicks) ^ 3) / a.n) / (stddev_clicks ^ 3)
    end skew_clicks,
    case
        when stddev_clicks = 0 then 0
        else (sum((c.sum_click - a.avg_clicks) ^ 4) / a.n) / (stddev_clicks ^ 4)
    end kurt_clicks,
    case
        when a.n > 2 then (sqrt(a.n * (a.n - 1))) /(a.n - 2)
        else 1
    end fp_coeff
from agg.student_activities_per_day v
    join agg.student_clicks_per_date c on c.student_id = v.student_id
    and c.date = v.date
    join act a on a.student_id = v.student_id
group by v.student_id,
    a.n,
    a.avg_n_activity_types,
    a.var_n_activity_types,
    a.stddev_n_activity_types,
    a.avg_n_activities,
    a.var_n_activities,
    a.stddev_n_activities,
    a.avg_date,
    a.var_date,
    a.stddev_date,
    a.avg_clicks,
    a.var_clicks,
    a.stddev_clicks