CREATE_ANALYSIS_ABROCA_TABLE = """
create or replace table analysis.abroca(
index integer primary key,
run_id integer not null,
iter_id integer not null,
course_id integer not null,
is_stem boolean not null,
is_female boolean not null,
has_disability boolean not null
);
"""
