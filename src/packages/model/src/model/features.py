from dataclasses import dataclass, field
from functools import cached_property
from itertools import chain
from random import choice

from duckdb import DuckDBPyConnection
from pandas import DataFrame

from alexlib.df import filter_df
from alexlib.iters import rm_pattern

from etl.elt_config import get_info_schema_df
from model.constants import (
    FEATURE_TABLE_NAME,
    FEATURE_TABLE_SCHEMA,
    FINAL_RESULT_COLUMNS,
    SPLIT_COLUMNS,
    TO_DROP_COLUMNS,
    USE_ACADEMIC,
    USE_BY_ACTIVITY,
    USE_DEMOGRAPHIC,
    USE_ENGAGEMENT,
    USE_IDS,
    USE_MOMENTS,
    USE_TEXT,
)


def wo_ids(x: str) -> str:
    """Remove _id from string."""
    return rm_pattern(x, "_id")


@dataclass
class Features:
    """A class to describe the features in a database table. Inherits from the ProjectTable class in the alexlib.db.objects module."""

    name: str
    schema: str = FEATURE_TABLE_SCHEMA
    table: str = FEATURE_TABLE_NAME
    field_col: str = "column_name"
    to_include: list[str] = field(default_factory=list)
    to_exclude: list[str] = field(default_factory=list)
    use_academic: bool = field(default=USE_ACADEMIC)
    use_demographic: bool = field(default=USE_DEMOGRAPHIC)
    use_engagement: bool = field(default=USE_ENGAGEMENT)
    use_moments: bool = field(default=USE_MOMENTS)
    use_ids: bool = field(default=USE_IDS)
    use_text: bool = field(default=USE_TEXT)
    use_by_activity: bool = field(default=USE_BY_ACTIVITY)

    @cached_property
    def info_schema(cnxn: DuckDBPyConnection) -> DataFrame:
        return get_info_schema_df(cnxn)

    def get_col_names(self) -> list:
        """Returns a list of column names from a DataFrame."""
        return self.df.loc[:, self.field_col].tolist()

    def get_col_cat(
        self,
        ind_col: str,
        ind_val,
    ) -> list:
        """Returns a list of column names from a DataFrame that match a given condition."""
        filtered_df = filter_df(self.tbl.df, ind_col, ind_val)
        return self.get_col_names(filtered_df)

    @property
    def all(self) -> list:
        """Returns a list of all column names in the DataFrame."""
        return self.get_col_names(self.tbl.df)

    @cached_property
    def obj(self) -> list:
        """Returns a list of object columns in the DataFrame."""
        return self.get_col_cat("is_obj", 1)

    @cached_property
    def ids(self) -> list:
        """Returns a list of ID columns in the DataFrame."""
        return self.get_col_cat("is_id", 1)

    @cached_property
    def bool(self) -> list:
        """Returns a list of boolean columns in the DataFrame."""
        return self.get_col_cat("is_bool", 1)

    @cached_property
    def num(self) -> list:
        """Returns a list of numeric columns in the DataFrame."""
        return [x for x in self.all if x not in self.obj + self.bool]

    @cached_property
    def keep_cols(self) -> set[str]:
        """Returns a list of columns to keep in the DataFrame."""
        keep_cols = [self.to_include]
        if self.use_academic:
            academic = self.get_col_cat("is_academic", 1)
            keep_cols.append(academic)
        if self.use_demographic:
            demographic = self.get_col_cat("is_demographics", 1)
            keep_cols.append(demographic)
        if self.use_engagement:
            engagement = self.get_col_cat("is_engagement", 1)
            keep_cols.append(engagement)
        if self.use_moments:
            moment = self.get_col_cat("is_moment", 1)
            keep_cols.append(moment)
        if self.use_ids:
            ids = self.get_col_cat("is_id", 1)
            keep_cols.append(ids)
        if self.use_text:
            obj = self.get_col_cat("is_obj", 1)
            keep_cols.append(obj)
        if self.use_by_activity:
            by_activity = self.get_col_cat("is_by_activity", 1)
            keep_cols.append(by_activity)
        return set(chain.from_iterable(keep_cols))

    @property
    def drop_cols(self) -> set[str]:
        """Returns a list of columns to drop in the DataFrame."""
        return set(
            chain.from_iterable([
                TO_DROP_COLUMNS,
                self.to_exclude,
                FINAL_RESULT_COLUMNS,
            ])
        )

    @property
    def columns(self) -> list:
        """Sets the columns to keep and drop in the DataFrame. Returns a list of columns to keep."""
        return [x for x in self.keep_cols if x not in self.drop_cols]

    def __repr__(self) -> str:
        """Returns a string representation of the Features object."""
        ncols = len(self.keep_cols)
        return f"{self.name} ncols={ncols}, schema={self.schema}, table={self.table}"

    def get_save_attr(self) -> dict[str:int]:
        """Returns a dictionary of attributes to save."""
        save_dict = {
            "schema": self.schema,
            "table": self.table,
        }
        save_attr = {
            x: self.x for x in dir(self) if (x[:3] == "inc" or x[-3:] == "col")
        }
        save_dict.update(save_attr)
        return save_dict

    def get_boolean_keep_cols(self) -> list:
        """Returns a list of boolean columns to keep."""
        return [x for x in self.keep_cols if x in self.bool]

    def get_categorical_keep_cols(self) -> list:
        """Returns a list of categorical columns to keep."""
        self.categorical_cols = self.obj + self.ids
        return [x for x in self.keep_cols if x in self.categorical_cols]

    def get_numeric_keep_cols(self) -> list:
        """Returns a list of numeric columns to keep."""
        non_numeric_cols = self.bool + self.obj + self.ids
        return [x for x in self.keep_cols if x not in non_numeric_cols]

    @classmethod
    def demographic(cls, df: DataFrame) -> "Features":
        return cls(
            name="demographic", df=df, to_include=SPLIT_COLUMNS, use_demographic=True
        )

    @classmethod
    def engagement(cls, df: DataFrame) -> "Features":
        return cls(
            name="engagement", df=df, to_include=SPLIT_COLUMNS, use_engagement=True
        )

    @classmethod
    def academic(cls, df: DataFrame) -> "Features":
        return cls(name="academic", df=df, to_include=SPLIT_COLUMNS, use_academic=True)

    @classmethod
    def use_all(cls, df: DataFrame) -> "Features":
        return cls(
            name="all",
            df=df,
            to_include=SPLIT_COLUMNS,
            use_demographic=True,
            use_engagement=True,
            use_academic=True,
        )

    @classmethod
    def rand(df: DataFrame) -> "Features":
        """Returns a dictionary of Features objects."""
        choices = ["demographic", "engagement", "academic", "all"]
        name = choice(choices)
        func = {
            "demographic": Features.demographic,
            "engagement": Features.engagement,
            "academic": Features.academic,
            "all": Features.use_all,
        }[name]
        return func(df)


def get_feature_dict(df: DataFrame) -> dict[str, Features]:
    """Returns a dictionary of Features objects."""
    return {
        "demographic": Features.demographic(df),
        "engagement": Features.engagement(df),
        "academic": Features.academic(df),
        "all": Features.use_all(df),
    }
