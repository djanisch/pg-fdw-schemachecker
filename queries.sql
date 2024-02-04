-- name: get_table_definition
-- Get the table defintion for a specific table
select column_name, ordinal_position, is_nullable, data_type, character_maximum_length, character_octet_length,
numeric_precision, numeric_precision_radix, numeric_scale, datetime_precision, interval_type, interval_precision,
character_set_catalog, character_set_schema, character_set_name, collation_catalog, collation_schema, collation_name
from information_schema.columns where table_name = :table_name and table_schema = :table_schema;

-- name: get_foreign_tables
--Get the foreign tables of a specific server
select
    ft.foreign_table_catalog
    ,  ft.foreign_table_schema
    , ft.foreign_table_name
    , max(option_value) filter (where option_name='schema_name') as schema_name
    , max(option_value)filter (where option_name='table_name') as table_name
from
information_schema.foreign_tables as ft
inner join information_schema.foreign_table_options as fto ON
(ft.foreign_table_catalog=fto.foreign_table_catalog AND ft.foreign_table_schema=fto.foreign_table_schema AND ft.foreign_table_name=fto.foreign_table_name)
where foreign_server_name = :foreignserver
group by 1,2,3
;

-- name: blala
SELECT
    s.srvname as foreign_server,
    ft.ftoptions as table_options,
    s.srvoptions as server_options
FROM
    pg_foreign_table ft
    JOIN pg_foreign_server s ON s.oid = ft.ftserver
    JOIN pg_class c ON c.oid = ft.ftrelid
WHERE
    c.relname = 'your_foreign_table_name';