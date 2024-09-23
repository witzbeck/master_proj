# standard library imports
from dataclasses import dataclass
from math import log

# third party imports
from matplotlib.pyplot import xticks, subplots
from pandas import Series
from seaborn import histplot

from alexlib.db.objects import Table, Column
from alexlib.maths import get_props, euclidean_distance as pyth
from setup import db_mgr as cnxn


class ProjectColumn(Column):
    """A class to describe a column in a database table. Inherits from the Column class in the alexlib.db.objects module."""

    @property
    def is_id(self) -> bool:
        """Returns True if the column name ends with '_id', else False."""
        return False if self.col_name[-3:] != "_id" else True

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
    ) -> int:
        """Returns the angle to rotate the x-axis labels in a histogram plot based on the number of unique values in the column, the length of the text in the unique values, the range of the frequency values, and the length of the series."""
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

        to_pyth = [self.len_prod, self.ndist_prod, self.logrange_prod, self.text_prod]
        angle = int(pyth(to_pyth))
        if angle > 45:
            return 45
        else:
            return angle

    def __init__(
        self,
        schema: str,
        table: str,
        col_name: str,
        series: Series,
    ) -> None:
        """Initializes the ProjectColumn object. Inherits from the Column class in the alexlib.db.objects module."""
        self.schema = schema
        self.table = table
        self.col_name = col_name
        self.series = series

    def desc(
        self,
        show_props: bool = False,
        show_nulls: bool = False,
        show_series_desc: bool = False,
        show_hist: bool = False,
        **kwargs,
    ) -> tuple:
        """Describes the column in the database table. Returns a tuple containing the figure and axis of the histogram plot."""
        try:
            to_pyth = [
                self.len_prod,
                self.ndist_prod,
                self.logrange_prod,
                self.text_prod,
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
        if show_hist and not self.is_id and ndist <= 31:
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
            fig, ax = subplots(
                nrows=1,
                ncols=1,
                figsize=(5, 4),
                dpi=200,
            )
            histplot(self.series, ax=ax, **kwargs)
            xticks(rotation=self.xtick_angle)
            return fig, ax


@dataclass
class ProjectTable(Table):
    """A class to describe a database table. Inherits from the Table class in the alexlib.db.objects module."""

    def __post_init__(self) -> None:
        """Initializes the ProjectTable object. Inherits from the Table class in the alexlib.db.objects module."""
        if self.df is None:
            self.df = cnxn.get_table(
                self.schema,
                self.name,
                nrows=self.nrows,
            )

    def desc_col(self, col: str, **kwargs) -> None:
        """Describes a column in the database table. Returns a tuple containing the figure and axis of the histogram plot."""
        col = self.cols[col]
        col.desc(**kwargs)

    def desc_all_cols(self) -> None:
        """Describes all columns in the database table."""
        for i, col in enumerate(self.col_names):
            print(f"({i+1}/{self.ncols})")
            self.desc_col(col, show_hist=False)
