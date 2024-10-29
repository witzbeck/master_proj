from logging import getLogger
from pathlib import Path

from click import command, option
from duckdb import DuckDBPyConnection
from tqdm import tqdm

from constants import DB_PATH, SCHEMAS
from etl.extract import load_landing_csv
from etl.files import DataDirectory, QueriesDirectory
from etl.utils import (
    create_table_from_query,
    get_cnxn,
)

logger = getLogger(__name__)
data_dir = DataDirectory()
queries_dir = QueriesDirectory()


def create_schema_logic(
    cnxn: DuckDBPyConnection = None, schema_name: str = None, all: bool = False
) -> DuckDBPyConnection:
    """Create a schema."""
    if cnxn is None:
        cnxn = get_cnxn(database=DB_PATH)
    if all or schema_name is None:
        for schema in SCHEMAS:
            cnxn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
        logger.info(f"Created all schemas: {', '.join(SCHEMAS)}")
    else:
        cnxn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
        logger.info(f"Created schema: {schema_name}")
    return cnxn


@command(name="create-schema", help="Create a schema.")
@option("--schema", "-s", default="landing", help="The schema to create.")
@option("--all", "-a", is_flag=True, help="Create all schemas.")
def create_schema(schema_name: str, all: bool = False) -> DuckDBPyConnection:
    """Create a schema."""
    return create_schema_logic(schema_name=schema_name, all=all)


def load_landing_data_logic(cnxn: DuckDBPyConnection = None) -> DuckDBPyConnection:
    """Load landing data into the database."""
    if cnxn is None:
        cnxn = get_cnxn()
    [load_landing_csv(table, cnxn) for table in queries_dir.landing_query_dict.keys()]
    logger.info("Loaded landing data.")
    return cnxn


@command(name="load-landing-data", help="Load landing data.")
def load_landing_data() -> DuckDBPyConnection:
    """Load landing data into the database."""
    return load_landing_data_logic()


def load_schema_logic(
    schema: str, replace: bool, cnxn: DuckDBPyConnection = None
) -> DuckDBPyConnection:
    """Load a schema."""
    if cnxn is None:
        cnxn = get_cnxn(database=DB_PATH)
    if schema not in SCHEMAS:
        raise ValueError(f"{schema} is not a valid schema in {SCHEMAS}")
    if schema == "landing":
        return load_landing_data()
    elif isinstance(schema, (list, tuple)):
        for schema_name in tqdm(schema, desc="Loading schemas"):
            load_schema_logic(schema_name, replace, cnxn)
        return cnxn
    query_paths = queries_dir.get_sorted_schema_query_paths(schema)
    for query_path in tqdm(query_paths, desc=f"Loading schema: {schema}"):
        if query_path.stem.startswith("_"):
            logger.info(f"skipping {query_path.relative_to(queries_dir.path)}")
            continue
        else:
            create_table_from_query(cnxn=cnxn, query_path=query_path, replace=replace)
    logger.info(f"Loaded schema: {schema}")
    return cnxn


@command(name="load-schema", help="Load a schema.")
@option("--schema", "-s", default="landing", help="The schema to load.")
@option("--replace", "-r", is_flag=True, help="Replace the schema.")
def load_schema(schema: str, replace: bool) -> DuckDBPyConnection:
    """Load a schema."""
    return load_schema_logic(schema, replace)


def export_database_logic(export_path: Path, cnxn: DuckDBPyConnection = None) -> None:
    """Export the database."""
    if cnxn is None:
        cnxn = get_cnxn(database=DB_PATH)
    [x.unlink() for x in export_path.iterdir() if x.is_file()]
    cnxn.execute(f"""EXPORT DATABASE '{str(export_path)}' (FORMAT PARQUET)""")
    logger.info(f"Exported database to {export_path}")


@command(name="export-database", help="Export the database.")
@option(
    "--export-path",
    "-e",
    type=Path,
    default=data_dir.export_path,
    help="The export path.",
)
def export_database(export_path: Path) -> None:
    """Export the database."""
    export_database_logic(export_path)
