create or replace function model.inc_model_types()
returns trigger 
language plpgsql
as $$

declare last_run_id_ integer := (select max(id) from model.runs);
declare last_run_type_ text := (select model_type from model.runs where id = last_run_id_);

begin
if (last_run_type_ not in (select model_type from model.types) or (select count(*) from model.types) = 0)
then insert into model.types (model_type) values (last_run_type_);
end if;
return NULL;
end;
$$