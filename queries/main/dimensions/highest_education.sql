drop table if exists main.highest_education;
CREATE TABLE main.highest_education (
    id SERIAL PRIMARY KEY,
    highest_education VARCHAR(27) NOT NULL
);
insert into main.highest_education (highest_education)
select distinct highest_education
from staging."studentInfo"
order by highest_education;
