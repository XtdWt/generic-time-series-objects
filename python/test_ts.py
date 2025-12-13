import pytest

from generic_time_series_objects import TimeSeriesObject


TEST_INIT_POINTS = [
    [1, 2, 3, 4, 5, 10],
    [-1.0, -7.5, -100.1, -50, -1000],
    [3, -1, -50.5, "X", ["OOPS"], {1, 2, 3, 4}, {"TEST": "TEST1"}, lambda x: x, ("1", True), None],
    range(1, 1_000_000),
]

TEST_POINT_DATA = [
    ([1, 5, 10, 15], [10, 20, 30, 40]),
]


@pytest.mark.parametrize("test_points", TEST_INIT_POINTS)
def test_initialise_ts_object(test_points: list):
    obj = TimeSeriesObject()
    assert obj is not None
    for i, val in enumerate(test_points):
        obj.insert(i, val)

    for i, val in enumerate(test_points):
        point_time, point_value = obj.point(i)
        assert point_time == i
        assert point_value == val
    assert len(obj) == len(test_points)

    assert obj.as_dict() == {i: val for i, val in enumerate(test_points)}
    assert obj.as_list() == [(i, val) for i, val in enumerate(test_points)]
    with pytest.raises(AttributeError):
        obj.get_insertion_index(3)
    with pytest.raises(AttributeError):
        obj.is_empty()


def test_empty_object():
    obj = TimeSeriesObject()
    assert obj is not None
    assert obj.as_dict() == {}
    assert obj.as_list() == []
    assert obj.point(0) is None
    assert obj.points_between(0, 1) == []
    with pytest.raises(ValueError):
        obj.update(100, None)
    with pytest.raises(ValueError):
        obj.delete(100)


@pytest.mark.parametrize(("test_ts", "test_points"), TEST_POINT_DATA)
def test_ts_object_point(test_ts: list, test_points: list):
    obj = TimeSeriesObject()
    for ts, val in zip(test_ts, test_points):
        obj.insert(ts, val)

    loop_test_ts = test_ts.copy()
    loop_test_points = test_points.copy()
    for i in range(0, max(test_ts)+1):
        if i < test_ts[0]:
            assert obj.point(i) is None
            continue
        point_time, point_value = obj.point(i)
        if i == loop_test_ts[1]:
            loop_test_ts = loop_test_ts[1:]
            loop_test_points = loop_test_points[1:]
        assert point_time >= loop_test_ts[0]
        assert point_value == loop_test_points[0]

    assert obj.point(100000) == (test_ts[-1], test_points[-1])


@pytest.mark.parametrize(("test_ts", "test_points"), TEST_POINT_DATA)
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

    assert obj.point_on(100000) is None


@pytest.mark.parametrize(("test_ts", "test_points"), TEST_POINT_DATA)
def test_ts_points_between(test_ts: list, test_points: list):
    obj = TimeSeriesObject()
    for ts, val in zip(test_ts, test_points):
        obj.insert(ts, val)
    assert [x for _, x in obj.points_between(0, 1_000_000)] == [10, 20, 30, 40]
    assert [x for _, x in obj.points_between(1, 16)] == [10, 20, 30, 40]
    assert [x for _, x in obj.points_between(1, 15)] == [10, 20, 30]
    assert [x for _, x in obj.points_between(1, 14)] == [10, 20, 30]
    assert [x for _, x in obj.points_between(2, 12)] == [20, 30]
    assert [x for _, x in obj.points_between(2, 11)] == [20, 30]
    assert [x for _, x in obj.points_between(1, 10)] == [10, 20]
    assert [x for _, x in obj.points_between(0, 0)] == []


@pytest.mark.parametrize(("test_ts", "test_points"), TEST_POINT_DATA)
def test_update_delete_from_object(test_ts: list, test_points: list):
    obj = TimeSeriesObject()
    for ts, val in zip(test_ts, test_points):
        obj.insert(ts, val)
    # cannot add same thing twice
    with pytest.raises(ValueError):
        obj.insert(test_ts[0], test_points[0])

    obj.insert(test_ts[0], test_points[0], overwrite=True)

    # check index must exist for update
    with pytest.raises(IndexError):
        obj.update(0, None)

    obj.update(test_ts[0], None)

    # check can delete
    with pytest.raises(IndexError):
        obj.delete(0)

    for ts in test_ts:
        obj.delete(ts)

    with pytest.raises(ValueError):
        obj.delete(test_ts[0])
