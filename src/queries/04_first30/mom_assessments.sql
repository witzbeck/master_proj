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