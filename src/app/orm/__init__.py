from utils.constants import QUERY_PATH

SCHEMAS = {x.name.split("_")[-1] for x in QUERY_PATH.iterdir() if x.is_dir()}
