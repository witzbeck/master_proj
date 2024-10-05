from dataclasses import dataclass, field
from functools import cached_property
from math import log
from pathlib import Path
from random import choice

from duckdb import DuckDBPyConnection
from matplotlib.axis import Axis
from matplotlib.figure import Figure
from matplotlib.pyplot import subplots, xticks
from numpy import ndarray
from pandas import DataFrame, Series
from seaborn import histplot
from tqdm import tqdm

from alexlib.core import to_clipboard
from alexlib.df import get_distinct_col_vals
from alexlib.maths import euclidean_distance as euclidean

from utils.elt_config import get_info_schema_df


def get_onehot_case_line(col: str, val: str):
    return f"CASE WHEN {col} = '{val}' THEN 1 ELSE 0 END AS is_{val}"


def get_table_abrv(table_name: str, sep: str = "_") -> str:
    """Get the abbreviation for a table name."""
    return "".join([x[0] for x in table_name.split(sep)])


@dataclass
class DbHelper:
    cnxn: DuckDBPyConnection = field(default_factory=DuckDBPyConnection)

    @property
    def info_schema(self) -> DataFrame:
        return get_info_schema_df(self.cnxn)

    def generate_select_query(
        self,
        schema: str,
        table: str,
        destination: Path = None,
        overwrite: bool = False,
    ) -> Path:
        df = self.info_schema
        if df.empty:
            raise ValueError("Object does not exist")
        abrv = get_table_abrv(table)

        cols = df["column_name"].tolist()
        lines = ["SELECT\n"]
        lines.extend([f"    {abrv}.{col}," for col in cols[:-1]])
        lines.append(f"    {abrv}.{cols[-1]}\n")
        lines.append(f"FROM {schema}.{table} {abrv}")
        query = "\n".join(lines)

        if destination is None:
            to_clipboard(query)
            return None
        else:
            filename = f"select_{schema}_{table}.sql"
            filepath = destination / filename

            if filepath.exists() and not overwrite:
                raise FileExistsError(
                    "File already exists. Use overwrite=True to overwrite."
                )
            filepath.write_text(query)
            return filepath

    # Add missing get_table method
    def get_table(self, schema: str, table: str, nrows: int = None) -> DataFrame:
        limit_clause = f"LIMIT {nrows}" if nrows else ""
        query = f"SELECT * FROM {schema}.{table} {limit_clause}"
        return self.cnxn.execute(query).fetchdf()

    def run_object_command(
        self,
        command: str,
        obj_type: str,
        obj_name: str,
        addl_cmd: str = "",
    ) -> None:
        sql = f"{command} {obj_type} {obj_name} {addl_cmd};"
        self.cnxn.sql(sql)

    def drop_table(self, schema: str, table: str):
        object_name = f"{schema}.{table}"
        self.run_object_command("DROP", "TABLE", object_name)

    def drop_view(self, schema: str, view: str):
        object_name = f"{schema}.{view}"
        self.run_object_command("DROP", "VIEW", object_name)


def create_onehot_view(
    cnxn: DuckDBPyConnection, schema: str, table: str, command: str = "create view"
) -> str:
    df = cnxn.sql(f"select * from {schema}.{table}").df()
    dist_col = [x for x in df.columns if x[-2:] != "id"][0]
    id_col = [x for x in df.columns if x != dist_col][0]
    dist_vals = get_distinct_col_vals(df, dist_col)

    first_line = f"{command} {schema}.v_{table}_onehot as select\n"
    lines = [first_line]
    lines.append(f" {id_col}\n")
    lines.append(f",{dist_col}\n")

    for val in dist_vals:
        com = ","
        new_col = f"is_{val}".replace(" ", "_")
        new_col = new_col.replace("%", "_percent")
        new_col = new_col.replace("-", "_")
        new_col = new_col.replace("<", "_less")
        new_col = new_col.replace("=", "_equal")
        new_col = new_col.replace(">", "_greater")
        case_stmt = get_onehot_case_line(dist_col, val)
        lines.append(f"{com}{case_stmt} {new_col}\n")
    lines.append(f"from {schema}.{table}")
    return "".join(lines)


@dataclass
class Column:
    schema: str
    table: str
    name: str
    series: Series
    is_id: bool = False
    calc_desc: bool = False

    def __post_init__(self):
        """Set the is_id attribute."""
        self.is_id = self.name.lower().endswith("_id")

    def __len__(self) -> int:
        """Get the length of the series."""
        return len(self.series)

    def __repr__(self) -> str:
        """Get the full name of the column."""
        return ".".join([x for x in [self.schema, self.table, self.name] if x])

    @cached_property
    def unique_vals(self) -> ndarray:
        """Get the unique values in the series."""
        return self.series.unique()

    @cached_property
    def nunique(self) -> int:
        """Get the number of unique values in the series."""
        return len(self.unique_vals)

    @property
    def frequency_range(self) -> int:
        """Get the range of frequencies for the unique values."""
        return max(self.frequencies) - min(self.frequencies)

    def auto_xtick_angle(
        self,
        ndist_min: int = 5,
        ndist_mult: int = 2,
        len_min: int = 50,
        len_mult: int = 2,
        range_min: int = 100,
        range_mult: int = 2,
        text_min: int = 30,
        text_mult: int = 2,
        max_angle: int = 45,
    ) -> int:
        """Automatically determine the xtick angle for a histogram."""
        # ndist_min: minimum number of distinct values
        if self.nunique < ndist_min:
            return 0
        # ndist_mult: multiplier for number of distinct values
        ndist_prod = ndist_mult * self.nunique

        # text_min: minimum number of characters in unique values
        text_len = sum(len(str(x)) for x in self.unique_vals)
        if text_len > text_min:
            text_prod = text_mult * log(text_len)
        else:
            return 0

        # len_min: minimum length of series
        _len = len(self)
        len_prod = 0 if _len < len_min else log(_len) * len_mult

        # range_min: minimum range of frequencies
        rng = 0 if self.frequency_range < range_min else log(self.frequency_range)
        logrange_prod = range_mult * rng

        # Calculate the angle
        to_pyth = [len_prod, ndist_prod, logrange_prod, text_prod]
        calc_angle = int(euclidean(to_pyth))
        return max_angle if calc_angle > max_angle else calc_angle

    @cached_property
    def frequencies(self) -> list[int]:
        """Get the frequency of each unique value in the series."""
        return [sum(self.series == x) for x in self.unique_vals]

    @cached_property
    def proportions(self) -> list[float]:
        """Get the proportion of each unique value in the series."""
        len_ = len(self)
        return [f / len_ for f in self.frequencies]

    @cached_property
    def proportions_df(self) -> DataFrame:
        return DataFrame.from_dict(
            {
                "value": self.unique_vals,
                "frequency": self.frequencies,
                "proportion": self.proportions,
            }
        )

    @property
    def nnulls(self) -> int:
        """Get the number of null values in the series."""
        return sum(self.series.isna())

    def desc(  # noqa: C901
        self,
        show_props: bool = False,
        show_nulls: bool = False,
        show_series_desc: bool = False,
        show_hist: bool = False,
        histplot_kwargs: dict = None,
    ) -> tuple[Figure, Axis]:
        """Describe the column."""
        print(f"Describing {repr(self)}\n")
        if self.nunique < 31 and show_props:
            print("Proportions:\n", self.proportions_df, "\n")
        if show_nulls:
            print(f"Null count: {self.nnulls}")
        if show_series_desc:
            print(self.series.describe(), "\n")
        if show_hist and not self.is_id and self.nunique <= 31:
            xtick_angle = self.auto_xtick_angle()
        else:
            xtick_angle = 0
        if show_hist:
            fig, ax = subplots(
                nrows=1,
                ncols=1,
                figsize=(5, 4),
                dpi=200,
            )
            kwargs = histplot_kwargs if histplot_kwargs else {}
            histplot(self.series, ax=ax, **kwargs)
            xticks(rotation=xtick_angle)
            return fig, ax


@dataclass
class Table:
    schema: str
    name: str
    df: DataFrame
    calc_desc: bool = False
    columns: dict[str, Column] = field(init=False)

    @property
    def ncolumns(self) -> int:
        return len(self.df.columns)

    def get_columns(self) -> dict[str, Column]:
        return {
            x: Column(self.schema, self.name, x, self.df.loc[:, x])
            for x in self.df.columns
        }

    def __post_init__(self):
        self.columns = self.get_columns()

    @property
    def rand_column(self) -> Column:
        return choice(list(self.columns.values()))

    def desc_all_cols(
        self,
        show_props: bool = False,
        show_nulls: bool = False,
        show_series_desc: bool = False,
        show_hist: bool = False,
        histplot_kwargs: dict = None,
    ) -> None:
        for i, col in tqdm(enumerate(self.df.columns)):
            print(f"({i + 1}/{self.ncolumns})")
            column = self.columns[col]
            column.desc(
                show_props=show_props,
                show_nulls=show_nulls,
                show_series_desc=show_series_desc,
                show_hist=show_hist,
                histplot_kwargs=histplot_kwargs,
            )
