"""Constants for the etl package."""

OULAD_BASE = "https://analyse.kmi.open.ac.uk"
OULAD_URL = f"{OULAD_BASE}/open_dataset/download"
OULAD_MD5_URL = f"{OULAD_BASE}/open_dataset/downloadCheckSum"
OULAD_MD5 = "7412686fd77cf0e0ee1e8c3e9b354308"

SCHEMAS = ("landing", "main", "agg", "model", "eval", "feat", "first30", "analysis")
SQL_BLACKLIST = (
    "CREATE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "DELETE",
    "UPDATE",
    "INSERT",
    "INTO",
)
