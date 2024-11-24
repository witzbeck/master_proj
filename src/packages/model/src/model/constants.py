"""Constants for the project."""

SCHEMAS = ("landing", "main", "agg", "model", "eval", "feat", "first30", "analysis")
BOOL_OPTIONS = [True, False]
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
)

# model search
INF_ITER = False
JOB_CORES = -1
PRE_DISPATCH = 96
SEARCH_GROUPED = True
SEARCH_ITER = 1
SEARCH_RANDOM = True
MODEL_TYPE = "logreg"
PREDICT_COL = "is_withdraw_or_fail"

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

CATEGORY_COLUMNS = (
    "course_id",
    "module_id",
    "presentation_id",
)
TO_DROP_COLUMNS = ("student_id", "unreg_date", "reg_date_dif")
FINAL_RESULT_COLUMNS = (
    "final_result",
    "final_result_id",
    "is_pass_or_distinction",
    "is_distinction",
    "is_pass",
    "is_fail",
    "is_withdrawn",
    "is_withdraw_or_fail",
)
SPLIT_COLUMNS = ("is_stem", "is_female", "has_disability")
FEATURE_TABLE_SCHEMA = "first30"
FEATURE_TABLE_NAME = "all_features"
