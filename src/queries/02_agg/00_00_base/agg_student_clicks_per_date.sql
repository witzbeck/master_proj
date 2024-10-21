select v.course_id,
    v.module_id,
    v.presentation_id,
    b.student_id,
    b.date,
    sum(b.sum_click) sum_click,
    from main.student_vle_bridge b
    join main.vle_course_bridge v on b.site_id = v.site_id
group by v.course_id,
    v.module_id,
    v.presentation_id,
    b.student_id,
    b.date