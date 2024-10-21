"""Constants for the project."""

from logging import WARNING
from pathlib import Path

LOG_LEVEL, EVENT_LEVEL = WARNING, WARNING

HOME = Path.home()
SOURCE_PATH = Path(__file__).parent.parent
PROJECT_PATH = SOURCE_PATH.parent
DOTENV_PATH = PROJECT_PATH / ".env"

OULAD_BASE = "https://analyse.kmi.open.ac.uk"
OULAD_URL = f"{OULAD_BASE}/open_dataset/download"
OULAD_MD5_URL = f"{OULAD_BASE}/open_dataset/downloadCheckSum"
OULAD_MD5 = "7412686fd77cf0e0ee1e8c3e9b354308"

FIGURES_PATH = PROJECT_PATH / "figures"
(DATA_PATH := PROJECT_PATH / "data").mkdir(exist_ok=True)
(RAW_PATH := DATA_PATH / "raw").mkdir(exist_ok=True)
(EXPORT_PATH := DATA_PATH / "export").mkdir(exist_ok=True)
DB_PATH = DATA_PATH / "learning.db"
SCHEMAS = ("landing", "main", "agg", "model", "eval", "feat", "first30", "analysis")

QUERY_PATH = SOURCE_PATH / "queries"
MODEL_TYPES = (
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
)
# logs
LOG_SCHEMA = "model"
(LOG_PATH := PROJECT_PATH / "logs").mkdir(exist_ok=True)

# model search
INF_ITER = False
JOB_CORES = -1
PRE_DISPATCH = 96
SEARCH_GROUPED = True
SEARCH_ITER = 1
SEARCH_RANDOM = True
MODEL_TYPE = "logreg"
PREDICT_COL = "is_withdraw_or_fail"

# analysis
EVAL_ROPE = 0.002
ROPE_UPBOUND = 0.95
ROPE_FLEXIBLE = False
ALPHA = 0.05

# cross validation
TEST_SIZE = 0.25
RANDOM_STATE = None
CV_VERBOSE = 2
CV_NSPLITS = 5
CV_NREPEATS = 2
CV_REFIT = "ROC_AUC"
CV_RESULTS = "ALL"
SIMPLE_NUM_IMPUTE = True

# preprocessing
NROWS = 10_000
REDUCE_DIM = True

# features
USE_MOMENTS = False
USE_STUDENT_INFO = True
USE_IDS = False
USE_TEXT = False
USE_BY_ACTIVITY = True
USE_DEMOGRAPHIC = True
USE_ENGAGEMENT = False
USE_ACADEMIC = True
USE_ALL = False

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
