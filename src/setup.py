from alexlib.envs import ConfigFile, chkenv

model_config = lambda: ConfigFile.from_dotenv_name("model")
db_config = lambda: ConfigFile.from_dotenv_name("db")
server_config = lambda: ConfigFile.from_dotenv_name("server")

nrows = chkenv("NROWS", type=int)
random_state = chkenv("RANDOM_STATE", type=int)
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
