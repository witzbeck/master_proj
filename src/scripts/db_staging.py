from tqdm import tqdm
from psycopg.errors import DuplicateSchema

from alexlib.files import Directory
from src.setup import cnxn, queries

d = Directory.from_path(queries / "staging")
schema = "staging"

if not cnxn.schema_exists(schema):
    try:
        cnxn.create_schema(schema)
    except DuplicateSchema:
        pass
for f in tqdm(d.filelist):
    cnxn.execute(f"drop table if exists {schema}.{f.path.stem}")
    cnxn.execute(f)
