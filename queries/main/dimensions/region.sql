drop table if exists main.region;
CREATE TABLE main.region (
    id SERIAL PRIMARY KEY,
    region VARCHAR(20) NOT NULL
);
insert into main.region (region)
select distinct region
from staging."studentInfo"
order by region;
