# import pytest
import datetime

from generic_time_series_objects import TimeSeriesDataBaseclass, time_series_data


class TestClass(TimeSeriesDataBaseclass):

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

test_obj = TestClass(2, 3, 4)
print(test_obj.A(), test_obj.B(), test_obj.C(), test_obj.D())
test_obj.set_date(datetime.datetime(2025, 12, 13))
test_obj.update({"A": 9, "B": 99, "C": 999})
print(test_obj.A(), test_obj.B(), test_obj.C(), test_obj.D())
test_obj.reset_data()
print(test_obj.A(), test_obj.B(), test_obj.C(), test_obj.D())
test_obj.set_date(datetime.datetime(2025, 12, 14))
print(test_obj.A(), test_obj.B(), test_obj.C(), test_obj.D())
print(test_obj.data)
