from itertools import chain, combinations
from pathlib import Path

from matplotlib.pyplot import savefig
from numpy import array
from numpy.random import randint
from pandas import DataFrame, Series

from utils.constants import FIGURES_PATH


def idx_list(nrows: int, ncols: int):
    """Create a list of index pairs for a 2D matrix"""
    return list(
        chain.from_iterable([[(i, j) for j in range(ncols)] for i in range(nrows)])
    )


def figsave(
    figname: str,
    figpath: Path = FIGURES_PATH,
    format: str = "png",
    **kwargs,  # use bb_inches=tight if cutoff
):
    fullpath = figpath / f"{figname}.{format}"
    savefig(fullpath, format=format, **kwargs)
    return fullpath.exists()


def get_comb_gen(_list: list, _int: int):
    for pair in combinations(_list, _int):
        yield pair


def list_gen(_list: list, rand: bool = False, inf: bool = False):
    _list = list(_list)
    while True:
        _len = len(_list)
        if _len > 0:
            _idx = randint(_len) if rand else 0
            if inf:
                yield _list[_idx]
            else:
                yield _list.pop(_idx)
        else:
            break


def unpack_clf_keys(params_dict: dict):
    return [x.split("__")[-1] for x in params_dict.keys()]


def unpack_clf_params(params_dict: dict):
    new_keys = unpack_clf_keys(params_dict)
    vals = list(params_dict.values())
    _range = range(len(new_keys))
    return {new_keys[i]: vals[i] for i in _range}


def lengthen_params_log(params_log: dict):
    keys = list(params_log.keys())
    vals = list(params_log.values())
    rg = range(len(params_log))
    log = []
    for i in rg:
        val = vals[i]
        if val is None:
            log.append([val])
        elif (valt := type(val)) in [str, float, int, bool]:
            log.append([val])
        elif valt in [list, tuple]:
            log.append(list(val))
        else:
            log.append(val.data.tolist())
    plen = max(len(x) for x in log)
    return {keys[i]: log[i] * plen if len(log[i]) == 1 else log[i] for i in rg}


def overwrite_std_params(clf_params: dict, std_params: dict, all: bool = True):
    new_params = unpack_clf_params(clf_params)
    out_params = {
        key: new_params[key] if key in new_params else std_val
        for key, std_val in std_params.items()
    }
    if all:
        return lengthen_params_log(out_params)
    else:
        return out_params


def get_props(series: Series):
    dist_vals = list(series.unique())
    n_all_vals = len(series)
    freqs = [sum(series == x) for x in dist_vals]
    props = [sum(series == x) / n_all_vals for x in dist_vals]
    return DataFrame.from_dict(
        {
            "value": dist_vals,
            "frequency": freqs,
            "proportion": props,
        }
    )


def make_prop_dict(df: DataFrame):
    non_id_cols = [x for x in df.columns if x[-3:] != "_id"]
    all_series = [Series(df.loc[:, x]) for x in non_id_cols]
    return {col: get_props(col) for col in all_series}


def rm_pattern(list_of_strs: list, pattern: str, end: bool = True):
    if end is True:
        p_len = -len(pattern)
        return [x for x in list_of_strs if x[p_len:] != pattern]
    else:
        p_len = len(pattern)
        return [x for x in list_of_strs if x[:p_len] != pattern]


def wo_ids(x: str):
    return rm_pattern(x, "_id")


def percentiles(_list: list, tiles: int = 100):
    _list = list(_list)
    _list.sort(key=lambda x: int(x))
    _len = len(_list)
    out_dict = {}
    tile_ratio = 1 / tiles
    idx_ratio = _len * tile_ratio

    out_dict["0"] = _list[0]
    for i in range(1, tiles):
        tile_idx = int(i * idx_ratio)
        out_dict[i] = _list[tile_idx]

    out_dict[tiles] = _list[-1]
    return out_dict


def combine_domains(x1: list, x2: list):
    x = list(set(list(x1) + list(x2)))
    domain = x * 2
    domain.sort()
    return array(domain)


def get_list_difs(_list):
    _range = range(len(_list))
    return [_list[i - 1] - _list[i] for i in _range if i > 0]


def get_list_mids(_list: list):
    _range = range(len(_list))
    return [(_list[i - 1] + _list[i]) / 2 for i in _range if i > 0]


def get_rect_area(heights: list, widths: list, absolute: bool = True):
    _range = range(len(heights))
    rect_areas = [heights[i] * widths[i] for i in _range]
    if absolute:
        return sum(abs(x) for x in rect_areas)
    return sum(rect_areas)


def get_idx_val(idx_counter, in_val, in_list, out_list):
    idx = in_list.index(in_val, idx_counter)
    return out_list[idx]
