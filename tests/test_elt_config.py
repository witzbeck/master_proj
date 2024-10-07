from pathlib import Path

from duckdb import DuckDBPyConnection
from pandas import DataFrame
from pytest import FixtureRequest, fixture

from alexlib.files import Directory, File

from orm import SCHEMAS
from utils.constants import CSV_PATHS
from utils.elt_config import (
    SQL_BLACKLIST,
    DataDirectory,
    QueriesDirectory,
    StagingPathGroup,
    check_sql_path_for_blacklist,
    get_all_schemas,
    get_all_table_names,
    get_create_object_command,
    get_info_schema_df,
    get_object_type,
    get_schema_table_name,
    get_staging_path_groups,
)


@fixture(scope="module", params=SCHEMAS)
def schema(request: FixtureRequest) -> str:
    return request.param


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
def all_schemas(cnxn_with_landing_data: DuckDBPyConnection) -> set[str]:
    return get_all_schemas(cnxn_with_landing_data)


@fixture(scope="module")
def all_table_names(cnxn_with_landing_data: DuckDBPyConnection) -> DuckDBPyConnection:
    return get_all_table_names(cnxn=cnxn_with_landing_data, concat_schema=False)


@fixture(scope="module")
def all_table_names_with_schema(
    cnxn_with_landing_data: DuckDBPyConnection,
) -> DuckDBPyConnection:
    return get_all_table_names(cnxn=cnxn_with_landing_data, concat_schema=True)


@fixture(scope="module")
def sorted_nonlanding_query_paths(queries_dir: QueriesDirectory) -> list[Path]:
    return queries_dir.get_sorted_nonlanding_query_paths()


def test_gets_cnxn(cnxn: DuckDBPyConnection) -> None:
    assert cnxn is not None
    assert isinstance(cnxn, DuckDBPyConnection)


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


def test_data_dir_export_path(data_dir: DataDirectory) -> None:
    assert data_dir.export_path.is_dir(), f"{data_dir.export_path}"


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


def test_sorted_nonlanding_query_paths_is(
    sorted_nonlanding_query_paths: list[Path],
) -> None:
    assert sorted_nonlanding_query_paths is not None


def test_sorted_nonlanding_query_paths_is_paths(
    sorted_nonlanding_query_paths: list[Path],
) -> None:
    assert all(
        isinstance(x, Path) for x in sorted_nonlanding_query_paths
    ), f"{sorted_nonlanding_query_paths}"


def test_sorted_nonlanding_query_paths_is_sql(
    sorted_nonlanding_query_paths: list[Path],
) -> None:
    assert all(
        x.suffix == ".sql" for x in sorted_nonlanding_query_paths
    ), f"{sorted_nonlanding_query_paths}"


def test_sorted_nonlanding_query_paths_is_nonlanding(
    sorted_nonlanding_query_paths: list[Path],
) -> None:
    assert all(
        "00_landing" not in x.parts for x in sorted_nonlanding_query_paths
    ), f"{sorted_nonlanding_query_paths}"


def test_sorted_nonlanding_query_paths_is_sorted(
    sorted_nonlanding_query_paths: list[Path],
) -> None:
    assert sorted_nonlanding_query_paths == sorted(
        sorted_nonlanding_query_paths, key=lambda x: str(x.parent)
    ), f"{sorted_nonlanding_query_paths}"


@fixture(scope="module")
def staging_path_groups(
    data_dir: DataDirectory, queries_dir: QueriesDirectory
) -> list[StagingPathGroup]:
    return get_staging_path_groups(data_dir, queries_dir)


def test_staging_path_groups_is_list(
    staging_path_groups: list[StagingPathGroup],
) -> None:
    assert staging_path_groups is not None
    assert isinstance(staging_path_groups, list), f"{staging_path_groups}"


def test_staging_path_groups_is_objects(
    staging_path_groups: list[StagingPathGroup],
) -> None:
    assert all(
        isinstance(x, StagingPathGroup) for x in staging_path_groups
    ), f"{staging_path_groups}"


def test_get_schema_table_name_with_path():
    query_path = Path("core_user_data.sql")
    schema, table_name = get_schema_table_name(query_path)
    assert schema == "core"
    assert table_name == "user_data"


def test_get_schema_table_name_with_file():
    query_path = File(Path("sales_transactions.sql"))
    schema, table_name = get_schema_table_name(query_path)
    assert schema == "sales"
    assert table_name == "transactions"


def test_get_schema_table_name_single_word():
    query_path = Path("public_table.sql")
    schema, table_name = get_schema_table_name(query_path)
    assert schema == "public"
    assert table_name == "table"


def test_get_schema_table_name_no_underscore():
    query_path = Path("public.sql")
    schema, table_name = get_schema_table_name(query_path)
    assert schema == "public"
    assert table_name == ""


def test_get_schema_table_name_leading_underscore():
    query_path = Path("_users_data.sql")
    schema, table_name = get_schema_table_name(query_path)
    assert schema == ""
    assert table_name == "users_data"


def test_get_schema_table_name_multiple_underscores():
    query_path = Path("finance_quarterly_reports_2021.sql")
    schema, table_name = get_schema_table_name(query_path)
    assert schema == "finance"
    assert table_name == "quarterly_reports_2021"


def test_check_sql_file_for_blacklist_no_blacklist(tmp_path: Path):
    sql_content = "SELECT * FROM users;"
    sql_file = tmp_path / "query.sql"
    sql_file.write_text(sql_content)
    sql_file = File(sql_file)
    result = check_sql_path_for_blacklist(sql_file, blacklist=SQL_BLACKLIST)
    assert result is False


def test_check_sql_path_for_blacklist_no_blacklist(tmp_path: Path):
    sql_content = "SELECT * FROM users;"
    sql_file = tmp_path / "query.sql"
    sql_file.write_text(sql_content)
    result = check_sql_path_for_blacklist(sql_file, blacklist=SQL_BLACKLIST)
    assert result is False


def test_check_sql_path_for_blacklist_with_blacklist(tmp_path):
    sql_content = "DELETE FROM users;"
    sql_file = tmp_path / "query.sql"
    sql_file.write_text(sql_content)
    result = check_sql_path_for_blacklist(sql_file, blacklist=SQL_BLACKLIST)
    assert result


def test_check_sql_path_for_blacklist_mixed_case(tmp_path):
    sql_content = "Drop TABLE users;"
    sql_file = tmp_path / "query.sql"
    sql_file.write_text(sql_content)
    result = check_sql_path_for_blacklist(sql_file, blacklist=SQL_BLACKLIST)
    assert result


def test_check_sql_path_for_blacklist_in_comments(tmp_path):
    sql_content = "-- This will DELETE the table\nSELECT * FROM users;"
    sql_file = tmp_path / "query.sql"
    sql_file.write_text(sql_content)
    result = check_sql_path_for_blacklist(sql_file, blacklist=SQL_BLACKLIST)
    assert result  # Since 'DELETE' is present in comments


def test_check_sql_path_for_blacklist_partial_match(tmp_path):
    sql_content = "SELECT * FROM dropped_items;"
    sql_file = tmp_path / "query.sql"
    sql_file.write_text(sql_content)
    result = check_sql_path_for_blacklist(sql_file, blacklist=("DROP",))
    assert result  # 'DROP' is a substring of 'DROPPED'


def test_get_object_type_table():
    assert get_object_type("sales_data") == "TABLE"


def test_get_object_type_view_lowercase():
    assert get_object_type("v_sales_data") == "VIEW"


def test_get_object_type_view_uppercase():
    assert get_object_type("V_sales_data") == "VIEW"


def test_get_object_type_view_mixed_case():
    assert get_object_type("V_Sales_Data") == "VIEW"


def test_get_create_object_command_default():
    sql = "SELECT * FROM users;"
    result = get_create_object_command("public", "users", sql)
    expected = "CREATE  TABLE IF NOT EXISTS public.users AS SELECT * FROM users;"
    assert result == expected


def test_get_create_object_command_or_replace():
    sql = "SELECT * FROM users;"
    result = get_create_object_command("public", "users", sql, orreplace=True)
    expected = "CREATE OR REPLACE TABLE  public.users AS SELECT * FROM users;"
    assert result == expected


def test_get_create_object_command_ifnotexists_false():
    sql = "SELECT * FROM users;"
    result = get_create_object_command("public", "users", sql, ifnotexists=False)
    expected = "CREATE  TABLE  public.users AS SELECT * FROM users;"
    assert result == expected


def test_get_create_object_command_view():
    sql = "SELECT * FROM users;"
    result = get_create_object_command("public", "v_users", sql, obj_type="VIEW")
    expected = "CREATE  VIEW IF NOT EXISTS public.v_users AS SELECT * FROM users;"
    assert result == expected


def test_get_create_object_command_with_all_options():
    sql = "SELECT * FROM users;"
    result = get_create_object_command(
        schema="public",
        table_name="users",
        sql=sql,
        obj_type="MATERIALIZED VIEW",
        ifnotexists=False,
        orreplace=True,
    )
    expected = (
        "CREATE OR REPLACE MATERIALIZED VIEW  public.users AS SELECT * FROM users;"
    )
    assert result == expected


def test_get_create_object_command_ifnotexists_ignored_with_orreplace():
    sql = "SELECT * FROM users;"
    result = get_create_object_command(
        "public", "users", sql, ifnotexists=True, orreplace=True
    )
    expected = "CREATE OR REPLACE TABLE  public.users AS SELECT * FROM users;"
    assert (
        result == expected
    )  # 'IF NOT EXISTS' should be ignored when 'OR REPLACE' is True


# def test_qdir_has_no_targets_without_sources(queries_dir: QueriesDirectory) -> None:
#    len_ = len(queries_dir.targets_without_sources)
#    assert (
#        len_ == 0
#    ), f"Targets Without Sources: {len_} | {queries_dir.targets_without_sources}"


@fixture(scope="module")
def target_names(queries_dir: QueriesDirectory) -> list[str]:
    return queries_dir.target_nsources_map.keys()


@fixture(scope="module")
def source_names(queries_dir: QueriesDirectory) -> list[str]:
    return queries_dir.source_ntargets_map.keys()


def test_target_names_without_view_code(target_names: list[str]) -> None:
    names = [x for x in target_names if "_V_" in x.upper()]
    assert not names, f"{len(names)} | {names}"


def test_source_names_without_view_code(source_names: list[str]) -> None:
    names = [x for x in source_names if "_V_" in x.upper()]
    assert not names, f"{len(names)} | {names}"
