drop table if exists main.region;
create table main.region (
    id SERIAL primary key,
    region VARCHAR(20) not null
);
insert into main.region (region)
select distinct region
from staging."studentInfo"
order by region;
