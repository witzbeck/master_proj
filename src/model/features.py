# standard library imports
from os import getenv
from itertools import chain

# third party imports
from pandas import DataFrame

# local imports
from utils import filter_df, istrue, set_envs
from db_helpers import Table

if __name__ == '__main__':
    set_envs("model")
    print(getenv("PREDICT_COL"))


class Features:
    cat_cols = [
        "course_id",
        "module_id",
        "presentation_id",
    ]
    to_drop_cols = [
        "student_id",
        "unreg_date",
        "reg_date_dif"
        ]
    final_result_cols = [
        'final_result',
        'final_result_id',
        'is_pass_or_distinction',
        'is_distinction',
        'is_pass',
        'is_fail',
        'is_withdrawn',
        'is_withdraw_or_fail'
        ]

    def get_col_names(self,
                      df: DataFrame
                      ):
        return df.loc[:, self.field_col]

    def get_col_cat(self,
                    ind_col: str,
                    ind_val,
                    ):
        filtered_df = filter_df(self.tbl.df, ind_col, ind_val)
        return list(self.get_col_names(filtered_df))

    def set_col_cats(self):
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

    def get_keep_cols(self):
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
        return list(chain.from_iterable(keep_cols))

    def get_drop_cols(self):
        drop_cols = [
            Features.to_drop_cols,
            self.to_exclude,
            Features.final_result_cols,
        ]
        return list(chain.from_iterable(drop_cols))

    def set_cols(self) -> list:
        self.set_col_cats()
        self.drop_cols = list(set(self.get_drop_cols()))
        self.keep_cols = list(set(self.get_keep_cols()))
        return [x for x in self.keep_cols if x not in self.drop_cols]

    def __init__(self,
                 to_predict_col: str = getenv("PREDICT_COL"),
                 context: str = getenv("CONTEXT"),
                 schema: str = "eval",  # features view cur only on eval
                 table: str = "v_features",
                 field_col: str = "column_name",
                 use_all: bool = istrue(getenv("USE_ALL")),
                 use_academic: bool = istrue(getenv("USE_ACADEMIC")),
                 use_demographic: bool = istrue(getenv("USE_DEMOGRAPHIC")),
                 use_engagement: bool = istrue(getenv("USE_ENGAGEMENT")),
                 use_moments: bool = istrue(getenv("USE_MOMENTS")),
                 use_student_info: bool = istrue(getenv("USE_STUDENT_INFO")),
                 use_ids: bool = istrue(getenv("USE_IDS")),
                 use_text: bool = istrue(getenv("USE_TEXT")),
                 use_by_activity: bool = istrue(getenv("USE_BY_ACTIVITY")),
                 to_exclude: list = [],
                 to_include: list = [],
                 ):
        self.field_col = field_col
        self.tbl = Table(context, schema, table)
        self.all = self.get_col_names(self.tbl.df)
        self.demographic = self.get_col_cat("is_demographics", 1)
        self.academic = self.get_col_cat("is_academic", 1)
        self.engagement = self.get_col_cat("is_engagement", 1)
        self.to_predict_col = to_predict_col
        self.use_academic = use_academic
        self.use_demographic = use_demographic
        self.use_engagement = use_engagement
        if use_all:
            self.name = "all"
            self.use_academic = True
            self.use_demographic = True
            self.use_engagement = True
        elif use_academic:
            self.name = "academ"
        elif use_demographic:
            self.name = "demog"
        elif use_engagement:
            self.name = "engage"
        else:
            self.name = ""
        self.use_moments = use_moments
        self.use_student_info = use_student_info
        self.use_ids = use_ids
        self.use_text = use_text
        self.use_by_activity = use_by_activity
        self.to_exclude = to_exclude
        self.to_include = to_include
        self.set_cols()

    def __repr__(self):
        ncols = len(self.keep_cols)
        s, t = self.tbl.schema, self.tbl.table
        return f"{self.name} ncols={ncols}, schema={s}, table={t}"

    def get_save_attr(self):
        save_dict = {}
        save_dict["schema"] = self.tbl.schema
        save_dict["table"] = self.tbl.table
        d = dir(self)
        save_attr = [x for x in d if (x[:3] == "inc" or x[-3:] == "col")]
        for att in save_attr:
            save_dict[att] = getattr(self, att)
        return save_dict

    def get_boolean_keep_cols(self):
        return [x for x in self.keep_cols if x in self.bool]

    def get_categorical_keep_cols(self):
        self.categorical_cols = self.obj + self.ids
        return [x for x in self.keep_cols if x in self.categorical_cols]

    def get_numeric_keep_cols(self):
        non_numeric_cols = self.bool + self.obj + self.ids
        return [x for x in self.keep_cols if x not in non_numeric_cols]
