from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

SCHEMA = "model"
Base = declarative_base()


class ModelTable:
    __tablename__: str
    __schema__: str = SCHEMA
    id: Column = Column(Integer, primary_key=True, autoincrement=True)

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
