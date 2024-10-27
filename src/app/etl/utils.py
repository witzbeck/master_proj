from logging import getLogger
from pathlib import Path

from duckdb import DuckDBPyConnection, connect
from pandas import DataFrame

from alexlib.core import to_clipboard
from alexlib.df import get_distinct_col_vals
from alexlib.files import File

from constants import DB_PATH, SCHEMAS, SQL_BLACKLIST

logger = getLogger(__name__)


def get_cnxn(
    database: Path = DB_PATH, read_only: bool = False, memory: bool = False
) -> DuckDBPyConnection:
    if memory:
        database = ":memory:"
    return connect(database=database, read_only=read_only)


def get_info_schema_df(cnxn: DuckDBPyConnection) -> DataFrame:
    """Return the information schema as a DataFrame."""
    return cnxn.sql("SHOW ALL TABLES").fetchdf()


def get_all_schemas(cnxn: DuckDBPyConnection) -> list[str]:
    info_schema_df = get_info_schema_df(cnxn)
    return info_schema_df.loc[:, "schema"].unique().tolist()


def get_all_table_names(
    cnxn: DuckDBPyConnection, concat_schema: bool = True
) -> DuckDBPyConnection:
    info_schema_df = get_info_schema_df(cnxn)
    if concat_schema:
        columns = ["schema", "name"]
        return (
            info_schema_df.loc[:, columns].apply(lambda x: ".".join(x), axis=1).unique()
        )
    else:
        columns = "name"
        return info_schema_df.loc[:, columns].unique()


def get_schema_table_name(query_path: Path | File) -> tuple[str, str]:
    """Return the schema and table name."""
    if isinstance(query_path, File):
        query_path = query_path.path
    name_parts = query_path.stem.split("_")
    return name_parts[0], "_".join(name_parts[1:])


def check_sql_path_for_blacklist(
    sql_path: Path | File, blacklist: tuple[str] = SQL_BLACKLIST
) -> bool:
    """Check if the SQL path contains any blacklisted strings."""
    if isinstance(sql_path, File):
        sql_path = sql_path.path
    check_text = sql_path.read_text().upper()
    return any(x in check_text for x in blacklist)


def get_object_type(table_name: str) -> str:
    """Return the object type."""
    return "VIEW" if table_name.lower().startswith("v_") else "TABLE"


def get_create_object_command(
    schema: str,
    table_name: str,
    sql: str,
    obj_type: str = "TABLE",
    ifnotexists: bool = True,
    orreplace: bool = False,
) -> str:
    """Return the create object command."""
    if ifnotexists:
        ifnotexists = "IF NOT EXISTS"
    else:
        ifnotexists = ""
    if orreplace:
        orreplace = "OR REPLACE"
        ifnotexists = ""
    else:
        orreplace = ""
    return f"CREATE {orreplace} {obj_type} {ifnotexists} {schema}.{table_name} AS {sql}"


def create_table_from_query(
    cnxn: DuckDBPyConnection,
    query_path: Path | File,
    replace: bool = True,
) -> DuckDBPyConnection:
    if check_sql_path_for_blacklist(query_path):
        raise ValueError(f"Blacklisted SQL in {query_path}")
    schema, table_name = get_schema_table_name(query_path)
    if schema not in SCHEMAS:
        raise ValueError(f"{schema} is not a valid schema in {SCHEMAS}")
    sql = get_create_object_command(
        schema, table_name, query_path.read_text(), orreplace=replace
    )
    logger.info(
        f"Creating {schema}.{table_name} from {'/'.join(query_path.parts[-3:])}",
        end="... ",
    )
    cnxn.execute(sql)
    return cnxn


def get_onehot_case_line(col: str, val: str):
    return f"CASE WHEN {col} = '{val}' THEN 1 ELSE 0 END AS is_{val}"


def get_table_abrv(table_name: str, sep: str = "_") -> str:
    """Get the abbreviation for a table name."""
    return "".join([x[0] for x in table_name.split(sep)])


def create_onehot_view(
    cnxn: DuckDBPyConnection, schema: str, table: str, command: str = "create view"
) -> str:
    df = cnxn.sql(f"select * from {schema}.{table}").df()
    dist_col = [x for x in df.columns if x[-2:] != "id"][0]
    id_col = [x for x in df.columns if x != dist_col][0]
    dist_vals = get_distinct_col_vals(df, dist_col)

    first_line = f"{command} {schema}.v_{table}_onehot as select\n"
    lines = [first_line]
    lines.append(f" {id_col}\n")
    lines.append(f",{dist_col}\n")

    for val in dist_vals:
        com = ","
        new_col = f"is_{val}".replace(" ", "_")
        new_col = new_col.replace("%", "_percent")
        new_col = new_col.replace("-", "_")
        new_col = new_col.replace("<", "_less")
        new_col = new_col.replace("=", "_equal")
        new_col = new_col.replace(">", "_greater")
        case_stmt = get_onehot_case_line(dist_col, val)
        lines.append(f"{com}{case_stmt} {new_col}\n")
    lines.append(f"from {schema}.{table}")
    return "".join(lines)


def generate_select_query(
    cnxn: DuckDBPyConnection,
    schema: str,
    table: str,
    destination: Path = None,
    overwrite: bool = False,
) -> Path:
    df = get_info_schema_df(cnxn)
    if df.empty:
        raise ValueError("Object does not exist")
    abrv = get_table_abrv(table)

    cols = df["column_name"].tolist()
    lines = ["SELECT\n"]
    lines.extend([f"    {abrv}.{col}," for col in cols[:-1]])
    lines.append(f"    {abrv}.{cols[-1]}\n")
    lines.append(f"FROM {schema}.{table} {abrv}")
    query = "\n".join(lines)

    if destination is None:
        to_clipboard(query)
        return None
    else:
        filename = f"select_{schema}_{table}.sql"
        filepath = destination / filename

        if filepath.exists() and not overwrite:
            raise FileExistsError(
                "File already exists. Use overwrite=True to overwrite."
            )
        filepath.write_text(query)
        return filepath


def get_table(
    cnxn: DuckDBPyConnection, schema: str, table: str, nrows: int = None
) -> DataFrame:
    limit_clause = f"LIMIT {nrows}" if nrows else ""
    query = f"SELECT * FROM {schema}.{table} {limit_clause}"
    return cnxn.execute(query).fetchdf()


def show_table(
    cnxn: DuckDBPyConnection, schema: str, table: str, nrows: int = 10
) -> None:
    df = get_table(cnxn, schema, table, nrows)
    print(f"Showing {nrows} rows of {schema}.{table}")
    return df


def run_object_command(
    cnxn: DuckDBPyConnection,
    command: str,
    obj_type: str,
    obj_name: str,
    addl_cmd: str = "",
) -> None:
    sql = f"{command} {obj_type} {obj_name} {addl_cmd};"
    cnxn.sql(sql)


def drop_table(cnxn: DuckDBPyConnection, schema: str, table: str):
    object_name = f"{schema}.{table}"
    run_object_command(cnxn, "DROP", "TABLE", object_name)


def drop_view(cnxn: DuckDBPyConnection, schema: str, view: str):
    object_name = f"{schema}.{view}"
    run_object_command(cnxn, "DROP", "VIEW", object_name)
