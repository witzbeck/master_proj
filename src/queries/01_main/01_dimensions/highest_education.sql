create table main.highest_education (
    id SERIAL primary key,
    highest_education VARCHAR(27) not null
);
insert into main.highest_education (highest_education)
select distinct highest_education
from staging.studentinfo
order by highest_education;