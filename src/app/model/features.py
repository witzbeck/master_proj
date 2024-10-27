from dataclasses import dataclass, field
from functools import cached_property
from itertools import chain

from pandas import DataFrame

from alexlib.df import filter_df
from alexlib.iters import rm_pattern

from constants import (
    USE_ACADEMIC,
    USE_ALL,
    USE_BY_ACTIVITY,
    USE_DEMOGRAPHIC,
    USE_ENGAGEMENT,
    USE_IDS,
    USE_MOMENTS,
    USE_TEXT,
)

CATEGORY_COLUMNS = (
    "course_id",
    "module_id",
    "presentation_id",
)
TO_DROP_COLUMNS = ("student_id", "unreg_date", "reg_date_dif")
FINAL_RESULT_COLUMNS = (
    "final_result",
    "final_result_id",
    "is_pass_or_distinction",
    "is_distinction",
    "is_pass",
    "is_fail",
    "is_withdrawn",
    "is_withdraw_or_fail",
)
SPLIT_COLUMNS = ("is_stem", "is_female", "has_disability")


def wo_ids(x: str) -> str:
    """Remove _id from string."""
    return rm_pattern(x, "_id")


@dataclass
class Features:
    """A class to describe the features in a database table. Inherits from the ProjectTable class in the alexlib.db.objects module."""

    df: DataFrame
    schema: str = "eval"
    table: str = "v_features"
    field_col: str = "column_name"
    to_include: list[str] = field(default_factory=list)
    to_exclude: list[str] = field(default_factory=list)

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
        if USE_ACADEMIC:
            academic = self.get_col_cat("is_academic", 1)
            keep_cols.append(academic)
        if USE_DEMOGRAPHIC:
            demographic = self.get_col_cat("is_demographics", 1)
            keep_cols.append(demographic)
        if USE_ENGAGEMENT:
            engagement = self.get_col_cat("is_engagement", 1)
            keep_cols.append(engagement)
        if USE_MOMENTS:
            moment = self.get_col_cat("is_moment", 1)
            keep_cols.append(moment)
        if USE_IDS:
            ids = self.get_col_cat("is_id", 1)
            keep_cols.append(ids)
        if USE_TEXT:
            obj = self.get_col_cat("is_obj", 1)
            keep_cols.append(obj)
        if USE_BY_ACTIVITY:
            by_activity = self.get_col_cat("is_by_activity", 1)
            keep_cols.append(by_activity)
        return set(chain.from_iterable(keep_cols))

    @property
    def drop_cols(self) -> set[str]:
        """Returns a list of columns to drop in the DataFrame."""
        return set(
            chain.from_iterable(
                [
                    TO_DROP_COLUMNS,
                    self.to_exclude,
                    FINAL_RESULT_COLUMNS,
                ]
            )
        )

    @property
    def columns(self) -> list:
        """Sets the columns to keep and drop in the DataFrame. Returns a list of columns to keep."""
        return [x for x in self.keep_cols if x not in self.drop_cols]

    def __post_init__(self) -> None:
        """Initializes the Features object."""
        self.demographic = self.get_col_cat("is_demographics", 1)
        self.academic = self.get_col_cat("is_academic", 1)
        self.engagement = self.get_col_cat("is_engagement", 1)
        if USE_ALL:
            self.name = "all"
            self.use_academic = True
            self.use_demographic = True
            self.use_engagement = True
        elif self.use_academic:
            self.name = "academ"
            self.use_academic = True
        elif self.use_demographic:
            self.name = "demog"
            self.use_demographic = True
        elif self.use_engagement:
            self.name = "engage"
            self.use_engagement = True
        else:
            raise ValueError("No features selected.")

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
