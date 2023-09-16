# standard library imports
from dataclasses import dataclass, field
from datetime import datetime

# third party imports
from tqdm import tqdm
from baycomp import two_on_multiple
import numpy as np
from numpy import zeros, array, nan, isnan
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.pyplot import subplots, title, legend
from matplotlib.pyplot import tick_params, xlabel, ylabel
from pandas import DataFrame, Series
from seaborn import heatmap
from scipy.stats import friedmanchisquare
from scikit_posthocs import posthoc_nemenyi_friedman

# eval and postprocessing
from sklearn.metrics import roc_curve, roc_auc_score

# local imports
from alexlib.db import Connection
from alexlib.df import filter_df, get_distinct_col_vals
from alexlib.config import chkenv
from alexlib.iters import keys, get_comb_gen, get_idx_val, link
from alexlib.maths import combine_domains, get_list_difs, get_rect_area
from setup import config

__range__ = range(-1, 3)
# values
LEFT, ROPE, RIGHT, OUT = __range__
MID = ROPE

# colors
BLUE = (68 / 255, 155 / 255, 214 / 255, 1.)
LIGHTGRAY = (.925, .925, .925, 1.)
WHITE = LIGHTGRAY
ORANGE = (222 / 255, 142 / 255, 8 / 255, 1.)
GRAY = (.5, .5, .5, 1.)

# decisions
XGREATER = "X > Y"
XLESS = "X < Y"
NODECISION = "No Decision"
XROPE = "ROPE"

window_params = {
    "bayes": {
        "rgb": {
            LEFT: BLUE,
            ROPE: GRAY,
            RIGHT: ORANGE,
            OUT: WHITE,
        },
        "vals": {
            LEFT: XGREATER,
            ROPE: XROPE,
            RIGHT: XLESS,
            OUT: NODECISION,
        },
    },
    "freq": {
        "rgb": {
            LEFT: BLUE,
            MID: WHITE,
            RIGHT: ORANGE,
        },
        "vals": {
            LEFT: XGREATER,
            MID: NODECISION,
            RIGHT: XLESS,
        },
    },
}

if __name__ == "__main__":
    config
    dbh = Connection.from_context("LOCAL")


class Abroca:
    def extend_tpr(self,
                   old_x: list,
                   old_y: list,
                   ):
        new_y = []
        idx_counter = 0
        for i in range(self.dlen):
            x = self.domain[i]
            if i < 2:
                new_y.append(0)
            elif (x in old_x and idx_counter == 0):
                val = get_idx_val(idx_counter, x, old_x, old_y)
                new_y.append(val)
                idx_counter += 1
            elif (x in old_x and idx_counter > 0):
                val = get_idx_val(idx_counter, x, old_x, old_y)
                new_y.append(val)
                idx_counter = 0
            else:
                new_y.append(new_y[-1])
        return array(new_y)

    def get_new_tpr(self, roc):
        x = list(roc.fpr)
        y = list(roc.tpr)
        return self.extend_tpr(x, y)

    def set_new_tprs(self):
        self.new_tpr1 = self.get_new_tpr(self.roc1)
        self.new_tpr2 = self.get_new_tpr(self.roc2)

    def set_domain(self):
        self.domain = combine_domains(self.roc1.fpr, self.roc2.fpr)
        self.ddifs = get_list_difs(self.domain)
        self.dlen = len(self.domain)

    def get_abroca(self):
        y1 = self.new_tpr1
        y2 = self.new_tpr2
        yrange = range(len(y1))
        heights = [y1[i] - y2[i] for i in yrange][1:]
        return get_rect_area(heights, self.ddifs)

    def set_abroca(self):
        self.abroca = self.get_abroca()

    def steps(self):
        self.set_domain()
        self.set_new_tprs()
        self.set_abroca()

    def __init__(self,
                 split_col: str,
                 curve_dict: dict
                 ):
        self.split_col = split_col
        self.keys = keys(curve_dict)
        self.roc1 = curve_dict[self.keys[0]]
        self.roc2 = curve_dict[self.keys[-1]]
        self.steps()

    @staticmethod
    def get_slice_label(split_col: str, key: str):
        val = key[5:]
        return f"{split_col} = {val}"

    @staticmethod
    def get_auc_str(auc: float, round_int: int = 4):
        return str(round(auc, round_int))

    def get_plot_label(self, key_idx: int, auc: float):
        key = self.keys[key_idx]
        slice_label = Abroca.get_slice_label(self.split_col, key)
        auc_str = Abroca.get_auc_str(auc)
        return f"{slice_label} | auc = {auc_str}"

    def plot(self, ax=None):
        x = self.domain
        y1 = self.new_tpr1
        y2 = self.new_tpr2
        abr_label = f"ABROCA = {Abroca.get_auc_str(self.abroca)}"
        if ax is None:
            _, ax = subplots(nrows=1, ncols=1, figsize=(16, 9))
        ax.plot(x, y1, label=self.get_plot_label(0, self.roc1.auc))
        ax.plot(x, y2, label=self.get_plot_label(-1, self.roc2.auc))
        ax.plot([], [], color="C0", alpha=0.3, label=abr_label)
        ax.fill_between(
            x,
            y1,
            y2,
            where=(y1 > y2),
            color="C0",
            interpolate=True,
            alpha=0.3
        )
        ax.fill_between(
            x,
            y1,
            y2,
            where=(y1 < y2),
            color="C0",
            interpolate=True,
            alpha=0.3
        )
        if ax is None:
            xlabel("False Positive Rate")
            ylabel("True Positive Rate")
            legend()
        else:
            return ax


class RocCurve:
    def get_rates(self):
        fpr, tpr, _ = roc_curve(self.y_true, self.y_prob)
        return fpr, tpr

    def set_rates(self):
        self.fpr, self.tpr = self.get_rates()

    def get_auc(self):
        return roc_auc_score(self.y_true, self.y_prob)

    def set_auc(self):
        self.auc = self.get_auc()

    def steps(self):
        self.set_rates()
        self.set_auc()

    def __init__(self,
                 y_true: list,
                 y_prob: list,
                 X_test: float,
                 ):
        self.y_true = y_true
        self.y_prob = y_prob
        self.X_test = X_test
        self.steps()

    @staticmethod
    def _mk_legend_text(auc: float,
                        round_dec: int = 2,
                        ):
        val = round(auc, 2)
        return f"AUC = {str(val)}"

    @staticmethod
    def _plot(fpr: list,
              tpr: list,
              auc: float,
              ax=None,
              _title: str = None,
              fill_auc: bool = False,
              ):
        if ax is None:
            _, ax = subplots(nrows=1, ncols=1, figsize=(12, 9))
        label = RocCurve._mk_legend_text(auc)
        ax.plot(fpr, tpr, label=label)
        if _title is not None:
            title(_title)
        if fill_auc:
            ax.fill_between(fpr, tpr, color="C0", interpolate=True, alpha=0.3)

    def plot(self, **kwargs):
        fpr = self.fpr
        tpr = self.tpr
        auc = self.auc
        RocCurve._plot(fpr, tpr, auc, **kwargs)

    def get_X_slices(self,
                     slice_col: str,
                     ):
        X_test = self.X_test
        vals = get_distinct_col_vals(X_test, slice_col)
        sc = slice_col
        fdf = filter_df
        return {f"slice{str(x)}": fdf(X_test, sc, x) for x in vals}

    def get_y_slice(self,
                    X_slice: dict,
                    y_series: Series
                    ):
        idx_list = list(X_slice.index)
        return y_series.loc[idx_list]

    def get_roc_obj(self,
                    X_test: list,
                    ):
        y_true = self.get_y_slice(X_test, self.y_true)
        y_prob = self.get_y_slice(X_test, self.y_prob)
        return RocCurve(y_true, y_prob, X_test)

    def get_roc_objs(self,
                     X_slices: dict,
                     ):
        curves = {}
        _keys = keys(X_slices)
        for key in _keys:
            X_test = X_slices[key]
            curves[key] = self.get_roc_obj(X_test)
        return curves

    def get_abroca(self, split_col: str):
        X_slices = self.get_X_slices(split_col)
        self.curves = self.get_roc_objs(X_slices)
        return Abroca(split_col, self.curves)

    def get_abrocas(self, split_cols: list):
        return [self.get_abroca(x) for x in split_cols]


def get_num(_str: str):
    if _str is None:
        return _str
    elif _str.isnumeric():
        return int(_str)
    elif _str.isalnum():
        return _str
    try:
        ret = int(_str)
    except ValueError:
        ret = float(_str)
    return ret


def try_array_float_list(_array: array,
                         key: str,
                         _type: str = "float",
                         ):
    if key == "n_jobs":
        return [int(x) for x in _array]
    elif key == "warm_start":
        return [bool(x) for x in _array]
    dtype = _array.dtype
    if dtype in [np.bool_, np.float_, np.int_]:
        return _array.tolist()
    try:
        return [get_num(x) for x in _array]
    except ValueError:
        return _array.tolist()


def format_clf_params(series: Series):
    keys = [x for x in series.columns if x[-3:] != "_id"]
    vals = [series[key].values for key in keys]
    rng = range(len(keys))
    func = try_array_float_list
    return {f"clf__{keys[i]}": func(vals[i], keys[i]) for i in rng}


@dataclass
class ModelResult:
    model_type: str = field(default="")
    run_id: int = field(default=0)
    iter_id: int = field(default=0)
    mean_fit_time: float = field(default=0.)
    std_fit_time: float = field(default=0.)
    mean_score_time: float = field(default=0.)
    std_score_time: float = field(default=0.)
    mean_test_roc_auc: float = field(default=0.)
    std_test_roc_auc: float = field(default=0.)
    rank_test_roc_auc: int = field(default=0)
    timestamp: datetime = field(default=datetime.now())
    inc_aca: bool = field(default=False)
    inc_dem: bool = field(default=False)
    inc_eng: bool = field(default=False)
    inc_all: bool = field(default=False)
    splits_test_roc_auc: list = field(default_factory=list)
    name: str = field(default="")
    params: list = field(default_factory=list)

    def get_name(self) -> str:
        m = self.model_type
        r = str(self.run_id)
        i = str(self.iter_id)
        n = self.feat = self.name
        return "_".join([m, r, i, n])

    def __repr__(self) -> str:
        return self.name

    def __post_init__(self):
        self.name = self.get_name()
        self.splits_test_roc_auc = array(self.splits_test_roc_auc).ravel()

    def sort_cols(df: DataFrame):
        if type(df) == dict:
            cols = list(df.keys())
        else:
            cols = list(df.columns)
        split_cols = [col for col in cols if "split" in col]
        other_cols = [col for col in cols if col not in split_cols]
        return split_cols, other_cols

    def from_engine(engine):
        series = engine.get_all_results_log()
        split_cols, other_cols = ModelResult.sort_cols(series)
        split_vals = [series[col] for col in split_cols]
        kwargs = {col: series[col] for col in other_cols}
        kwargs["splits_test_roc_auc"] = split_vals
        return ModelResult(**kwargs)

    def get_params(self, dbh: Connection):
        sql = f"""
        select *
        from {chkenv("LOG_SCHEMA")}.params_{self.model_type}
        where run_id={self.run_id}
        and iter_id={self.iter_id}
        """
        series = dbh.run_pd_query(sql)
        return format_clf_params(series)

    def set_params(self, dbh: Connection):
        self.params = self.get_params(dbh)


@dataclass
class Results:
    schema: str = field(default=chkenv("LOG_SCHEMA"))
    table: str = field(default="v_all_runs_results")
    rope: float = field(default=chkenv("EVAL_ROPE", type=float))
    runs: int = field(default=chkenv("CV_NREPEATS", type=int))
    lim: int = field(default=None)
    obj_list: list = field(default_factory=list)

    @staticmethod
    def alpha_eval(p: float,
                   i: int,
                   j: int,
                   alpha: float = chkenv("ALPHA", type=float),
                   ):
        if p > alpha:
            return MID
        else:
            return LEFT if i < j else RIGHT

    @staticmethod
    def rope_eval(outcome: tuple,
                  flexible: bool = chkenv("ROPE_FLEXIBLE", type=bool),
                  upbound: float = chkenv("ROPE_UPBOUND", type=float),
                  ) -> float:
        pleft, prope, pright = outcome
        absdif = abs(pleft - pright)

        if prope >= upbound:
            return ROPE
        elif pright >= upbound:
            return RIGHT
        elif pleft >= upbound:
            return LEFT
        elif absdif <= 1 - upbound:
            return ROPE
        elif (pleft > (prope + pright) and flexible):
            return LEFT
        elif (pright > (prope + pleft) and flexible):
            return RIGHT
        elif (prope > (pright + pleft) and flexible):
            return ROPE
        else:
            return OUT

    def get_splits(self):
        return [x.splits_test_roc_auc for x in self.obj_list]

    def get_splits_array(self):
        splits = self.get_splits()
        return array(splits).T

    def do_friedman(self):
        splits = self.get_splits()
        return friedmanchisquare(splits)

    def do_nemenyi(self):
        splits_array = self.get_splits_array()
        return posthoc_nemenyi_friedman(splits_array)

    def iter_df(self):
        _range = range(len(self.df))
        for i in _range:
            yield self.df.iloc[i, :]

    def sort_cols(self):
        self.cols = list(self.df.columns)
        sc = self.split_cols
        self.split_cols = [col for col in self.cols if "split" in col]
        self.other_cols = [col for col in self.cols if col not in sc]

    def get_res_obj(self, series: Series):
        split_vals = [series[col] for col in self.split_cols]
        kwargs = {col: series[col] for col in self.other_cols}
        kwargs["splits_test_roc_auc"] = split_vals
        return ModelResult(**kwargs)

    def get_res_objs(self):
        self.iseries = self.iter_df()
        self.obj_list = [self.get_res_obj(s) for s in self.iseries]
        self.obj_dict = {str(obj): obj for obj in self.obj_list}
        self.sort_cols()

    def get_results(self) -> DataFrame:
        s = self.schema
        t = self.table
        if self.lim is None:
            return self.dbh.get_table(s, t)
        else:
            return self.dbh.get_table(s, t, nrows=self.lim)

    def get_index_grid(self,
                       nanvar: str = None,
                       asarray: bool = True
                       ):
        rng = self._range
        index = [[i if i != j else nanvar for i in self._range] for j in rng]
        if asarray:
            return array(index)
        return index

    def init_steps(self):
        if len(self.obj_list) == 0:
            self.df = self.get_results()
            self.sort_cols()
            self.get_res_objs()
        self._len = len(self.obj_list)
        self._range = range(self._len)
        ol = self.obj_list
        self.obj_names = [f"{str(ol[i])} ({i})" for i in range(len(ol))]
        self.index = self.get_comp_index()
        self.index_grid = self.get_index_grid()

    def __len__(self):
        return len(self.obj_list)

    def __post_init__(self):
        self.dbh = Connection.from_context("LOCAL")
        self.init_steps()

    def get_comp_index(self):
        lists = [[(i, j) for i in self._range] for j in self._range]
        _list = link(lists)
        return _list

    def get_comp_grid(self, bayes: bool):
        z = zeros((self._len, self._len))
        for i in self._range:
            z[i][i] = OUT if bayes else MID
        return z

    def bayes_comp_2_objs(self,
                          obj1: ModelResult,
                          obj2: ModelResult,
                          runs: int = None,
                          plot: bool = False,
                          names: tuple = None,
                          ) -> tuple | list:
        if runs is None:
            runs = 1
        obj1_vals = obj1.splits_test_roc_auc
        obj2_vals = obj2.splits_test_roc_auc
        if (plot and names is None):
            names = (str(obj1), str(obj2))
        return two_on_multiple(
            obj1_vals,
            obj2_vals,
            rope=self.rope,
            runs=runs,
            plot=plot,
            names=names
        )

    def comp_2_idx(self,
                   idx1: int,
                   idx2: int,
                   bayes: bool,
                   plot: bool = False,
                   runs: int = None,
                   names: bool = None,
                   nemenyi_grid: array = None,
                   ) -> tuple:
        if bayes:
            obj1 = self.obj_list[idx1]
            obj2 = self.obj_list[idx2]
            runs = 1 if runs is None else runs
            comp = self.bayes_comp_2_objs(obj1,
                                          obj2,
                                          plot=plot,
                                          names=names
                                          )
            return comp if not plot else comp[0]
        else:
            return nemenyi_grid[idx1][idx2]

    def get_mask_grid(self):
        mask_grid = self.get_comp_grid()
        for pair in self.index:
            i, j = pair[0], pair[-1]
            if i == j:
                mask_grid[i][j] = True
            else:
                mask_grid[i][j] = 0
        return mask_grid

    def gen_eval_steps(self,
                       bayes: bool,
                       grid: array,
                       use_matsym: bool,
                       nemenyi_grid: array = None
                       ) -> DataFrame:
        if not bayes:
            nemenyi_grid = self.do_nemenyi()
        if use_matsym:
            idx = [x for x in self.index if x[0] > x[-1]]
        else:
            idx = [x for x in self.index if x[0] != x[-1]]

        for pair in idx:
            i, j = pair
            comp = self.comp_2_idx(i,
                                   j,
                                   bayes,
                                   plot=False,
                                   nemenyi_grid=nemenyi_grid,
                                   )
            if bayes:
                eval = Results.rope_eval(comp)
            else:
                eval = Results.alpha_eval(comp, i, j)
            grid[i][j] = eval
            if (use_matsym and eval == LEFT):
                grid[j][i] = RIGHT
            elif (use_matsym and eval == RIGHT):
                grid[j][i] = LEFT
            elif use_matsym:
                grid[j][i] = eval
        return DataFrame(grid.T, index=self.obj_names)

    def eval_all(self,
                 bayes: bool,
                 use_matsym: bool = True):
        self.grid = self.get_comp_grid(bayes)
        return self.gen_eval_steps(bayes, self.grid, use_matsym)

    @staticmethod
    def get_window_params(bayes: bool,
                          params: dict = window_params
                          ):
        if bayes:
            return params["bayes"]
        else:
            return params["freq"]

    def plot_windowpane(self,
                        bayes: bool = True,
                        df: DataFrame = None,
                        use_matsym: bool = True,
                        figsize: tuple = None,
                        annot: str = None,  # vals, index, none
                        labelsize: int = 3,
                        dpi: int = 800,
                        annot_fontsize: str = "x-small"
                        ):
        rng = self._range
        if df is None:
            df = self.eval_all(bayes, use_matsym)
        cbar_params = Results.get_window_params(bayes)
        if figsize is None:
            aspectratio = 16 / 25
            lenratio = 1 / 2
            w = int(len(df) * lenratio)
            h = int(w * aspectratio)
            figsize = (w, h)

        cbar_rgb = cbar_params["rgb"]
        cbar_vals = cbar_params["vals"]
        n = len(cbar_vals)
        _range = range(-1, n)
        norm = BoundaryNorm(_range, n)
        cmap = ListedColormap(list(cbar_rgb.values()), n)
        fig, ax = subplots(
            nrows=1,
            ncols=1,
            figsize=figsize,
            dpi=dpi,
        )
        if annot is False:
            pass
        elif annot is None:
            annot = False
        elif annot == "index":
            annot = [[str(i) if i != j else "" for i in rng] for j in rng]
        elif annot == "values":
            sg = self.grid.astype(str)
            annot = [[sg[i][j] if i != j else "" for i in rng] for j in rng]
        else:
            raise ValueError("invalid input for annot")
        ax.tick_params(axis="both", labelsize=labelsize, pad=0)
        ax = heatmap(df,
                     ax=ax,
                     cmap=cmap,
                     norm=norm,
                     xticklabels=False,
                     cbar_kws={"shrink": 0.15},
                     annot=annot,
                     annot_kws={
                         "fontsize": annot_fontsize,
                         "color": "black",
                     },
                     linewidths=0.5,
                     )
        for text in ax.texts:
            if (text.get_text() in [str(OUT), None, nan, "None"]):
                text.set_text("")
        cbar = ax.collections[0].colorbar
        r = cbar.vmax - cbar.vmin
        cbar.set_ticks([cbar.vmin + r / n * (0.5 + i) for i in range(n)])
        cbar.set_ticklabels(list(cbar_vals.values()))
        tick_params(left=False,)
        return fig, ax

    def get_top_cluster(self,
                        _len: bool = False,
                        _obj_list: bool = False,
                        _res_obj: bool = True,
                        ):
        grid = self.grid
        top_row = grid[0][1:]
        top_val = top_row[0]
        i = 1
        ival = top_row[0]
        while True:
            ival = top_row[i]
            if i == 1:
                i += 1
            elif (ival == top_val or (isnan(ival) and isnan(top_row[i - 1]))):
                i += 1
            elif _len:
                return i
            elif _res_obj:
                return Results(lim=i)
            elif _obj_list:
                return self.obj_list[:i]
            else:
                return top_row[:i]

    def get_top_cluster_gen(self):
        cluster_len = self.get_top_cluster(_len=True)
        cluster_range = range(cluster_len)
        return get_comb_gen(cluster_range, 2)

    def get_cluster_comp_gen(self, plot: bool = False):
        for pair in self.get_top_cluster_gen():
            yield self.comp_2_idx(*pair, plot=plot)

    @staticmethod
    def from_engines(engine_list: list, **kwargs):
        obj_list = [ModelResult.from_engine(engine) for engine in engine_list]
        return Results(obj_list=obj_list, **kwargs)


def comp_rope_vals():
    rope_comp_id = 0
    ropes = [i / 10000 for i in range(5, 101, 5)]
    for rope in tqdm(ropes):
        for runs in [1]:
            records = []
            res = Results(rope=rope, runs=runs, lim=150)
            if rope_comp_id == 0:
                res.dbh.trunc_table(chkenv("LOG_SCHEMA"), "rope_comp")
                if_exists = "append"
                ncomp = (len(res.obj_list) ** 2) / 2
                print(f"n comparisons = {ncomp}")
            else:
                if_exists = "append"
            idx = res.get_comp_index()
            for pair in idx:
                i, j = pair[0], pair[-1]
                if j >= i:
                    pass
                else:
                    obj1, obj2 = res.obj_list[i], res.obj_list[j]
                    comp = res.comp_2_idx(i, j, runs=runs)
                    eval = res.eval_comp(comp)
                    rec = {
                        "rope_comp_id": rope_comp_id,
                        "i": i,
                        "j": j,
                        "run_id1": obj1.run_id,
                        "run_id2": obj2.run_id,
                        "iter_id1": obj1.iter_id,
                        "iter_id2": obj2.iter_id,
                        "name1": obj1.name,
                        "name2": obj2.name,
                        "mean_test_roc_auc1": obj1.mean_test_roc_auc,
                        "std_test_roc_auc1": obj1.std_test_roc_auc,
                        "mean_test_roc_auc2": obj2.mean_test_roc_auc,
                        "std_test_roc_auc2": obj2.std_test_roc_auc,
                        "rope": rope,
                        "runs": runs,
                        "pleft": comp[0],
                        "prope": comp[1],
                        "pright": comp[2],
                        "eval": eval
                    }
                    records.append(rec)
            rope_comp_id += 1
            df = DataFrame.from_records(records)
            df.to_sql(
                "rope_comp",
                con=res.dbh.engine,
                schema=chkenv("LOG_SCHEMA"),
                if_exists=if_exists,
                index=True,
                method="multi"
            )
