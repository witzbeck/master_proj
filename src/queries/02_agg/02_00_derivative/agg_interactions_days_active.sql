select
    vis.student_id

    , sum(vis.sum_click * vis.is_dataplus) n_clicks_dataplus
    , sum(vis.sum_click * vis.is_dualpane) n_clicks_dualpane
    , sum(vis.sum_click * vis.is_externalquiz) n_clicks_externalquiz
    , sum(vis.sum_click * vis.is_folder) n_clicks_folder
    , sum(vis.sum_click * vis.is_forumng) n_clicks_forumng
    , sum(vis.sum_click * vis.is_glossary) n_clicks_glossary
    , sum(vis.sum_click * vis.is_homepage) n_clicks_homepage
    , sum(vis.sum_click * vis.is_htmlactivity) n_clicks_htmlactivity
    , sum(vis.sum_click * vis.is_oucollaborate) n_clicks_oucollaborate
    , sum(vis.sum_click * vis.is_oucontent) n_clicks_oucontent
    , sum(vis.sum_click * vis.is_ouelluminate) n_clicks_ouelluminate
    , sum(vis.sum_click * vis.is_ouwiki) n_clicks_ouwiki
    , sum(vis.sum_click * vis.is_page) n_clicks_page
    , sum(vis.sum_click * vis.is_questionnaire) n_clicks_questionnaire
    , sum(vis.sum_click * vis.is_quiz) n_clicks_quiz
    , sum(vis.sum_click * vis.is_repeatactivity) n_clicks_repeatactivity
    , sum(vis.sum_click * vis.is_resource) n_clicks_resource
    , sum(vis.sum_click * vis.is_sharedsubpage) n_clicks_sharedsubpage
    , sum(vis.sum_click * vis.is_subpage) n_clicks_subpage
    , sum(vis.sum_click * vis.is_url) n_clicks_url
from agg.interaction_types_staging vis
group by student_id
