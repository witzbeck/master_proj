from itertools import chain
from logging import warning

from tqdm import tqdm
from psycopg.errors import UndefinedTable

from alexlib.files import Directory
from src.setup import cnxn, queries

schema = "model"
cnxn.drop_all_schema_tables(schema)
parent = queries / schema
files = chain.from_iterable([
    Directory.from_path(parent / x).filelist
    for x in ["tables", "views", "funcs"]
])
for f in tqdm(files):
    print(f.path)
    try:
        cnxn.execute(f)
    except UndefinedTable as e:
        warning(f"{f} does not exist")
        raise UndefinedTable(e)
    except UnicodeDecodeError as e:
        print(e)
        warning(f"{e} for {f}")
