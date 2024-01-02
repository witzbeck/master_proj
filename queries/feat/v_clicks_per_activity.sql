create view feat.v_clicks_per_activity as
select
 vis.student_id
,vis.course_id
,vis.activity_type_id
,vis.site_id
,vis.date
,vis.sum_click
,vis.sum_click * vis.activity_type
,vis.sum_click * vis.is_dataplus           clicks_dataplus
,vis.sum_click * vis.is_dualpane           clicks_dualpane
,vis.sum_click * vis.is_externalquiz       clicks_externalquiz
,vis.sum_click * vis.is_folder             clicks_folder
,vis.sum_click * vis.is_forumng            clicks_forumng
,vis.sum_click * vis.is_glossary           clicks_glossary
,vis.sum_click * vis.is_homepage           clicks_homepage
,vis.sum_click * vis.is_htmlactivity       clicks_htmlactivity
,vis.sum_click * vis.is_oucollaborate      clicks_oucollaborate
,vis.sum_click * vis.is_oucontent          clicks_oucontent
,vis.sum_click * vis.is_ouelluminate       clicks_ouelluminate
,vis.sum_click * vis.is_ouwiki             clicks_ouwiki
,vis.sum_click * vis.is_page               clicks_page
,vis.sum_click * vis.is_questionnaire      clicks_questionnaire
,vis.sum_click * vis.is_quiz               clicks_quiz
,vis.sum_click * vis.is_repeatactivity     clicks_repeatactivity
,vis.sum_click * vis.is_resource           clicks_resource
,vis.sum_click * vis.is_sharedsubpage      clicks_sharedsubpage
,vis.sum_click * vis.is_subpage            clicks_subpage
,vis.sum_click * vis.is_url                clicks_url
from agg.vle_interactions_staging vis