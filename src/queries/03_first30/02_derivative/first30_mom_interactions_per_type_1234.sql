with act as (
    select m.student_id,
        m.activity_type_id,
        m.n,
        m.avg_date,
        m.var_date,
        m.stddev_date,
        m.avg_clicks,
        m.var_clicks,
        m.stddev_clicks
    from first30.mom_interactions_per_type_12 m
)
select v.student_id,
    v.course_id,
    v.activity_type_id,
    a.n,
    a.avg_date,
    a.var_date,
    a.stddev_date,
case
        when stddev_date = 0 then 0
        else (sum((v.date - a.avg_date) ^ 3) / n) / (stddev_date ^ 3)
    end skew_date,
case
        when stddev_date = 0 then 0
        else (sum((v.date - a.avg_date) ^ 4) / n) / (stddev_date ^ 4)
    end kurt_date,
    a.avg_clicks,
    a.var_clicks,
    a.stddev_clicks,
case
        when stddev_clicks = 0 then 0
        else (sum((v.sum_click - a.avg_clicks) ^ 3) / n) / (stddev_clicks ^ 3)
    end skew_clicks,
case
        when stddev_clicks = 0 then 0
        else (sum((v.sum_click - a.avg_clicks) ^ 4) / n) / (stddev_clicks ^ 4)
    end kurt_clicks,
case
        when n > 2 then (sqrt(n * (n - 1))) /(n - 2)
        else 1
    end fp_coeff
from agg.interaction_types_staging v
    join act a on a.student_id = v.student_id
    and a.activity_type_id = v.activity_type_id
where v.date <= 30
group by v.student_id,
    v.course_id,
    v.activity_type_id,
    a.n,
    a.avg_date,
    a.var_date,
    a.stddev_date,
    a.avg_clicks,
    a.var_clicks,
    a.stddev_clicks