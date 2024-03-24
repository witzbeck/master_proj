"""Constants for the project."""
from pathlib import Path


HOME = Path.home()
PROJECT_PATH = HOME / "repos/master_proj"
DATA_PATH = PROJECT_PATH / "data"
DOCKER_PATH = PROJECT_PATH / "docker"
QUERY_PATH = PROJECT_PATH / "queries"
MODEL_TYPES = [
    "hxg_boost",
    "logreg",
    "rforest",
    "ada_boost",
    "etree",
    "dtree",
    "knn",
    "mlp",
    "svc",
    # "compnb",
    # "gauss",
]

__range__ = range(-1, 3)
# rope values
LEFT, ROPE, RIGHT, OUT = __range__
MID = ROPE

# windowpane plot colors
BLUE = (68 / 255, 155 / 255, 214 / 255, 1.0)
LIGHTGRAY = (0.925, 0.925, 0.925, 1.0)
WHITE = LIGHTGRAY
ORANGE = (222 / 255, 142 / 255, 8 / 255, 1.0)
GRAY = (0.5, 0.5, 0.5, 1.0)

# model comparison decisions
XGREATER = "X > Y"
XLESS = "X < Y"
NODECISION = "No Decision"
XROPE = "ROPE"

WINDOWPANE_PLOT_PARAMS = {
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
