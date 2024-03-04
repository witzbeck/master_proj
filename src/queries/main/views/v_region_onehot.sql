create view main.v_region_onehot as
select
    id
    , case when region = 'East Anglian Region' then 1 else 0 end is_east_anglian
    , case when region = 'East Midlands Region' then 1 else 0 end is_east_midlands
    , case when region = 'Ireland' then 1 else 0 end is_ireland
    , case when region = 'London Region' then 1 else 0 end is_london
    , case when region = 'North Region' then 1 else 0 end is_north
    , case when region = 'North Western Region' then 1 else 0 end is_north_western
    , case when region = 'Scotland' then 1 else 0 end is_scotland
    , case when region = 'South East Region' then 1 else 0 end is_south_east
    , case when region = 'South Region' then 1 else 0 end is_south
    , case when region = 'South West Region' then 1 else 0 end is_south_west
    , case when region = 'Wales' then 1 else 0 end is_wales
    , case when region = 'West Midlands Region' then 1 else 0 end is_west_midlands
    , case when region = 'Yorkshire Region' then 1 else 0 end is_yorkshire
    , region
from main.region
;
