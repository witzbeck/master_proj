with avg as (
    SELECT b.student_id,
        v.course_id,
        v.module_id,
        v.presentation_id,
        count(DISTINCT b.date) n_days,
        count(DISTINCT v.site_id) n_activities,
        count(DISTINCT v.activity_type_id) n_activity_types,
        count(*) n_total_visits,
        sum(b.sum_click) n_total_clicks,
        sum(cast(b.sum_click as float)) / count(DISTINCT b.date) avg_clicks_per_day,
        cast(count(DISTINCT v.site_id) as float) / count(DISTINCT b.date) avg_activities_per_day,
        cast(count(DISTINCT v.activity_type_id) as float) / count(DISTINCT b.date) avg_activity_types_per_day,
        sum(cast(b.sum_click as float)) / count(*) avg_clicks_per_visit,
        cast(count(DISTINCT b.date) as float) / count(*) avg_visits_per_day
    FROM main.student_vle_bridge b
        JOIN main.vle_course_bridge v on b.site_id = v.site_id
    group by b.student_id,
        v.course_id,
        v.module_id,
        v.presentation_id
)
select avg.student_id,
    avg.course_id,
    avg.module_id,
    avg.presentation_id,
    avg.n_days,
    avg.n_total_visits,
    avg.n_total_clicks,
    avg.n_activities,
    avg.avg_activities_per_day,
    sum(avg.avg_activities_per_day - avg.n_activities) ^ 2 / avg.n_days var_activities_per_day,
    sqrt(
        sum(avg.avg_activities_per_day - avg.n_activities) ^ 2 / avg.n_days
    ) stddev_activities_per_day -- noqa
,
    avg.n_activity_types,
    avg.avg_activity_types_per_day,
    sum(
        avg.avg_activity_types_per_day - avg.n_activity_types
    ) ^ 2 / avg.n_days var_activity_types_per_day,
    sqrt(
        sum(
            avg.avg_activity_types_per_day - avg.n_activity_types
        ) ^ 2 / avg.n_days
    ) stddev_activity_types_per_day -- noqa
,
    avg.avg_clicks_per_day,
    sum(avg.avg_clicks_per_day - avg.n_total_clicks) ^ 2 / avg.n_days var_clicks_per_day,
    sqrt(
        sum(avg.avg_clicks_per_day - avg.n_total_clicks) ^ 2 / avg.n_days
    ) stddev_clicks_per_day -- noqa
,
    avg.avg_clicks_per_visit,
    sum(avg.avg_clicks_per_visit - avg.n_total_visits) ^ 2 / avg.n_total_visits var_clicks_per_visit,
    sqrt(
        sum(avg.avg_clicks_per_visit - avg.n_total_visits) ^ 2 / avg.n_total_visits
    ) stddev_clicks_per_visit -- noqa
,
    avg.avg_visits_per_day,
    sum(avg.avg_visits_per_day - avg.n_days) ^ 2 / avg.n_days var_visits_per_day,
    sqrt(
        sum(avg.avg_visits_per_day - avg.n_days) ^ 2 / avg.n_days
    ) stddev_visits_per_day -- noqa
from avg
group by avg.student_id,
    avg.course_id,
    avg.module_id,
    avg.presentation_id,
    avg.n_days,
    avg.n_total_visits,
    avg.n_total_clicks,
    avg.n_activities,
    avg.n_activity_types,
    avg.avg_activities_per_day,
    avg.avg_activity_types_per_day,
    avg.avg_clicks_per_day,
    avg.avg_clicks_per_visit,
    avg.avg_visits_per_day