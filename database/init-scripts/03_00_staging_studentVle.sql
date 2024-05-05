select
    cast(id_site as int) site_id
    , cast(id_student as int) student_id
    , cast(code_module as varchar(3)) code_module
    , cast(code_presentation as varchar(5)) code_presentation
    , cast(date as int) date
    , cast(sum_click as int) sum_click
into staging."studentVle"
from landing."studentVle"
