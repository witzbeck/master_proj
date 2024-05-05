create view main.v_imd_band_onehot as
select
    id
    , case when id = 1 then 1 else 0 end imd_band_00_10
    , case when id = 2 then 1 else 0 end imd_band_10_20
    , case when id = 3 then 1 else 0 end imd_band_20_30
    , case when id = 4 then 1 else 0 end imd_band_30_40
    , case when id = 5 then 1 else 0 end imd_band_40_50
    , case when id = 6 then 1 else 0 end imd_band_50_60
    , case when id = 7 then 1 else 0 end imd_band_60_70
    , case when id = 8 then 1 else 0 end imd_band_70_80
    , case when id = 9 then 1 else 0 end imd_band_80_90
    , case when id = 10 then 1 else 0 end imd_band_90_100

    , imd_band
from main.imd_band
;
