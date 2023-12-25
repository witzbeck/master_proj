CREATE TABLE main.final_result (
    id SERIAL PRIMARY KEY,
    final_result VARCHAR(11) NOT NULL
);
insert into main.final_result (final_result)
select distinct final_result
from staging."studentInfo"
where final_result is not null
order by final_result;
