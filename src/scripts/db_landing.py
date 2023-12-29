from logging import info

from tqdm import tqdm

from alexlib.files import Directory
from src.setup import cnxn, data

d = Directory.from_path(data)
schema = "landing"

try:
    cnxn.create_db()
except ValueError:
    info("database already exists")
cnxn.create_schema(schema)
for file in tqdm(d.csv_filelist):
    cnxn.file_to_db(
        file,
        schema,
        file.path.stem,
    )
