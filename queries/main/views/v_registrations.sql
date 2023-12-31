create view main.v_registrations as
select 
 module_code
,presentation_code
,count(distinct student_id)             n_student_ids
,cast(sum(n_registrations) as int)      n_registrations
,cast(sum(n_unregistrations) as int)    n_unregistrations
,cast(sum(n_records) as int)            n_records
from (
select
 m.module_code
,p.presentation_code
,sr.id student_id
,sr.date_registration
,sr.date_unregistration
,count(*) n_records
,sum(case 
    when sr.date_registration is not null 
    then 1 else 0 end)      n_registrations
,sum(case 
    when sr.date_unregistration is not null 
    then 1 else 0 end)      n_unregistrations
from main.student_info sr
join main.modules m on m.id=sr.module_id
join main.presentations p on p.id=sr.presentation_id

group by 
 module_code
,presentation_code
,sr.id
,sr.date_registration
,sr.date_unregistration
) a
group by
module_code, presentation_code
