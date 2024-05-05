CREATE VIEW main.v_vle_activities AS
SELECT
    vcb.site_id,
    svb.student_id,
    c.module_id,
    c.presentation_id,
    at.id AS activity_type_id,
    c.module_code,
    c.presentation_code,
    at.activity_type,
    svb.date AS activity_date,
    svb.sum_click,
    CASE
        WHEN vcb.week_from IS NULL THEN 0
        ELSE 1 END AS has_date_range,
    vcb.week_from,
    vcb.week_to
FROM main.vle_course_bridge vcb
JOIN main.course_info c ON c.course_id = vcb.course_id
JOIN main.student_vle_bridge svb ON svb.site_id = vcb.site_id
JOIN main.activity_types at ON at.activity_type_id = vcb.activity_type_id;
;
