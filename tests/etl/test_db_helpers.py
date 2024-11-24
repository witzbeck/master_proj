from random import seed
from unittest.mock import patch

from duckdb import DuckDBPyConnection
from pandas import DataFrame, Series
from pytest import approx, fixture, raises

from etl.db_helpers import (
    Column,
    DbHelper,
    Table,
    get_onehot_case_line,
    get_table_abrv,
)


@fixture(scope="module")
def dbhelper(cnxn_with_landing_data: DuckDBPyConnection) -> DbHelper:
    return DbHelper(cnxn=cnxn_with_landing_data)


@fixture(scope="module")
def info_schema_df_from_db(dbhelper: DbHelper) -> DataFrame:
    return dbhelper.info_schema


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
    patch("etl.elt_config.get_info_schema_df") as mock_get_info_schema_df,
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

        db_helper = DbHelper(cnxn=mock_cnxn)
        df = db_helper.get_table("test_schema", "test_table", nrows=2)

        # Assertions
        mock_cnxn.execute.assert_called_with(
            "SELECT * FROM test_schema.test_table LIMIT 2"
        )
        assert isinstance(df, DataFrame)
        assert list(df.columns) == ["id", "name"]

    @patch("duckdb.DuckDBPyConnection")
    def test_dbhelper_run_object_command(mock_cnxn):
        db_helper = DbHelper(cnxn=mock_cnxn)
        db_helper.run_object_command(
            "DROP", "TABLE", "test_schema.test_table", "CASCADE"
        )

        # Assertions
        mock_cnxn.sql.assert_called_with("DROP TABLE test_schema.test_table CASCADE;")

    @patch("duckdb.DuckDBPyConnection")
    def test_dbhelper_drop_table(mock_cnxn):
        db_helper = DbHelper(cnxn=mock_cnxn)
        with patch.object(db_helper, "run_object_command") as mock_run_command:
            db_helper.drop_table("test_schema", "test_table")
            mock_run_command.assert_called_with(
                "DROP", "TABLE", "test_schema.test_table"
            )

    @patch("duckdb.DuckDBPyConnection")
    def test_dbhelper_drop_view(mock_cnxn):
        db_helper = DbHelper(cnxn=mock_cnxn)
        with patch.object(db_helper, "run_object_command") as mock_run_command:
            db_helper.drop_view("test_schema", "test_view")
            mock_run_command.assert_called_with("DROP", "VIEW", "test_schema.test_view")

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
