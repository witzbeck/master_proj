from pathlib import Path

from pytest import FixtureRequest, fixture

from src.constants import (
    BLUE,
    DATA_PATH,
    GRAY,
    HOME,
    LEFT,
    LIGHTGRAY,
    MID,
    MODEL_TYPES,
    NODECISION,
    ORANGE,
    OUT,
    PROJECT_PATH,
    QUERY_PATH,
    RIGHT,
    ROPE,
    SOURCE_PATH,
    WHITE,
    WINDOWPANE_PLOT_PARAMS,
    XGREATER,
    XLESS,
    XROPE,
)


@fixture(
    scope="session",
    params=(
        PROJECT_PATH,
        DATA_PATH,
        QUERY_PATH,
    ),
)
def constant_path(request: FixtureRequest) -> Path:
    return request.param


@fixture(
    scope="session",
    params=(
        LEFT,
        ROPE,
        OUT,
    ),
)
def rope_value(request: FixtureRequest) -> int:
    return request.param


@fixture(
    scope="session",
    params=(
        "bayes",
        "freq",
    ),
)
def windowpane_plot_param_key(request: FixtureRequest) -> int:
    return request.param


@fixture(scope="session")
def windowpane_plot_rgb_vals(windowpane_plot_param_key: str) -> int:
    params = WINDOWPANE_PLOT_PARAMS[windowpane_plot_param_key]
    return params["rgb"], params["vals"]


@fixture(scope="session")
def windowpane_rgb(windowpane_plot_rgb_vals: int) -> int:
    return windowpane_plot_rgb_vals[0]


@fixture(scope="session")
def windowpane_vals(windowpane_plot_rgb_vals: int) -> int:
    return windowpane_plot_rgb_vals[1]


@fixture(
    scope="session",
    params=(
        LEFT,
        ROPE,
        RIGHT,
        OUT,
    ),
)
def windowpane_bayes_key(request: FixtureRequest) -> int:
    return request.param


@fixture(
    scope="session",
    params=(
        LEFT,
        MID,
        RIGHT,
    ),
)
def windowpane_freq_key(request: FixtureRequest) -> int:
    return request.param


@fixture(scope="session", params=(BLUE, LIGHTGRAY, WHITE, ORANGE, GRAY))
def windowpane_color(request: FixtureRequest) -> int:
    return request.param


@fixture(scope="session", params=(XGREATER, XROPE, XLESS, NODECISION))
def windowpane_decision(request: FixtureRequest) -> int:
    return request.param


@fixture(scope="session", params=MODEL_TYPES)
def model_type(request: FixtureRequest) -> int:
    return request.param


@fixture(
    scope="session",
    params=(
        HOME,
        SOURCE_PATH,
        PROJECT_PATH,
        DATA_PATH,
        QUERY_PATH,
    ),
)
def path(request: FixtureRequest) -> Path:
    return request.param
