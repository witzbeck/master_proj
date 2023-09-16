# standard library imports
from dataclasses import dataclass, field

# third party imports
from scipy.stats import expon, uniform

# local imports
from alexlib.config import chkenv
from alexlib.iters import keys, vals
from setup import nrows as nr, random_state as rs, jobint, model_types

if __name__ == '__main__':
    from setup import config
    config


def discrete_exp_dist(
        exp_min: int,
        exp_max: int,
        exp_int: int = 10,
        exp_inc: int = 1,
        numerator: int = 1
) -> list[float]:
    exp_max += 1
    rng = range(exp_min, exp_max, exp_inc)
    return [numerator / (exp_int ** i) for i in rng]


def wrap_dict_vals(_dict: dict):
    for key in keys(_dict):
        val = _dict[key]
        _dict[key] = [val]
    return _dict


def unpack_clf_keys(params_dict: dict):
    _keys = keys(params_dict)
    return [x.split("__")[-1] for x in _keys]


def unpack_clf_params(params_dict: dict):
    new_keys = unpack_clf_keys(params_dict)
    _vals = vals(params_dict)
    _range = range(len(new_keys))
    return {new_keys[i]: _vals[i] for i in _range}


def lengthen_params_log(params_log: dict):
    _keys = keys(params_log)
    _vals = vals(params_log)
    r = range(len(keys))
    log = []
    for i in r:
        val = _vals[i]
        if val is None:
            log.append([val])
        elif (valt := type(val)) in [str, float, int, bool]:
            log.append([val])
        elif valt in [list, tuple]:
            log.append(list(val))
        else:
            log.append(val.data.tolist())
    plen = max([len(x) for x in log])
    return {_keys[i]: log[i] * plen if len(log[i]) == 1 else log[i] for i in r}


def overwrite_std_params(clf_params: dict,
                         std_params: dict,
                         all: bool = True
                         ):
    sp = std_params
    np = unpack_clf_params(clf_params)
    _ks = keys(std_params)
    new_keys = keys(np)
    out_params = {key: np[key] if key in new_keys else sp[key] for key in _ks}
    if all:
        return lengthen_params_log(out_params)
    else:
        return out_params


@dataclass
class Params:
    model_type: str = chkenv("MODEL_TYPE")
    predict_col: int = chkenv("PREDICT_COL")
    nrows: int = nr
    test_size: float = chkenv("TEST_SIZE", type=float)
    random_state: int = rs
    params: dict = field(default_factory=dict)

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

    def __post_init__(self):
        self.pre_dispatch = chkenv("PRE_DISPATCH", type=int)
        self.n_iter = chkenv("SEARCH_ITER", type=int)
        self.rand = chkenv("SEARCH_RANDOM", type=bool)
        self.refit = chkenv("CV_REFIT").lower()
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
