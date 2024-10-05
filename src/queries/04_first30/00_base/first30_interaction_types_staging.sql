SELECT
    b.student_id
    , v.course_id
    , v.activity_type_id
    , v.site_id
    , b.date
    , b.sum_click
    , o.activity_type
    , o.is_dataplus
    , o.is_dualpane
    , o.is_externalquiz
    , o.is_folder
    , o.is_forumng
    , o.is_glossary
    , o.is_homepage
    , o.is_htmlactivity
    , o.is_oucollaborate
    , o.is_oucontent
    , o.is_ouelluminate
    , o.is_ouwiki
    , o.is_page
    , o.is_questionnaire
    , o.is_quiz
    , o.is_repeatactivity
    , o.is_resource
    , o.is_sharedsubpage
    , o.is_subpage
    , o.is_url
FROM main.student_vle_bridge b
    JOIN main.vle_course_bridge v ON b.site_id = v.site_id
    JOIN main.v_activity_types_onehot o ON o.id = v.activity_type_id
WHERE b.date <= 30
