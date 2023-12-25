select 
 cast(code_module as varchar(3))        code_module
,cast(code_presentation as varchar(5))  code_presentation
,cast(id_student as int)                student_id
,cast(date_registration as int)         date_registration
,cast(date_unregistration as int)       date_unregistration
into staging."studentRegistration"
from landing."studentRegistration"
;