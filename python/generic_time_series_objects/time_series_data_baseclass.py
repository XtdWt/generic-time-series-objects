import datetime
from abc import ABC
from typing import Any
from functools import wraps


from generic_time_series_objects import TimeSeriesObject


TS_DATA_FLAG = 'is_time_series_data'

class TimeSeriesDataBaseclass(ABC):
    def __init__(self):
        self.timestamp: int | None = None
        self.data = {}
        ts_data_flag = TS_DATA_FLAG
        for method_name in dir(self):
            method = getattr(self, method_name)
            if not getattr(method, ts_data_flag, lambda: False):
               continue
            self.data[method_name] = TimeSeriesObject()

    def set_date(self, new_date: datetime.datetime) -> None:
        self.timestamp = int(new_date.timestamp())

    def reset_data(self):
        self.timestamp = None

    def update(self, new_data: dict[str, Any], overwrite: bool=False) -> None:
        if self.timestamp is None:
            raise ValueError("`set_date` before attempting to `update`")
        for method_name, data_point in new_data.items():
            self.data[method_name].insert(self.timestamp, data_point, overwrite)


def time_series_data(fn):
    fn.TS_DATA_FLAG = True
    @wraps(fn)
    def wrapper(self, *args, **kwargs) -> Any:
        if self.timestamp is None:
            return fn(self, *args, **kwargs)

        data_point = self.data[fn.__name__].point(self.timestamp)
        if not data_point:
            return fn(self, *args, **kwargs)

        return data_point[1]

    return wrapper
