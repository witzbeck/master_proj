from pathlib import Path

from pandas import read_csv

from utils.db_helpers import build_engine


def get_info_schema(filename: str, dirpath: Path):
    filepath = dirpath / filename
    return read_csv(filepath, keep_default_na=False)


def path_list_to_dict(path_list: list[Path]):
    return {x.stem: x for x in path_list}


def paths_to_df_dict(path_list: list[Path]):
    return {x.stem: read_csv(x) for x in path_list}


class FileHelper:
    def insert_landing_tables(self):
        engine = build_engine("learning")
        total_rows = 0
        for table in self.table_names:
            df = self.source_df_dict[table]
            df.to_sql(
                table,
                engine,
                if_exists="replace",
                schema="landing",
                index=False,
                chunksize=10000,
                method="multi",
            )
            inserted_rows = len(df)
            total_rows += inserted_rows
            print(f"{inserted_rows} rows have been inserted into {table}")
        print("total number of rows inserted:", total_rows)

    def __init__(self):
        self.source_csv_paths = Path("OULAD_dataset").glob("*.csv")
        self.table_names = [x.stem for x in self.source_csv_paths]
        self.source_df_dict = paths_to_df_dict(self.source_csv_paths)


def copy_csv_str(table_name, csv_path):
    return f"""COPY {table_name}
    FROM '{csv_path}'
    DELIMITER ','
    CSV HEADER
    """
