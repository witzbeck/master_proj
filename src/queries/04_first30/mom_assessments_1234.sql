with ass as (
    with avg as (
        select s.student_id,
            count(*) n,
            cast(sum(s.days_before_due_submitted) as float) / count(*) days
        from agg.assessment_staging s
        where (
                date_due <= 30
                or date_submitted <= 30
            )
        group by student_id
    )
    select avg.student_id,
        avg.n n,
        avg.days avg_days,
        sum((s.days_before_due_submitted - avg.days) ^ 2) / avg.n var_days,
        sqrt(
            sum((s.days_before_due_submitted - avg.days) ^ 2) / avg.n
        ) stddev_days
    from agg.assessment_staging s
        join avg on avg.student_id = s.student_id
    where (
            date_due <= 30
            or date_submitted <= 30
        )
    group by avg.student_id,
        avg.n,
        avg.days
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
from agg.assessment_staging s
    join ass a on a.student_id = s.student_id
where (
        date_due <= 30
        or date_submitted <= 30
    )
group by s.student_id,
    a.n,
    a.avg_days,
    a.var_days,
    a.stddev_days