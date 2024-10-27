from dataclasses import dataclass, field
from datetime import datetime
from functools import partial

from duckdb import DuckDBPyConnection
from pandas import DataFrame

from constants import CV_RESULTS, LOG_SCHEMA
from etl.utils import get_cnxn


@dataclass
class Logger:
    """A class to log the results of a model to a database table. Inherits from the ProjectTable class"""

    model_type: str
    cnxn: DuckDBPyConnection = field(default_factory=get_cnxn)
    log_schema: str = LOG_SCHEMA
    log_runs_table: str = field(default="runs")
    log_runs_id_col: str = field(default="id")
    log_id_col: str = field(default="run_id")
    log_data_table: str = field(default="data")
    log_feat_table: str = field(default="feat")
    log_results_table: str = field(default="results")
    log_warnings_table: str = field(default="warnings")

    def set_run_id(self) -> int:
        """Returns the next id for the runs table."""
        return self.cnxn.get_next_id(
            self.log_schema, self.log_runs_table, self.log_runs_id_col
        )

    def get_table_attr(self) -> list:
        """Returns a list of the table attributes of the Logger object."""
        return [x for x in self.__dict__.keys() if "table" in x]

    def add_run_id(self, _dict: dict) -> dict:
        """Adds the run_id to a dictionary."""
        _dict[self.log_id_col] = self.run_id
        return _dict

    def log_to_table(self, table: str, _dict: dict) -> None:
        """Logs a dictionary to a database table."""
        _dict = self.add_run_id(_dict)
        self.send_log(table, _dict)

    def set_partials(self) -> None:
        """Sets the partial functions for the Logger object."""
        self.log_warn = partial(self.log_to_table, self.log_warnings_table)
        self.log_params = partial(self.log_to_table, self.log_params_table)
        self.log_feat = partial(self.log_to_table, self.log_feat_table)
        self.log_data = partial(self.log_to_table, self.log_data_table)
        self.log_results = partial(self.log_to_table, self.log_results_table)

    def __post_init__(self) -> None:
        """Initializes the Logger object."""
        self.cv_results = CV_RESULTS
        ptab = f"params_{self.model_type}"
        if self.cv_results == "ALL":
            self.log_results_table = self.log_results_table + "_all"
        self.log_params_table = ptab
        self.if_exists = "append"
        self.run_id = self.set_run_id()
        self.tables = self.get_table_attr()
        self.set_partials()

    def send_log(
        self,
        log_table: str,
        _dict: dict,
    ) -> None:
        """Sends a dictionary to a database table."""
        cvisall = self.cv_results == "ALL"
        if cvisall and ("param" in log_table or "result" in log_table):
            list_dict = _dict
        else:
            list_dict = {v: [v] for k, v in _dict.items()}

        df = DataFrame.from_dict(list_dict)
        if "param" in log_table or "result" in log_table:
            df.reset_index(inplace=True, names="iter_id")
        df.to_sql(
            log_table,
            self.cnxn,
            schema=self.log_schema,
            if_exists=self.if_exists,
            index=False,
        )

    @property
    def log_record(self) -> dict:
        """Returns the log record for the Logger object."""
        return {
            "run_id": self.run_id,
            "model_type": self.model_type,
            "timestamp": datetime.now(),
        }

    def log_run(self) -> None:
        """Logs a run to the runs table."""
        self.send_log(self.log_runs_table, self.log_record)
