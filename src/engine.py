# standard library imports
from warnings import catch_warnings

# third party imports
from numpy import array
from pandas import DataFrame, Series

# preprocessing
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import Pipeline

# eval and postprocessing
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import RepeatedStratifiedKFold

# local imports
from alexlib.cnfg import chkenv
from alexlib.iters import keys
from analysis import RocCurve
from features import Features
from logger import Logger
from params import Params, overwrite_std_params
from preprocessing import DataPrep

if __name__ == "__main__":
    from setup import config
    config

LEFT, ROPE, RIGHT, OUT = range(-1, 3)


class ModelEngine:
    def get_crossval(
        self,
        n_splits=None,
        n_repeats=None
    ):
        if n_splits is None:
            n_splits = chkenv("CV_NSPLITS", type=int)
        if n_repeats is None:
            n_repeats = chkenv("CV_NREPEATS", type=int)
        rskf = RepeatedStratifiedKFold(
            n_splits=n_splits,
            n_repeats=n_repeats,
            random_state=self.params.random_state
        )
        self.n_splits = n_splits
        self.n_repeats = n_repeats
        return rskf

    def set_data(self):
        data = DataPrep(
            self.feat,
            nrows=self.params.nrows,
            test_size=self.params.test_size,
            random_state=self.params.random_state,
            simpnum=chkenv("SIMPLE_NUM_IMPUTE", type=bool),
            df_filter=self.df_filter
        )
        return data

    def get_pipe(self):
        prep = ("preprocessing", self.data.preprocessor)
        var_thresh = ("var_thresh", VarianceThreshold())
        dim_reduce = ("dim_reduce", PCA(n_components="mle"))
        clf = ("clf", self.params.clf())
        steps = [prep, var_thresh, clf]
        if self.reduce_dim:
            steps.insert(2, dim_reduce)
        return Pipeline(steps)

    def set_gridsearch(
        self,
        scoring: list = [
            "roc_auc",
        ],
        n_jobs: int = -1,
    ):
        verbose = self.verbose
        rand = chkenv("SEARCH_RANDOM", type=bool)
        if rand:
            gs = self.params.searchcv(
                self.pipe,
                self.params._dict,
                cv=self.crossval,
                pre_dispatch=self.params.pre_dispatch,
                n_iter=self.params.n_iter,
                scoring=scoring,
                refit=self.params.refit,
                n_jobs=n_jobs,
                verbose=verbose,
                random_state=self.params.random_state
            )
        else:
            gs = self.params.searchcv(
                self.pipe,
                self.params._dict,
                cv=self.crossval,
                pre_dispatch=self.params.pre_dispatch,
                scoring=scoring,
                refit=self.params.refit,
                n_jobs=n_jobs,
                verbose=verbose,
            )
        return gs

    def set_logger(self):
        self.logger = Logger(self.params.model_type)

    def get_all_params_log(self):
        all_params = {}
        cv_keys = keys(self.gridsearch.cv_results_)
        p_keys = [x for x in cv_keys if x[:6] == "param_"]
        for key in p_keys:
            all_params[key] = self.gridsearch.cv_results_[key]
        std_params = self.params.get_std_clf_params()
        return overwrite_std_params(all_params, std_params)

    def get_best_params_log(self):
        std_params = self.params.get_std_clf_params()
        best_params = self.gridsearch.best_params_
        return overwrite_std_params(best_params, std_params, all=False)

    def set_params_log(self, all: bool = True):
        if all:
            log = self.get_all_params_log()
        else:
            log = self.get_best_params_log()
            log["n_splits"] = self.n_splits
            log["n_repeats"] = self.n_repeats
        self.logger.log_params(log)

    def get_feat_log(self):
        return self.feat.get_save_attr()

    def set_feat_log(self):
        log = self.get_feat_log()
        self.logger.log_feat(log)

    def get_all_results_log(self):
        cv_keys = keys(self.gridsearch.cv_results_)
        nonp_keys = [x for x in cv_keys if x[:5] != "param"]
        cvr = self.gridsearch.cv_results_
        results_log = {key: cvr[key].tolist() for key in nonp_keys}
        return results_log

    def get_best_results_log(self):
        results_log = {}
        results_log["true_pos"] = self.conf_matrix[0][0]
        results_log["false_pos"] = self.conf_matrix[0][1]
        results_log["false_neg"] = self.conf_matrix[1][0]
        results_log["true_neg"] = self.conf_matrix[1][1]
        cv_keys = keys(self.gridsearch.cv_results_)
        nonp_keys = [x for x in cv_keys if x[:5] not in ["param", "split"]]
        for key in nonp_keys:
            results_log[key] = self.gridsearch.cv_results_[key][0]
        return results_log

    def set_results_log(self, all: bool = True):
        if all:
            log = self.get_all_results_log()
        else:
            log = self.get_best_results_log()
        self.logger.log_results(log)

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

    def __init__(
        self,
        feat: Features = None,
        params: Params = None,
        reduce_dim: bool = None,
        n_splits: int = None,
        n_repeats: int = None,
        verbose: int = None,
        df_filter: tuple = None
    ):
        if feat is None:
            self.feat = Features()
        else:
            self.feat = feat
        if params is None:
            self.params = Params()
        else:
            self.params = params
        if reduce_dim is not None:
            self.reduce_dim = reduce_dim
        else:
            self.reduce_dim = chkenv("REDUCE_DIM", type=bool)
        if verbose is not None:
            self.verbose = verbose
        else:
            self.verbose = chkenv("CV_VERBOSE", type=int)
        if df_filter == -1:
            self.df_filter = None
        else:
            self.df_filter = df_filter
        self.data = self.set_data()
        self.crossval = self.get_crossval(n_splits=n_splits,
                                          n_repeats=n_repeats
                                          )
        self.pipe = self.get_pipe()
        self.gridsearch = self.set_gridsearch()
        self.set_logger()

    def fit_data(self):
        print(f"Model Type: {self.params.model_type}")
        X_train = self.data.X_train
        y_train = self.data.y_train
        with catch_warnings(record=True) as caught_warnings:
            gsf = self.gridsearch.fit(X_train, y_train)
        if len(caught_warnings) > 0:
            warns = [str(x) for x in caught_warnings]
            self.logger.log_warn({"warnings": warns})
        return gsf

    def get_predictions(self):
        X_test = self.data.X_test
        return self.gridsearch.predict(X_test)

    def get_probabilities(self, X_test: DataFrame):
        return self.gridsearch.predict_proba(X_test)

    def get_scores(self):
        y_true = list(self.data.y_test)
        y_pred = list(self.get_predictions())
        rng = range(len(y_true))
        scores = [1 if y_true[i] == y_pred[i] else 0 for i in rng]
        return array(scores)

    def test_data(self):
        y_true = self.data.y_test
        y_pred = self.get_predictions()
        self.report = classification_report(y_true, y_pred, zero_division=0)
        self.conf_matrix = confusion_matrix(y_true, y_pred)

    def get_roc_curve(self,
                      ):
        y_true = self.data.y_test
        X_test = self.data.X_test
        yi = y_true.index
        gp = self.get_probabilities
        y_prob = Series([x[1] for x in gp(X_test)], index=yi)
        return RocCurve(y_true, y_prob, X_test)

    def set_roc_curve(self):
        self.roc_curve = self.get_roc_curve()

    def show_results(self):
        print(f"Best parameter set: {self.gridsearch.best_params_}\n")
        print(f"Best score: {self.gridsearch.best_score_}\n")
        print("Confustion Matrix\n", self.conf_matrix)
        print(self.report)

    def fit(self,
            fit: bool = True,
            test: bool = True,
            log: bool = False,
            roc: bool = True,
            show: bool = False,
            title: str = None
            ):
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

    def fit_test_log(self):
        self.fit(log=True)

    def fit_test_log_show(self):
        self.fit(log=True, show=True)

    def get_abroca(self,
                   split_col: str,
                   plot: bool = True,
                   ax=None
                   ):
        abroca = self.roc_curve.get_abroca(split_col=split_col)
        if plot:
            abroca.plot(ax=ax)
        return {split_col: abroca.abroca}

    def get_abrocas(self,
                    split_cols: list,
                    **kwargs
                    ):
        abrocas = {}
        for col in split_cols:
            _dict = self.get_abroca(col, **kwargs)
            abrocas.update(_dict)
        return abrocas
