select
    cast(id_site as int) AS site_id,
    cast(code_module as varchar(3)) AS module_code,
    cast(code_presentation as varchar(5)) AS presentation_code,
    cast(activity_type as varchar(14)) AS activity_type,
    cast(week_from as smallint) AS week_from,
    cast(week_to as smallint) AS week_to
from vle
