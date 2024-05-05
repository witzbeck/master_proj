drop table if exists main.modules;

create table main.modules (
    id SERIAL primary key,
    module_code VARCHAR(3) not null
);

insert into main.modules (module_code)
select distinct code_module module_code
from staging.courses
order by code_module;
