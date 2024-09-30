from alexlib.files import DotenvFile
from utils.constants import DOTENV_PATH, EVENT_LEVEL, LOG_LEVEL

config = DotenvFile.from_path(
    DOTENV_PATH,
    loglevel=LOG_LEVEL,
    eventlevel=EVENT_LEVEL,
)

NROWS = 1000
RANDOM_STATE = None
JOB_CORES = -1
