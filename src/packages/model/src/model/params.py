from collections.abc import Generator
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from scipy.stats import expon, uniform
from sklearn.base import ClassifierMixin
from sklearn.ensemble import (
    AdaBoostClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    BaseCrossValidator,
    GridSearchCV,
    ParameterGrid,
    ParameterSampler,
    RandomizedSearchCV,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from alexlib.maths import discrete_exp_dist

from model.constants import (
    BOOL_OPTIONS,
    JOB_CORES,
    RANDOM_STATE,
    SEARCH_ITER,
    SEARCH_RANDOM,
)


@dataclass
class ModelParameterInputs:
    model_type: str
    classifier: ClassifierMixin
    rand_params: dict
    grid_params: dict


class ModelParameters(Enum):
    LOGREG = ModelParameterInputs(
        "logreg",
        LogisticRegression,
        rand_params=[
            {
                "clf__solver": ["lbfgs", "sag", "newton-cg", "newton-cholesky"],
                "clf__penalty": [None, "l2"],
                "clf__C": expon(scale=0.1),
                "clf__warm_start": [False],
                "clf__max_iter": list(range(30, 150)),
                "clf__random_state": [RANDOM_STATE],
                "clf__n_jobs": [JOB_CORES],
            },
            {
                "clf__solver": ["saga"],
                "clf__penalty": [None, "l2", "l1"],
                "clf__C": expon(scale=0.1),
                "clf__warm_start": BOOL_OPTIONS,
                "clf__random_state": [RANDOM_STATE],
                "clf__n_jobs": [-1],
            },
            {
                "clf__solver": ["saga"],
                "clf__penalty": ["elasticnet"],
                "clf__C": expon(scale=0.1),
                "clf__l1_ratio": uniform(),
                "clf__warm_start": BOOL_OPTIONS,
                "clf__random_state": [RANDOM_STATE],
                "clf__n_jobs": [JOB_CORES],
            },
            {
                "clf__solver": ["liblinear"],
                "clf__penalty": ["l1", "l2"],
                "clf__C": expon(scale=0.1),
                "clf__warm_start": BOOL_OPTIONS,
                "clf__random_state": [RANDOM_STATE],
            },
        ],
        grid_params=[
            {
                "clf__solver": ["lbfgs", "newton-cg", "sag", "newton-cholesky"],
                "clf__penalty": ["l2"],
                "clf__C": discrete_exp_dist(-2, 2),
                "clf__random_state": [RANDOM_STATE],
                "clf__n_jobs": [JOB_CORES],
            },
            {
                "clf__solver": ["lbfgs", "newton-cg", "sag", "newton-cholesky"],
                "clf__penalty": [None],
                "clf__random_state": [RANDOM_STATE],
                "clf__n_jobs": [JOB_CORES],
            },
            {
                "clf__solver": ["liblinear"],
                "clf__penalty": ["l1", "l2"],
                "clf__C": discrete_exp_dist(-2, 2),
                "clf__random_state": [RANDOM_STATE],
            },
        ],
    )
    SVC = ModelParameterInputs(
        "svc",
        SVC,
        rand_params={
            "clf__C": expon(scale=0.1),
            "clf__kernel": ["linear", "rbf", "poly", "sigmoid"],
            "clf__degree": list(range(1, 5)),
            "clf__probability": [True],
            "clf__gamma": ["auto", "scale"],
            "clf__random_state": [RANDOM_STATE],
        },
        grid_params={
            "clf__C": discrete_exp_dist(-2, 2),
            "clf__kernel": ["linear", "rbf"],
            "clf__degree": list(range(1, 3)),
            "clf__probability": [True],  # need for abroca
            "clf__random_state": [RANDOM_STATE],
        },
    )
    KNN = ModelParameterInputs(
        "knn",
        KNeighborsClassifier,
        rand_params={
            "clf__n_neighbors": list(range(2, 6)),
            "clf__weights": ["uniform", "distance"],
            "clf__algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
            "clf__leaf_size": list(range(10, 100)),
            "clf__p": list(range(1, 5)),
            "clf__n_jobs": [JOB_CORES],
        },
        grid_params={
            "clf__n_neighbors": list(range(2, 4)),
            "clf__weights": ["uniform", "distance"],
            "clf__leaf_size": list(range(10, 61, 10)),
            "clf__p": list(range(1, 4)),
            "clf__n_jobs": [JOB_CORES],
        },
    )
    DTREE = ModelParameterInputs(
        "dtree",
        DecisionTreeClassifier,
        rand_params={
            "clf__criterion": ["gini", "entropy", "log_loss"],
            "clf__splitter": ["best", "random"],
            "clf__max_depth": list(range(10, 100)),
            "clf__min_samples_leaf": list(range(1, 10)),
            "clf__min_samples_split": list(range(2, 100)),
            "clf__max_features": [None, "sqrt", "log2"],
            "clf__random_state": [RANDOM_STATE],
        },
        grid_params={
            "clf__criterion": ["gini", "log_loss"],
            "clf__splitter": ["best", "random"],
            "clf__min_samples_leaf": list(range(1, 11, 9)),
            "clf__random_state": [RANDOM_STATE],
        },
    )
    ETREE = ModelParameterInputs(
        "etree",
        ExtraTreesClassifier,
        rand_params={
            "clf__criterion": ["gini", "entropy", "log_loss"],
            "clf__n_estimators": list(range(10, 200)),
            "clf__max_features": [None, "sqrt", "log2"],
            "clf__min_samples_split": list(range(2, 10)),
            "clf__min_samples_leaf": list(range(1, 10)),
            "clf__bootstrap": [True],
            "clf__oob_score": [True],
            "clf__warm_start": BOOL_OPTIONS,
            "clf__max_samples": uniform(),
            "clf__random_state": [RANDOM_STATE],
            "clf__n_jobs": [JOB_CORES],
        },
        grid_params={
            "clf__criterion": ["gini", "log_loss"],
            "clf__n_estimators": list(range(20, 101, 40)),
            "clf__min_samples_leaf": list(range(1, 11, 9)),
            "clf__random_state": [RANDOM_STATE],
            "clf__n_jobs": [JOB_CORES],
        },
    )
    RFOREST = ModelParameterInputs(
        "rforest",
        RandomForestClassifier,
        rand_params={
            "clf__criterion": ["gini", "entropy", "log_loss"],
            "clf__n_estimators": list(range(10, 200)),
            "clf__min_samples_split": list(range(2, 10)),
            "clf__min_samples_leaf": list(range(1, 10)),
            "clf__max_features": [None, "sqrt", "log2"],
            "clf__bootstrap": [True],
            "clf__oob_score": [True],
            "clf__warm_start": BOOL_OPTIONS,
            "clf__max_samples": uniform(),
            "clf__random_state": [RANDOM_STATE],
            "clf__n_jobs": [JOB_CORES],
        },
        grid_params={
            "clf__criterion": ["gini", "log_loss"],
            "clf__n_estimators": list(range(20, 101, 40)),
            "clf__min_samples_leaf": list(range(1, 11, 9)),
            "clf__random_state": [RANDOM_STATE],
            "clf__n_jobs": [JOB_CORES],
        },
    )
    MLP = ModelParameterInputs(
        "mlp",
        MLPClassifier,
        rand_params={
            "clf__hidden_layer_sizes": list(range(10, 200)),
            "clf__activation": ["identity", "logistic", "tanh", "relu"],
            "clf__solver": ["adam", "lbfgs", "sgd"],
            "clf__learning_rate": ["constant", "adaptive", "invscaling"],
            "clf__learning_rate_init": expon(scale=0.01),
            "clf__power_t": expon(scale=0.1),
            "clf__alpha": expon(scale=0.01),
            "clf__max_iter": list(range(30, 150)),
            "clf__warm_start": BOOL_OPTIONS,
            "clf__early_stopping": BOOL_OPTIONS,
            "clf__random_state": [RANDOM_STATE],
        },
        grid_params={
            "clf__hidden_layer_sizes": list(range(25, 101, 25)),
            "clf__activation": ["tanh"],
            "clf__solver": ["adam"],
            "clf__learning_rate": ["constant", "adaptive"],
            "clf__learning_rate_init": discrete_exp_dist(1, 2),
            "clf__random_state": [RANDOM_STATE],
        },
    )
    HXG_BOOST = ModelParameterInputs(
        "hxg_boost",
        HistGradientBoostingClassifier,
        rand_params={
            "clf__random_state": [RANDOM_STATE],
            "clf__learning_rate": expon(scale=0.01),
            "clf__max_iter": list(range(30, 150)),
            "clf__max_depth": list(range(10, 100)),
            "clf__max_bins": list(range(100, 256)),
            "clf__warm_start": BOOL_OPTIONS,
            "clf__l2_regularization": uniform(),
            "clf__min_samples_leaf": list(range(1, 10)),
            "clf__interaction_cst": ["pairwise", "no_interactions"],
        },
        grid_params={
            "clf__random_state": [RANDOM_STATE],
            "clf__learning_rate": discrete_exp_dist(1, 4),
        },
    )
    ADA_BOOST = ModelParameterInputs(
        "ada_boost",
        AdaBoostClassifier,
        rand_params={
            "clf__random_state": [RANDOM_STATE],
            "clf__learning_rate": expon(scale=0.01),
        },
        grid_params={
            "clf__random_state": [RANDOM_STATE],
            "clf__learning_rate": discrete_exp_dist(1, 2),
        },
    )


MODEL_PARAMETER_MAP = {x.value.model_type: x.value for x in ModelParameters}


def wrap_dict_vals(dict_: dict) -> dict[str:list]:
    """Wrap values in a dictionary in a list if they are not already a list"""
    return {k: [v] if not isinstance(v, list) else v for k, v in dict_.items()}


def unpack_clf_keys(params_dict: dict[str, str]) -> list[str]:
    """Get the keys of a dictionary that start with 'clf__'"""
    return [x.split("__")[-1] for x in params_dict.keys() if x.startswith("clf__")]


def unpack_clf_params(params_dict: dict) -> dict[str:Any]:
    new_keys = unpack_clf_keys(params_dict)
    vals = list(params_dict.values())
    return {new_keys[i]: vals[i] for i in range(len(new_keys))}


def lengthen_params_log(params_log: dict) -> dict:
    keys = list(params_log.keys())
    log = []
    for v in params_log.values():
        if v is None:
            log.append([v])
        elif max(isinstance(v, t) for t in [str, float, int, bool]):
            log.append([v])
        elif isinstance(v, list):
            log.append(v)
        elif isinstance(v, tuple):
            log.append(list(v))
        else:
            log.append(v.data.tolist())
    plen = max(len(x) for x in log)
    return {
        keys[i]: log[i] * plen if len(log[i]) == 1 else log[i]
        for i in range(len(params_log))
    }


def overwrite_std_params(clf_params: dict, std_params: dict, all: bool = True) -> dict:
    sp = std_params
    np = unpack_clf_params(clf_params)
    new_keys = list(np.keys())
    out_params = {
        key: np[key] if key in new_keys else sp[key] for key in std_params.keys()
    }
    return lengthen_params_log(out_params) if all else out_params


@dataclass
class Params:
    model_type: str
    clf: ClassifierMixin = field(init=False)
    grid: ParameterGrid = field(init=False)
    sampler: ParameterSampler = field(init=False)
    searchcv: BaseCrossValidator = field(init=False)
    list_: list = field(init=False)

    def __post_init__(self):
        inputs = MODEL_PARAMETER_MAP[self.model_type]
        self.clf = inputs.classifier
        if SEARCH_RANDOM:
            self.searchcv = RandomizedSearchCV
        else:
            self.searchcv = GridSearchCV

        if len(self.params) > 0:
            self._dict = self.params
        elif SEARCH_RANDOM:
            self.sampler = ParameterSampler(inputs.rand_params, n_iter=SEARCH_ITER)
            self._list = list(self.sampler)
        else:
            self.grid = ParameterGrid(inputs.grid_params)
            self._list = list(self.grid)

    @staticmethod
    def get_std_clf_params(clf: ClassifierMixin) -> dict:
        return clf().get_params()

    def get_parameter_generator(self) -> Generator[dict, None, None]:
        wrapped_parameter_list = [wrap_dict_vals(x) for x in self._list]
        for parameters in wrapped_parameter_list:
            yield parameters
