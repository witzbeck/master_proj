select
 cast(code_module as varchar(3))            code_module
,cast(code_presentation as varchar(5))      code_presentation
,cast(module_presentation_length as int)    module_presentation_length
into staging.courses
from landing.courses
;