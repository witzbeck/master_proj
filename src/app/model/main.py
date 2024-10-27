from numpy.random import choice
from tqdm import tqdm

from constants import INF_ITER, MODEL_TYPES, SEARCH_GROUPED, SEARCH_RANDOM
from model.engine import ModelEngine
from model.features import SPLIT_COLUMNS, Features
from model.params import Params

feat_dict = {
    "demographic": Features(to_include=SPLIT_COLUMNS, use_demographic=True),
    "engagement": Features(to_include=SPLIT_COLUMNS, use_engagement=True),
    "academic": Features(to_include=SPLIT_COLUMNS, use_academic=True),
    "all": Features(to_include=SPLIT_COLUMNS, use_all=True),
}
feat_list = list(feat_dict.values())


def rand_feat():
    return [choice(feat_list)] if SEARCH_RANDOM else feat_list


# redo how logs work
# log to files instead of db


def list_gen(lst, rand=False, inf=False):
    while True:
        if rand:
            yield choice(lst)
        else:
            for item in lst:
                yield item
        if not inf:
            break


def run_all_models():
    model_gen = list_gen(MODEL_TYPES, rand=SEARCH_RANDOM, inf=INF_ITER)
    while True:
        try:
            model = next(model_gen)
            for feat in tqdm(rand_feat()):
                params = Params(model_type=model)
                if SEARCH_GROUPED:
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
