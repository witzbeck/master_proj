from duckdb import DuckDBPyConnection
from pandas import DataFrame
from pytest import fixture

from model.features import Features
from model.preprocessing import DataPrep

SCHEMA = "first30"
TABLE = "all_features"


@fixture(scope="module")
def schema():
    return SCHEMA


@fixture(scope="module")
def table():
    return TABLE


@fixture(scope="module")
def data(schema: str, table: str, cnxn: DuckDBPyConnection):
    return cnxn.sql(f"select * from {schema}.{table}").df()


@fixture(scope="module")
def features():
    return Features()


@fixture(scope="module")
def dataprep(data: DataFrame, features: Features):
    return DataPrep(data, features)
