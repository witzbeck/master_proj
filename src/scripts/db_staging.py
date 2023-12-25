from pathlib import Path

from alexlib.files import Directory
from master_proj.setup import cnxn

queries_path = Path.home() / "repos/master_proj/queries"
d = Directory.from_path(queries_path / "staging")
schema = "staging"
cnxn.create_schema(schema)
[
    cnxn.file_to_db(f, schema, f.path.stem)
    for f in d.csv_filelist
]
