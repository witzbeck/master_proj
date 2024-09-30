from os import getenv

from numpy.random import choice
from tqdm import tqdm

from alexlib.core import istrue
from alexlib.files.utils import path_search
from model.engine import ModelEngine
from model.features import Features
from model.params import Params
from utils.constants import MODEL_TYPES
from utils.db_helpers import DbHelper
from utils.utils import list_gen

split_cols = ["is_stem", "is_female", "has_disability"]
search_int = int(getenv("SEARCH_ITER"))
grouped = istrue(getenv("SEARCH_GROUPED"))
rand = istrue(getenv("SEARCH_RANDOM"))
inf = istrue(getenv("INF_ITER"))
schema = getenv("LOG_SCHEMA")
reset_schema = istrue(getenv("RESET_SCHEMA"))

feat_dict = {
    "demographic": Features(to_include=split_cols, use_demographic=True),
    "engagement": Features(to_include=split_cols, use_engagement=True),
    "academic": Features(to_include=split_cols, use_academic=True),
    "all": Features(to_include=split_cols, use_all=True),
}
feat_list = list(feat_dict.values())


def rand_feat():
    return [choice(feat_list)] if rand else feat_list


def drop_tab_pattern(
    dbh: DbHelper,
    pattern: str,
    schema: str = schema,
    cascade: bool = True,
):
    tabs = dbh.get_all_schema_tables(schema)
    droptabs = [x for x in tabs if pattern in x]
    for tab in droptabs:
        dbh.drop_table(schema, tab, cascade=cascade)


def run_all_models(schema: str, reset_schema: bool, dbh: DbHelper):
    if reset_schema:
        drop_tab_pattern("results")
        drop_tab_pattern("param")
        dbh.trunc_schema(schema)
    model_gen = list_gen(MODEL_TYPES, rand=rand, inf=inf)
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


def try_except_pass(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except RuntimeError:
        pass


def create_view(dbh: DbHelper):
    path = path_search("eval_run_iter_results.sql")
    text = path.read_text()
    dbh.run_postgres_query(text)
