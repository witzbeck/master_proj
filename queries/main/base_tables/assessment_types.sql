CREATE TABLE main.assessment_types (
    id SERIAL PRIMARY KEY,
    assessment_type VARCHAR(4) NOT NULL
);
insert into main.assessment_types (assessment_type)
select distinct
    assessment_type
from staging.assessments a 
order by assessment_type;
