select v.course_id,
    v.module_id,
    v.presentation_id,
    v.site_id,
    v.activity_type_id,
    count(distinct b.date) n_distinct_visits,
    count(*) n_total_visits,
    sum(b.sum_click) n_total_clicks,
    sum(cast(b.sum_click as float)) / count(distinct b.date) avg_clicks_per_day,
    sum(cast(b.sum_click as float)) / count(*) avg_clicks_per_visit
from main.student_vle_bridge b
    join main.vle_course_bridge v on b.site_id = v.site_id
group by v.course_id,
    v.module_id,
    v.presentation_id,
    v.site_id,
    v.activity_type_id