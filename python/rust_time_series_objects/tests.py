import pytest

from rust_time_series_objects import TimeSeriesObject


TEST_INIT_VALUES = [
    [1, 2, 3, 4, 5, 10],
    [-1.0, -7.5, -100.1, -50, -1000],
    [3, -1, -50.5, "X", ["OOPS"], {1, 2, 3, 4}, {"TEST": "TEST1"}, lambda x: x, ("1", True), None],
    range(1, 1_000_000),
]

TEST_VALUE_AT_ON = [
    ([1, 5, 10, 15], [10, 20, 30, 40])
]


@pytest.mark.parametrize("test_values", TEST_INIT_VALUES)
def test_initialise_ts_object(test_values: list):
    obj = TimeSeriesObject()
    assert obj is not None
    for i, val in enumerate(test_values):
        obj.add(i, val)

    for i, val in enumerate(test_values):
        assert obj.value_at(i) == val


# @pytest.mark.parametrize(("test_ts", "test_values"), TEST_VALUE_AT_ON)
# def test_ts_object_value_at(test_ts: list, test_values: list):
#     obj = TimeSeriesObject()
#     for ts, val in zip(test_ts, test_values):
#         obj.add(ts, val)
#
#     prev_ts = 0
#     for ts, val in zip(test_ts, test_values):
#         for i in range(prev_ts, ts+1):
#             print(i, obj.value_at(i), val)
#             assert obj.value_at(i) == val
#         prev_ts = ts + 1


@pytest.mark.parametrize(("test_ts", "test_values"), TEST_VALUE_AT_ON)
def test_ts_object_value_on(test_ts: list, test_values: list):
    obj = TimeSeriesObject()
    for ts, val in zip(test_ts, test_values):
        obj.add(ts, val)

    for i in range(0, max(test_ts)+1):
        if i not in test_ts:
            try:
                val = obj.value_on(i)
            except IndexError as e:
                continue
        assert obj.value_on(i) in test_values