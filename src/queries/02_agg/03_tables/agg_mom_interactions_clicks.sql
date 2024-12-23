with avg as (
    select vis.student_id,
        count(*) n,
        cast(sum(vis.date) as float) / count(*) date,
        cast(sum(vis.sum_click) as float) / count(*) clicks
    from agg.vle_interactions_staging vis
    where date <= 30
    group by student_id
)
select avg.student_id,
    avg.n n,
    avg.date avg_date,
    sum((v.date - avg.date) ^ 2) / avg.n var_date,
    sqrt(sum((v.date - avg.date) ^ 2) / avg.n) stddev_date,
    avg.clicks avg_clicks,
    sum((v.sum_click - avg.clicks) ^ 2) / avg.n var_clicks,
    sqrt(sum((v.sum_click - avg.clicks) ^ 2) / avg.n) stddev_clicks
from agg.vle_interactions_staging v
    join avg on avg.student_id = v.student_id
where v.date <= 30
group by avg.student_id,
    avg.n,
    avg.date,
    avg.clicks