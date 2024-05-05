from itertools import chain
from logging import warning

from tqdm import tqdm
from psycopg.errors import UndefinedTable, DuplicateTable

from alexlib.files import Directory
from src.setup import cnxn, queries

schema = "first30"
cnxn.drop_all_schema_tables(schema)
parent = queries / schema
dirs = [Directory.from_path(parent / str(i)) for i in range(6)]
files = list(chain.from_iterable([d.filelist for d in dirs]))
files = [f for f in files if not cnxn.table_exists(schema, f.path.stem)]
for f in tqdm(files):
    print(f.path)
    try:
        cnxn.execute(f)
    except UndefinedTable as e:
        warning(f"{f} does not exist")
        raise UndefinedTable(e) from e
    except (UnicodeDecodeError, DuplicateTable) as e:
        print(e)
        warning(f"{e} for {f}")
