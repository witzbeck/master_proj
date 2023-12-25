CREATE TABLE main.imd_band (
    id SERIAL PRIMARY KEY,
    imd_band VARCHAR(7) NOT NULL
);
insert into main.imd_band (imd_band)
select distinct imd_band
from staging."studentInfo"
where imd_band is not null
order by imd_band;
