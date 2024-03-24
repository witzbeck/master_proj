SELECT

    b.student_id
    , v.course_id
    , b.date
    , sum(b.sum_click) total_clicks

INTO first30.clicks_per_date
FROM main.student_vle_bridge b
    JOIN main.vle_course_bridge v ON b.site_id = v.site_id
    JOIN main.v_activity_types_onehot o ON o.id = v.activity_type_id
WHERE b.date <= 30
GROUP BY
    b.student_id
    , v.course_id
    , b.date
