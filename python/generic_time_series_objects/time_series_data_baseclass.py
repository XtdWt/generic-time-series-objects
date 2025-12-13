import datetime
from abc import ABC
from functools import wraps
from typing import Any, Callable

from generic_time_series_objects import TimeSeriesObject


TS_DATA_FLAG = 'is_time_series_data'


class TimeSeriesDataBaseclass(ABC):
    def __init__(self):
        self.timestamp: int = -1
        self.data: dict[str, TimeSeriesObject] = {}
        ts_data_flag = TS_DATA_FLAG
        for method_name in dir(self):
            method = getattr(self, method_name)
            if not getattr(method, ts_data_flag, False):
               continue
            self.data[method_name] = TimeSeriesObject()

    def set_date(self, new_date: datetime.datetime) -> None:
        self.timestamp = int(new_date.timestamp())

    def reset_data(self) -> None:
        self.timestamp = -1

    def update(self, new_data: dict[str, Any], overwrite: bool=False) -> None:
        if self.timestamp == -1:
            raise ValueError("`set_date` before attempting to `update`")
        for method_name, data_point in new_data.items():
            self.data[method_name].insert(self.timestamp, data_point, overwrite)


def time_series_data(fn: Callable) -> Callable:
    fn.is_time_series_data = True
    @wraps(fn)
    def wrapper(self, *args, **kwargs) -> Any:
        if self.timestamp == -1:
            return fn(self, *args, **kwargs)

        data_point = self.data[fn.__name__].point(self.timestamp)
        if not data_point:
            return fn(self, *args, **kwargs)

        return data_point[1]

    return wrapper
