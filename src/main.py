"""A module to run all models in the database."""
from random import choice

from tqdm import tqdm

from alexlib.db.managers import PostgresManager
from alexlib.core import chkenv
from alexlib.iters import list_gen
from engine import ModelEngine
from params import Params
from features import Features
from constants import MODEL_TYPES
from setup import db_mgr as cnxn, random_state


split_cols = ["is_stem", "is_female", "has_disability"]
search_int = chkenv("SEARCH_ITER", type=int)
grouped = chkenv("SEARCH_GROUPED", type=bool)
inf = chkenv("INF_ITER", type=bool)
schema = chkenv("LOG_SCHEMA")
reset_schema = chkenv("RESET_SCHEMA", type=bool)

feat_dict = {
    "demographic": Features(to_include=split_cols, use_demographic=True),
    "engagement": Features(to_include=split_cols, use_engagement=True),
    "academic": Features(to_include=split_cols, use_academic=True),
    "all": Features(to_include=split_cols, use_all=True),
}
feat_list = list(feat_dict.values())


def rand_feat() -> list:
    """Returns a random feature from the feat_list. If random_state is False, returns the entire list."""
    return [choice(feat_list)] if random_state else feat_list


def run_all_models(
    schema: str = schema,
    reset_schema: bool = reset_schema,
    cnxn: PostgresManager = cnxn,
) -> bool:
    """Runs all models in the database. If reset_schema is True, resets the schema. If random_state is False, runs all models. If random_state is True, runs a random model. If grouped is True, runs all models with the same feature. If grouped is False, runs all models with all features. If inf is True, runs the models infinitely. If inf is False, runs the models once."""
    if reset_schema:
        cnxn.drop_table_pattern("results")
        cnxn.drop_table_pattern("param")
        cnxn.truncate_schema(schema)
    model_gen = list_gen(MODEL_TYPES, rand=random_state, inf=inf)
    while True:
        try:
            model = next(model_gen)
            for feat in tqdm(rand_feat()):
                params = Params(model_type=model)
                if grouped:
                    m = ModelEngine(feat=feat, params=params)
                    m.fit_test_log()
                else:
                    params_list = list(params.get_param_gen())
                    for param in params_list:
                        m = ModelEngine(feat=feat, params=param)
                        m.fit_test_log()
        except StopIteration:
            return True


def try_except_pass(func, *args, **kwargs) -> None:
    """Runs a function and passes if a RuntimeError is raised."""
    try:
        func(*args, **kwargs)
    except RuntimeError:
        pass


if __name__ == "__main__":
    run_all_models()
