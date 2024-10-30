from dataclasses import dataclass, field
from functools import cached_property
from json import dumps, loads
from os import environ
from pathlib import Path
from subprocess import run
from typing import Any

from scipy.stats import expon, uniform
from sklearn.ensemble import (
    AdaBoostClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    BaseCrossValidator,
    GridSearchCV,
    ParameterGrid,
    ParameterSampler,
    RandomizedSearchCV,
)
from sklearn.naive_bayes import ComplementNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from alexlib.maths import discrete_exp_dist

from constants import (
    CV_REFIT,
    JOB_CORES,
    MODEL_TYPES,
    PRE_DISPATCH,
    PREDICT_COL,
    RANDOM_STATE,
    SEARCH_ITER,
    SEARCH_RANDOM,
    TEST_SIZE,
)

MODEL_TYPE_MAP = {
    "logreg": LogisticRegression,
    "svc": SVC,
    "compnb": ComplementNB,
    "knn": KNeighborsClassifier,
    "dtree": DecisionTreeClassifier,
    "etree": ExtraTreesClassifier,
    "rforest": RandomForestClassifier,
    "ada_boost": AdaBoostClassifier,
    "mlp": MLPClassifier,
    "xg_boost": GradientBoostingClassifier,
    "hxg_boost": HistGradientBoostingClassifier,
    "gauss": GaussianProcessClassifier,
}
BOOL_OPTIONS = [True, False]
RAND_PARAM_MAP = {
    "logreg": [
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
            # "clf__l1_ratio": uniform(),
            "clf__warm_start": BOOL_OPTIONS,
            # "clf__max_iter": max_iter_dist,
            "clf__random_state": [RANDOM_STATE],
            "clf__n_jobs": [-1],
        },
        {
            "clf__solver": ["saga"],
            "clf__penalty": ["elasticnet"],
            "clf__C": expon(scale=0.1),
            "clf__l1_ratio": uniform(),
            "clf__warm_start": BOOL_OPTIONS,
            # "clf__max_iter": max_iter_dist,
            "clf__random_state": [RANDOM_STATE],
            "clf__n_jobs": [JOB_CORES],
        },
        {
            "clf__solver": ["liblinear"],
            "clf__penalty": ["l1", "l2"],
            "clf__C": expon(scale=0.1),
            "clf__warm_start": BOOL_OPTIONS,
            # "clf__max_iter": max_iter_dist,
            "clf__random_state": [RANDOM_STATE],
        },
    ],
    "svc": {
        "clf__C": expon(scale=0.1),
        "clf__kernel": ["linear", "rbf", "poly", "sigmoid"],
        "clf__degree": list(range(1, 5)),
        # "clf__max_iter": max_iter_dist,
        "clf__probability": [True],
        "clf__gamma": ["auto", "scale"],
        "clf__random_state": [RANDOM_STATE],
    },
    "knn": {
        "clf__n_neighbors": list(range(2, 6)),
        "clf__weights": ["uniform", "distance"],
        "clf__algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
        "clf__leaf_size": list(range(10, 100)),
        "clf__p": list(range(1, 5)),
        "clf__n_jobs": [JOB_CORES],
    },
    "dtree": {
        "clf__criterion": ["gini", "entropy", "log_loss"],
        "clf__splitter": ["best", "random"],
        "clf__max_depth": list(range(10, 100)),
        "clf__min_samples_leaf": list(range(1, 10)),
        "clf__min_samples_split": list(range(2, 100)),
        "clf__max_features": [None, "sqrt", "log2"],
        "clf__random_state": [RANDOM_STATE],
    },
    "etree": {
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
    "rforest": {
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
    "mlp": {
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
    "ada_boost": {
        "clf__random_state": [RANDOM_STATE],
        "clf__learning_rate": expon(scale=0.01),
    },
    "hxg_boost": {
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
    "xg_boost": {
        "clf__random_state": [RANDOM_STATE],
    },
    "compnb": {
        "clf__alpha": expon(scale=0.01),
        "clf__norm": BOOL_OPTIONS,
    },
    "gauss": {"clf__random_state": [RANDOM_STATE]},
}
GRID_PARAM_MAP = {
    "logreg": [
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
            "clf__solver": ["saga"],
            "clf__penalty": [None, "l2", "l1"],
            "clf__C": discrete_exp_dist(-3, 3),
            "clf__random_state": [RANDOM_STATE],
            "clf__n_jobs": [JOB_CORES],
        },
        {
            "clf__solver": ["saga"],
            "clf__penalty": ["elasticnet"],
            "clf__C": discrete_exp_dist(-3, 3),
            "clf__l1_ratio": [i / 10 for i in range(1, 10, 3)],
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
    "svc": {
        "clf__C": discrete_exp_dist(-2, 2),
        "clf__kernel": ["linear", "rbf"],
        "clf__degree": list(range(1, 3)),
        "clf__probability": [True],  # need for abroca
        "clf__random_state": [RANDOM_STATE],
    },
    "knn": {
        "clf__n_neighbors": list(range(2, 4)),
        "clf__weights": ["uniform", "distance"],
        "clf__leaf_size": list(range(10, 61, 10)),
        "clf__p": list(range(1, 4)),
        "clf__n_jobs": [JOB_CORES],
    },
    "dtree": {
        "clf__criterion": ["gini", "log_loss"],
        "clf__splitter": ["best", "random"],
        "clf__max_depth": list(range(10, 101, 40)),
        "clf__min_samples_leaf": list(range(1, 11, 9)),
        "clf__min_samples_split": list(range(5, 101, 25)),
        "clf__max_features": ["sqrt", "log2"],
        "clf__random_state": [RANDOM_STATE],
    },
    "etree": {
        "clf__criterion": ["gini", "log_loss"],
        "clf__n_estimators": list(range(20, 101, 40)),
        "clf__max_features": ["sqrt", "log2"],
        "clf__min_samples_split": list(range(2, 18, 7)),
        "clf__min_samples_leaf": list(range(1, 11, 9)),
        "clf__random_state": [RANDOM_STATE],
        "clf__n_jobs": [JOB_CORES],
    },
    "rforest": {
        "clf__criterion": ["gini", "log_loss"],
        "clf__n_estimators": list(range(20, 101, 40)),
        "clf__min_samples_split": list(range(1, 11, 7)),
        "clf__min_samples_leaf": list(range(1, 11, 9)),
        "clf__max_features": ["sqrt", "log2"],
        "clf__random_state": [RANDOM_STATE],
        "clf__n_jobs": [JOB_CORES],
    },
    "mlp": {
        "clf__hidden_layer_sizes": list(range(25, 101, 25)),
        "clf__activation": ["tanh"],
        "clf__solver": ["adam"],
        "clf__learning_rate": ["constant", "adaptive"],
        "clf__learning_rate_init": discrete_exp_dist(1, 2),
        "clf__random_state": [RANDOM_STATE],
    },
    "ada_boost": {
        "clf__random_state": [RANDOM_STATE],
        "clf__learning_rate": discrete_exp_dist(1, 2),
    },
    "hxg_boost": {
        "clf__random_state": [RANDOM_STATE],
        "clf__learning_rate": discrete_exp_dist(1, 4),
        "clf__l2_regularization": [i / 5 for i in range(0, 6, 2)],
    },
    "xg_boost": {
        "clf__random_state": [RANDOM_STATE],
    },
    "compnb": {
        "clf__alpha": discrete_exp_dist(1, 3),
        "clf__norm": BOOL_OPTIONS,
    },
    "gauss": {
        "clf__random_state": [RANDOM_STATE],
    },
}


def wrap_dict_vals(dict_: dict) -> dict[str:list]:
    """Wrap the values of a dictionary in a list."""
    return {k: [v] if not isinstance(v, list) else v for k, v in dict_.items()}


def unpack_clf_keys(params_dict: dict) -> list[str]:
    """Unpack the keys of a classifier parameter dictionary."""
    return [x.split("__")[-1] for x in params_dict.keys()]


def unpack_clf_params(params_dict: dict) -> dict[str:Any]:
    """Unpack the values of a classifier parameter dictionary."""
    new_keys = unpack_clf_keys(params_dict)
    vals = list(params_dict.values())
    return {new_keys[i]: vals[i] for i in range(len(new_keys))}


def lengthen_params_log(params_log: dict) -> dict:
    """Lengthen the parameters log."""
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
    """Overwrite the standard parameters with the classifier parameters."""
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
    predict_col: str = PREDICT_COL
    test_size: float = TEST_SIZE
    pre_dispatch: int = PRE_DISPATCH
    n_iter: int = SEARCH_ITER
    rand: bool = SEARCH_RANDOM
    refit: str = CV_REFIT.lower()
    random_state: int = RANDOM_STATE
    params: dict = field(default_factory=dict)

    @cached_property
    def searchcv(self) -> BaseCrossValidator:
        """Return the search cross-validation object."""
        return RandomizedSearchCV if self.rand else GridSearchCV

    @cached_property
    def param_dict(self) -> dict:
        """Return the parameter dictionary."""
        if self.params:
            return self.params
        elif self.rand:
            return RAND_PARAM_MAP[self.model_type]
        else:
            return GRID_PARAM_MAP[self.model_type]

    def __post_init__(self):
        """Initializes the Params object."""
        self.clf = MODEL_TYPE_MAP[self.model_type]
        self.model_types = MODEL_TYPES
        if len(self.params) > 0:
            self._dict = self.params
        elif self.rand:
            self.sampler = ParameterSampler(self.param_dict, n_iter=self.n_iter)
            self._list = list(self.sampler)
        else:
            self.grid = ParameterGrid(self.param_dict)
            self._list = list(self.grid)

    def get_std_clf_params(self):
        """Return the standard classifier parameters."""
        return self.clf().get_params()

    def get_param_gen(self):
        """Return a generator of the parameter dictionary."""
        for _params in self._list:
            _params = wrap_dict_vals(_params)
            pobj = Params(
                model_type=self.model_type,
                predict_col=self.predict_col,
                test_size=self.test_size,
                random_state=RANDOM_STATE,
                params=_params,
            )
            yield pobj


def show_params(model_type: str, is_rand: bool = True, n: int = 1):
    """Show the parameters for a model type."""
    stype = "Randomized" if is_rand else "Grid"
    stype = f"{stype}Search Cross-Validation Parameters"
    print(f"Example of {stype} for {model_type}:")
    environ["SEARCH_RANDOM"] = str(is_rand)
    params = Params(model_type=model_type).get_param_gen()
    for _ in range(n):
        try:
            gs_params = next(params).param_dict
        except StopIteration:
            gs_params = next(Params(model_type=model_type).get_param_gen()).param_dict

        for key in list(gs_params.keys()):
            print(key, gs_params[key])
        print("\n")


def create_or_update_configmap(config_name: str, namespace: str, json_file: Path):
    if not isinstance(json_file, Path):
        raise TypeError(f"Expected Path, got {type(json_file)}")
    if json_file.exists():
        hyperparams = loads(json_file.read_text())
    else:
        hyperparams = []
    # Flatten the hyperparameters for easy consumption in ConfigMap
    hyperparam_dict = {
        f"set{i + 1}": dumps(params) for i, params in enumerate(hyperparams)
    }

    # Generate the command for creating/updating ConfigMap
    cmd = [
        "kubectl",
        "create",
        "configmap",
        config_name,
        "--namespace",
        namespace,
        "--from-literal="
        + " ".join([f"{key}='{value}'" for key, value in hyperparam_dict.items()]),
        "--dry-run=client",
        "-o",
        "yaml",
        "|",
        "kubectl",
        "apply",
        "-f",
        "-",
    ]

    run(" ".join(cmd), shell=True)
    print(f"ConfigMap {config_name} created/updated in namespace {namespace}")
