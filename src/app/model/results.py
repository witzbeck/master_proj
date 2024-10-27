from logging import getLogger

from orm.analysis import CREATE_ANALYSIS_ABROCA_TABLE
from orm.model import (
    CREATE_MODEL_FEATURES_TABLE,
    CREATE_MODEL_RESULTS_TABLE,
    CREATE_MODEL_RUNS_TABLE,
    CREATE_MODEL_TYPES_TABLE,
    CREATE_MODEL_WARNINGS_TABLE,
)

logger = getLogger(__name__)


CREATE_TABLES = (
    CREATE_MODEL_RUNS_TABLE,
    CREATE_MODEL_TYPES_TABLE,
    CREATE_MODEL_RESULTS_TABLE,
    CREATE_MODEL_FEATURES_TABLE,
    CREATE_MODEL_WARNINGS_TABLE,
    CREATE_ANALYSIS_ABROCA_TABLE,
)
SOURCE_TABLES = {
    "MODEL_RUNS",
    "MODEL_TYPES",
    "MODEL_RESULTS",
}
