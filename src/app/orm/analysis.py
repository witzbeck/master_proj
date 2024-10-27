from logging import getLogger

from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

SCHEMA = "analysis"
Base = declarative_base()
logger = getLogger(__name__)


class AnalysisTable:
    __tablename__: str
    __schema__: str = SCHEMA
    id: Column = Column(Integer, primary_key=True, autoincrement=True)

    def __str__(self) -> str:
        return f"{self.__schema__}.{self.__tablename__}"


class Abroca(Base, AnalysisTable):
    __tablename__ = "abroca"
    run_id = Column(Integer)
    iter_id = Column(Integer)
    course_id = Column(Integer)
    is_stem = Column(Boolean)
    is_female = Column(Boolean)
    has_disability = Column(Boolean)


CREATE_ANALYSIS_ABROCA_TABLE = """
create or replace table analysis.abroca(
index integer primary key,
run_id integer not null,
iter_id integer not null,
course_id integer not null,
is_stem boolean not null,
is_female boolean not null,
has_disability boolean not null
);
"""
