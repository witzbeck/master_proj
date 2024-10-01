select
    id,
    case
        when activity_type = 'dataplus' then 1
        else 0
    end is_dataplus,
    case
        when activity_type = 'dualpane' then 1
        else 0
    end is_dualpane,
    case
        when activity_type = 'externalquiz' then 1
        else 0
    end is_externalquiz,
    case
        when activity_type = 'folder' then 1
        else 0
    end is_folder,
    case
        when activity_type = 'forumng' then 1
        else 0
    end is_forumng,
    case
        when activity_type = 'glossary' then 1
        else 0
    end is_glossary,
    case
        when activity_type = 'homepage' then 1
        else 0
    end is_homepage,
    case
        when activity_type = 'htmlactivity' then 1
        else 0
    end is_htmlactivity,
    case
        when activity_type = 'oucollaborate' then 1
        else 0
    end is_oucollaborate,
    case
        when activity_type = 'oucontent' then 1
        else 0
    end is_oucontent,
    case
        when activity_type = 'ouelluminate' then 1
        else 0
    end is_ouelluminate,
    case
        when activity_type = 'ouwiki' then 1
        else 0
    end is_ouwiki,
    case
        when activity_type = 'page' then 1
        else 0
    end is_page,
    case
        when activity_type = 'questionnaire' then 1
        else 0
    end is_questionnaire,
    case
        when activity_type = 'quiz' then 1
        else 0
    end is_quiz,
    case
        when activity_type = 'repeatactivity' then 1
        else 0
    end is_repeatactivity,
    case
        when activity_type = 'resource' then 1
        else 0
    end is_resource,
    case
        when activity_type = 'sharedsubpage' then 1
        else 0
    end is_sharedsubpage,
    case
        when activity_type = 'subpage' then 1
        else 0
    end is_subpage,
    case
        when activity_type = 'url' then 1
        else 0
    end is_url,
    activity_type
from main.activity_types
