from tqdm import tqdm

from alexlib.files import Directory
from src.setup import cnxn, data

d = Directory.from_path(data)
schema = "landing"
for file in tqdm(d.csv_filelist):
    cnxn.file_to_db(file, schema, file.path.stem, if_exists="replace")
