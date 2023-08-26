# standard library imports
from math import log

# third party imports
from matplotlib.pyplot import xticks, subplots
from numpy.random import choice
from pandas import DataFrame, Series
from seaborn import histplot

from alexlib.db import Connection, Table, Column
from alexlib.df import series_col
from alexlib.envs import ConfigFile
from alexlib.maths import get_props, pyth

config = ConfigFile(name=".env.db")
__dbvars__ = [
    "DBNAME",
    "DBHOST",
    "DBPORT",
]


class ProjectColumn(Column):
    def is_id(col: str):
        return False if col[-3:] != "_id" else True

    def auto_xtick_angle(self,
                         ndist_min: int = 5,
                         ndist_mult: int = 2,
                         len_min: int = 50,
                         len_mult: int = 2,
                         range_min: int = 100,
                         range_mult: int = 2,
                         text_min: int = 30,
                         text_mult: int = 2
                         ):
        uni = list(self.series.unique())
        self.ndist = len(uni)
        if self.ndist < ndist_min:
            return 0
        self.ndist_prod = ndist_mult * self.ndist

        text_len = sum([len(str(x)) for x in uni])
        if text_len > text_min:
            logtext = log(text_len)
            self.text_prod = text_mult * logtext
        else:
            return 0

        _len = len(self.series)
        if _len > len_min:
            _len = log(_len)
            self.len_prod = len_mult * _len
        else:
            self.len_prod = 0

        freq_range = max(self.freqs) - min(self.freqs)
        if freq_range > range_min:
            _range = log(freq_range)
        else:
            _range = 0
        self.logrange_prod = range_mult * _range

        to_pyth = [
            self.len_prod,
            self.ndist_prod,
            self.logrange_prod,
            self.text_prod
        ]
        angle = int(pyth(to_pyth))
        if angle > 45:
            return 45
        else:
            return angle

    def __init__(self,
                 schema: str,
                 table: str,
                 col_name: str,
                 series: Series,
                 calc_desc: bool = False
                 ) -> None:
        self.schema = schema
        self.table = table
        self.col_name = col_name
        self.series = series
        self.is_id = Column.is_id(self.col_name)

    def desc(self,
             show_props: bool = False,
             show_nulls: bool = False,
             show_series_desc: bool = False,
             show_hist: bool = False,
             **kwargs
             ):
        try:
            to_pyth = [
                self.len_prod,
                self.ndist_prod,
                self.logrange_prod,
                self.text_prod
            ]
        except AttributeError:
            pass
        db_col = self.col_name
        if self.schema is not None:
            db_col = f"{self.schema}.{self.table}.{db_col}"
        print(f"Describing {db_col}\n")
        if (ndist := len(list(self.series.unique()))) < 31:
            self.props = get_props(self.series)
            self.freqs = self.props["frequency"].values
            self.distvals = self.props["value"].values
            self.n_vals = sum(self.freqs)
            if show_props:
                print("Proportions:\n", self.props, "\n")
        if show_nulls:
            self.n_nulls = sum(self.series.isna())
            print(f"Null count: {self.n_nulls}")
        if show_series_desc:
            print(self.series.describe(), "\n")
        if (show_hist and not self.is_id and ndist <= 31):
            try:
                print([round(x, 4) for x in to_pyth])
            except AttributeError:
                pass
            except UnboundLocalError:
                pass
            self.xtick_angle = self.auto_xtick_angle()
        else:
            self.xtick_angle = 0
        if show_hist:
            fig, ax = subplots(nrows=1,
                               ncols=1,
                               figsize=(5, 4),
                               dpi=200,
                               )
            histplot(self.series,
                     ax=ax,
                     **kwargs
                     )
            xticks(rotation=self.xtick_angle)
            return fig, ax


class ProjectTable(Table):
    def set_cols(self):
        self.col_names = self.df.columns
        self.ncols = len(self.col_names)
        self.col_series = {x: series_col(self.df, x) for x in self.col_names}
        s, t, c = self.schema, self.table, self.col_series
        d, n = self.calc_desc, self.col_names
        self.cols = {x: Column(s, t, x, c[x], calc_desc=d) for x in n}

    def set_funcs(self):
        self.rand_col = lambda: choice(list(self.cols.values()))
        self.head = lambda x: self.df.head(x)

    def __init__(self,
                 context: str,
                 schema: str,
                 table: str,
                 calc_desc: bool = False,
                 df: DataFrame = None,
                 nrows: int = None
                 ) -> None:
        self.schema = schema
        self.table = table
        if df is None:
            dbh = Connection.from_context(context)
            self.df = dbh.get_table(schema, table, nrows=nrows)
        else:
            self.df = df
        self.calc_desc = calc_desc
        self.set_cols()
        self.set_funcs()

    def desc_col(self, col: str, **kwargs):
        col = self.cols[col]
        col.desc(**kwargs)

    def desc_all_cols(self):
        for i, col in enumerate(self.col_names):
            print(f"({i+1}/{self.ncols})")
            self.desc_col(col, show_hist=False)

    @classmethod
    def from_df(cls,
                df: DataFrame,
                calc_desc: bool = False,
                context: str = None,
                schema: str = None,
                table: str = None,
                ):
        return cls(context, schema, table, calc_desc=calc_desc, df=df)
