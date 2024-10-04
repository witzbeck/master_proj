select
    cast(code_module as varchar(3)) module_code,
    cast(code_presentation as varchar(5)) presentation_code,
    cast(module_presentation_length as int) module_presentation_length
from courses
