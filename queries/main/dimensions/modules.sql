drop table if exists main.modules;

CREATE TABLE main.modules (
    id SERIAL PRIMARY KEY,
    module_code VARCHAR(3) NOT NULL
);

insert into main.modules (module_code)
select distinct code_module module_code 
from staging.courses
order by code_module;