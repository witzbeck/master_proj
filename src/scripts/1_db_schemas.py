from alexlib.files import Directory
from src.setup import cnxn, queries

d = Directory.from_path(queries)
schemas = [x.name for x in d.dirlist]
cnxn.create_db()
for s in schemas:
    cnxn.create_schema(s)
