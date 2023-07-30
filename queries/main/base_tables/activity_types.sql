CREATE TABLE main.activity_types (
    id SERIAL PRIMARY KEY,
    activity_type VARCHAR(14) NOT NULL
);
insert into main.activity_types (activity_type)
select distinct activity_type
from staging."vle"
order by activity_type;