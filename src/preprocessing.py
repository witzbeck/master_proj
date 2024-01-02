from dataclasses import dataclass, field

from numpy import ravel, ascontiguousarray
from pandas import DataFrame, Series
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from alexlib.df import filter_df
from alexlib.core import chkenv
from src.db_helpers import ProjectTable
from src.features import Features


@dataclass
class DataPrep:
    feat: Features = field()
    schema: str = field(default="first30")
    table: str = field(default="all_features")
    df_filter: tuple = field(default=None)

    @property
    def context(self) -> str:
        return chkenv("CONTEXT")

    @property
    def nrows(self) -> int:
        return chkenv("NROWS", type=int)

    @property
    def test_size(self) -> float:
        return chkenv("TEST_SIZE", type=float)

    @property
    def random_state(self) -> int:
        return chkenv("RANDOM_STATE", type=int)

    @property
    def simple_num_impute(self) -> bool:
        return chkenv("SIMPLE_NUM_IMPUTE", type=bool)

    def __post_init__(self) -> None:
        self.main_steps()

    cat_trans = Pipeline(
        [
            ("cat_imputer", SimpleImputer(strategy="constant", fill_value=0)),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    knn_num_trans = Pipeline(
        [("knn_num_imputer", KNNImputer()), ("scaler", StandardScaler())]
    )
    simp_num_trans = Pipeline(
        [
            ("num_imputer", SimpleImputer(strategy="constant", fill_value=0)),
            ("scaler", StandardScaler()),
        ]
    )
    bool_trans = Pipeline(
        [("bool_imputer", SimpleImputer(strategy="constant", fill_value=0))]
    )

    def get_data(self) -> DataFrame:
        self.data = ProjectTable(
            self.context, self.schema, self.table, nrows=self.nrows
        )
        return self.data.df

    def set_y(self) -> Series:
        y = self.df.loc[:, self.feat.to_predict_col]
        self.y_1d = ravel(y)
        return y

    def set_X(self) -> DataFrame:
        return self.df.loc[:, self.feat.keep_cols]

    def sort_cols(self):
        self.boolean_cols = self.feat.get_boolean_keep_cols()
        self.categorical_cols = self.feat.get_categorical_keep_cols()
        self.numeric_cols = self.feat.get_numeric_keep_cols()

    def set_preprocessor(self):
        if self.simple_num_impute:
            num_trans = DataPrep.simp_num_trans
        else:
            num_trans = DataPrep.knn_num_trans

        prep = ColumnTransformer(
            [
                ("categorical", DataPrep.cat_trans, self.categorical_cols),
                ("numeric", num_trans, self.numeric_cols),
                ("boolean", DataPrep.bool_trans, self.boolean_cols),
            ],
            remainder="drop",
        )
        return prep

    def set_test_sets(
        self,
        make_c_cont: bool = False,
        shuffle: bool = False
    ) -> None:
        rand_state = None if shuffle else self.random_state
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=rand_state
        )

        if make_c_cont:
            X_train = ascontiguousarray(X_train)
            X_test = ascontiguousarray(X_test)

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def main_steps(self):
        self.df = self.get_data()
        if self.df_filter is not None:
            self.df = filter_df(self.df, self.df_filter[0], self.df_filter[-1])
        self.y = self.set_y()
        self.X = self.set_X()
        self.sort_cols()
        self.preprocessor = self.set_preprocessor()
        self.set_test_sets()

    def __repr__(self):
        self.nrows = len(self.data.df)
        return f"nrows={self.nrows}, schema={self.schema}, table={self.table}"

    def get_save_attr(self) -> dict[str:int]:
        bools = len(self.boolean_cols)
        cats = len(self.categorical_cols)
        nums = len(self.numeric_cols)
        return {
            "nrows": self.nrows,
            "ncols": bools + cats + nums,
            "n_bool_cols": bools,
            "n_cat_cols": cats,
            "n_num_cols": nums,
            "test_size": self.test_size,
            "simple_num_impute": self.simple_num_impute,
            "source_schema": self.schema,
            "source_table": self.table,
        }

    def desc_col(self, *args, **kwargs):
        self.data.desc_col(*args, **kwargs)

    def desc_predict_col(self):
        self.desc_col(self.feat.to_predict_col)
