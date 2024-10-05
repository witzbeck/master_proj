from dataclasses import dataclass
from functools import cached_property
from logging import getLogger
from pathlib import Path

from duckdb import CatalogException, DuckDBPyConnection, connect
from pandas import DataFrame
from tqdm import tqdm

from alexlib.files import Directory, File
from alexlib.times import Timer

from utils.constants import DATA_PATH, DB_PATH, QUERY_PATH, RAW_PATH, SCHEMAS

logger = getLogger(__name__)

SQL_BLACKLIST = ("CREATE", "DROP", "ALTER", "TRUNCATE", "DELETE", "UPDATE", "INSERT")


def get_cnxn(database: Path = DB_PATH, read_only: bool = False) -> DuckDBPyConnection:
    return connect(database=database, read_only=read_only)


def create_schema(
    cnxn: DuckDBPyConnection, schema: str = "landing"
) -> DuckDBPyConnection:
    cnxn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
    return cnxn


def create_all_schemas(
    cnxn: DuckDBPyConnection, schemas: tuple[str] = SCHEMAS
) -> DuckDBPyConnection:
    for schema in schemas:
        try:
            create_schema(cnxn=cnxn, schema=schema)
        except CatalogException:
            logger.info(f"{schema} already exists")
    return cnxn


def get_info_schema_df(cnxn: DuckDBPyConnection = None) -> DataFrame:
    if cnxn is None:
        cnxn = get_cnxn()
    return cnxn.sql("SHOW ALL TABLES").fetchdf()


def get_all_schemas(info_schema_df: DataFrame = None) -> list[str]:
    if info_schema_df is None:
        info_schema_df = get_info_schema_df()
    return info_schema_df.loc[:, "schema"].unique().tolist()


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
    sql = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} AS {select}"
    cnxn.execute(sql)


def load_landing_data(
    landing_query_keys: set[str], cnxn: DuckDBPyConnection
) -> DuckDBPyConnection:
    """Load landing data into the database."""
    [load_landing_csv(table, cnxn) for table in landing_query_keys]
    return cnxn


@dataclass(frozen=True)
class StagingPathGroup:
    source_path: Path
    query_path: Path
    staging_path: Path


@dataclass
class QueriesDirectory(Directory):
    path: Path = QUERY_PATH

    @cached_property
    def schema_dict(self) -> dict[str, Directory]:
        """Return a dictionary of schema directories."""
        return {x.path.stem[x.path.stem.index("_") + 1 :]: x for x in self.dirlist}

    @property
    def landing_dir(self) -> Directory:
        """Return the landing directory."""
        return self.schema_dict["landing"]

    @cached_property
    def landing_query_dict(self) -> dict[str]:
        """Return a dictionary of landing queries."""
        return {x.path.stem: x for x in self.landing_dir.filelist}

    def get_sorted_nonlanding_query_paths(self) -> list[Path]:
        return sorted(
            [
                x.path
                for x in self.allchildfiles
                if x.path.suffix == ".sql" and "00_landing" not in x.path.parts
            ],
            key=lambda x: str(x.parent),
        )


@dataclass
class DataDirectory(Directory):
    path: Path = DATA_PATH

    def make_subdir(self, name: str) -> Path:
        """Make a subdirectory."""
        (path := self.path / name).mkdir(exist_ok=True)
        return path

    @cached_property
    def export_path(self) -> Path:
        """Return the staging path."""
        return self.make_subdir("export")

    @cached_property
    def staging_path(self) -> Path:
        """Return the staging path."""
        return self.make_subdir("staging")

    @cached_property
    def source_path_dict(self) -> dict[str, Path]:
        """Return a dictionary of source paths."""
        return {x.stem: x for x in RAW_PATH.glob("*.csv")}

    @cached_property
    def staging_path_dict(self) -> dict[str, Path]:
        """Return a dictionary of staging paths."""
        return {
            x.stem: (self.staging_path / f"landing_{x.stem}").with_suffix(".parquet")
            for x in self.source_path_dict.values()
        }


def get_staging_path_groups(
    data_dir: DataDirectory, queries: QueriesDirectory
) -> list[StagingPathGroup]:
    """Return a list of StagingPathGroup objects."""
    return [
        StagingPathGroup(
            source_path=data_dir.source_path_dict[name],
            query_path=queries.landing_query_dict[name],
            staging_path=staging_path,
        )
        for name, staging_path in data_dir.staging_path_dict.items()
    ]


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


def main(
    timer: Timer = None,
    replace: bool = True,
) -> None:
    """Main function."""

    if timer is None:
        timer = Timer()
    # Create a connection & all schemas
    cnxn = get_cnxn()
    timer.log_from_last("Connection & schemas")
    create_all_schemas(cnxn)

    # Load landing data
    data_dir = DataDirectory()
    queries = QueriesDirectory()
    load_landing_data(queries.landing_query_dict.keys(), cnxn)
    timer.log_from_last("Landing data")

    # Load non-landing data
    for query_path in tqdm(queries.get_sorted_nonlanding_query_paths()):
        if query_path.stem.startswith("_"):
            print(f"skipping {query_path.relative_to(queries.path)}")
            continue
        if check_sql_path_for_blacklist(query_path):
            raise ValueError(f"Blacklisted SQL in {query_path}")
        schema, table_name = get_schema_table_name(query_path)
        if schema not in SCHEMAS:
            raise ValueError(f"{schema} is not a valid schema in {SCHEMAS}")
        sql = get_create_object_command(
            schema, table_name, query_path.read_text(), orreplace=replace
        )
        print(
            f"Creating {schema}.{table_name} from {"/".join(query_path.parts[-3:])}",
            end="... ",
        )
        cnxn.execute(sql)
        timer.log_from_start(f"{schema}.{table_name}")

    # Export database
    [x.unlink() for x in data_dir.export_path.iterdir() if x.is_file()]
    cnxn.execute(f"""EXPORT DATABASE '{str(data_dir.export_path)}' (FORMAT PARQUET)""")
    timer.log_from_last("Export database")
    cnxn.close()


if __name__ == "__main__":
    main()
