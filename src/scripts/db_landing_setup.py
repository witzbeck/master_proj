from pathlib import Path

from alexlib.auth import Auth
from alexlib.db import Connection
from alexlib.files import Directory

auth = Auth("remote.dev.learning")
datadir = Path.home() / "repos/master_proj/data"
cnxn = Connection.from_auth(auth)
d = Directory.from_path(datadir)
for f in d.csv_filelist:
    cnxn.file_to_db(f, auth.database, f.path.stem)
