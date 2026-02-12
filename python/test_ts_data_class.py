import pytest
import datetime

from generic_time_series_objects import TimeSeriesDataBaseclass, time_series_data


class TSObject(TimeSeriesDataBaseclass):

    def __init__(self, a, b, c):
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @time_series_data
    def A(self):
        return self.a

    @time_series_data
    def B(self):
        return self.b

    @time_series_data
    def C(self):
        return self.c

    @time_series_data
    def D(self):
        return 1

    def E(self):
        return 0


@pytest.fixture
def ts_based_obj():
    yield TSObject(1, 2, 3)


def test_set_date(ts_based_obj):
    assert ts_based_obj is not None
    ts_based_obj.set_date(datetime.datetime(2025, 12, 13))
    assert ts_based_obj.timestamp == datetime.datetime(2025, 12, 13).timestamp()



def test_update_raises_error(ts_based_obj):
    ts_based_obj.set_date(datetime.datetime(2025, 12, 13))
    ts_based_obj.update({"A": 9, "B": 99, "C": 999}, overwrite=True)
    assert ts_based_obj.A() == 9
    assert ts_based_obj.B() == 99
    assert ts_based_obj.C() == 999
    assert ts_based_obj.D() == 1
    assert ts_based_obj.E() == 0


def test_timestamp_resets(ts_based_obj):
    ts_based_obj.set_date(datetime.datetime(2025, 12, 13))
    ts_based_obj.reset_data()
    assert ts_based_obj.timestamp == -1


def test_multiple_dates(ts_based_obj):
    ts_based_obj.set_date(datetime.datetime(2025, 12, 13))
    ts_based_obj.update({"A": 9, "B": 99, "C": 999}, overwrite=True)
    ts_based_obj.set_date(datetime.datetime(2025, 12, 14))
    ts_based_obj.update({"A": 99, "B": 999, "C": 9999, "D": "String test hello"}, overwrite=True)
    ts_based_obj.set_date(datetime.datetime(2025, 12, 13, 12))
    assert ts_based_obj.A() == 9
    assert ts_based_obj.B() == 99
    assert ts_based_obj.C() == 999
    assert ts_based_obj.D() == 1
    assert ts_based_obj.E() == 0
    ts_based_obj.set_date(datetime.datetime(2025, 12, 14, 12))
    assert ts_based_obj.A() == 99
    assert ts_based_obj.B() == 999
    assert ts_based_obj.C() == 9999
    assert ts_based_obj.D() == "String test hello"
    assert ts_based_obj.E() == 0
