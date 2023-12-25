from tqdm import tqdm

from alexlib.files import Directory
from src.setup import cnxn, queries

schema = "main"
main = queries / schema
tables = Directory.from_path(main / "base_tables")
views = Directory.from_path(main / "views")

cnxn.create_schema(schema)
for f in tqdm(tables.filelist):
    if not cnxn.table_exists(schema, f.path.stem):
        cnxn.execute(f)
for f in tqdm(views.filelist):
    if not cnxn.table_exists(schema, f.path.stem):
        cnxn.execute(f)
