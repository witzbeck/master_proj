from functools import cached_property
from warnings import catch_warnings

from numpy import array
from pandas import DataFrame, Series
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold

from alexlib.core import chkenv
from src.analysis import RocCurve
from src.features import Features
from src.logger import Logger
from src.params import Params, overwrite_std_params
from src.preprocessing import DataPrep
from src.setup import random_state

if __name__ == "__main__":
    from setup import config
    config

LEFT, ROPE, RIGHT, OUT = range(-1, 3)


class ModelEngine:
    @property
    def n_splits(self) -> int:
        return chkenv("CV_NSPLITS", type=int)

    @property
    def n_repeats(self) -> int:
        return chkenv("CV_NREPEATS", type=int)

    @property
    def reduce_dim(self) -> bool:
        return chkenv("REDUCE_DIM", type=bool)

    @property
    def verbose(self) -> int:
        return chkenv("CV_VERBOSE", type=int)

    @property
    def simple_num_impute(self) -> bool:
        return chkenv("SIMPLE_NUM_IMPUTE", type=bool)

    @property
    def search_random(self) -> bool:
        return chkenv("SEARCH_RANDOM", type=bool)

    @cached_property
    def params(self) -> Params:
        return Params()

    @cached_property
    def feat(self) -> Features:
        return Features()

    @cached_property
    def crossval(self) -> RepeatedStratifiedKFold:
        return RepeatedStratifiedKFold(
            n_splits=self.n_splits,
            n_repeats=self.n_repeats,
            random_state=random_state
        )

    @cached_property
    def data(self):
        return DataPrep(
            self.feat,
            nrows=self.params.nrows,
            test_size=self.params.test_size,
            random_state=random_state,
            simpnum=self.simple_num_impute,
            df_filter=self.df_filter
        )

    @cached_property
    def pipeline(self) -> Pipeline:
        prep = ("preprocessing", self.data.preprocessor)
        var_thresh = ("var_thresh", VarianceThreshold())
        dim_reduce = ("dim_reduce", PCA(n_components="mle"))
        clf = ("clf", self.params.clf())
        steps = [prep, var_thresh, clf]
        if self.reduce_dim:
            steps.insert(2, dim_reduce)
        return Pipeline(steps)

    @cached_property
    def gridsearch(self) -> GridSearchCV:
        n_jobs = -1
        if self.search_random:
            gs = self.params.searchcv(
                self.pipe,
                self.params._dict,
                cv=self.crossval,
                pre_dispatch=self.params.pre_dispatch,
                n_iter=self.params.n_iter,
                scoring=["roc_auc"],
                refit=self.params.refit,
                n_jobs=n_jobs,
                verbose=self.verbose,
                random_state=self.params.random_state
            )
        else:
            gs = self.params.searchcv(
                self.pipe,
                self.params._dict,
                cv=self.crossval,
                pre_dispatch=self.params.pre_dispatch,
                scoring=["roc_auc"],
                refit=self.params.refit,
                n_jobs=n_jobs,
                verbose=self.verbose,
            )
        return gs

    @cached_property
    def logger(self) -> Logger:
        return Logger(self.params.model_type)

    def get_all_params_log(self) -> dict:
        all_params = {}
        p_keys = [
            x for x in self.gridsearch.cv_results_.keys()
            if x[:6] == "param_"
        ]
        for key in p_keys:
            all_params[key] = self.gridsearch.cv_results_[key]
        std_params = self.params.get_std_clf_params()
        return overwrite_std_params(all_params, std_params)

    def get_best_params_log(self) -> dict:
        std_params = self.params.get_std_clf_params()
        best_params = self.gridsearch.best_params_
        return overwrite_std_params(best_params, std_params, all=False)

    def set_params_log(self, all: bool = True) -> None:
        if all:
            log = self.get_all_params_log()
        else:
            log = self.get_best_params_log()
            log["n_splits"] = self.n_splits
            log["n_repeats"] = self.n_repeats
        self.logger.log_params(log)

    def get_feat_log(self) -> dict:
        return self.feat.get_save_attr()

    def set_feat_log(self) -> None:
        log = self.get_feat_log()
        self.logger.log_feat(log)

    def get_all_results_log(self) -> dict:
        return {
            k: v.tolist()
            for k, v in self.gridsearch.cv_results_.items()
            if k[:5] != "param"
        }

    def get_best_results_log(self):
        results_log = {}
        results_log["true_pos"] = self.conf_matrix[0][0]
        results_log["false_pos"] = self.conf_matrix[0][1]
        results_log["false_neg"] = self.conf_matrix[1][0]
        results_log["true_neg"] = self.conf_matrix[1][1]
        nonp_keys = [
            x for x in self.gridsearch.cv_results_.keys()
            if x[:5] not in ["param", "split"]
        ]
        for key in nonp_keys:
            results_log[key] = self.gridsearch.cv_results_[key][0]
        return results_log

    def set_results_log(self, all: bool = True) -> None:
        self.logger.log_results(
            self.get_all_results_log() if all else self.get_best_results_log()
        )

    def get_data_log(self):
        return self.data.get_save_attr()

    def set_data_log(self):
        log = self.get_data_log()
        self.logger.log_data(log)

    def log(self):
        self.logger.log_run()
        self.set_feat_log()
        self.set_data_log()
        self.set_params_log()
        self.set_results_log()

    def __init__(self, df_filter: tuple = None) -> None:
        self.df_filter = None if df_filter == -1 else df_filter

    def fit_data(self) -> GridSearchCV:
        print(f"Model Type: {self.params.model_type}")
        X_train = self.data.X_train
        y_train = self.data.y_train
        with catch_warnings(record=True) as caught_warnings:
            gsf = self.gridsearch.fit(X_train, y_train)
        if len(caught_warnings) > 0:
            warns = [str(x) for x in caught_warnings]
            self.logger.log_warn({"warnings": warns})
        return gsf

    def get_predictions(self) -> array:
        return self.gridsearch.predict(self.data.X_test)

    def get_probabilities(self, X_test: DataFrame) -> array:
        return self.gridsearch.predict_proba(X_test)

    def get_scores(self) -> array:
        y_true = list(self.data.y_test)
        y_pred = list(self.get_predictions())
        rng = range(len(y_true))
        scores = [1 if y_true[i] == y_pred[i] else 0 for i in rng]
        return array(scores)

    def test_data(self) -> None:
        y_true = self.data.y_test
        y_pred = self.get_predictions()
        self.report = classification_report(y_true, y_pred, zero_division=0)
        self.conf_matrix = confusion_matrix(y_true, y_pred)

    def get_roc_curve(self) -> RocCurve:
        y_true = self.data.y_test
        X_test = self.data.X_test
        yi = y_true.index
        gp = self.get_probabilities
        y_prob = Series([x[1] for x in gp(X_test)], index=yi)
        return RocCurve(y_true, y_prob, X_test)

    def set_roc_curve(self) -> None:
        self.roc_curve = self.get_roc_curve()

    def show_results(self) -> None:
        print(f"Best parameter set: {self.gridsearch.best_params_}\n")
        print(f"Best score: {self.gridsearch.best_score_}\n")
        print("Confustion Matrix\n", self.conf_matrix)
        print(self.report)

    def fit(
        self,
        fit: bool = True,
        test: bool = True,
        log: bool = False,
        roc: bool = True,
        show: bool = False,
        title: str = None
    ) -> None:
        if fit:
            self.fit_data()
        if test:
            self.test_data()
        if log:
            self.log()
        if roc:
            self.set_roc_curve()
        if show:
            self.show_results()
        if (show and roc):
            self.roc_curve.plot(_title=title)

    def fit_test_log(self) -> None:
        self.fit(log=True)

    def fit_test_log_show(self) -> None:
        self.fit(log=True, show=True)

    def get_abroca(
        self,
        split_col: str,
        plot: bool = True,
        ax=None
    ) -> dict[str: float]:
        abroca = self.roc_curve.get_abroca(split_col=split_col)
        if plot:
            abroca.plot(ax=ax)
        return {split_col: abroca.abroca}

    def get_abrocas(
        self,
        split_cols: list,
        **kwargs
    ) -> dict[str: float]:
        return {
            col: self.get_abroca(col, **kwargs)
            for col in split_cols
        }
