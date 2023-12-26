create or replace view main.v_highest_education_onehot as
select
id
,case when highest_education = 'No Formal quals' then 1 else 0 end is_no_formal_quals
,case when highest_education = 'Lower Than A Level' then 1 else 0 end is_lower_than_a_level
,case when highest_education = 'A Level or Equivalent' then 1 else 0 end is_a_level_or_equivalent
,case when highest_education = 'HE Qualification' then 1 else 0 end is_he_qualification
,case when highest_education = 'Post Graduate Qualification' then 1 else 0 end is_post_graduate_qualification
,highest_education
from main.highest_education
;