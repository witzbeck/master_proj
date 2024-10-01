from tqdm import tqdm

from alexlib.files import Directory
from src.setup import cnxn, queries

d = Directory.from_path(queries / "staging")
schema = "staging"

for f in tqdm(d.filelist):
    cnxn.execute(f'drop table if exists {schema}."{f.path.stem}"')
    cnxn.execute(f)
