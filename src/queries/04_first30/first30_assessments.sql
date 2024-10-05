select *
from agg.vle_interactions_staging s
where s.date <= 30
limit 10;
select 
max(student_id)  max_id,
min(student_id)  min_id

from agg.vle_interactions_staging
select count(*) from first30.interactions