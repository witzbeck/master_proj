create table model.runs (
    id serial primary key,
    model_type text not null,
    timestamp timestamp not null
)
