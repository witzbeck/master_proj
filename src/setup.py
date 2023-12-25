from pathlib import Path

from alexlib.auth import Auth
from alexlib.config import DotEnv
from alexlib.core import chkenv
from alexlib.db import Connection

config = DotEnv.from_path(Path(__file__).parent.parent / ".env")
home = Path.home()
proj = home / "repos/master_proj"
data = proj / "data"
queries = proj / "queries"
auth = Auth("local.sudo.learning")
cnxn = Connection.from_auth(auth)

nrows = chkenv("NROWS", astype=int, need=False)
random_state = chkenv("RANDOM_STATE", astype=int, need=False)
jobint = chkenv("JOB_CORES", astype=int)

model_types = [
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
