select a.student_id,
    a.course_id,
    a.module_id,
    a.presentation_id,
    a.n_days,
    a.n_total_visits,
    a.n_total_clicks,
    a.n_activities,
    a.n_activity_types,
    a.avg_activities_per_day,
    a.avg_activity_types_per_day,
    a.avg_clicks_per_day,
    a.avg_clicks_per_visit,
    a.avg_visits_per_day,
    a.var_activities_per_day,
    a.var_activity_types_per_day,
    a.var_clicks_per_day,
    a.var_clicks_per_visit,
    a.var_visits_per_day,
    a.stddev_activities_per_day,
    a.stddev_activity_types_per_day,
    a.stddev_clicks_per_day,
    a.stddev_clicks_per_visit,
    a.stddev_visits_per_day,
case
        when stddev_activities_per_day = 0 then 0
        else (
            sum((a.n_activities - a.avg_activities_per_day) ^ 3) / a.n_days
        ) / (stddev_activities_per_day ^ 3)
    end skew_activities_per_day,
case
        when stddev_activity_types_per_day = 0 then 0
        else (
            sum(
                (
                    a.n_activity_types - a.avg_activity_types_per_day
                ) ^ 3
            ) / a.n_days
        ) / (stddev_activity_types_per_day ^ 3)
    end skew_activity_types_per_day,
case
        when stddev_clicks_per_day = 0 then 0
        else (
            sum((a.n_total_clicks - a.avg_clicks_per_day) ^ 3) / a.n_days
        ) / (stddev_clicks_per_day ^ 3)
    end skew_clicks_per_day,
case
        when stddev_clicks_per_visit = 0 then 0
        else (
            sum((a.n_total_clicks - a.avg_clicks_per_visit) ^ 3) / a.n_total_visits
        ) / (stddev_clicks_per_visit ^ 3)
    end skew_clicks_per_visit,
case
        when stddev_visits_per_day = 0 then 0
        else (
            sum((a.n_total_visits - a.avg_visits_per_day) ^ 3) / a.n_days
        ) / (stddev_visits_per_day ^ 3)
    end skew_visits_per_day,
case
        when stddev_activities_per_day = 0 then 0
        else (
            sum((a.n_activities - a.avg_activities_per_day) ^ 3) / a.n_days
        ) / (stddev_activities_per_day ^ 4)
    end kurt_activities_per_day,
case
        when stddev_activity_types_per_day = 0 then 0
        else (
            sum(
                (
                    a.n_activity_types - a.avg_activity_types_per_day
                ) ^ 3
            ) / a.n_days
        ) / (stddev_activity_types_per_day ^ 4)
    end kurt_activity_types_per_day,
case
        when stddev_clicks_per_day = 0 then 0
        else (
            sum((a.n_total_clicks - a.avg_clicks_per_day) ^ 3) / a.n_days
        ) / (stddev_clicks_per_day ^ 4)
    end kurt_clicks_per_day,
case
        when stddev_clicks_per_visit = 0 then 0
        else (
            sum((a.n_total_clicks - a.avg_clicks_per_visit) ^ 3) / a.n_total_visits
        ) / (stddev_clicks_per_visit ^ 4)
    end kurt_clicks_per_visit,
case
        when stddev_visits_per_day = 0 then 0
        else (
            sum((a.n_total_visits - a.avg_visits_per_day) ^ 3) / a.n_days
        ) / (stddev_visits_per_day ^ 4)
    end kurt_visits_per_day,
case
        when a.n_days > 2 then (sqrt(a.n_days * (a.n_days - 1))) / (a.n_days - 2)
        else 1
    end fp_coeff_days
from agg.mom_interactions_12 a
group by a.student_id,
    a.course_id,
    a.module_id,
    a.presentation_id,
    a.n_days,
    a.n_total_visits,
    a.n_total_clicks,
    a.n_activities,
    a.n_activity_types,
    a.avg_activities_per_day,
    a.avg_activity_types_per_day,
    a.avg_clicks_per_day,
    a.avg_clicks_per_visit,
    a.avg_visits_per_day,
    a.var_activities_per_day,
    a.var_activity_types_per_day,
    a.var_clicks_per_day,
    a.var_clicks_per_visit,
    a.var_visits_per_day,
    a.stddev_activities_per_day,
    a.stddev_activity_types_per_day,
    a.stddev_clicks_per_day,
    a.stddev_clicks_per_visit,
    a.stddev_visits_per_day