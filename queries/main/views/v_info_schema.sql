CREATE VIEW main.v_info_schema as
select 
t.table_catalog
,t.table_schema
,t.table_name
,t.table_type
,c.column_name
,c.ordinal_position
,c.data_type
,c.character_maximum_length
,c.numeric_precision
,c.numeric_scale
,c.datetime_precision

 
from learning.information_schema.tables t
join learning.information_schema.columns c on t.table_catalog=c.table_catalog
                                        and t.table_schema=c.table_schema
                                        and t.table_name=c.table_name
order by t.table_schema, t.table_name, c.ordinal_position 