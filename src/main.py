from random import choice

from tqdm import tqdm

# local imports
from alexlib.db import Connection
from alexlib.core import chkenv
from alexlib.iters import list_gen
from engine import ModelEngine
from params import Params, model_types
from features import Features
from setup import dbh, random_state as rand


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


def rand_feat():
    return [choice(feat_list)] if rand else feat_list


def drop_tab_pattern(pattern: str,
                     schema: str = schema,
                     dbh: Connection = dbh,
                     cascade: bool = True,
                     ):
    tabs = dbh.get_all_schema_tables(schema)
    droptabs = [x for x in tabs if pattern in x]
    for tab in droptabs:
        dbh.drop_table(schema, tab, cascade=cascade)


def run_all_models(schema: str = schema,
                   reset_schema: bool = reset_schema,
                   dbh: Connection = dbh
                   ):
    if reset_schema:
        drop_tab_pattern("results")
        drop_tab_pattern("param")
        dbh.trunc_schema(schema)
    model_gen = list_gen(model_types, rand=rand, inf=inf)
    while True:
        try:
            model = next(model_gen)
            for feat in tqdm(rand_feat()):
                params = Params(model_type=model)
                if grouped:
                    m = ModelEngine(
                        feat=feat,
                        params=params
                    )
                    m.fit_test_log()
                else:
                    params_list = list(params.get_param_gen())
                    for param in params_list:
                        m = ModelEngine(
                            feat=feat,
                            params=param
                        )
                        m.fit_test_log()
        except StopIteration:
            return True


def try_except_pass(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except RuntimeError:
        pass


if __name__ == "__main__":
    run_all_models()
