"""A module for analyzing the results of a model run."""

from collections.abc import Generator
from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property
from itertools import chain

from baycomp import two_on_multiple
from duckdb import DuckDBPyConnection
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.pyplot import legend, subplots, tick_params, title, xlabel, ylabel
from numpy import array, bool_, floating, int_, integer, isnan, nan, ndarray, zeros
from pandas import DataFrame, Series
from scikit_posthocs import posthoc_nemenyi_friedman
from scipy.stats import friedmanchisquare
from seaborn import heatmap
from sklearn.metrics import roc_auc_score, roc_curve
from tqdm import tqdm

from alexlib.db.managers import PostgresManager
from alexlib.df import filter_df, get_distinct_col_vals
from alexlib.iters import get_comb_gen
from alexlib.maths import combine_domains, get_list_difs, get_rect_area

from constants import (
    ALPHA,
    CV_NREPEATS,
    EVAL_ROPE,
    LEFT,
    LOG_SCHEMA,
    MID,
    OUT,
    RIGHT,
    ROPE,
    ROPE_FLEXIBLE,
    ROPE_UPBOUND,
    WINDOWPANE_PLOT_PARAMS,
)
from utils import get_idx_val


class Abroca:
    """A class for calculating the area between two ROC curves."""

    def extend_tpr(
        self,
        old_x: list,
        old_y: list,
    ) -> list:
        """Extend the TPR to the new domain."""
        new_y = []
        idx_counter = 0
        for i in range(self.dlen):
            x = self.domain[i]
            if i < 2:
                new_y.append(0)
            elif x in old_x and idx_counter == 0:
                val = get_idx_val(idx_counter, x, old_x, old_y)
                new_y.append(val)
                idx_counter += 1
            elif x in old_x and idx_counter > 0:
                val = get_idx_val(idx_counter, x, old_x, old_y)
                new_y.append(val)
                idx_counter = 0
            else:
                new_y.append(new_y[-1])
        return array(new_y)

    def get_new_tpr(self, roc) -> list:
        """Get the new TPR for the new domain."""
        x = list(roc.fpr)
        y = list(roc.tpr)
        return self.extend_tpr(x, y)

    def set_new_tprs(self) -> None:
        """Set the new TPRs for the new domain."""
        self.new_tpr1 = self.get_new_tpr(self.roc1)
        self.new_tpr2 = self.get_new_tpr(self.roc2)

    def set_domain(self) -> None:
        """Set the domain for the new TPRs."""
        self.domain = combine_domains(self.roc1.fpr, self.roc2.fpr)
        self.ddifs = get_list_difs(self.domain)
        self.dlen = len(self.domain)

    def get_abroca(self) -> float:
        """Get the ABROCA."""
        y1 = self.new_tpr1
        y2 = self.new_tpr2
        yrange = range(len(y1))
        heights = [y1[i] - y2[i] for i in yrange][1:]
        return get_rect_area(heights, self.ddifs)

    def set_abroca(self) -> None:
        """Set the ABROCA."""
        self.abroca = self.get_abroca()

    def steps(self) -> None:
        """Run the steps for the class."""
        self.set_domain()
        self.set_new_tprs()
        self.set_abroca()

    @property
    def keys(self) -> list[str]:
        """Get the keys for the curves."""
        return list(self.curves.keys())

    def __init__(self, split_col: str, curve_dict: dict) -> None:
        """Initialize the class."""
        self.split_col = split_col
        self.curves = curve_dict  # Add this line
        self.roc1 = self.curves[self.keys[0]]
        self.roc2 = self.curves[self.keys[-1]]
        self.steps()

    @staticmethod
    def get_slice_label(split_col: str, key: str) -> str:
        """Get the slice label for the ABROCA plot."""
        val = key[5:]
        return f"{split_col} = {val}"

    @staticmethod
    def get_auc_str(auc: float, round_int: int = 4) -> str:
        """Get the AUC string."""
        return str(round(auc, round_int))

    def get_plot_label(self, key_idx: int, auc: float):
        """Get the plot label for the ABROCA plot."""
        key = self.keys[key_idx]
        slice_label = Abroca.get_slice_label(self.split_col, key)
        auc_str = Abroca.get_auc_str(auc)
        return f"{slice_label} | auc = {auc_str}"

    def plot(self, ax=None) -> None:
        """Plot the ABROCA."""
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
            x, y1, y2, where=(y1 > y2), color="C0", interpolate=True, alpha=0.3
        )
        ax.fill_between(
            x, y1, y2, where=(y1 < y2), color="C0", interpolate=True, alpha=0.3
        )
        if ax is None:
            xlabel("False Positive Rate")
            ylabel("True Positive Rate")
            legend()
        else:
            return ax


@dataclass
class RocCurve:
    """A class for calculating the ROC curve."""

    y_true: ndarray
    y_prob: ndarray
    X_test: ndarray
    fpr: ndarray = field(init=False)
    tpr: ndarray = field(init=False)

    @cached_property
    def roc_curve(self) -> tuple[ndarray, ndarray, ndarray]:
        """Get the ROC curve."""
        return roc_curve(self.y_true, self.y_prob)

    def set_rates(self) -> None:
        """Set the rates for the ROC curve."""
        self.fpr, self.tpr, _ = self.roc_curve

    @cached_property
    def auc(self) -> float:
        """Get the AUC for the ROC curve."""
        return roc_auc_score(self.y_true, self.y_prob)

    def __post_init__(self) -> None:
        """Initialize the class."""
        self.set_rates()

    @staticmethod
    def _mk_legend_text(
        auc: float,
        roundto: int = 2,
    ) -> str:
        """Make the legend text for the ROC curve."""
        val = round(auc, roundto)
        return f"AUC = {str(val)}"

    @staticmethod
    def _plot(
        fpr: list,
        tpr: list,
        auc: float,
        ax=None,
        _title: str = None,
        fill_auc: bool = False,
    ) -> None:
        """Plot the ROC curve."""
        if ax is None:
            _, ax = subplots(nrows=1, ncols=1, figsize=(12, 9))
        label = RocCurve._mk_legend_text(auc)
        ax.plot(fpr, tpr, label=label)
        if _title is not None:
            title(_title)
        if fill_auc:
            ax.fill_between(fpr, tpr, color="C0", interpolate=True, alpha=0.3)

    def plot(self, **kwargs) -> None:
        """Plot the ROC curve."""
        RocCurve._plot(self.fpr, self.tpr, self.auc, **kwargs)

    def get_X_slices(
        X_test: DataFrame,
        slice_col: str,
    ) -> dict:
        """Get the slices for the ROC curve."""
        vals = get_distinct_col_vals(X_test, slice_col)
        return {f"slice{str(x)}": filter_df(X_test, slice_col, x) for x in vals}

    @staticmethod
    def get_y_slice(X_slice: DataFrame, y_series: Series) -> Series:
        """Get the Y slice for the ROC curve."""
        return y_series.loc[X_slice.index]

    def get_roc_obj(
        self,
        X_test: list,
    ) -> "RocCurve":
        """Get the ROC object for the ROC curve."""
        y_true = self.get_y_slice(X_test, self.y_true)
        y_prob = self.get_y_slice(X_test, self.y_prob)
        return RocCurve(y_true=y_true, y_prob=y_prob, X_test=X_test)

    def get_roc_objs(
        self,
        X_slices: dict,
    ) -> dict:
        """Get the ROC objects for the ROC curve."""
        return {k: self.get_roc_obj(v) for k, v in X_slices.items()}

    def get_abroca(self, split_col: str) -> Abroca:
        """Get the ABROCA for the ROC curve."""
        X_slices = self.get_X_slices(split_col)
        self.curves = self.get_roc_objs(X_slices)
        return Abroca(split_col, self.curves)

    def get_abrocas(self, split_cols: list) -> list[float]:
        """Get the ABROCAs for the ROC curve."""
        return [self.get_abroca(x) for x in split_cols]


def get_num(value) -> float | int | str | None:
    """Attempt to convert the value to an int or float, return original value if fails."""
    if value is None:
        return value
    if isinstance(value, (int, float, integer, floating)):
        return value
    try:
        return int(value)
    except (ValueError, TypeError):
        pass
    try:
        return float(value)
    except (ValueError, TypeError):
        return value


def try_array_float_list(
    array_: array,
    key: str,
    _type: str = "float",
) -> list:
    """Try to convert the array to a list."""
    if key == "n_jobs":
        return [int(x) for x in array_]
    elif key == "warm_start":
        return [bool(x) for x in array_]
    dtype = array_.dtype
    if max(isinstance(dtype, t) for t in [bool_, floating, int_]):
        return array_.tolist()
    try:
        return [get_num(x) for x in array_]
    except ValueError:
        return array_.tolist()


def format_clf_params(series: Series) -> dict[str, list]:
    """Format the classifier parameters."""
    keys = [x for x in series.columns if x[-3:] != "_id"]
    vals = [series[key].values for key in keys]
    rng = range(len(keys))
    func = try_array_float_list
    return {f"clf__{keys[i]}": func(vals[i], keys[i]) for i in rng}


@dataclass
class ModelResult:
    """A class for the model results."""

    model_type: str = field(default="")
    run_id: int = field(default=0)
    iter_id: int = field(default=0)
    mean_fit_time: float = field(default=0.0)
    std_fit_time: float = field(default=0.0)
    mean_score_time: float = field(default=0.0)
    std_score_time: float = field(default=0.0)
    mean_test_roc_auc: float = field(default=0.0)
    std_test_roc_auc: float = field(default=0.0)
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
        """Get the name for the model result."""
        return "_".join(
            [
                str(x)
                for x in [self.model_type, self.run_id, self.iter_id, self.name]
                if x
            ]
        )

    def __repr__(self) -> str:
        """Get the representation for the model result."""
        return self.name

    def __post_init__(self) -> None:
        """Run the post init steps for the class."""
        self.name = self.get_name()
        self.splits_test_roc_auc = array(self.splits_test_roc_auc).ravel()

    def sort_cols(df: DataFrame) -> tuple[list, list]:
        """Sort the columns for the dataframe."""
        cols = list(df.keys()) if isinstance(df, dict) else list(df.columns)
        split_cols = [col for col in cols if "split" in col]
        other_cols = [col for col in cols if col not in split_cols]
        return split_cols, other_cols

    def from_engine(engine) -> "ModelResult":
        """Get the model result from the engine."""
        series = engine.get_all_results_log()
        split_cols, other_cols = ModelResult.sort_cols(series)
        split_vals = [series[col] for col in split_cols]
        kwargs = {col: series[col] for col in other_cols}
        kwargs["splits_test_roc_auc"] = split_vals
        return ModelResult(**kwargs)

    def get_params(self, dbh: PostgresManager) -> dict[str:list]:
        """Get the parameters for the model result."""
        sql = f"""
        select *
        from {LOG_SCHEMA}.params_{self.model_type}
        where run_id={self.run_id}
        and iter_id={self.iter_id}
        """
        series = dbh.run_pd_query(sql)
        return format_clf_params(series)

    def set_params(self, dbh: PostgresManager) -> None:
        """Set the parameters for the model result."""
        self.params = self.get_params(dbh)


@dataclass
class Results:
    """A class for the model results."""

    schema: str = LOG_SCHEMA
    table: str = "v_all_runs_results"
    rope: float = EVAL_ROPE
    runs: int = CV_NREPEATS
    lim: int = field(default=None)
    obj_list: list = field(default_factory=list)

    @staticmethod
    def alpha_eval(
        p: float,
        i: int,
        j: int,
        alpha: float = ALPHA,
    ) -> int:
        """Evaluate the alpha."""
        if p > alpha:
            return MID
        else:
            return LEFT if i < j else RIGHT

    @staticmethod
    def rope_eval(
        outcome: tuple,
        flexible: bool = ROPE_FLEXIBLE,
        upbound: float = ROPE_UPBOUND,
    ) -> float:
        """Evaluate the ROPE."""
        pleft, prope, pright = outcome
        absdif = abs(pleft - pright)

        if prope >= upbound:
            ret = ROPE
        elif pright >= upbound:
            ret = RIGHT
        elif pleft >= upbound:
            ret = LEFT
        elif absdif <= 1 - upbound:
            ret = ROPE
        elif pleft > (prope + pright) and flexible:
            ret = LEFT
        elif pright > (prope + pleft) and flexible:
            ret = RIGHT
        elif prope > (pright + pleft) and flexible:
            ret = ROPE
        else:
            ret = OUT
        return ret

    def get_splits(self) -> list:
        """Get the splits for the model results."""
        return [x.splits_test_roc_auc for x in self.obj_list]

    def get_splits_array(self) -> array:
        """Get the splits array for the model results."""
        splits = self.get_splits()
        return array(splits).T

    def do_friedman(self) -> tuple:
        """Do the Friedman test for the model results."""
        splits = self.get_splits()
        return friedmanchisquare(*splits)

    def do_nemenyi(self) -> array:
        """Do the Nemenyi test for the model results."""
        splits_array = self.get_splits_array()
        return posthoc_nemenyi_friedman(splits_array)

    def iter_df(self) -> Generator[Series]:
        """Iterate through the dataframe."""
        _range = range(len(self.df))
        for i in _range:
            yield self.df.iloc[i, :]

    def sort_cols(self) -> None:
        """Sort the columns for the dataframe."""
        self.cols = list(self.df.columns)
        sc = self.split_cols
        self.split_cols = [col for col in self.cols if "split" in col]
        self.other_cols = [col for col in self.cols if col not in sc]

    def get_res_obj(self, series: Series) -> ModelResult:
        """Get the result object for the dataframe."""
        split_vals = [series[col] for col in self.split_cols]
        kwargs = {col: series[col] for col in self.other_cols}
        kwargs["splits_test_roc_auc"] = split_vals
        return ModelResult(**kwargs)

    def get_res_objs(self) -> None:
        """Get the result objects for the dataframe."""
        self.iseries = self.iter_df()
        self.obj_list = [self.get_res_obj(s) for s in self.iseries]
        self.obj_dict = {str(obj): obj for obj in self.obj_list}
        self.sort_cols()

    def get_results(self, cnxn: DuckDBPyConnection) -> DataFrame:
        """Get the results for the model."""
        return cnxn.sql(f"select * from {self.schema}.{self.table}").df()

    def get_index_grid(self, nanvar: str = None, asarray: bool = True) -> list:
        """Get the index grid for the model results."""
        rng = range(len(self))
        index = [[i if i != j else nanvar for i in rng] for j in rng]
        if asarray:
            return array(index)
        return index

    def __len__(self) -> int:
        """Get the length of the model results."""
        return len(self.obj_list)

    def __post_init__(self) -> None:
        """Run the post init steps for the class."""
        if len(self.obj_list) == 0:
            self.df = self.get_results()
            self.sort_cols()
            self.get_res_objs()
        self.obj_names = [
            f"{str(self.obj_list[i])} ({i})" for i in range(len(self.obj_list))
        ]
        self._range = range(len(self))  # Add this line
        self.index = self.get_comp_index()
        self.index_grid = self.get_index_grid()

    def get_comp_index(self) -> chain:
        """Get the comparison index for the model results."""
        return chain.from_iterable([[(i, j) for i in self._range] for j in self._range])

    def get_comp_grid(self, bayes: bool) -> array:
        """Get the comparison grid for the model results."""
        _len = len(self)
        z = zeros((_len, _len))
        for i in range(_len):
            z[i][i] = OUT if bayes else MID
        return z

    def bayes_comp_2_objs(
        self,
        obj1: ModelResult,
        obj2: ModelResult,
        runs: int = None,
        plot: bool = False,
        names: tuple = None,
    ) -> tuple | list:
        """Compare two objects for the model results."""
        if runs is None:
            runs = 1
        obj1_vals = obj1.splits_test_roc_auc
        obj2_vals = obj2.splits_test_roc_auc
        if plot and names is None:
            names = (str(obj1), str(obj2))
        return two_on_multiple(
            obj1_vals, obj2_vals, rope=self.rope, runs=runs, plot=plot, names=names
        )

    def comp_2_idx(
        self,
        idx1: int,
        idx2: int,
        bayes: bool,
        plot: bool = False,
        runs: int = None,
        names: bool = None,
        nemenyi_grid: array = None,
    ) -> tuple:
        """Compare two indices for the model results."""
        if bayes:
            obj1 = self.obj_list[idx1]
            obj2 = self.obj_list[idx2]
            runs = 1 if runs is None else runs
            comp = self.bayes_comp_2_objs(obj1, obj2, plot=plot, names=names)
            return comp if not plot else comp[0]
        else:
            return nemenyi_grid[idx1][idx2]

    def get_mask_grid(self) -> array:
        """Get the mask grid for the model results."""
        mask_grid = self.get_comp_grid()
        for pair in self.index:
            i, j = pair[0], pair[-1]
            if i == j:
                mask_grid[i][j] = True
            else:
                mask_grid[i][j] = 0
        return mask_grid

    def gen_eval_steps(
        self, bayes: bool, grid: array, use_matsym: bool, nemenyi_grid: array = None
    ) -> DataFrame:
        """Generate the evaluation steps for the model results."""
        if not bayes:
            nemenyi_grid = self.do_nemenyi()
        if use_matsym:
            idx = [x for x in self.index if x[0] > x[-1]]
        else:
            idx = [x for x in self.index if x[0] != x[-1]]

        for pair in idx:
            i, j = pair
            comp = self.comp_2_idx(
                i,
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
            if use_matsym and eval == LEFT:
                grid[j][i] = RIGHT
            elif use_matsym and eval == RIGHT:
                grid[j][i] = LEFT
            elif use_matsym:
                grid[j][i] = eval
        return DataFrame(grid.T, index=self.obj_names)

    def eval_all(self, bayes: bool, use_matsym: bool = True) -> DataFrame:
        """Evaluate all the results for the model."""
        self.grid = self.get_comp_grid(bayes)
        return self.gen_eval_steps(bayes, self.grid, use_matsym)

    @staticmethod
    def get_window_params(bayes: bool, params: dict = WINDOWPANE_PLOT_PARAMS) -> dict:
        """return the windowpane plot parameters for either bayes or freq"""
        return params["bayes"] if bayes else params["freq"]

    def plot_windowpane(
        self,
        bayes: bool = True,
        df: DataFrame = None,
        use_matsym: bool = True,
        figsize: tuple = None,
        annot: str = None,  # vals, index, none
        labelsize: int = 3,
        dpi: int = 800,
        annot_fontsize: str = "x-small",
    ) -> tuple:
        """Plot the windowpane for the model results."""
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
        ax = heatmap(
            df,
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
            if text.get_text() in [str(OUT), None, nan, "None"]:
                text.set_text("")
        cbar = ax.collections[0].colorbar
        r = cbar.vmax - cbar.vmin
        cbar.set_ticks([cbar.vmin + r / n * (0.5 + i) for i in range(n)])
        cbar.set_ticklabels(list(cbar_vals.values()))
        tick_params(
            left=False,
        )
        return fig, ax

    def get_top_cluster(
        self,
        _len: bool = False,
        _obj_list: bool = False,
        _res_obj: bool = True,
    ) -> list["Results"]:
        """Get the top cluster for the model results."""
        grid = self.grid
        top_row = grid[0][1:]
        top_val = top_row[0]
        i = 1
        ival = top_row[0]
        while True:
            ival = top_row[i]
            if i == 1:
                i += 1
            elif ival == top_val or (isnan(ival) and isnan(top_row[i - 1])):
                i += 1
            elif _len:
                return i
            elif _res_obj:
                return Results(lim=i)
            elif _obj_list:
                return self.obj_list[:i]
            else:
                return top_row[:i]

    def get_top_cluster_gen(self) -> list:
        """Get the top cluster generator for the model results."""
        cluster_len = self.get_top_cluster(_len=True)
        cluster_range = range(cluster_len)
        return get_comb_gen(cluster_range, 2)

    def get_cluster_comp_gen(self, plot: bool = False) -> Generator[list, None, None]:
        """Get the cluster comparison generator for the model results."""
        for pair in self.get_top_cluster_gen():
            yield self.comp_2_idx(*pair, plot=plot)

    @classmethod
    def from_engines(cls, engine_list: list, **kwargs) -> "Results":
        """Get the results from the engines."""
        obj_list = [ModelResult.from_engine(engine) for engine in engine_list]
        return cls(obj_list=obj_list, **kwargs)


def comp_rope_vals() -> None:
    """Compare the ROPE values."""
    rope_comp_id = 0
    ropes = [i / 10000 for i in range(5, 101, 5)]
    for rope in tqdm(ropes):
        for runs in [1]:
            records = []
            res = Results(rope=rope, runs=runs, lim=150)
            if rope_comp_id == 0:
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
                        "eval": eval,
                    }
                    records.append(rec)
            rope_comp_id += 1
            df = DataFrame.from_records(records)
            df.to_sql(
                "rope_comp",
                con=res.dbh.engine,
                schema=LOG_SCHEMA,
                if_exists=if_exists,
                index=True,
                method="multi",
            )
