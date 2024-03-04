drop table if exists main.presentations;

create table main.presentations (
    id SERIAL primary key,
    presentation_code VARCHAR(5) not null
);

insert into main.presentations (presentation_code)
select distinct code_presentation presentation_code
from staging.courses
order by code_presentation;
