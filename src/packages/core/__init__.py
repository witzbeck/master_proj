"""Constants for the project."""

from logging import WARNING
from pathlib import Path

from alexlib.files import DotenvFile

HOME = Path.home()
SOURCE_PATH = Path(__file__).parent.parent.parent
assert SOURCE_PATH.name == "src"

PROJECT_PATH = SOURCE_PATH.parent
assert PROJECT_PATH.name == "master_proj"

LOG_LEVEL, EVENT_LEVEL = WARNING, WARNING
LOG_SCHEMA = "model"
(LOG_PATH := PROJECT_PATH / "logs").mkdir(exist_ok=True)

DOTENV_PATH = PROJECT_PATH / ".env"

(DATA_PATH := PROJECT_PATH / "data").mkdir(exist_ok=True)
(RAW_PATH := DATA_PATH / "raw").mkdir(exist_ok=True)
(EXPORT_PATH := DATA_PATH / "export").mkdir(exist_ok=True)

DB_PATH = DATA_PATH / "learning.db"
RESEARCH_PATH = PROJECT_PATH / "research"
FIGURES_PATH = RESEARCH_PATH / "figures"
PAPER_PATH = RESEARCH_PATH / "paper"
PRESENTATION_PATH = RESEARCH_PATH / "presentation"

config = DotenvFile.from_path(
    DOTENV_PATH,
    loglevel=LOG_LEVEL,
    eventlevel=EVENT_LEVEL,
)
QUERY_PATH = SOURCE_PATH / "queries"
