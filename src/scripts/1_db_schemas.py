from alexlib.files.objects import Directory
from src.setup import db_mgr
from src.constants import QUERY_PATH

if __name__ == "__main__":
    d = Directory.from_path(QUERY_PATH)
    schemas = [x.name for x in d.dirlist]
    for d in d.dirlist:
        db_mgr.create_schema(d.name)
