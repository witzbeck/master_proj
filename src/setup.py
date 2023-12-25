from alexlib.auth import Auth
from alexlib.config import ConfigFile
from alexlib.core import chkenv
from alexlib.db import Connection

config = ConfigFile.from_dotenv_name_list(["model", "db", "server"])
auth = Auth("local.sudo.learning")
cnxn = Connection.from_auth(auth)

nrows = chkenv("NROWS", type=int, required=False)
random_state = chkenv("RANDOM_STATE", type=int, required=False)
jobint = chkenv("JOB_CORES", type=int)

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
