import pytest

from rust_time_series_objects import TimeSeriesObject


TEST_INIT_POINTS = [
    [1, 2, 3, 4, 5, 10],
    [-1.0, -7.5, -100.1, -50, -1000],
    [3, -1, -50.5, "X", ["OOPS"], {1, 2, 3, 4}, {"TEST": "TEST1"}, lambda x: x, ("1", True), None],
    range(1, 1_000_000),
]

TEST_POINT_AT_ON = [
    ([1, 5, 10, 15], [10, 20, 30, 40])
]


@pytest.mark.parametrize("test_points", TEST_INIT_POINTS)
def test_initialise_ts_object(test_points: list):
    obj = TimeSeriesObject()
    assert obj is not None
    for i, val in enumerate(test_points):
        obj.insert(i, val)

    for i, val in enumerate(test_points):
        point_time, point_value = obj.point_at(i)
        assert point_time == i
        assert point_value == val


@pytest.mark.parametrize(("test_ts", "test_points"), TEST_POINT_AT_ON)
def test_ts_object_point_at(test_ts: list, test_points: list):
    obj = TimeSeriesObject()
    for ts, val in zip(test_ts, test_points):
        obj.insert(ts, val)

    loop_test_ts = test_ts.copy()
    loop_test_points = test_points.copy()
    for i in range(0, max(test_ts)+1):
        if i < test_ts[0]:
            assert obj.point_at(i) is None
            continue
        point_time, point_value = obj.point_at(i)
        if i == loop_test_ts[1]:
            loop_test_ts = loop_test_ts[1:]
            loop_test_points = loop_test_points[1:]
        assert point_time >= loop_test_ts[0]
        assert point_value == loop_test_points[0]


@pytest.mark.parametrize(("test_ts", "test_points"), TEST_POINT_AT_ON)
def test_ts_object_point_on(test_ts: list, test_points: list):
    obj = TimeSeriesObject()
    for ts, val in zip(test_ts, test_points):
        obj.insert(ts, val)

    for i in range(0, max(test_ts)+1):
        if i not in test_ts:
            assert obj.point_on(i) is None
            continue
        point_time, point_value = obj.point_on(i)
        assert point_time in test_ts
        assert point_value in test_points