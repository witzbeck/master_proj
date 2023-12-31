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
for group in dirs:
    d = Directory.from_path(main / group)
    print(d.name)
    lst = [
        x for x in d.sql_filelist
        if not cnxn.table_exists(schema, x.path.stem)
    ]
    for f in tqdm(lst):
        try:
            cnxn.execute(f)
        except UndefinedTable:
            print(f"{f} does not exist")
        except DuplicateTable:
            print(f"{f} already exists")
        except UnicodeDecodeError as e:
            print(f"{e} for {f}")
