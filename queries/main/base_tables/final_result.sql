CREATE TABLE main.age_band (
    id SERIAL PRIMARY KEY,
    age_band VARCHAR(5) NOT NULL
);
insert into main.age_band (age_band)
select distinct age_band
from staging."studentInfo"
where age_band is not null
order by age_band;
