with is_5th_perc as (
    select p.course_id,
        p.site_id,
        case
            when p.total_visits_percentile < 6 then 1
            else 0
        end is_5th_perc_visits,
        case
            when p.total_clicks_percentile < 6 then 1
            else 0
        end is_5th_perc_clicks
    from agg.activity_interaction_percentiles p
    where (
            p.total_clicks_percentile < 6
            or p.total_visits_percentile < 6
        )
)
select f.course_id,
    coalesce(
        sum(
            case
                when is_5th_perc_clicks = 1 then f.n_total_clicks
                else 0
            end
        ),
        0
    ) n_total_clicks_by_top_5th_clicks,
    coalesce(
        sum(
            case
                when is_5th_perc_clicks = 1 then f.n_total_visits
                else 0
            end
        ),
        0
    ) n_total_clicks_by_top_5th_visits,
    coalesce(
        sum(
            case
                when is_5th_perc_visits = 1 then f.n_total_clicks
                else 0
            end
        ),
        0
    ) n_total_visits_by_top_5th_clicks,
    coalesce(
        sum(
            case
                when is_5th_perc_visits = 1 then f.n_total_visits
                else 0
            end
        ),
        0
    ) n_total_visits_by_top_5th_visits,
    coalesce(sum(p.is_5th_perc_clicks), 0) n_distinct_top_5th_by_clicks,
    coalesce(sum(p.is_5th_perc_visits), 0) n_distinct_top_5th_by_visits
from agg.activity_interaction_percentiles f
    left join is_5th_perc p on p.course_id = f.course_id
    and p.site_id = f.site_id
group by f.course_id
order by f.course_id