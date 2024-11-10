from duckdb import DuckDBPyConnection
from pandas import DataFrame
from pytest import fixture

from model.constants import FEATURE_TABLE_NAME, FEATURE_TABLE_SCHEMA
from model.features import Features
from model.preprocessing import DataPrep


@fixture(scope="module")
def schema():
    return FEATURE_TABLE_SCHEMA


@fixture(scope="module")
def table():
    return FEATURE_TABLE_NAME


@fixture(scope="module")
def data(schema: str, table: str, cnxn: DuckDBPyConnection):
    return cnxn.sql(f"select * from {schema}.{table}").df()


@fixture(scope="module")
def features():
    return Features()


@fixture(scope="module")
def dataprep(data: DataFrame, features: Features):
    return DataPrep(data, features)
