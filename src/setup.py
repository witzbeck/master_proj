"""Setup for the project."""
from logging import WARNING

from sqlalchemy.orm import declarative_base

from alexlib.auth import Auth
from alexlib.files.config import DotEnv
from alexlib.core import chkenv
from alexlib.db.managers import PostgresManager

from constants import PROJECT_PATH

config = DotEnv.from_path(
    PROJECT_PATH / ".env",
    loglevel=WARNING,
    eventlevel=WARNING,
)
auth = Auth("local.sudo.learning")
db_mgr = PostgresManager.from_auth(auth)
Base = declarative_base()

nrows = chkenv("NROWS", astype=int, need=False)
random_state = chkenv("RANDOM_STATE", astype=int, need=False)
jobint = chkenv("JOB_CORES", astype=int)
