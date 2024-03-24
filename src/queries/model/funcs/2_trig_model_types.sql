create or replace trigger trg_model_types
after insert on model.runs
for each statement
execute procedure model.inc_model_types()
