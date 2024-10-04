from pathlib import Path

from duckdb import DuckDBPyConnection
from pandas import DataFrame
from pytest import FixtureRequest, fixture

from alexlib.files import Directory

from orm import SCHEMAS
from utils.constants import CSV_PATHS
from utils.elt_config import (
    DataDirectory,
    QueriesDirectory,
    get_all_schemas,
    get_all_table_names,
    get_info_schema_df,
)


@fixture(scope="module", params=SCHEMAS)
def schema(request: FixtureRequest) -> str:
    return request.param.stem


@fixture(scope="module", params=CSV_PATHS)
def csv_path(request: FixtureRequest) -> Path:
    return request.param


@fixture(scope="module")
def landing_table_name(csv_path: Path) -> str:
    return csv_path.stem


@fixture(scope="module")
def landing_table_name_with_schema(csv_path: Path) -> str:
    return f"landing.{csv_path.stem}"


@fixture(scope="module")
def info_schema_df(cnxn_with_landing_data: DuckDBPyConnection) -> DuckDBPyConnection:
    return get_info_schema_df(cnxn=cnxn_with_landing_data)


@fixture(scope="module")
def all_schemas(info_schema_df: DataFrame) -> DuckDBPyConnection:
    return get_all_schemas(info_schema_df=info_schema_df)


@fixture(scope="module")
def all_table_names(info_schema_df: DataFrame) -> DuckDBPyConnection:
    return get_all_table_names(info_schema_df=info_schema_df)


@fixture(scope="module")
def all_table_names_with_schema(info_schema_df: DataFrame) -> DuckDBPyConnection:
    return get_all_table_names(info_schema_df=info_schema_df, concat_schema=True)


def test_gets_cnxn(memory_cnxn: DuckDBPyConnection) -> None:
    assert memory_cnxn is not None
    assert isinstance(memory_cnxn, DuckDBPyConnection)


def test_info_schema_df(info_schema_df: DuckDBPyConnection) -> None:
    assert info_schema_df is not None
    assert isinstance(info_schema_df, DataFrame)
    assert not info_schema_df.empty, f"{info_schema_df}"


def test_all_schemas(all_schemas: DuckDBPyConnection) -> None:
    assert all_schemas is not None, f"{all_schemas}"
    assert all(isinstance(x, str) for x in all_schemas), f"{all_schemas}"


def test_all_table_names(all_table_names: DuckDBPyConnection) -> None:
    assert all_table_names is not None, f"{all_table_names}"
    assert all(isinstance(x, str) for x in all_table_names), f"{all_table_names}"


def test_get_all_table_names_with_schema(
    all_table_names_with_schema: DuckDBPyConnection,
) -> None:
    assert all_table_names_with_schema is not None, f"{all_table_names_with_schema}"
    assert all(
        isinstance(x, str) for x in all_table_names_with_schema
    ), f"{all_table_names_with_schema}"
    assert all(
        "." in x for x in all_table_names_with_schema
    ), f"{all_table_names_with_schema}"


def test_data_dir(data_dir: DataDirectory) -> None:
    assert data_dir is not None
    assert isinstance(data_dir, DataDirectory)
    assert data_dir.path.is_dir(), f"{data_dir.path}"


def test_queries_dir(queries_dir: QueriesDirectory) -> None:
    assert queries_dir is not None
    assert isinstance(queries_dir, QueriesDirectory)
    assert queries_dir.path.is_dir(), f"{queries_dir.path}"


def test_data_dir_staging_path(data_dir: DataDirectory) -> None:
    assert data_dir.staging_path.is_dir(), f"{data_dir.staging_path}"


def test_data_dir_source_path_dict(data_dir: DataDirectory) -> None:
    assert data_dir.source_path_dict is not None
    assert all(
        isinstance(x, Path) for x in data_dir.source_path_dict.values()
    ), f"{data_dir.source_path_dict}"
    assert all(
        x.is_file() for x in data_dir.source_path_dict.values()
    ), f"{data_dir.source_path_dict}"


def test_data_dir_staging_path_dict(data_dir: DataDirectory) -> None:
    assert data_dir.staging_path_dict is not None
    assert all(
        isinstance(x, Path) for x in data_dir.staging_path_dict.values()
    ), f"{data_dir.staging_path_dict}"
    assert all(
        x.is_file() for x in data_dir.staging_path_dict.values()
    ), f"{data_dir.staging_path_dict}"


def test_queries_dir_schema_dict(queries_dir: QueriesDirectory) -> None:
    assert queries_dir.schema_dict is not None


def test_queries_dir_schema_dict_has_all_subdirs(queries_dir: QueriesDirectory) -> None:
    assert all(
        isinstance(x, Directory) for x in queries_dir.schema_dict.values()
    ), f"{queries_dir.schema_dict}"


def test_queries_dir_schema_dict_has_valid_schema_names(
    queries_dir: QueriesDirectory,
) -> None:
    assert all(
        not x[0].isnumeric() for x in queries_dir.schema_dict.keys()
    ), f"{queries_dir.schema_dict}"


def test_queries_dir_schema_dict_has_only_sql_files(
    queries_dir: QueriesDirectory,
) -> None:
    assert all(
        x.istype(".sql") for x in queries_dir.landing_dir.filelist
    ), f"{queries_dir.landing_dir.filelist}"
