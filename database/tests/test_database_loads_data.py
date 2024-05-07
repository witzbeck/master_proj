from itertools import product
from pathlib import Path
from unittest import TestCase, main
from os import getenv

from pandas import DataFrame, read_csv
from sqlalchemy import Engine, create_engine

def table_exists(table_name: str, engine: Engine, schema: str = None) -> bool:
    conditions = " AND ".join([
        f"table_name = '{table_name}'",
        f"table_schema = '{schema}'" if schema else "TRUE"
    ])
    query = f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE ({conditions}));"
    return engine.execute(query).fetchone()[0]


class TestDatabaseLoadsData(TestCase):

    def setUp(self):
        self.db_name = getenv("POSTGRES_DB")
        self.db_user = getenv("POSTGRES_USER")
        self.db_password = getenv("POSTGRES_PASSWORD")
        self.db_host = "localhost"
        self.db_port = 5432
        self.url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        self.schema_path = Path(__file__).parent.parent / "source_data/oulad_info_schema.csv"

    def test_get_info_schema_csv(self):
        # Load info schema from CSV
        self.assertTrue(self.schema_path.exists())
        df = read_csv(self.schema_path)

        # Check data is a DataFrame
        self.assertIsInstance(df, DataFrame)

        # Check data is not empty
        self.assertFalse(df.empty)

    def test_data_has_expected_tables(self):
        # Load info schema from CSV
        df = read_csv(self.schema_path)
        engine = create_engine(self.url)
        SCHEMAS = ("landing", "staging")
        TABLES = set(df.loc[:, "table_name"])


        for schema, table in product(SCHEMAS, TABLES):
            # Check table exists in database
            self.assertTrue(table_exists(table, engine, schema=schema))

