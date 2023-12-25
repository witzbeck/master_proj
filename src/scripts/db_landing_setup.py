from logging import info
from pathlib import Path

from alexlib.files import Directory
from master_proj.setup import auth, cnxn

datadir = Path.home() / "repos/master_proj/data"
d = Directory.from_path(datadir)
schema = "landing"

try:
    cnxn.create_db()
except ValueError:
    info("database already exists")
cnxn.create_schema(schema)
[
    cnxn.file_to_db(f, schema, f.path.stem)
    for f in d.csv_filelist
]
