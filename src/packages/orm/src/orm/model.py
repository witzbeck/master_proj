from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

SCHEMA = "model"
Base = declarative_base()


class ModelTable:
    __tablename__: str
    __schema__: str = SCHEMA
    id = Column(Integer, primary_key=True, autoincrement=True)

    def __str__(self) -> str:
        return f"{self.__schema__}.{self.__tablename__}"


class ModelTypes(Base, ModelTable):
    __tablename__ = "types"
    model_type = Column(String(45))


class ModelRuns(Base, ModelTable):
    __tablename__ = "runs"
    model_type_id = Column(String(45))
    model_params = Column(JSON)
    timestamp = Column(DateTime)


class ModelResults(Base, ModelTable):
    __tablename__ = "results"
    run_id = Column(Integer)
    mean_fit_time = Column(Float)
    std_fit_time = Column(Float)
    mean_score_time = Column(Float)
    std_score_time = Column(Float)
    mean_test_roc_auc = Column(Float)
    std_test_roc_auc = Column(Float)
    rank_test_roc_auc = Column(Integer)


CREATE_MODEL_TYPES_TABLE = """
create or replace table model.types(
id integer primary key,
model_type text not null
);
"""
CREATE_MODEL_RUNS_TABLE = """
create or replace table model.runs (
    id integer primary key,
    iter_id integer not null,
    model_type_id integer not null,
    model_params json not null,
    timestamp timestamp not null
)
"""
CREATE_MODEL_RESULTS_TABLE = """
create or replace table model.results(
id integer primary key,
run_id integer not null,
iter_id integer not null,
mean_fit_time float not null,
std_fit_time float not null,
mean_score_time float not null,
std_score_time float not null,
mean_test_roc_auc float not null,
std_test_roc_auc float not null,
rank_test_roc_auc integer not null,
mean_test_accuracy float not null,
std_test_accuracy float not null
);
"""
CREATE_MODEL_FEATURES_TABLE = """
create or replace table model.features(
id integer primary key,
run_id integer not null,
to_predict_column text not null,
use_academic boolean not null,
use_demographic boolean not null,
use_engagement boolean not null,
use_moments boolean not null,
use_ids boolean not null,
use_text boolean not null,
use_by_activity boolean not null
);
"""
CREATE_MODEL_WARNINGS_TABLE = """
create or replace table model.warnings(
id integer primary key,
run_id integer not null,
warnings text not null
);
"""
