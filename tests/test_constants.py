from pathlib import Path

from utils.constants import SOURCE_PATH


def test_source_path_is_source(src_path: Path = SOURCE_PATH) -> None:
    assert src_path.name == "src"


def test_constant_exists(constant_path: Path, rope_value: int) -> None:
    assert constant_path.exists()


def test_rope_value_is_int(rope_value: int) -> None:
    assert isinstance(rope_value, int)


def test_windowpane_plot_nrgb_is_nvals(windowpane_plot_rgb_vals: int) -> None:
    rgb, vals = windowpane_plot_rgb_vals
    assert len(rgb) == len(vals)


def test_windowpane_rgb_is_dict(windowpane_rgb: int) -> None:
    assert isinstance(windowpane_rgb, dict)


def test_windowpane_vals_is_dict(windowpane_vals: int) -> None:
    assert isinstance(windowpane_vals, dict)


def test_windowpane_bayes_key_is_int(windowpane_bayes_key: int) -> None:
    assert isinstance(windowpane_bayes_key, int)


def test_windowpane_freq_key_is_int(windowpane_freq_key: int) -> None:
    assert isinstance(windowpane_freq_key, int)


def test_windowpane_color_is_4tuple_of_floats(windowpane_color: tuple) -> None:
    assert isinstance(windowpane_color, tuple)
    assert len(windowpane_color) == 4
    assert all(isinstance(x, float) for x in windowpane_color)


def test_windowpane_decision_is_str(windowpane_decision: str) -> None:
    assert isinstance(windowpane_decision, str)


def test_model_type_is_str(model_type: str) -> None:
    assert isinstance(model_type, str)


def test_path_exists(path: Path) -> None:
    assert isinstance(path, Path)
    assert path.exists()
