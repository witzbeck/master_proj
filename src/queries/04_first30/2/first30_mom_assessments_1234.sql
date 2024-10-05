with ass as (
    select s.student_id,
        s.n,
        s.avg_days,
        s.var_days,
        s.stddev_days
    from agg.mom_assessments_12 s
)
select s.student_id,
    a.n,
    a.avg_days,
    a.var_days,
    a.stddev_days,
case
        when stddev_days = 0 then 0
        else (
            sum((s.days_before_due_submitted - a.avg_days) ^ 3) / a.n
        ) / (stddev_days ^ 3)
    end skew_days,
case
        when stddev_days = 0 then 0
        else (
            sum((s.days_before_due_submitted - a.avg_days) ^ 4) / a.n
        ) / (stddev_days ^ 4)
    end kurt_days,
case
        when a.n > 2 then (sqrt(a.n * (a.n - 1))) /(a.n - 2)
        else 1
    end fp_coeff into first30.mom_assessments_1234
from main.v_assessment_staging s
    join ass a on a.student_id = s.student_id
where (
        s.date_due <= 30
        or s.date_submitted <= 30
    )
group by s.student_id,
    a.n,
    a.avg_days,
    a.var_days,
    a.stddev_days