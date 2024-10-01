from pathlib import Path

from duckdb import DuckDBPyConnection, connect
from pandas import DataFrame
from tqdm import tqdm

from utils.constants import DB_PATH, QUERY_PATH, RAW_PATH


def get_cnxn(database: Path = DB_PATH, read_only: bool = False) -> DuckDBPyConnection:
    return connect(database=database, read_only=read_only)


def get_info_schema_df(cnxn: DuckDBPyConnection = None) -> DataFrame:
    if cnxn is None:
        cnxn = get_cnxn()
    return cnxn.sql("SHOW ALL TABLES").fetchdf()


def get_all_schemas(info_schema_df: DataFrame = None) -> DuckDBPyConnection:
    if info_schema_df is None:
        info_schema_df = get_info_schema_df()
    return info_schema_df.loc[:, "schema"].unique()


def get_all_table_names(
    info_schema_df: DataFrame = None, concat_schema: bool = True
) -> DuckDBPyConnection:
    if info_schema_df is None:
        info_schema_df = get_info_schema_df()
    if concat_schema:
        columns = ["schema", "name"]
        return (
            info_schema_df.loc[:, columns].apply(lambda x: ".".join(x), axis=1).unique()
        )
    else:
        columns = "name"
        return info_schema_df.loc[:, columns].unique()


def create_schema(
    cnxn: DuckDBPyConnection, schema: str = "landing"
) -> DuckDBPyConnection:
    cnxn.execute(f"CREATE SCHEMA {schema};")
    return cnxn


def load_landing_data(
    cnxn: DuckDBPyConnection, schema: str = "landing"
) -> DuckDBPyConnection:
    create_schema(cnxn=cnxn, schema=schema)
    landing_queries = (QUERY_PATH / "00_landing").glob("*.sql")

    for query in tqdm(landing_queries):
        table = query.stem
        csv_path = RAW_PATH / f"{table}.csv"
        select = query.read_text().replace(table, f"'{str(csv_path)}';")
        sql = f"CREATE TABLE {schema}.{table} AS {select}"
        cnxn.execute(sql)

    print(cnxn.sql("SHOW TABLES").fetchdf())
    return cnxn


AGG_PATH = QUERY_PATH / "agg"
