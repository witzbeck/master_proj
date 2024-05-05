CREATE OR REPLACE VIEW main.v_activity_types_onehot as
select
    activity_type_id
    , CASE WHEN activity_type = 'dataplus' THEN 1 ELSE 0 END  is_dataplus
    , CASE WHEN activity_type = 'dualpane' THEN 1 ELSE 0 END  is_dualpane
    , CASE WHEN activity_type = 'externalquiz' THEN 1 ELSE 0 END  is_externalquiz
    , CASE WHEN activity_type = 'folder' THEN 1 ELSE 0 END  is_folder
    , CASE WHEN activity_type = 'forumng' THEN 1 ELSE 0 END  is_forumng
    , CASE WHEN activity_type = 'glossary' THEN 1 ELSE 0 END  is_glossary
    , CASE WHEN activity_type = 'homepage' THEN 1 ELSE 0 END  is_homepage
    , CASE WHEN activity_type = 'htmlactivity' THEN 1 ELSE 0 END  is_htmlactivity
    , CASE WHEN activity_type = 'oucollaborate' THEN 1 ELSE 0 END  is_oucollaborate
    , CASE WHEN activity_type = 'oucontent' THEN 1 ELSE 0 END  is_oucontent
    , CASE WHEN activity_type = 'ouelluminate' THEN 1 ELSE 0 END  is_ouelluminate
    , CASE WHEN activity_type = 'ouwiki' THEN 1 ELSE 0 END  is_ouwiki
    , CASE WHEN activity_type = 'page' THEN 1 ELSE 0 END  is_page
    , CASE WHEN activity_type = 'questionnaire' THEN 1 ELSE 0 END  is_questionnaire
    , CASE WHEN activity_type = 'quiz' THEN 1 ELSE 0 END  is_quiz
    , CASE WHEN activity_type = 'repeatactivity' THEN 1 ELSE 0 END  is_repeatactivity
    , CASE WHEN activity_type = 'resource' THEN 1 ELSE 0 END  is_resource
    , CASE WHEN activity_type = 'sharedsubpage' THEN 1 ELSE 0 END  is_sharedsubpage
    , CASE WHEN activity_type = 'subpage' THEN 1 ELSE 0 END  is_subpage
    , CASE WHEN activity_type = 'url' THEN 1 ELSE 0 END  is_url
    , activity_type
FROM main.activity_type
;

CREATE OR REPLACE VIEW main.v_age_band_onehot as
select
    age_band_id
    , CASE WHEN age_band = '0-35' THEN 1 ELSE 0 END  is_le_35
    , CASE WHEN age_band = '35-55' THEN 1 ELSE 0 END  is_35_55
    , CASE WHEN age_band = '55<=' THEN 1 ELSE 0 END  is_ge_55
    , age_band
FROM main.age_band
;

CREATE OR REPLACE VIEW main.v_imd_band_onehot as
select
    imd_band_id
    , CASE WHEN id = 1 THEN 1 ELSE 0 END  imd_band_00_10
    , CASE WHEN id = 2 THEN 1 ELSE 0 END  imd_band_10_20
    , CASE WHEN id = 3 THEN 1 ELSE 0 END  imd_band_20_30
    , CASE WHEN id = 4 THEN 1 ELSE 0 END  imd_band_30_40
    , CASE WHEN id = 5 THEN 1 ELSE 0 END  imd_band_40_50
    , CASE WHEN id = 6 THEN 1 ELSE 0 END  imd_band_50_60
    , CASE WHEN id = 7 THEN 1 ELSE 0 END  imd_band_60_70
    , CASE WHEN id = 8 THEN 1 ELSE 0 END  imd_band_70_80
    , CASE WHEN id = 9 THEN 1 ELSE 0 END  imd_band_80_90
    , CASE WHEN id = 10 THEN 1 ELSE 0 END  imd_band_90_100

    , imd_band
FROM main.imd_band
;

CREATE OR REPLACE VIEW main.v_region_onehot as
select
    region_id
    , CASE WHEN region = 'East Anglian Region' THEN 1 ELSE 0 END  is_east_anglian
    , CASE WHEN region = 'East Midlands Region' THEN 1 ELSE 0 END  is_east_midlands
    , CASE WHEN region = 'Ireland' THEN 1 ELSE 0 END  is_ireland
    , CASE WHEN region = 'London Region' THEN 1 ELSE 0 END  is_london
    , CASE WHEN region = 'North Region' THEN 1 ELSE 0 END  is_north
    , CASE WHEN region = 'North Western Region' THEN 1 ELSE 0 END  is_north_western
    , CASE WHEN region = 'Scotland' THEN 1 ELSE 0 END  is_scotland
    , CASE WHEN region = 'South East Region' THEN 1 ELSE 0 END  is_south_east
    , CASE WHEN region = 'South Region' THEN 1 ELSE 0 END  is_south
    , CASE WHEN region = 'South West Region' THEN 1 ELSE 0 END  is_south_west
    , CASE WHEN region = 'Wales' THEN 1 ELSE 0 END  is_wales
    , CASE WHEN region = 'West Midlands Region' THEN 1 ELSE 0 END  is_west_midlands
    , CASE WHEN region = 'Yorkshire Region' THEN 1 ELSE 0 END  is_yorkshire
    , region
FROM main.region
;

CREATE OR REPLACE VIEW main.v_highest_education_onehot as
select
    highest_education_id
    , CASE WHEN highest_education = 'No Formal quals' THEN 1 ELSE 0 END  is_no_formal_quals
    , CASE WHEN highest_education = 'Lower Than A Level' THEN 1 ELSE 0 END  is_lower_than_a_level
    , CASE WHEN highest_education = 'A Level or Equivalent' THEN 1 ELSE 0 END  is_a_level_or_equivalent
    , CASE WHEN highest_education = 'HE Qualification' THEN 1 ELSE 0 END  is_he_qualification
    , CASE WHEN highest_education = 'Post Graduate Qualification' THEN 1 ELSE 0 END  is_post_graduate_qualification
    , highest_education
FROM main.highest_education
;

CREATE OR REPLACE VIEW main.v_final_result_onehot as
select
    final_result_id
    , CASE WHEN final_result = 'Distinction' THEN 1 ELSE 0 END  is_distinction
    , CASE WHEN final_result = 'Fail' THEN 1 ELSE 0 END  is_fail
    , CASE WHEN final_result = 'Pass' THEN 1 ELSE 0 END  is_pass
    , CASE WHEN final_result = 'Withdrawn' THEN 1 ELSE 0 END  is_withdrawn
    , final_result
FROM main.final_result

