SELECT
    t.table_catalog,
    t.table_schema,
    t.table_name,
    t.table_type,
    c.column_name,
    c.ordinal_position,
    c.data_type,
    c.character_maximum_length,
    c.numeric_precision,
    c.numeric_scale,
    c.datetime_precision
FROM learning.information_schema.tables t
    JOIN learning.information_schema.columns c ON
        t.table_catalog = c.table_catalog
        AND t.table_schema = c.table_schema
        AND t.table_name = c.table_name
ORDER BY
    t.table_schema,
    t.table_name,
    c.ordinal_position
