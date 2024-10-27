from dataclasses import dataclass, field
from functools import cached_property
from math import log
from random import choice

from matplotlib.axis import Axis
from matplotlib.figure import Figure
from matplotlib.pyplot import subplots, xticks
from numpy import ndarray
from pandas import DataFrame, Series
from seaborn import histplot
from tqdm import tqdm

from alexlib.maths import euclidean_distance as euclidean

from constants import QUERY_PATH

SCHEMAS = {x.name.split("_")[-1] for x in QUERY_PATH.iterdir() if x.is_dir()}


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
