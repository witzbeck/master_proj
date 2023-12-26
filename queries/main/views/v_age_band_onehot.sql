create or replace view main.v_age_band_onehot as
select
 id
,case when age_band = '0-35' then 1 else 0 end is_le_35
,case when age_band = '35-55' then 1 else 0 end is_35_55
,case when age_band = '55<=' then 1 else 0 end is_ge_55
,age_band
from main.age_band
;
