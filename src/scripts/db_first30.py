from itertools import chain
from logging import warning

from tqdm import tqdm
from psycopg.errors import DuplicateTable, UndefinedTable

from alexlib.files import Directory
from src.setup import cnxn, queries

schema = "first30"
parent = queries / schema
dirs = [Directory.from_path(parent / str(i)) for i in range(1, 5)]
files = list(chain.from_iterable([d.filelist for d in dirs]))
files = [f for f in files if not cnxn.table_exists(schema, f.path.stem)]
cnxn.create_schema(schema)
for f in tqdm(files):
    print(f.path)
    try:
        cnxn.execute(f)
    except UndefinedTable as e:
        warning(f"{f} does not exist")
        raise UndefinedTable(e)
    except DuplicateTable as e:
        print(e)
        warning(f"{f} already exists")
    except UnicodeDecodeError as e:
        print(e)
        warning(f"{e} for {f}")
    except Exception as e:
        print(f, "\n", e)
        raise Exception

"""
"""