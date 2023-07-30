drop table if exists main.presentations;

CREATE TABLE main.presentations (
    id SERIAL PRIMARY KEY,
    presentation_code VARCHAR(5) NOT NULL
);

insert into main.presentations (presentation_code)
select distinct code_presentation presentation_code 
from staging.courses
order by code_presentation;
