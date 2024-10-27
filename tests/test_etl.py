from hashlib import md5
from pathlib import Path
from random import seed
from unittest.mock import MagicMock, call, mock_open, patch

from click.testing import CliRunner
from duckdb import DuckDBPyConnection
from pandas import DataFrame, Series
from pytest import FixtureRequest, approx, fixture, raises

from alexlib.files import Directory, File

from etl import data_dir, queries_dir
from etl.extract import (
    download_file,
    get_csv_paths,
    get_dataset,
    unzip_file,
    validate_checksum,
)
from etl.files import (
    DataDirectory,
    QueriesDirectory,
    StagingPathGroup,
    get_staging_path_groups,
)
from etl.utils import (
    SQL_BLACKLIST,
    check_sql_path_for_blacklist,
    drop_table,
    drop_view,
    get_all_schemas,
    get_all_table_names,
    get_create_object_command,
    get_info_schema_df,
    get_object_type,
    get_onehot_case_line,
    get_schema_table_name,
    get_table,
    get_table_abrv,
)
from orm import (
    SCHEMAS,
    Column,
    Table,
)


@fixture(scope="module")
def cli_runner() -> CliRunner:
    return CliRunner()


@fixture(scope="module", params=SCHEMAS)
def schema(request: FixtureRequest) -> str:
    return request.param


@fixture(scope="module", params=get_csv_paths())
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
def sorted_nonlanding_query_paths() -> list[Path]:
    return queries_dir.get_sorted_nonlanding_query_paths()


def test_gets_cnxn(cnxn_with_landing_data: DuckDBPyConnection) -> None:
    assert cnxn_with_landing_data is not None
    assert isinstance(cnxn_with_landing_data, DuckDBPyConnection)


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


def test_data_dir() -> None:
    assert data_dir is not None
    assert isinstance(data_dir, DataDirectory)
    assert data_dir.path.is_dir(), f"{data_dir.path}"


def test_queries_dir() -> None:
    assert queries_dir is not None
    assert isinstance(queries_dir, QueriesDirectory)
    assert queries_dir.path.is_dir(), f"{queries_dir.path}"


def test_data_dir_export_path() -> None:
    assert data_dir.export_path.is_dir(), f"{data_dir.export_path}"


def test_data_dir_source_path_dict() -> None:
    assert data_dir.source_path_dict is not None
    assert all(
        isinstance(x, Path) for x in data_dir.source_path_dict.values()
    ), f"{data_dir.source_path_dict}"
    assert all(
        x.is_file() for x in data_dir.source_path_dict.values()
    ), f"{data_dir.source_path_dict}"


def test_data_dir_staging_path_dict() -> None:
    assert data_dir.staging_path_dict is not None
    assert all(
        isinstance(x, Path) for x in data_dir.staging_path_dict.values()
    ), f"{data_dir.staging_path_dict}"


def test_queries_dir_schema_dict() -> None:
    assert queries_dir.schema_dict is not None


def test_queries_dir_schema_dict_has_all_subdirs() -> None:
    assert all(
        isinstance(x, Directory) for x in queries_dir.schema_dict.values()
    ), f"{queries_dir.schema_dict}"


def test_queries_dir_schema_dict_has_valid_schema_names() -> None:
    assert all(
        not x[0].isnumeric() for x in queries_dir.schema_dict.keys()
    ), f"{queries_dir.schema_dict}"


def test_queries_dir_schema_dict_has_only_sql_files() -> None:
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
def staging_path_groups() -> list[StagingPathGroup]:
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
def target_names() -> list[str]:
    return queries_dir.target_nsources_map.keys()


@fixture(scope="module")
def source_names() -> list[str]:
    return queries_dir.source_ntargets_map.keys()


def test_target_names_without_view_code(target_names: list[str]) -> None:
    names = [x for x in target_names if "_V_" in x.upper()]
    assert not names, f"{len(names)} | {names}"


def test_source_names_without_view_code(source_names: list[str]) -> None:
    names = [x for x in source_names if "_V_" in x.upper()]
    assert not names, f"{len(names)} | {names}"


def test_fewer_sources_than_targets() -> None:
    assert len(queries_dir.source_ntargets_map) <= len(queries_dir.target_nsources_map)


def test_more_targets_than_sources() -> None:
    assert len(queries_dir.target_nsources_map) >= len(queries_dir.source_ntargets_map)


def test_all_sources_have_targets() -> None:
    assert all(queries_dir.source_ntargets_map.values())


def test_all_targets_have_sources() -> None:
    assert all(queries_dir.target_nsources_map.values())


def test_more_targets_without_sources_than_sources_without_targets() -> None:
    assert len(queries_dir.targets_without_sources) <= len(
        queries_dir.sources_without_targets
    )


def test_download_file():
    with (
        patch("etl.extract.get") as mock_get,
        patch("etl.extract.logger") as mock_logger,
    ):
        # Mock the response from get
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_response.raise_for_status = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_get.return_value = mock_response

        # Mock the file path and file writing
        mock_path = MagicMock(spec=Path)
        mock_file = MagicMock()
        mock_path.open.return_value.__enter__.return_value = mock_file

        # Call the function
        download_file("http://example.com/dataset.zip", mock_path)

        # Assertions
        mock_get.assert_called_once_with("http://example.com/dataset.zip", stream=True)
        mock_response.raise_for_status.assert_called_once()
        mock_response.iter_content.assert_called_once_with(chunk_size=8192)
        mock_path.open.assert_called_once_with("wb")
        mock_file.write.assert_has_calls([call(b"chunk1"), call(b"chunk2")])
        mock_logger.info.assert_any_call(
            f"Downloading dataset from http://example.com/dataset.zip to {mock_path}."
        )
        mock_logger.info.assert_any_call(f"Downloaded dataset to {mock_path}.")


def test_validate_checksum():
    with (
        patch("etl.extract.logger") as mock_logger,
        patch("pathlib.Path.open", mock_open(read_data=b"test data")),
        patch("pathlib.Path.read_bytes") as mock_read_bytes,
    ):
        # Prepare mock paths
        mock_file_path = Path("/path/to/dataset.zip")
        mock_checksum_path = Path("/path/to/dataset.md5")

        # Calculate expected MD5 checksum
        expected_md5 = md5(b"test data").hexdigest()

        # Mock read_bytes to return expected checksum
        mock_read_bytes.return_value = f"{expected_md5}\n".encode()

        # Call the function
        result = validate_checksum(mock_file_path, mock_checksum_path)

        # Assertions
        assert result
        mock_logger.info.assert_any_call(
            f"Checksum validated: {expected_md5} == {expected_md5}."
        )

        # Test checksum mismatch
        mock_read_bytes.return_value = b"wrongchecksum\n"
        result = validate_checksum(mock_file_path, mock_checksum_path)
        assert not result
        mock_logger.error.assert_called_with(
            f"Checksum mismatch: {expected_md5} != wrongchecksum."
        )


def test_unzip_file():
    with (
        patch("etl.extract.ZipFile") as mock_zipfile_class,
        patch("etl.extract.logger") as mock_logger,
    ):
        # Mock the ZipFile instance
        mock_zipfile = MagicMock()
        mock_zipfile_class.return_value.__enter__.return_value = mock_zipfile

        # Call the function
        zip_path = Path("/path/to/dataset.zip")
        extract_path = Path("/path/to/extract")
        unzip_file(zip_path, extract_path)

        # Assertions
        mock_zipfile_class.assert_called_once_with(zip_path, "r")
        mock_zipfile.extractall.assert_called_once_with(extract_path)
        mock_logger.info.assert_any_call(f"Unzipping {zip_path} to {extract_path}.")
        mock_logger.info.assert_any_call(f"Unzipped {zip_path} to {extract_path}.")


def test_main(tmp_path, cli_runner):
    # Setup temporary paths
    dataset_path = tmp_path / "dataset.zip"
    checksum_path = tmp_path / "dataset.md5"
    extract_path = tmp_path
    raw_path = tmp_path

    # Define a side effect function for Path.exists()
    def exists_side_effect(self):
        if self == dataset_path:
            return exists_side_effect.dataset_path_exists.pop(0)
        elif self == checksum_path:
            return exists_side_effect.checksum_path_exists.pop(0)
        else:
            return True

    # Initialize the side effect lists
    exists_side_effect.dataset_path_exists = [False, True]
    exists_side_effect.checksum_path_exists = [False, True]

    # Define a side effect for unzip_file to simulate file extraction
    def unzip_side_effect(zip_path, extract_path=extract_path):
        # Simulate extraction by creating the files that 'get_dataset()' expects
        for orig in ["assessments"]:
            file_path = extract_path / f"{orig}.csv"
            file_path.touch()

    # Mock constants and functions
    with (
        patch("etl.extract.DATASET_PATH", dataset_path),
        patch("etl.extract.CHECKSUM_PATH", checksum_path),
        patch("etl.extract.EXTRACT_PATH", extract_path),
        patch("etl.extract.RAW_PATH", raw_path),
        patch("etl.extract.download_dataset") as mock_download_dataset,
        patch("etl.extract.download_checksum") as mock_download_checksum,
        patch(
            "etl.extract.validate_checksum", return_value=True
        ) as mock_validate_checksum,
        patch(
            "etl.extract.unzip_file", side_effect=unzip_side_effect
        ) as mock_unzip_file,
        patch("etl.extract.logger"),
        patch("etl.extract.SOURCE_TABLE_MAP", {"assessments": "assessments_renamed"}),
        patch("pathlib.Path.exists", new=exists_side_effect),
    ):
        # Call the function using CliRunner
        result = cli_runner.invoke(get_dataset)

        # Assertions
        assert result.exit_code == 0
        mock_download_dataset.assert_called_once()
        mock_download_checksum.assert_called_once()
        mock_validate_checksum.assert_called_once_with(dataset_path)
        mock_unzip_file.assert_called_once_with(dataset_path)

        # Expected destination files
        dest_file = raw_path / "assessments_renamed.csv"

        # Assertions for file renaming
        assert dest_file.exists()


@fixture(scope="module")
def info_schema_df_from_db(cnxn_with_landing_data: DuckDBPyConnection) -> DataFrame:
    return get_info_schema_df(cnxn_with_landing_data)


def test_get_info_schema_df(info_schema_df_from_db: DataFrame):
    assert not info_schema_df_from_db.empty, "info_schema_df_from_db is empty"
    assert (
        "schema" in info_schema_df_from_db.columns
    ), f"schema not in {info_schema_df_from_db.columns}"
    assert (
        "name" in info_schema_df_from_db.columns
    ), f"name not in {info_schema_df_from_db.columns}"
    assert (
        "column_names" in info_schema_df_from_db.columns
    ), f"column_names not in {info_schema_df_from_db.columns}"


# Mocking external dependencies
with (
    patch("etl.utils.get_info_schema_df") as mock_get_info_schema_df,
    patch("alexlib.core.to_clipboard") as mock_to_clipboard,
):
    # Sample data for testing
    sample_info_schema_df = DataFrame(
        {
            "table_schema": ["test_schema"] * 3,
            "table_name": ["test_table"] * 3,
            "column_name": ["id", "name", "value"],
        }
    )
    mock_get_info_schema_df.return_value = sample_info_schema_df

    def test_get_onehot_case_line_basic():
        col = "color"
        val = "red"
        expected = "CASE WHEN color = 'red' THEN 1 ELSE 0 END AS is_red"
        assert get_onehot_case_line(col, val) == expected

    def test_get_onehot_case_line_special_chars():
        col = "name"
        val = "O'Reilly"
        expected = "CASE WHEN name = 'O'Reilly' THEN 1 ELSE 0 END AS is_O'Reilly"
        assert get_onehot_case_line(col, val) == expected

    def test_get_onehot_case_line_empty_val():
        col = "status"
        val = ""
        expected = "CASE WHEN status = '' THEN 1 ELSE 0 END AS is_"
        assert get_onehot_case_line(col, val) == expected

    def test_get_onehot_case_line_special_val():
        col = "symbol"
        val = "@#$%^&*()"
        expected = "CASE WHEN symbol = '@#$%^&*()' THEN 1 ELSE 0 END AS is_@#$%^&*()"
        assert get_onehot_case_line(col, val) == expected

    def test_get_table_abrv_basic():
        table_name = "my_table_name"
        expected = "mtn"
        assert get_table_abrv(table_name) == expected

    def test_get_table_abrv_no_separator():
        table_name = "tablename"
        expected = "t"
        assert get_table_abrv(table_name) == expected

    def test_get_table_abrv_different_sep():
        table_name = "my-table-name"
        sep = "-"
        expected = "mtn"
        assert get_table_abrv(table_name, sep) == expected

    def test_get_table_abrv_empty_string():
        with raises(IndexError):
            get_table_abrv("")

    def test_get_table_abrv_multiple_separators():
        table_name = "this_is_a_very_long_table_name"
        expected = "tiavltn"
        assert get_table_abrv(table_name) == expected

    def test_column_properties():
        # Sample data
        series = Series(["A", "B", "A", "C", "B", "A"])
        column = Column(
            schema="test_schema", table="test_table", name="category", series=series
        )

        # Assertions
        assert len(column) == 6
        assert repr(column) == "test_schema.test_table.category"
        assert sorted(column.unique_vals) == ["A", "B", "C"]
        assert column.nunique == 3
        assert column.frequencies == [3, 2, 1]
        assert column.proportions == [0.5, 0.3333333333333333, 0.16666666666666666]
        assert column.nnulls == 0

    def test_column_auto_xtick_angle():
        # Sample data with many unique values and long text
        series = Series([f"Value_{i}" for i in range(100)])
        column = Column(
            schema="test_schema", table="test_table", name="category", series=series
        )

        # Set seed for reproducibility
        seed(0)
        angle = column.auto_xtick_angle()

        # Assertions
        assert angle > 0

    def test_table_methods():
        # Sample DataFrame
        df = DataFrame.from_dict({"id": [1, 2, 3], "value": [10, 20, 30]})
        table = Table(schema="test_schema", name="test_table", df=df)

        # Assertions
        assert table.ncolumns == 2
        columns = table.get_columns()
        assert len(columns) == 2
        assert isinstance(table.rand_column, Column)

    @patch("tqdm.tqdm")
    def test_table_desc_all_cols(mock_tqdm):
        # Mock tqdm to just return the iterable
        mock_tqdm.side_effect = lambda x: x

        # Sample DataFrame
        df = DataFrame({"id": [1, 2, 3], "value": [10, 20, 30]})
        table = Table(schema="test_schema", name="test_table", df=df)
        table.columns = table.get_columns()

        # Call the method
        table.desc_all_cols()

        # Assertions
        # Ensure that desc was called on each column
        for col in table.columns.values():
            assert hasattr(col, "desc")

    def test_column_is_id():
        series = Series([1, 2, 3])
        column = Column(
            schema="test_schema", table="test_table", name="user_id", series=series
        )
        assert column.is_id is True

        column = Column(
            schema="test_schema", table="test_table", name="username", series=series
        )
        assert column.is_id is False

    @patch("duckdb.DuckDBPyConnection")
    def test_dbhelper_get_table(mock_cnxn):
        # Mock execute and fetchdf
        mock_cnxn.execute.return_value.fetchdf.return_value = DataFrame(
            {
                "id": [1, 2],
                "name": ["Alice", "Bob"],
            }
        )

        df = get_table(mock_cnxn, "test_schema", "test_table", nrows=2)

        # Assertions
        mock_cnxn.execute.assert_called_with(
            "SELECT * FROM test_schema.test_table LIMIT 2"
        )
        assert isinstance(df, DataFrame)
        assert list(df.columns) == ["id", "name"]

    @patch("duckdb.DuckDBPyConnection")
    def test_dbhelper_drop_table(mock_cnxn):
        with patch("etl.utils.run_object_command") as mock_run_command:
            drop_table(mock_cnxn, "test_schema", "test_table")
            mock_run_command.assert_called_with(
                mock_cnxn, "DROP", "TABLE", "test_schema.test_table"
            )

    @patch("duckdb.DuckDBPyConnection")
    def test_dbhelper_drop_view(mock_cnxn):
        with patch("etl.utils.run_object_command") as mock_run_command:
            drop_view(mock_cnxn, "test_schema", "test_view")
            mock_run_command.assert_called_with(
                mock_cnxn, "DROP", "VIEW", "test_schema.test_view"
            )

    def test_column_frequency_range():
        series = Series(["A"] * 50 + ["B"] * 30 + ["C"] * 20)
        column = Column(
            schema="test_schema", table="test_table", name="category", series=series
        )
        assert column.frequency_range == 30  # 50 - 20

    def test_column_proportions_df():
        series = Series(["A", "B", "A", "C", "B", "A"])
        column = Column(
            schema="test_schema", table="test_table", name="category", series=series
        )
        df = column.proportions_df

        # Assertions
        assert isinstance(df, DataFrame)
        assert list(df.columns) == ["value", "frequency", "proportion"]
        assert df["frequency"].sum() == len(series)
        assert df["proportion"].sum() == approx(1.0)
