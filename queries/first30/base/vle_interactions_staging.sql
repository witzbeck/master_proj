select *
into first30.vle_interactions_staging
from agg.vle_interactions_staging s
where s.date <= 30
;
