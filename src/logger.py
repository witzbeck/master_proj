# standard library imports
from dataclasses import dataclass, field
from datetime import datetime as dt
from functools import partial

# third party imports
from pandas import DataFrame, concat
from psycopg2.errors import DatatypeMismatch

# local imports
from alexlib.config import chkenv
from alexlib.iters import keys
from setup import dbh

if __name__ == "__main__":
    from setup import config
    config


@dataclass
class Logger:
    model_type: str
    log_schema: str = field(default=chkenv("LOG_SCHEMA"))
    log_runs_table: str = field(default="runs")
    log_runs_id_col: str = field(default="id")
    log_id_col: str = field(default="run_id")
    log_data_table: str = field(default="data")
    log_feat_table: str = field(default="feat")
    log_results_table: str = field(default="results")
    log_warnings_table: str = field(default="warnings")

    def set_run_id(self):
        return self.dbh.get_next_id(self.log_schema,
                                    self.log_runs_table,
                                    self.log_runs_id_col)

    def get_table_attr(self):
        return [x for x in list(self.__dict__.keys()) if "table" in x]

    def add_run_id(self, _dict: dict):
        _dict[self.log_id_col] = self.run_id
        return _dict

    def log_to_table(self, table: str, _dict: dict):
        _dict = self.add_run_id(_dict)
        self.send_log(table, _dict)

    def set_partials(self):
        self.log_warn = partial(self.log_to_table, self.log_warnings_table)
        self.log_params = partial(self.log_to_table, self.log_params_table)
        self.log_feat = partial(self.log_to_table, self.log_feat_table)
        self.log_data = partial(self.log_to_table, self.log_data_table)
        self.log_results = partial(self.log_to_table, self.log_results_table)

    def __post_init__(self):
        self.dbh = dbh
        self.cv_results = chkenv("CV_RESULTS")
        ptab = f"params_{self.model_type}"
        if self.cv_results == "ALL":
            self.log_results_table = self.log_results_table + "_all"
        self.log_params_table = ptab
        self.if_exists = "append"
        self.run_id = self.set_run_id()
        self.tables = self.get_table_attr()
        self.set_partials()

    def send_log(self,
                 log_table: str,
                 _dict: dict,
                 ):
        cvisall = self.cv_results == "ALL"
        if (cvisall and ("param" in log_table or "result" in log_table)):
            list_dict = _dict
        else:
            list_dict = {x: [_dict[x]] for x in keys(_dict)}

        df = DataFrame.from_dict(list_dict)
        if ("param" in log_table or "result" in log_table):
            df.reset_index(
                inplace=True,
                names="iter_id"
            )
        try:
            df.to_sql(
                log_table,
                con=self.dbh.engine,
                schema=self.log_schema,
                if_exists=self.if_exists,
                index=False,
            )
        except DatatypeMismatch:
            existing = self.dbh.get_table(self.log_schema, log_table)
            if len(existing.columns) == len(df.columns):
                new_df = concat([existing, df])
                new_df.to_sql(
                    log_table,
                    con=self.dbh.engine,
                    schema=self.log_schema,
                    if_exists="replace",
                    index=False,
                )

    def log_run(self,
                _keys: list = ["id", "model_type", "timestamp"]
                ) -> None:
        now: dt = dt.now(),
        vals = [self.run_id, self.model_type, now]
        _range = range(len(_keys))
        _dict = {_keys[i]: vals[i] for i in _range}
        self.send_log(self.log_runs_table, _dict)
