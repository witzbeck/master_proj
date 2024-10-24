from collections.abc import Generator
from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from logging import getLogger
from pathlib import Path

from duckdb import DuckDBPyConnection, connect
from pandas import DataFrame
from tqdm import tqdm

from alexlib.files import Directory, File
from alexlib.times import Timer

from utils.constants import DATA_PATH, DB_PATH, QUERY_PATH, RAW_PATH, SCHEMAS

logger = getLogger(__name__)

SQL_BLACKLIST = (
    "CREATE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "DELETE",
    "UPDATE",
    "INSERT",
    "INTO",
)
CREATE_MODEL_TYPES_TABLE = """
create or replace table model.types(
id integer primary key,
model_type text not null
);
"""
CREATE_MODEL_RUNS_TABLE = """
create or replace table model.runs (
    id integer primary key,
    iter_id integer not null,
    model_type_id integer not null,
    model_params json not null,
    timestamp timestamp not null
)
"""
CREATE_MODEL_RESULTS_TABLE = """
create or replace table model.results(
id integer primary key,
run_id integer not null,
iter_id integer not null,
mean_fit_time float not null,
std_fit_time float not null,
mean_score_time float not null,
std_score_time float not null,
mean_test_roc_auc float not null,
std_test_roc_auc float not null,
rank_test_roc_auc integer not null,
mean_test_accuracy float not null,
std_test_accuracy float not null
);
"""
CREATE_MODEL_FEATURES_TABLE = """
create or replace table model.features(
id integer primary key,
run_id integer not null,
to_predict_column text not null,
use_academic boolean not null,
use_demographic boolean not null,
use_engagement boolean not null,
use_moments boolean not null,
use_ids boolean not null,
use_text boolean not null,
use_by_activity boolean not null
);
"""
CREATE_MODEL_WARNINGS_TABLE = """
create or replace table model.warnings(
id integer primary key,
run_id integer not null,
warnings text not null
);
"""
CREATE_ANALYSIS_ABROCA_TABLE = """
create or replace table analysis.abroca(
index integer primary key,
run_id integer not null,
iter_id integer not null,
course_id integer not null,
is_stem boolean not null,
is_female boolean not null,
has_disability boolean not null
);
"""

CREATE_TABLES = (
    CREATE_MODEL_RUNS_TABLE,
    CREATE_MODEL_TYPES_TABLE,
    CREATE_MODEL_RESULTS_TABLE,
    CREATE_MODEL_FEATURES_TABLE,
    CREATE_MODEL_WARNINGS_TABLE,
    CREATE_ANALYSIS_ABROCA_TABLE,
)
SOURCE_TABLES = {
    "MODEL_RUNS",
    "MODEL_TYPES",
    "MODEL_RESULTS",
    "LANDING_ASSESSMENTS",
    "LANDING_COURSES",
    "LANDING_STUDENT_ASSESSMENT",
    "LANDING_STUDENT_INFO",
    "LANDING_STUDENT_REGISTRATION",
    "LANDING_STUDENT_VLE",
    "LANDING_VLE",
}


def get_csv_paths(parent_path: Path = RAW_PATH) -> list[Path]:
    """Return a list of CSV paths."""
    return list(parent_path.glob("*.csv"))


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
    for schema in tqdm(schemas, desc="Creating schemas"):
        create_schema(cnxn=cnxn, schema=schema)
    return cnxn


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

    @property
    def allsqlfiles(self) -> list[File]:
        """Return a list of all SQL files."""
        return [x for x in self.allchildfiles if x.path.suffix == ".sql"]

    def get_sorted_nonlanding_query_paths(self) -> list[Path]:
        return sorted(
            [x.path for x in self.allsqlfiles if "00_landing" not in x.path.parts],
            key=lambda x: str(x.parent),
        )

    @cached_property
    def path_lines_map(self) -> dict[Path, list[str]]:
        return {
            x.path: [line.strip().upper() for line in x.lines] for x in self.allsqlfiles
        }

    @cached_property
    def path_normalized_name_map(self) -> dict[str, set[str]]:
        return {file.path: file.path.stem.upper() for file in self.allsqlfiles}

    @cached_property
    def path_parent_order_map(self) -> dict[Path, int]:
        return {
            f.path: i
            for i, f in enumerate(
                sorted(self.allsqlfiles, key=lambda x: str(x.path.parent))
            )
        }

    @cached_property
    def path_source_map(self) -> dict[Path, set[str]]:
        # Get all lines with FROM or JOIN
        line_map = {
            path: [x for x in lines if "FROM " in x or "JOIN " in x]
            for path, lines in self.path_lines_map.items()
        }
        # Pair the index of FROM or JOIN with the line
        idx_map = {
            path: [
                (x.index("FROM "), x) if "FROM " in x else (x.index("JOIN "), x)
                for x in lines
            ]
            for path, lines in line_map.items()
        }
        # Slice the line to get the source
        return {
            path: {
                line[idx + 5 :].split()[0].strip(" ),;").replace(".", "_")
                for idx, line in idx_lines
                if len(line[idx + 5 :].split()[0]) > 3
                and "." in line[idx + 5 :].split()[0]
            }
            for path, idx_lines in idx_map.items()
        }

    @cached_property
    def target_source_df(self) -> DataFrame:
        df = DataFrame(
            chain.from_iterable(
                [
                    [
                        self.path_normalized_name_map[path],
                        source,
                        self.path_parent_order_map[path],
                    ]
                    for source in sources
                ]
                for path, sources in self.path_source_map.items()
            ),
            columns=["Target", "Source", "ParentOrder"],
        )
        df.loc[:, "ScaledParentOrder"] = (
            df.loc[:, "ParentOrder"] / df.loc[:, "ParentOrder"].max()
        )
        return df

    @cached_property
    def source_groupby(self) -> DataFrame:
        return (
            self.target_source_df.loc[:, ["Source", "Target"]]
            .groupby("Source")
            .count()
            .sort_values("Target", ascending=False)
        )

    @cached_property
    def source_ntargets_map(self) -> dict[str, int]:
        return self.source_groupby.to_dict()["Target"]

    @cached_property
    def target_groupby(self) -> DataFrame:
        return (
            self.target_source_df.loc[:, ["Source", "Target"]]
            .groupby("Target")
            .count()
            .sort_values("Source", ascending=False)
        )

    @cached_property
    def target_nsources_map(self) -> dict[str, int]:
        return self.target_groupby.to_dict()["Source"]

    @cached_property
    def sources_without_targets(self) -> set[str]:
        return (
            set(self.target_nsources_map.keys())
            - set(self.source_ntargets_map.keys())
            - SOURCE_TABLES
        )

    @cached_property
    def targets_without_sources(self) -> set[str]:
        return (
            set(self.source_ntargets_map.keys())
            - set(self.target_nsources_map.keys())
            - SOURCE_TABLES
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


def export_database(cnxn: DuckDBPyConnection, export_path: Path) -> None:
    """Export the database."""
    [x.unlink() for x in export_path.iterdir() if x.is_file()]
    cnxn.execute(f"""EXPORT DATABASE '{str(export_path)}' (FORMAT PARQUET)""")


def main(
    timer: Timer = None,
    replace: bool = True,
    export_db: bool = False,
) -> Generator[DuckDBPyConnection, None, None]:
    """Main function."""

    if timer is None:
        timer = Timer()
    # Create a connection & all schemas
    cnxn = get_cnxn()
    timer.log_from_last("Connection & schemas")
    create_all_schemas(cnxn)

    # Create model & analysis tables
    for sql in CREATE_TABLES:
        cnxn.execute(sql)

    # Load landing data
    data_dir = DataDirectory()
    queries = QueriesDirectory()
    load_landing_data(queries.landing_query_dict.keys(), cnxn)
    timer.log_from_last("Landing data")

    # Load non-landing data
    for query_path in tqdm(queries.get_sorted_nonlanding_query_paths()):
        if query_path.stem.startswith("_"):
            logger.info(f"skipping {query_path.relative_to(queries.path)}")
            continue
        if check_sql_path_for_blacklist(query_path):
            raise ValueError(f"Blacklisted SQL in {query_path}")
        schema, table_name = get_schema_table_name(query_path)
        if schema not in SCHEMAS:
            raise ValueError(f"{schema} is not a valid schema in {SCHEMAS}")
        sql = get_create_object_command(
            schema, table_name, query_path.read_text(), orreplace=replace
        )
        logger.info(
            f"Creating {schema}.{table_name} from {"/".join(query_path.parts[-3:])}",
            end="... ",
        )
        cnxn.execute(sql)
        timer.log_from_start(f"{schema}.{table_name}")

    if export_db:
        # Export database
        export_database(cnxn, data_dir.export_path)
        timer.log_from_last("Exported database")
    return cnxn
