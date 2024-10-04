select
    cast(id_site as int) site_id,
    cast(code_module as varchar(3)) module_code,
    cast(code_presentation as varchar(5)) presentation_code,
    cast(activity_type as varchar(14)) activity_type,
    cast(week_from as smallint) week_from,
    cast(week_to as smallint) week_to
from vle
