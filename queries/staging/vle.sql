drop table if exists staging.vle;
select 
 cast(id_site as int)                   site_id
,cast(code_module as varchar(3))        code_module
,cast(code_presentation as varchar(5))  code_presentation
,cast(activity_type as varchar(14))     activity_type
,cast(week_from as smallint)            week_from
,cast(week_to as smallint)              week_to

into staging.vle
from landing.vle;
