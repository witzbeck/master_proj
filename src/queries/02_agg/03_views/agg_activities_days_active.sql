select vis.student_id,
    sum(vis.is_dataplus) n_times_accessed_dataplus,
    sum(vis.is_dualpane) n_times_accessed_dualpane,
    sum(vis.is_externalquiz) n_times_accessed_externalquiz,
    sum(vis.is_folder) n_times_accessed_folder,
    sum(vis.is_forumng) n_times_accessed_forumng,
    sum(vis.is_glossary) n_times_accessed_glossary,
    sum(vis.is_homepage) n_times_accessed_homepage,
    sum(vis.is_htmlactivity) n_times_accessed_htmlactivity,
    sum(vis.is_oucollaborate) n_times_accessed_oucollaborate,
    sum(vis.is_oucontent) n_times_accessed_oucontent,
    sum(vis.is_ouelluminate) n_times_accessed_ouelluminate,
    sum(vis.is_ouwiki) n_times_accessed_ouwiki,
    sum(vis.is_page) n_times_accessed_page,
    sum(vis.is_questionnaire) n_times_accessed_questionnaire,
    sum(vis.is_quiz) n_times_accessed_quiz,
    sum(vis.is_repeatactivity) n_times_accessed_repeatactivity,
    sum(vis.is_resource) n_times_accessed_resource,
    sum(vis.is_sharedsubpage) n_times_accessed_sharedsubpage,
    sum(vis.is_subpage) n_times_accessed_subpage,
    sum(vis.is_url) n_times_accessed_url
from agg.vle_interactions_staging vis
group by student_id