select
    mit1.student_id
    , mit1.n_total_clicks n_interactions
    , mit1.n_days
    , mit1.n_activities
    , mit1.avg_activities_per_day
    , mit1.var_activities_per_day
    , mit1.stddev_activities_per_day
    , mit1.skew_activities
    , mit1.kurt_activities
    , mit1.n_activity_types
    , mit1.avg_activity_types_per_day
    , mit1.var_activity_types_per_day
    , mit1.stddev_activity_types_per_day
    , mit1.skew_activity_types
    , mit1.kurt_activity_types
    , mit1.n_total_clicks
    , mit1.avg_clicks_per_day
    , mit1.var_clicks_per_day
    , mit1.stddev_clicks_per_day
    , skew_clicks_per_day
    , kurt_clicks_per_day
    , mit1.n_total_visits
    , mit1.avg_clicks_per_visit
    , mit1.var_clicks_per_visit
    , mit1.stddev_clicks_per_visit
    , mit1.skew_clicks_per_visit
    , mit1.kurt_clicks_per_visit
    , mit1.avg_visits_per_day
    , mit1.var_visits_per_day
    , mit1.stddev_visits_per_day
    , mit1.skew_date_visits_per_day
    , mit1.kurt_date_visits_per_day
    , mit1.fp_coeff_clicks
    , mit1.fp_coeff_visits
    , coalesce(ma1.n, 0) n_assessments
    , coalesce(ma1.avg_days, 0) avg_days_before_due_submitted
    , coalesce(ma1.var_days, 0) var_days_before_due_submitted
    , coalesce(ma1.stddev_days, 0) stddev_days_before_due_submitted
    , coalesce(ma1.skew_days, 0) skew_days_before_due_submitted
    , coalesce(ma1.kurt_days, 0) kurt_days_before_due_submitted
    , coalesce(ma1.fp_coeff, 0) fp_coeff_assessments
    , coalesce(mipt1p.dataplus_n, 0) dataplus_n
    , coalesce(mipt1p.dataplus_avg_date, 0) dataplus_avg_date
    , coalesce(mipt1p.dataplus_var_date, 0) dataplus_var_date
    , coalesce(mipt1p.dataplus_stddev_date, 0) dataplus_stddev_date
    , coalesce(mipt1p.dataplus_skew_date, 0) dataplus_skew_date
    , coalesce(mipt1p.dataplus_kurt_date, 0) dataplus_kurt_date
    , coalesce(mipt1p.dataplus_avg_clicks, 0) dataplus_avg_clicks
    , coalesce(mipt1p.dataplus_var_clicks, 0) dataplus_var_clicks
    , coalesce(mipt1p.dataplus_stddev_clicks, 0) dataplus_stddev_clicks
    , coalesce(mipt1p.dataplus_skew_clicks, 0) dataplus_skew_clicks
    , coalesce(mipt1p.dataplus_kurt_clicks, 0) dataplus_kurt_clicks
    , coalesce(mipt1p.dataplus_fp_coeff, 0) dataplus_fp_coeff
    , coalesce(mipt1p.dualpane_n, 0) dualpane_n
    , coalesce(mipt1p.dualpane_avg_date, 0) dualpane_avg_date
    , coalesce(mipt1p.dualpane_var_date, 0) dualpane_var_date
    , coalesce(mipt1p.dualpane_stddev_date, 0) dualpane_stddev_date
    , coalesce(mipt1p.dualpane_skew_date, 0) dualpane_skew_date
    , coalesce(mipt1p.dualpane_kurt_date, 0) dualpane_kurt_date
    , coalesce(mipt1p.dualpane_avg_clicks, 0) dualpane_avg_clicks
    , coalesce(mipt1p.dualpane_var_clicks, 0) dualpane_var_clicks
    , coalesce(mipt1p.dualpane_stddev_clicks, 0) dualpane_stddev_clicks
    , coalesce(mipt1p.dualpane_skew_clicks, 0) dualpane_skew_clicks
    , coalesce(mipt1p.dualpane_kurt_clicks, 0) dualpane_kurt_clicks
    , coalesce(mipt1p.dualpane_fp_coeff, 0) dualpane_fp_coeff
    , coalesce(mipt1p.folder_n, 0) folder_n
    , coalesce(mipt1p.folder_avg_date, 0) folder_avg_date
    , coalesce(mipt1p.folder_var_date, 0) folder_var_date
    , coalesce(mipt1p.folder_stddev_date, 0) folder_stddev_date
    , coalesce(mipt1p.folder_skew_date, 0) folder_skew_date
    , coalesce(mipt1p.folder_kurt_date, 0) folder_kurt_date
    , coalesce(mipt1p.folder_avg_clicks, 0) folder_avg_clicks
    , coalesce(mipt1p.folder_var_clicks, 0) folder_var_clicks
    , coalesce(mipt1p.folder_stddev_clicks, 0) folder_stddev_clicks
    , coalesce(mipt1p.folder_skew_clicks, 0) folder_skew_clicks
    , coalesce(mipt1p.folder_kurt_clicks, 0) folder_kurt_clicks
    , coalesce(mipt1p.folder_fp_coeff, 0) folder_fp_coeff
    , coalesce(mipt1p.forumng_n, 0) forumng_n
    , coalesce(mipt1p.forumng_avg_date, 0) forumng_avg_date
    , coalesce(mipt1p.forumng_var_date, 0) forumng_var_date
    , coalesce(mipt1p.forumng_stddev_date, 0) forumng_stddev_date
    , coalesce(mipt1p.forumng_skew_date, 0) forumng_skew_date
    , coalesce(mipt1p.forumng_kurt_date, 0) forumng_kurt_date
    , coalesce(mipt1p.forumng_avg_clicks, 0) forumng_avg_clicks
    , coalesce(mipt1p.forumng_var_clicks, 0) forumng_var_clicks
    , coalesce(mipt1p.forumng_stddev_clicks, 0) forumng_stddev_clicks
    , coalesce(mipt1p.forumng_skew_clicks, 0) forumng_skew_clicks
    , coalesce(mipt1p.forumng_kurt_clicks, 0) forumng_kurt_clicks
    , coalesce(mipt1p.forumng_fp_coeff, 0) forumng_fp_coeff
    , coalesce(mipt1p.glossary_n, 0) glossary_n
    , coalesce(mipt1p.glossary_avg_date, 0) glossary_avg_date
    , coalesce(mipt1p.glossary_var_date, 0) glossary_var_date
    , coalesce(mipt1p.glossary_stddev_date, 0) glossary_stddev_date
    , coalesce(mipt1p.glossary_skew_date, 0) glossary_skew_date
    , coalesce(mipt1p.glossary_kurt_date, 0) glossary_kurt_date
    , coalesce(mipt1p.glossary_avg_clicks, 0) glossary_avg_clicks
    , coalesce(mipt1p.glossary_var_clicks, 0) glossary_var_clicks
    , coalesce(mipt1p.glossary_stddev_clicks, 0) glossary_stddev_clicks
    , coalesce(mipt1p.glossary_skew_clicks, 0) glossary_skew_clicks
    , coalesce(mipt1p.glossary_kurt_clicks, 0) glossary_kurt_clicks
    , coalesce(mipt1p.glossary_fp_coeff, 0) glossary_fp_coeff
    , coalesce(mipt1p.homepage_n, 0) homepage_n
    , coalesce(mipt1p.homepage_avg_date, 0) homepage_avg_date
    , coalesce(mipt1p.homepage_var_date, 0) homepage_var_date
    , coalesce(mipt1p.homepage_stddev_date, 0) homepage_stddev_date
    , coalesce(mipt1p.homepage_skew_date, 0) homepage_skew_date
    , coalesce(mipt1p.homepage_kurt_date, 0) homepage_kurt_date
    , coalesce(mipt1p.homepage_avg_clicks, 0) homepage_avg_clicks
    , coalesce(mipt1p.homepage_var_clicks, 0) homepage_var_clicks
    , coalesce(mipt1p.homepage_stddev_clicks, 0) homepage_stddev_clicks
    , coalesce(mipt1p.homepage_skew_clicks, 0) homepage_skew_clicks
    , coalesce(mipt1p.homepage_kurt_clicks, 0) homepage_kurt_clicks
    , coalesce(mipt1p.homepage_fp_coeff, 0) homepage_fp_coeff
    , coalesce(mipt1p.html_activity_n, 0) html_activity_n
    , coalesce(mipt1p.html_activity_avg_date, 0) html_activity_avg_date
    , coalesce(mipt1p.html_activity_var_date, 0) html_activity_var_date
    , coalesce(mipt1p.html_activity_stddev_date, 0) html_activity_stddev_date
    , coalesce(mipt1p.html_activity_skew_date, 0) html_activity_skew_date
    , coalesce(mipt1p.html_activity_kurt_date, 0) html_activity_kurt_date
    , coalesce(mipt1p.html_activity_avg_clicks, 0) html_activity_avg_clicks
    , coalesce(mipt1p.html_activity_var_clicks, 0) html_activity_var_clicks
    , coalesce(mipt1p.html_activity_stddev_clicks, 0) html_activity_stddev_clicks
    , coalesce(mipt1p.html_activity_skew_clicks, 0) html_activity_skew_clicks
    , coalesce(mipt1p.html_activity_kurt_clicks, 0) html_activity_kurt_clicks
    , coalesce(mipt1p.html_activity_fp_coeff, 0) html_activity_fp_coeff
    , coalesce(mipt1p.oucollaborate_n, 0) oucollaborate_n
    , coalesce(mipt1p.oucollaborate_avg_date, 0) oucollaborate_avg_date
    , coalesce(mipt1p.oucollaborate_var_date, 0) oucollaborate_var_date
    , coalesce(mipt1p.oucollaborate_stddev_date, 0) oucollaborate_stddev_date
    , coalesce(mipt1p.oucollaborate_skew_date, 0) oucollaborate_skew_date
    , coalesce(mipt1p.oucollaborate_kurt_date, 0) oucollaborate_kurt_date
    , coalesce(mipt1p.oucollaborate_avg_clicks, 0) oucollaborate_avg_clicks
    , coalesce(mipt1p.oucollaborate_var_clicks, 0) oucollaborate_var_clicks
    , coalesce(mipt1p.oucollaborate_stddev_clicks, 0) oucollaborate_stddev_clicks
    , coalesce(mipt1p.oucollaborate_skew_clicks, 0) oucollaborate_skew_clicks
    , coalesce(mipt1p.oucollaborate_kurt_clicks, 0) oucollaborate_kurt_clicks
    , coalesce(mipt1p.oucollaborate_fp_coeff, 0) oucollaborate_fp_coeff
    , coalesce(mipt1p.oucontent_n, 0) oucontent_n
    , coalesce(mipt1p.oucontent_avg_date, 0) oucontent_avg_date
    , coalesce(mipt1p.oucontent_var_date, 0) oucontent_var_date
    , coalesce(mipt1p.oucontent_stddev_date, 0) oucontent_stddev_date
    , coalesce(mipt1p.oucontent_skew_date, 0) oucontent_skew_date
    , coalesce(mipt1p.oucontent_kurt_date, 0) oucontent_kurt_date
    , coalesce(mipt1p.oucontent_avg_clicks, 0) oucontent_avg_clicks
    , coalesce(mipt1p.oucontent_var_clicks, 0) oucontent_var_clicks
    , coalesce(mipt1p.oucontent_stddev_clicks, 0) oucontent_stddev_clicks
    , coalesce(mipt1p.oucontent_skew_clicks, 0) oucontent_skew_clicks
    , coalesce(mipt1p.oucontent_kurt_clicks, 0) oucontent_kurt_clicks
    , coalesce(mipt1p.oucontent_fp_coeff, 0) oucontent_fp_coeff
    , coalesce(mipt1p.ouelluminate_n, 0) ouelluminate_n
    , coalesce(mipt1p.ouelluminate_avg_date, 0) ouelluminate_avg_date
    , coalesce(mipt1p.ouelluminate_var_date, 0) ouelluminate_var_date
    , coalesce(mipt1p.ouelluminate_stddev_date, 0) ouelluminate_stddev_date
    , coalesce(mipt1p.ouelluminate_skew_date, 0) ouelluminate_skew_date
    , coalesce(mipt1p.ouelluminate_kurt_date, 0) ouelluminate_kurt_date
    , coalesce(mipt1p.ouelluminate_avg_clicks, 0) ouelluminate_avg_clicks
    , coalesce(mipt1p.ouelluminate_var_clicks, 0) ouelluminate_var_clicks
    , coalesce(mipt1p.ouelluminate_stddev_clicks, 0) ouelluminate_stddev_clicks
    , coalesce(mipt1p.ouelluminate_skew_clicks, 0) ouelluminate_skew_clicks
    , coalesce(mipt1p.ouelluminate_kurt_clicks, 0) ouelluminate_kurt_clicks
    , coalesce(mipt1p.ouelluminate_fp_coeff, 0) ouelluminate_fp_coeff
    , coalesce(mipt1p.ouwiki_n, 0) ouwiki_n
    , coalesce(mipt1p.ouwiki_avg_date, 0) ouwiki_avg_date
    , coalesce(mipt1p.ouwiki_var_date, 0) ouwiki_var_date
    , coalesce(mipt1p.ouwiki_stddev_date, 0) ouwiki_stddev_date
    , coalesce(mipt1p.ouwiki_skew_date, 0) ouwiki_skew_date
    , coalesce(mipt1p.ouwiki_kurt_date, 0) ouwiki_kurt_date
    , coalesce(mipt1p.ouwiki_avg_clicks, 0) ouwiki_avg_clicks
    , coalesce(mipt1p.ouwiki_var_clicks, 0) ouwiki_var_clicks
    , coalesce(mipt1p.ouwiki_stddev_clicks, 0) ouwiki_stddev_clicks
    , coalesce(mipt1p.ouwiki_skew_clicks, 0) ouwiki_skew_clicks
    , coalesce(mipt1p.ouwiki_kurt_clicks, 0) ouwiki_kurt_clicks
    , coalesce(mipt1p.ouwiki_fp_coeff, 0) ouwiki_fp_coeff
    , coalesce(mipt1p.page_n, 0) page_n
    , coalesce(mipt1p.page_avg_date, 0) page_avg_date
    , coalesce(mipt1p.page_var_date, 0) page_var_date
    , coalesce(mipt1p.page_stddev_date, 0) page_stddev_date
    , coalesce(mipt1p.page_skew_date, 0) page_skew_date
    , coalesce(mipt1p.page_kurt_date, 0) page_kurt_date
    , coalesce(mipt1p.page_avg_clicks, 0) page_avg_clicks
    , coalesce(mipt1p.page_var_clicks, 0) page_var_clicks
    , coalesce(mipt1p.page_stddev_clicks, 0) page_stddev_clicks
    , coalesce(mipt1p.page_skew_clicks, 0) page_skew_clicks
    , coalesce(mipt1p.page_kurt_clicks, 0) page_kurt_clicks
    , coalesce(mipt1p.page_fp_coeff, 0) page_fp_coeff
    , coalesce(mipt1p.questionnaire_n, 0) questionnaire_n
    , coalesce(mipt1p.questionnaire_avg_date, 0) questionnaire_avg_date
    , coalesce(mipt1p.questionnaire_var_date, 0) questionnaire_var_date
    , coalesce(mipt1p.questionnaire_stddev_date, 0) questionnaire_stddev_date
    , coalesce(mipt1p.questionnaire_skew_date, 0) questionnaire_skew_date
    , coalesce(mipt1p.questionnaire_kurt_date, 0) questionnaire_kurt_date
    , coalesce(mipt1p.questionnaire_avg_clicks, 0) questionnaire_avg_clicks
    , coalesce(mipt1p.questionnaire_var_clicks, 0) questionnaire_var_clicks
    , coalesce(mipt1p.questionnaire_stddev_clicks, 0) questionnaire_stddev_clicks
    , coalesce(mipt1p.questionnaire_skew_clicks, 0) questionnaire_skew_clicks
    , coalesce(mipt1p.questionnaire_kurt_clicks, 0) questionnaire_kurt_clicks
    , coalesce(mipt1p.questionnaire_fp_coeff, 0) questionnaire_fp_coeff
    , coalesce(mipt1p.externalquiz_n, 0) externalquiz_n
    , coalesce(mipt1p.externalquiz_avg_date, 0) externalquiz_avg_date
    , coalesce(mipt1p.externalquiz_var_date, 0) externalquiz_var_date
    , coalesce(mipt1p.externalquiz_stddev_date, 0) externalquiz_stddev_date
    , coalesce(mipt1p.externalquiz_skew_date, 0) externalquiz_skew_date
    , coalesce(mipt1p.externalquiz_kurt_date, 0) externalquiz_kurt_date
    , coalesce(mipt1p.externalquiz_avg_clicks, 0) externalquiz_avg_clicks
    , coalesce(mipt1p.externalquiz_var_clicks, 0) externalquiz_var_clicks
    , coalesce(mipt1p.externalquiz_stddev_clicks, 0) externalquiz_stddev_clicks
    , coalesce(mipt1p.externalquiz_skew_clicks, 0) externalquiz_skew_clicks
    , coalesce(mipt1p.externalquiz_kurt_clicks, 0) externalquiz_kurt_clicks
    , coalesce(mipt1p.externalquiz_fp_coeff, 0) externalquiz_fp_coeff
    , coalesce(mipt1p.quiz_n, 0) quiz_n
    , coalesce(mipt1p.quiz_avg_date, 0) quiz_avg_date
    , coalesce(mipt1p.quiz_var_date, 0) quiz_var_date
    , coalesce(mipt1p.quiz_stddev_date, 0) quiz_stddev_date
    , coalesce(mipt1p.quiz_skew_date, 0) quiz_skew_date
    , coalesce(mipt1p.quiz_kurt_date, 0) quiz_kurt_date
    , coalesce(mipt1p.quiz_avg_clicks, 0) quiz_avg_clicks
    , coalesce(mipt1p.quiz_var_clicks, 0) quiz_var_clicks
    , coalesce(mipt1p.quiz_stddev_clicks, 0) quiz_stddev_clicks
    , coalesce(mipt1p.quiz_skew_clicks, 0) quiz_skew_clicks
    , coalesce(mipt1p.quiz_kurt_clicks, 0) quiz_kurt_clicks
    , coalesce(mipt1p.quiz_fp_coeff, 0) quiz_fp_coeff
    , coalesce(mipt1p.repeatactivity_n, 0) repeatactivity_n
    , coalesce(mipt1p.repeatactivity_avg_date, 0) repeatactivity_avg_date
    , coalesce(mipt1p.repeatactivity_var_date, 0) repeatactivity_var_date
    , coalesce(mipt1p.repeatactivity_stddev_date, 0) repeatactivity_stddev_date
    , coalesce(mipt1p.repeatactivity_skew_date, 0) repeatactivity_skew_date
    , coalesce(mipt1p.repeatactivity_kurt_date, 0) repeatactivity_kurt_date
    , coalesce(mipt1p.repeatactivity_avg_clicks, 0) repeatactivity_avg_clicks
    , coalesce(mipt1p.repeatactivity_var_clicks, 0) repeatactivity_var_clicks
    , coalesce(mipt1p.repeatactivity_stddev_clicks, 0) repeatactivity_stddev_clicks
    , coalesce(mipt1p.repeatactivity_skew_clicks, 0) repeatactivity_skew_clicks
    , coalesce(mipt1p.repeatactivity_kurt_clicks, 0) repeatactivity_kurt_clicks
    , coalesce(mipt1p.repeatactivity_fp_coeff, 0) repeatactivity_fp_coeff
    , coalesce(mipt1p.resource_n, 0) resource_n
    , coalesce(mipt1p.resource_avg_date, 0) resource_avg_date
    , coalesce(mipt1p.resource_var_date, 0) resource_var_date
    , coalesce(mipt1p.resource_stddev_date, 0) resource_stddev_date
    , coalesce(mipt1p.resource_skew_date, 0) resource_skew_date
    , coalesce(mipt1p.resource_kurt_date, 0) resource_kurt_date
    , coalesce(mipt1p.resource_avg_clicks, 0) resource_avg_clicks
    , coalesce(mipt1p.resource_var_clicks, 0) resource_var_clicks
    , coalesce(mipt1p.resource_stddev_clicks, 0) resource_stddev_clicks
    , coalesce(mipt1p.resource_skew_clicks, 0) resource_skew_clicks
    , coalesce(mipt1p.resource_kurt_clicks, 0) resource_kurt_clicks
    , coalesce(mipt1p.resource_fp_coeff, 0) resource_fp_coeff
    , coalesce(mipt1p.sharedsubpage_n, 0) sharedsubpage_n
    , coalesce(mipt1p.sharedsubpage_avg_date, 0) sharedsubpage_avg_date
    , coalesce(mipt1p.sharedsubpage_var_date, 0) sharedsubpage_var_date
    , coalesce(mipt1p.sharedsubpage_stddev_date, 0) sharedsubpage_stddev_date
    , coalesce(mipt1p.sharedsubpage_skew_date, 0) sharedsubpage_skew_date
    , coalesce(mipt1p.sharedsubpage_kurt_date, 0) sharedsubpage_kurt_date
    , coalesce(mipt1p.sharedsubpage_avg_clicks, 0) sharedsubpage_avg_clicks
    , coalesce(mipt1p.sharedsubpage_var_clicks, 0) sharedsubpage_var_clicks
    , coalesce(mipt1p.sharedsubpage_stddev_clicks, 0) sharedsubpage_stddev_clicks
    , coalesce(mipt1p.sharedsubpage_skew_clicks, 0) sharedsubpage_skew_clicks
    , coalesce(mipt1p.sharedsubpage_kurt_clicks, 0) sharedsubpage_kurt_clicks
    , coalesce(mipt1p.sharedsubpage_fp_coeff, 0) sharedsubpage_fp_coeff
    , coalesce(mipt1p.subpage_n, 0) subpage_n
    , coalesce(mipt1p.subpage_avg_date, 0) subpage_avg_date
    , coalesce(mipt1p.subpage_var_date, 0) subpage_var_date
    , coalesce(mipt1p.subpage_stddev_date, 0) subpage_stddev_date
    , coalesce(mipt1p.subpage_skew_date, 0) subpage_skew_date
    , coalesce(mipt1p.subpage_kurt_date, 0) subpage_kurt_date
    , coalesce(mipt1p.subpage_avg_clicks, 0) subpage_avg_clicks
    , coalesce(mipt1p.subpage_var_clicks, 0) subpage_var_clicks
    , coalesce(mipt1p.subpage_stddev_clicks, 0) subpage_stddev_clicks
    , coalesce(mipt1p.subpage_skew_clicks, 0) subpage_skew_clicks
    , coalesce(mipt1p.subpage_kurt_clicks, 0) subpage_kurt_clicks
    , coalesce(mipt1p.subpage_fp_coeff, 0) subpage_fp_coeff
    , coalesce(mipt1p.url_n, 0) url_n
    , coalesce(mipt1p.url_avg_date, 0) url_avg_date
    , coalesce(mipt1p.url_var_date, 0) url_var_date
    , coalesce(mipt1p.url_stddev_date, 0) url_stddev_date
    , coalesce(mipt1p.url_skew_date, 0) url_skew_date
    , coalesce(mipt1p.url_kurt_date, 0) url_kurt_date
    , coalesce(mipt1p.url_avg_clicks, 0) url_avg_clicks
    , coalesce(mipt1p.url_var_clicks, 0) url_var_clicks
    , coalesce(mipt1p.url_stddev_clicks, 0) url_stddev_clicks
    , coalesce(mipt1p.url_skew_clicks, 0) url_skew_clicks
    , coalesce(mipt1p.url_kurt_clicks, 0) url_kurt_clicks
    , coalesce(mipt1p.url_fp_coeff, 0) url_fp_coeff
from first30.mom_interactions_1234 mit1
    left join first30.mom_assessments_1234 ma1 on ma1.student_id = mit1.student_id
    left join first30.mom_interactions_per_type_1234_pivot mipt1p on mipt1p.student_id = mit1.student_id
