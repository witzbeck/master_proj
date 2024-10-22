select cast(code_module as varchar(3)) AS module_code,
    cast(code_presentation as varchar(5)) AS presentation_code,
    cast(module_presentation_length as int) AS module_presentation_length
from courses