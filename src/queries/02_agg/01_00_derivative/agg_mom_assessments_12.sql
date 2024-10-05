with avg as (
    select s.student_id,
        count(*) AS n,
        cast(sum(s.days_before_due_submitted) as float) / count(*) AS days
    from main.assessment_staging s
    group by student_id
)
select avg.student_id,
    avg.n AS n,
    avg.days AS avg_days,
    sum((s.days_before_due_submitted - avg.days) ^ 2) / avg.n AS var_days,
    sqrt(
        sum((s.days_before_due_submitted - avg.days) ^ 2) / avg.n
    ) AS stddev_days
from main.assessment_staging s
    join avg on avg.student_id = s.student_id
group by avg.student_id,
    avg.n,
    avg.days