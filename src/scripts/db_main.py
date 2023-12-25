from logging import warning

from tqdm import tqdm
from psycopg.errors import DuplicateTable, UndefinedTable

from alexlib.files import Directory
from src.setup import cnxn, queries

schema = "main"
main = queries / schema
dirs = [
    "dimensions",
    "measures",
    "bridges",
    "views",
]
cnxn.create_schema(schema)

for group in tqdm(dirs):
    lst = Directory.from_path(main / group).filelist
    for f in tqdm(lst):
        if not cnxn.table_exists(schema, f.path.stem):
            try:
                cnxn.execute(f)
            except UndefinedTable:
                warning(f"{f} does not exist")
            except DuplicateTable:
                warning(f"{f} already exists")
            except UnicodeDecodeError as e:
                warning(f"{e} for {f}")
            except Exception as e:
                print(f)
                warning(f"{e} for {f}")
                raise Exception
