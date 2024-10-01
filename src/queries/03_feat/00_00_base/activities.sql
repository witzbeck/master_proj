select
    r.student_id
    , r.n_max_revists
    , r.n_min_revists
    , r.n_sum_top_5_revists
    , r.avg_top_5_revists
    , r.n_top_days
    , a.n_times_accessed_dataplus
    , a.n_times_accessed_dualpane
    , a.n_times_accessed_externalquiz
    , a.n_times_accessed_folder
    , a.n_times_accessed_forumng
    , a.n_times_accessed_glossary
    , a.n_times_accessed_homepage
    , a.n_times_accessed_htmlactivity
    , a.n_times_accessed_oucollaborate
    , a.n_times_accessed_oucontent
    , a.n_times_accessed_ouelluminate
    , a.n_times_accessed_ouwiki
    , a.n_times_accessed_page
    , a.n_times_accessed_questionnaire
    , a.n_times_accessed_quiz
    , a.n_times_accessed_repeatactivity
    , a.n_times_accessed_resource
    , a.n_times_accessed_sharedsubpage
    , a.n_times_accessed_subpage
    , a.n_times_accessed_url
from agg.v_student_activity_revisits r
    join agg.v_interactions_times_accessed_activity a on a.student_id = r.student_id
;
select
    m.student_id
    , m.course_id
    , m.activity_type_id
    , m.n
    , m.avg_date
    , m.var_date
    , m.stddev_date
    , m.skew_date
    , m.kurt_date
    , m.avg_clicks
    , m.var_clicks
    , m.stddev_clicks
    , m.skew_clicks
    , m.kurt_clicks
    , m.fp_coeff
from agg.mom_1234_by_activity_type m
