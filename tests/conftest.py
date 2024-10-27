from pathlib import Path

from duckdb import DuckDBPyConnection
from pytest import FixtureRequest, fixture

from constants import (
    BLUE,
    DATA_PATH,
    FIGURES_PATH,
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
from etl import create_schema_logic, load_landing_data_logic
from etl.extract import get_csv_paths
from etl.utils import get_cnxn
from utils.figures import GENERATED_FIGURES_PATH


@fixture(scope="session")
def cnxn() -> DuckDBPyConnection:
    return get_cnxn()


@fixture(scope="session")
def cnxn_with_landing_data(cnxn: DuckDBPyConnection) -> DuckDBPyConnection:
    create_schema_logic(cnxn=cnxn)
    load_landing_data_logic(cnxn=cnxn)
    return cnxn


@fixture(
    scope="session",
    params=(
        PROJECT_PATH,
        DATA_PATH,
        QUERY_PATH,
        FIGURES_PATH,
        GENERATED_FIGURES_PATH,
    )
    + tuple(get_csv_paths()),
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
