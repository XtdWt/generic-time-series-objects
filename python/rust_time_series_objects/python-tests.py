# from rust_time_series_objects import TimeSeriesObject
import rust_time_series_objects


if __name__ == "__main__":
    obj = rust_time_series_objects.TimeSeriesObject()
    obj.add(1, 2)
    print(obj.show())
    obj.add(2, 3)
    print(obj.show())