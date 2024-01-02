# standard library imports
from dataclasses import dataclass, field
from typing import Any

from scipy.stats import expon, uniform

from alexlib.core import chkenv
from alexlib.maths import discrete_exp_dist
from setup import nrows as nr, random_state as rs, jobint, model_types

if __name__ == '__main__':
    from setup import config
    config


def wrap_dict_vals(dict_: dict) -> dict[str: list]:
    return {
        k: [v] if not isinstance(v, list) else v
        for k, v in dict_.items()
    }


def unpack_clf_keys(params_dict: dict) -> list[str]:
    return [x.split("__")[-1] for x in params_dict.keys()]


def unpack_clf_params(params_dict: dict) -> dict[str: Any]:
    new_keys = unpack_clf_keys(params_dict)
    vals = list(params_dict.values())
    return {new_keys[i]: vals[i] for i in range(len(new_keys))}


def lengthen_params_log(params_log: dict) -> dict:
    keys = list(params_log.keys())
    log = []
    for v in params_log.values():
        if v is None:
            log.append([v])
        elif max([isinstance(v, t) for t in [str, float, int, bool]]):
            log.append([v])
        elif isinstance(v, list):
            log.append(v)
        elif isinstance(v, tuple):
            log.append(list(v))
        else:
            log.append(v.data.tolist())
    plen = max([len(x) for x in log])
    return {
        keys[i]: log[i] * plen if len(log[i]) == 1 else log[i]
        for i in range(len(params_log))
    }


def overwrite_std_params(
    clf_params: dict,
    std_params: dict,
    all: bool = True
) -> dict:
    sp = std_params
    np = unpack_clf_params(clf_params)
    new_keys = list(np.keys())
    out_params = {
        key: np[key] if key in new_keys else sp[key]
        for key in std_params.keys()
    }
    return lengthen_params_log(out_params) if all else out_params


@dataclass
class Params:
    params: dict = field(default_factory=dict)

    @property
    def model_type(self) -> str:
        return chkenv("MODEL_TYPE")

    @property
    def predict_col(self) -> str:
        return chkenv("PREDICT_COL")

    @property
    def nrows(self) -> int:
        return nr

    @property
    def test_size(self) -> float:
        return chkenv("TEST_SIZE", type=float)

    @property
    def random_state(self) -> int:
        return rs

    def set_rand_param_dict(self):

        # slight better performance noticed without warm start
        _bool = [True, False]
        if self.model_type == "logreg":
            params = [
                {
                    "clf__solver": [
                        "lbfgs",
                        "sag",
                        "newton-cg",
                        "newton-cholesky"
                    ],
                    "clf__penalty": [None, "l2"],
                    "clf__C": expon(scale=0.1),
                    "clf__warm_start": [False],
                    "clf__max_iter": [i for i in range(30, 150)],
                    "clf__random_state": [self.random_state],
                    "clf__n_jobs": [jobint],
                },
                {
                    "clf__solver": ["saga"],
                    "clf__penalty": [None, "l2", "l1"],
                    "clf__C": expon(scale=0.1),
                    # "clf__l1_ratio": uniform(),
                    "clf__warm_start": _bool,
                    # "clf__max_iter": max_iter_dist,
                    "clf__random_state": [self.random_state],
                    "clf__n_jobs": [-1],
                },
                {
                    "clf__solver": ["saga"],
                    "clf__penalty": ["elasticnet"],
                    "clf__C": expon(scale=0.1),
                    "clf__l1_ratio": uniform(),
                    "clf__warm_start": _bool,
                    # "clf__max_iter": max_iter_dist,
                    "clf__random_state": [self.random_state],
                    "clf__n_jobs": [jobint],
                },
                {
                    "clf__solver": ["liblinear"],
                    "clf__penalty": ["l1", "l2"],
                    "clf__C": expon(scale=0.1),
                    "clf__warm_start": _bool,
                    # "clf__max_iter": max_iter_dist,
                    "clf__random_state": [self.random_state],
                },
            ]
        elif self.model_type == "svc":
            params = {
                "clf__C": expon(scale=0.1),
                "clf__kernel": ["linear", "rbf", "poly", "sigmoid"],
                "clf__degree": [i for i in range(1, 5)],
                # "clf__max_iter": max_iter_dist,
                "clf__probability": [True],
                "clf__gamma": ["auto", "scale"],
                "clf__random_state": [self.random_state],
            }
        elif self.model_type == "knn":
            params = {
                "clf__n_neighbors": [i for i in range(2, 6)],
                "clf__weights": ["uniform", "distance"],
                "clf__algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
                "clf__leaf_size": [i for i in range(10, 100)],
                "clf__p": [i for i in range(1, 5)],
                "clf__n_jobs": [jobint],
            }
        elif self.model_type == "dtree":
            params = {
                "clf__criterion": ["gini", "entropy", "log_loss"],
                "clf__splitter": ["best", "random"],
                "clf__max_depth": [i for i in range(10, 100)],
                "clf__min_samples_leaf": [i for i in range(1, 10)],
                "clf__min_samples_split": [i for i in range(2, 100)],
                "clf__max_features": [None, "sqrt", "log2"],
                "clf__random_state": [self.random_state],
            }
        elif self.model_type == "etree":
            params = {
                "clf__criterion": ["gini", "entropy", "log_loss"],
                "clf__n_estimators": [i for i in range(10, 200)],
                "clf__max_features": [None, "sqrt", "log2"],
                "clf__min_samples_split": [i for i in range(2, 10)],
                "clf__min_samples_leaf": [i for i in range(1, 10)],
                "clf__bootstrap": [True],
                "clf__oob_score": [True],
                "clf__warm_start": _bool,
                "clf__max_samples": uniform(),
                "clf__random_state": [self.random_state],
                "clf__n_jobs": [jobint],
            }
        elif self.model_type == "rforest":
            params = {
                "clf__criterion": ["gini", "entropy", "log_loss"],
                "clf__n_estimators": [i for i in range(10, 200)],
                "clf__min_samples_split": [i for i in range(2, 10)],
                "clf__min_samples_leaf": [i for i in range(1, 10)],
                "clf__max_features": [None, "sqrt", "log2"],
                "clf__bootstrap": [True],
                "clf__oob_score": [True],
                "clf__warm_start": _bool,
                "clf__max_samples": uniform(),
                "clf__random_state": [self.random_state],
                "clf__n_jobs": [jobint],
            }
        elif self.model_type == "mlp":
            params = {
                "clf__hidden_layer_sizes": [i for i in range(10, 200)],
                "clf__activation": ["identity", "logistic", "tanh", "relu"],
                "clf__solver": ["adam", "lbfgs", "sgd"],
                "clf__learning_rate": ["constant", "adaptive", "invscaling"],
                "clf__learning_rate_init": expon(scale=0.01),
                "clf__power_t": expon(scale=0.1),
                "clf__alpha": expon(scale=0.01),
                "clf__max_iter": [i for i in range(30, 150)],
                "clf__warm_start": _bool,
                "clf__early_stopping": _bool,
                "clf__random_state": [self.random_state],
            }
        elif self.model_type == "ada_boost":
            params = {
                "clf__random_state": [self.random_state],
                "clf__learning_rate": expon(scale=0.01),
            }
        elif self.model_type == "hxg_boost":
            params = {
                "clf__random_state": [self.random_state],
                "clf__learning_rate": expon(scale=0.01),
                "clf__max_iter": [i for i in range(30, 150)],
                "clf__max_depth": [i for i in range(10, 100)],
                "clf__max_bins": [i for i in range(100, 256)],
                "clf__warm_start": _bool,
                "clf__l2_regularization": uniform(),
                "clf__min_samples_leaf": [i for i in range(1, 10)],
                "clf__interaction_cst": ["pairwise", "no_interactions"],
            }
        elif self.model_type == "xg_boost":
            params = {
                "clf__random_state": [self.random_state],
            }
        elif self.model_type == "compnb":
            params = {
                "clf__alpha": expon(scale=0.01),
                "clf__norm": _bool,
            }
        elif self.model_type == "gauss":
            params = {
                "clf__random_state": [self.random_state],
            }
        else:
            raise ValueError("param dict not selected")
        return params

    def set_grid_param_dict(self):
        # slight better performance noticed without warm start
        _bool = [True, False]
        if self.model_type == "logreg":
            params = [
                {
                    "clf__solver": [
                        "lbfgs",
                        "newton-cg",
                        "sag",
                        "newton-cholesky"
                    ],
                    "clf__penalty": ["l2"],
                    "clf__C": discrete_exp_dist(-2, 2),
                    "clf__random_state": [self.random_state],
                    "clf__n_jobs": [jobint],
                },
                {
                    "clf__solver": [
                        "lbfgs",
                        "newton-cg",
                        "sag",
                        "newton-cholesky"
                    ],
                    "clf__penalty": [None],
                    "clf__random_state": [self.random_state],
                    "clf__n_jobs": [jobint],
                },
                # {
                #    "clf__solver": ["saga"],
                #    "clf__penalty": [None, "l2", "l1"],
                #    "clf__C": discrete_exp_dist(-3, 3),
                #    "clf__random_state": [self.random_state],
                #    "clf__n_jobs": [jobint],
                # },
                # {
                #    "clf__solver": ["saga"],
                #    "clf__penalty": ["elasticnet"],
                #    "clf__C": discrete_exp_dist(-3, 3),
                #    "clf__l1_ratio": [i / 10 for i in range(1, 10, 3)],
                #    "clf__random_state": [self.random_state],
                #    "clf__n_jobs": [jobint],
                # },
                {
                    "clf__solver": ["liblinear"],
                    "clf__penalty": ["l1", "l2"],
                    "clf__C": discrete_exp_dist(-2, 2),
                    "clf__random_state": [self.random_state],
                },
            ]
        elif self.model_type == "svc":
            params = {
                "clf__C": discrete_exp_dist(-2, 2),
                # "clf__kernel": ["linear", "rbf"],
                "clf__degree": [i for i in range(1, 3)],
                # "clf__probability": [True], # need for abroca
                "clf__random_state": [self.random_state],
            }
        elif self.model_type == "knn":
            params = {
                "clf__n_neighbors": [i for i in range(2, 4)],
                "clf__weights": ["uniform", "distance"],
                # "clf__leaf_size": [i for i in range(10, 61, 10)],
                "clf__p": [i for i in range(1, 4)],
                "clf__n_jobs": [jobint],
            }
        elif self.model_type == "dtree":
            params = {
                "clf__criterion": ["gini", "log_loss"],
                "clf__splitter": ["best", "random"],
                # "clf__max_depth": [i for i in range(10, 101, 40)],
                "clf__min_samples_leaf": [i for i in range(1, 11, 9)],
                # "clf__min_samples_split": [i for i in range(5, 101, 25)],
                # "clf__max_features": ["sqrt", "log2"],
                "clf__random_state": [self.random_state],
            }
        elif self.model_type == "etree":
            params = {
                "clf__criterion": ["gini", "log_loss"],
                "clf__n_estimators": [i for i in range(20, 101, 40)],
                # "clf__max_features": ["sqrt", "log2"],
                # "clf__min_samples_split": [i for i in range(2, 18, 7)],
                "clf__min_samples_leaf": [i for i in range(1, 11, 9)],
                "clf__random_state": [self.random_state],
                "clf__n_jobs": [jobint],
            }
        elif self.model_type == "rforest":
            params = {
                "clf__criterion": ["gini", "log_loss"],
                "clf__n_estimators": [i for i in range(20, 101, 40)],
                # "clf__min_samples_split": [i for i in range(1, 11, 7)],
                "clf__min_samples_leaf": [i for i in range(1, 11, 9)],
                # "clf__max_features": ["sqrt", "log2"],
                "clf__random_state": [self.random_state],
                "clf__n_jobs": [jobint],
            }
        elif self.model_type == "mlp":
            params = {
                "clf__hidden_layer_sizes": [i for i in range(25, 101, 25)],
                "clf__activation": ["tanh"],
                "clf__solver": ["adam"],
                "clf__learning_rate": ["constant", "adaptive"],
                "clf__learning_rate_init": discrete_exp_dist(1, 2),
                "clf__random_state": [self.random_state],
            }
        elif self.model_type == "ada_boost":
            params = {
                "clf__random_state": [self.random_state],
                "clf__learning_rate": discrete_exp_dist(1, 2),
            }
        elif self.model_type == "hxg_boost":
            params = {
                "clf__random_state": [self.random_state],
                "clf__learning_rate": discrete_exp_dist(1, 4),
                # "clf__l2_regularization": [i / 5 for i in range(0, 6, 2)],
            }
        elif self.model_type == "xg_boost":
            params = {
                "clf__random_state": [self.random_state],
            }
        elif self.model_type == "compnb":
            params = {
                "clf__alpha": discrete_exp_dist(1, 3),
                "clf__norm": _bool,
            }
        elif self.model_type == "gauss":
            params = {
                "clf__random_state": [self.random_state],
            }
        else:
            raise ValueError("param dict not selected")
        return params

    def set_model_type(self):
        if self.model_type == "logreg":
            from sklearn.linear_model import LogisticRegression
            clf = LogisticRegression
        elif self.model_type == "svc":
            from sklearn.svm import SVC
            clf = SVC
        elif self.model_type == "compnb":
            from sklearn.naive_bayes import ComplementNB
            clf = ComplementNB
        elif self.model_type == "knn":
            from sklearn.neighbors import KNeighborsClassifier
            clf = KNeighborsClassifier
        elif self.model_type == "dtree":
            from sklearn.tree import DecisionTreeClassifier
            clf = DecisionTreeClassifier
        elif self.model_type == "etree":
            from sklearn.ensemble import ExtraTreesClassifier
            clf = ExtraTreesClassifier
        elif self.model_type == "rforest":
            from sklearn.ensemble import RandomForestClassifier
            clf = RandomForestClassifier
        elif self.model_type == "ada_boost":
            from sklearn.ensemble import AdaBoostClassifier
            clf = AdaBoostClassifier
        elif self.model_type == "mlp":
            from sklearn.neural_network import MLPClassifier
            clf = MLPClassifier
        elif self.model_type == "xg_boost":
            from sklearn.ensemble import GradientBoostingClassifier
            clf = GradientBoostingClassifier
        elif self.model_type == "hxg_boost":
            from sklearn.ensemble import HistGradientBoostingClassifier
            clf = HistGradientBoostingClassifier
        elif self.model_type == "gauss":
            from sklearn.gaussian_process import GaussianProcessClassifier
            clf = GaussianProcessClassifier
        else:
            raise ValueError(self.model_type)
        return clf

    @property
    def pre_dispatch(self) -> int:
        return chkenv("PRE_DISPATCH", type=int)

    @property
    def n_iter(self) -> int:
        return chkenv("SEARCH_ITER", type=int)

    @property
    def rand(self) -> bool:
        return chkenv("SEARCH_RANDOM", type=bool)

    @property
    def refit(self) -> str:
        return chkenv("CV_REFIT").lower()

    def __post_init__(self):
        self.clf = self.set_model_type()
        self.model_types = model_types

        if self.rand:
            from sklearn.model_selection import RandomizedSearchCV
            self.searchcv = RandomizedSearchCV
        else:
            from sklearn.model_selection import GridSearchCV
            self.searchcv = GridSearchCV

        if len(self.params) > 0:
            self._dict = self.params
        elif self.rand:
            from sklearn.model_selection import ParameterSampler
            self._dict = self.set_rand_param_dict()
            self.sampler = ParameterSampler(self._dict, n_iter=self.n_iter)
            self._list = list(self.sampler)
        else:
            from sklearn.model_selection import ParameterGrid
            self._dict = self.set_grid_param_dict()
            self.grid = ParameterGrid(self._dict)
            self._list = list(self.grid)

    def get_std_clf_params(self):
        base_clf = self.set_model_type()
        return base_clf().get_params()

    def get_param_gen(self):
        for _params in self._list:
            _params = wrap_dict_vals(_params)
            pobj = Params(
                model_type=self.model_type,
                predict_col=self.predict_col,
                nrows=self.nrows,
                test_size=self.test_size,
                random_state=self.random_state,
                params=_params
            )
            yield pobj
