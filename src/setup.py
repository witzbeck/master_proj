from pathlib import Path
from os import getenv

from dotenv import load_dotenv
from numpy.random import randint
from sqlalchemy import engine

from alexlib.file import Directory
from alexlib.mystdlib import set_envint


def set_envs(envname: str):
    return load_dotenv(f".env.{envname}")


def set_nrows():
    set_envint(getenv("NROWS"))


def set_rand_state():
    set_envint(getenv("RANDOM_STATE"))


schema = "landing"
datadir = Directory(Path(__file__).parent.parent / "data")

mkengine = engine


if __name__ == "__main__":
    datadir.insert_all_files(
        mkengine("learning"),
        schema=schema,
    )
