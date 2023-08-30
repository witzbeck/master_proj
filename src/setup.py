from alexlib.cnfg import ConfigFile, chkenv
from alexlib.db import Connection

config = ConfigFile.from_dotenv_name_list(["model", "db", "server"])
dbh = Connection()

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

if __name__ == "__main__":
    print(dbh.dbname)
    print(dbh.user)
    print(dbh.pw)
    print(dbh.host)
    print(dbh.port)
    print(dbh.info_schema)
