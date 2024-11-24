"""A module for analyzing the results of a model run."""

from dataclasses import dataclass, field
from functools import cached_property

from matplotlib.pyplot import legend, subplots, title, xlabel, ylabel
from numpy import array, bool_, floating, int_, integer, ndarray
from pandas import DataFrame, Series
from sklearn.metrics import roc_auc_score, roc_curve

from alexlib.df import filter_df, get_distinct_col_vals
from alexlib.maths import combine_domains, get_list_difs, get_rect_area


def get_idx_val(
    value: str, index_start: int, get_index_list: list, get_value_list: list
):
    idx = get_index_list.index(value, index_start)
    return get_value_list[idx]


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
                val = get_idx_val(x, idx_counter, old_x, old_y)
                new_y.append(val)
                idx_counter += 1
            elif x in old_x and idx_counter > 0:
                val = get_idx_val(x, idx_counter, old_x, old_y)
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
