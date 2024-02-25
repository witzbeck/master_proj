from pandas import DataFrame

from alexlib.core import chkenv
from alexlib.df import filter_df
from alexlib.iters import rm_pattern, link
from src.db_helpers import ProjectTable

if __name__ == "__main__":
    from setup import config

    config


def wo_ids(x: str) -> str:
    """Remove _id from string."""
    return rm_pattern(x, "_id")


class Features:
    """A class to describe the features in a database table. Inherits from the ProjectTable class in the alexlib.db.objects module."""

    cat_cols = [
        "course_id",
        "module_id",
        "presentation_id",
    ]
    to_drop_cols = ["student_id", "unreg_date", "reg_date_dif"]
    final_result_cols = [
        "final_result",
        "final_result_id",
        "is_pass_or_distinction",
        "is_distinction",
        "is_pass",
        "is_fail",
        "is_withdrawn",
        "is_withdraw_or_fail",
    ]

    def get_col_names(self, df: DataFrame) -> list:
        """Returns a list of column names from a DataFrame."""
        return df.loc[:, self.field_col]

    def get_col_cat(
        self,
        ind_col: str,
        ind_val,
    ) -> list:
        """Returns a list of column names from a DataFrame that match a given condition."""
        filtered_df = filter_df(self.tbl.df, ind_col, ind_val)
        return list(self.get_col_names(filtered_df))

    def set_col_cats(self) -> None:
        """Sets the column categories for the Features object."""
        self.all = self.get_col_names(self.tbl.df)
        self.demographic = self.get_col_cat("is_demographics", 1)
        self.academic = self.get_col_cat("is_academic", 1)
        self.engagement = self.get_col_cat("is_engagement", 1)
        self.final_result = self.get_col_cat("is_final_result", 1)
        self.moment = self.get_col_cat("is_moment", 1)
        self.student_info = self.get_col_cat("is_student_info", 1)
        self.by_activity = self.get_col_cat("is_by_activity", 1)
        self.obj = self.get_col_cat("is_obj", 1)
        self.ids = self.get_col_cat("is_id", 1)
        self.bool = self.get_col_cat("is_bool", 1)
        self.num = [x for x in self.all if x not in self.obj + self.bool]

    def get_keep_cols(self) -> list:
        """Returns a list of columns to keep in the DataFrame."""
        keep_cols = [self.to_include]
        if self.use_academic:
            keep_cols.append(self.academic)
        if self.use_demographic:
            keep_cols.append(self.demographic)
        if self.use_engagement:
            keep_cols.append(self.engagement)
        if self.use_moments:
            keep_cols.append(self.moment)
        if self.use_student_info:
            keep_cols.append(self.student_info)
        if self.use_ids:
            keep_cols.append(self.ids)
        if self.use_text:
            keep_cols.append(self.obj)
        if self.use_by_activity:
            keep_cols.append(self.by_activity)
        return link(keep_cols)

    def get_drop_cols(self) -> list:
        """Returns a list of columns to drop in the DataFrame."""
        drop_cols = [
            Features.to_drop_cols,
            self.to_exclude,
            Features.final_result_cols,
        ]
        return link(drop_cols)

    def set_cols(self) -> list:
        """Sets the columns to keep and drop in the DataFrame. Returns a list of columns to keep."""
        self.set_col_cats()
        self.drop_cols = list(set(self.get_drop_cols()))
        self.keep_cols = list(set(self.get_keep_cols()))
        return [x for x in self.keep_cols if x not in self.drop_cols]

    @property
    def to_predict_col(self) -> str:
        """Returns the column to predict."""
        return chkenv("PREDICT_COL")

    @property
    def context(self) -> str:
        """Returns the context of the database table."""
        return chkenv("CONTEXT")

    @property
    def use_all(self) -> bool:
        """Returns True if the USE_ALL environment variable is set to True, else False."""
        return (chkenv("USE_ALL", astype=bool),)

    @property
    def use_academic(self) -> bool:
        """Returns True if the USE_ACADEMIC environment variable is set to True, else False."""
        return (chkenv("USE_ACADEMIC", astype=bool),)

    @property
    def use_demographic(self) -> bool:
        """Returns True if the USE_DEMOGRAPHIC environment variable is set to True, else False."""
        return (chkenv("USE_DEMOGRAPHIC", astype=bool),)

    @property
    def use_engagement(self) -> bool:
        """Returns True if the USE_ENGAGEMENT environment variable is set to True, else False."""
        return (chkenv("USE_ENGAGEMENT", astype=bool),)

    @property
    def use_moments(self) -> bool:
        """Returns True if the USE_MOMENTS environment variable is set to True, else False."""
        return (chkenv("USE_MOMENTS", astype=bool),)

    @property
    def use_stud_info(self) -> bool:
        """Returns True if the USE_STUDENT_INFO environment variable is set to True, else False."""
        return (chkenv("USE_STUDENT_INFO", astype=bool),)

    @property
    def use_ids(self) -> bool:
        """Returns True if the USE_IDS environment variable is set to True, else False."""
        return (chkenv("USE_IDS", astype=bool),)

    @property
    def use_text(self) -> bool:
        """Returns True if the USE_TEXT environment variable is set to True, else False."""
        return (chkenv("USE_TEXT", astype=bool),)

    @property
    def use_by_activity(self) -> bool:
        """Returns True if the USE_BY_ACTIVITY environment variable is set to True, else False."""
        return (chkenv("USE_BY_ACTIVITY", astype=bool),)

    def __init__(
        self,
        schema: str = "eval",  # features view cur only on eval
        table: str = "v_features",
        field_col: str = "column_name",
        to_include: list = [],
        to_exclude: list = [],
    ) -> None:
        """Initializes the Features object."""
        self.field_col = field_col
        self.tbl = ProjectTable(self.context, schema, table)
        self.all = self.get_col_names(self.tbl.df)
        self.demographic = self.get_col_cat("is_demographics", 1)
        self.academic = self.get_col_cat("is_academic", 1)
        self.engagement = self.get_col_cat("is_engagement", 1)
        if self.use_all:
            self.name = "all"
            self.use_academic = True
            self.use_demographic = True
            self.use_engagement = True
        elif self.use_academic:
            self.name = "academ"
        elif self.use_demographic:
            self.name = "demog"
        elif self.use_engagement:
            self.name = "engage"
        else:
            self.name = ""
        self.to_exclude = to_exclude
        self.to_include = to_include
        self.set_cols()

    def __repr__(self) -> str:
        """Returns a string representation of the Features object."""
        ncols = len(self.keep_cols)
        s, t = self.tbl.schema, self.tbl.table
        return f"{self.name} ncols={ncols}, schema={s}, table={t}"

    def get_save_attr(self) -> dict[str:int]:
        """Returns a dictionary of attributes to save."""
        save_dict = {}
        save_dict["schema"] = self.tbl.schema
        save_dict["table"] = self.tbl.table
        d = dir(self)
        save_attr = [x for x in d if (x[:3] == "inc" or x[-3:] == "col")]
        for att in save_attr:
            save_dict[att] = getattr(self, att)
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
