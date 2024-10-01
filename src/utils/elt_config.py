from pathlib import Path

from duckdb import CatalogException, DuckDBPyConnection, connect
from pandas import DataFrame

from utils.constants import DB_PATH, QUERY_PATH, RAW_PATH, SCHEMAS


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


def create_all_schemas(
    cnxn: DuckDBPyConnection, schemas: tuple[str] = SCHEMAS
) -> DuckDBPyConnection:
    for schema in schemas:
        try:
            create_schema(cnxn=cnxn, schema=schema)
        except CatalogException:
            continue
    return cnxn


def load_landing_csv(
    table_name: str,
    cnxn: DuckDBPyConnection,
    parent_path: Path = RAW_PATH,
    query_path: Path = QUERY_PATH,
    schema: str = "landing",
) -> DuckDBPyConnection:
    assert parent_path.is_dir(), f"{parent_path} is not a directory"
    csv_path = (parent_path / table_name).with_suffix(".csv")
    assert csv_path.is_file(), f"{csv_path} is not a file"
    sql_path = query_path / "00_landing" / f"{table_name}.sql"
    assert sql_path.is_file(), f"{sql_path} is not a file"
    select = sql_path.read_text().replace(table_name, f"'{str(csv_path)}';")
    sql = f"CREATE TABLE {schema}.{table_name} AS {select}"
    cnxn.execute(sql)


def load_landing_data(cnxn: DuckDBPyConnection) -> DuckDBPyConnection:
    landing_queries = (QUERY_PATH / "00_landing").glob("*.sql")
    table_names = [query.stem for query in landing_queries]
    [load_landing_csv(table, cnxn) for table in table_names]
    return cnxn
