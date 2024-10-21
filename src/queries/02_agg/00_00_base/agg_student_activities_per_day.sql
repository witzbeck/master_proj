SELECT b.student_id,
    v.course_id,
    b.date,
    count(DISTINCT v.activity_type_id) n_activity_types,
    count(DISTINCT v.site_id) n_activities,
    sum(b.sum_click) sum_click,
    sum(b.sum_click) / count(DISTINCT v.activity_type_id) avg_clicks_per_activity_type,
    sum(b.sum_click) / count(DISTINCT v.site_id) avg_clicks_per_activity
FROM main.student_vle_bridge b
    JOIN main.vle_course_bridge v ON b.site_id = v.site_id
GROUP BY b.student_id,
    v.course_id,
    b.date