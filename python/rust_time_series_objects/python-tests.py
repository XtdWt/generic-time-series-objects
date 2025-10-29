# from rust_time_series_objects import TimeSeriesObject
import rust_time_series_objects


if __name__ == "__main__":
    obj = rust_time_series_objects.TimeSeriesObject()
    obj.add(1, 2)
    print(obj.get(0), type(obj.get(0)))
    obj.add(2, 3)
    print(obj.get(1), type(obj.get(1)))
    obj.add(2, "3")
    print(obj.get(2), type(obj.get(2)))
