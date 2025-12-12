# Generic Time Series Objects
Store Python objects in a time series to capture evolving data over time. Built to be highly
generic and capable of storing any python class, even custom, against a timestamp (integer) 
value. This project is built in rust, with [pyo3](https://github.com/PyO3/pyo3) bindings, and 
compiled using [maturin](https://github.com/PyO3/maturin). Tests are written in python 
(with pytest).

> [!NOTE]
>
> Rust code is compiled using `maturin develop --uv`. <br>
> Test cases are run using `pytest .\python\tests.py`.

## TimeSeriesObject Interface
Methods to interact with the TimeSeriesObject Class.
### Dunder Methods
#### __new\_\_
Creates the object with no arguments. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.

_Output/Exceptions_
*  (`TimeSeriesObject`): Returns the created object.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
```
#### __repr\_\_
Representation of the object. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.

_Output/Exceptions_
*  (`str`): Returns a string with the object name and a list of timestamps.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
print(obj)  # prints "TimeSeriesObject(timestamps=[])"
```
#### __len\_\_
Returns the number of data points currently stored in the time series object. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.

_Output/Exceptions_
* (`int`): Number of data points inserted into the object.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
print(len(obj))  # prints 0
```
#### __bool\_\_
Returns a boolean for if the object contains data points or not. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.

_Output/Exceptions_
*  (`bool`): False if there are no data points, otherwise True.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
print(bool(obj))  # prints False
```
### Mutating Data
Methods return None for success and raises Exception if failed to perform operation.
#### insert
Inserts a Python object at a given timestamp. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.
*  **`ts`** (`int`): Timestamp of the data point.
*  **`value`** (`Any`): The Python object to be stored.
*  **`overwrite`** (`bool`): Defaults to `False`. Determines what to do if a provide timestamp already exists, if 
`overwrite=False`, raises Exception otherwise overwrites the existing data point.

_Output/Exceptions_
*  (`None`): Successfully inserted data point at timestamp.
* **`ValueError`** (`Exception`): Timestamp provided already has existing data point and overwrite is set to False.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
obj.insert(1, {1, 2, 3})  # overwrite defaults to False
# obj.insert(1, {1, 2, 3})  # !raises ValueError
obj.insert(1, {1, 2, 3}, overwrite=True)
```
#### update
Updates the point at a given timestamp. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.
*  **`ts`** (`int`): Timestamp of the point we want to update.
*  **`value`** (`Any`): The Python object we want to update with.

_Output/Exceptions_
*  (`None`): Successfully inserted Python object at timestamp.
*  **`ValueError`** (`Exception`): TimeSeriesObject was empty and could not update.
*  **`IndexError`** (`Exception`): Provided timestamp does not exist within TimeSeriesObject.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
# obj.update(2, {1, 2, 3, 4})  # !raises ValueError
obj.insert(1, {1, 2, 3})
obj.update(1, {1, 2, 3, 4})
# obj.update(2, {1, 2, 3, 4})  # !raises IndexError
```
#### delete
Deletes the data point at a given timestamp. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.
*  **`ts`** (`int`): Timestamp of the point we want to delete.

_Output/Exceptions_
*  (`None`): Successfully deleted data point.
*  **`ValueError`** (`Exception`): TimeSeriesObject was empty and could not delete.
*  **`IndexError`** (`Exception`): Provided timestamp does not exist within TimeSeriesObject.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
# obj.delete(2)  # !raises ValueError
obj.insert(1, {1, 2, 3})
# obj.delete(2)  # !raises IndexError
obj.delete(1)
```
### Retrieving Data Points
Methods return a tuple of the timestamp and Python object for success and None if nothing is found.
#### point
Fetches the data point on or before a certain timestamp.<br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.
*  **`ts`** (`int`): Timestamp on or before the time we want to retrieve data for.

_Output/Exceptions_
*  (`tuple[int, Any]`): The data point, as a tuple of timestamp and Python object, that was retrieved.
*  **`None`** (`NoneType`): Nothing was found, in this case timestamp provided was before the minimum timestamp in the 
TimeSeriesObject.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
obj.insert(2, {1, 2, 3})
obj.insert(10, {1, 2, 3, 4})
print(obj.point(10))  # prints {1, 2, 3, 4}
print(obj.point(5))  # prints {1, 2, 3}
print(obj.point(1))  # prints None
```
#### point_on
Fetches the data point exactly on a certain timestamp.<br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.
*  **`ts`** (`int`): Timestamp exactly equal to the time we want to retrieve data for.

_Output/Exceptions_
*  (`tuple[int, Any]`): The data point, as a tuple of timestamp and Python object, that was retrieved.
*  **`None`** (`NoneType`): Nothing was found at provided timestamp.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
obj.insert(2, {1, 2, 3})
obj.insert(10, {1, 2, 3, 4})
print(obj.point_on(10))  # prints {1, 2, 3, 4}
print(obj.point_on(5))  # prints None
print(obj.point_on(2))  # prints {1, 2, 3}
```

#### points_between
Fetches all data points between the two provided timestamps, inclusive of start and exclusive of end [start_ts, end_ts).
<br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.
*  **`start_ts`** (`int`): Start timestamp to filter for, inclusive.
*  **`end_ts`** (`int`): End timestamp to filter for, exclusive.

_Output/Exceptions_
*  (`list[tuple[int, Any]]`): List of points between the starting and ending timestamp.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
obj.insert(2, {1})
obj.insert(5, {1, 2})
obj.insert(10, {1, 2, 3})
print(obj.point_between(1, 100))  # prints [(2, {1}), (5, {1, 2}), (10, {1, 2, 3})]
print(obj.point_between(1, 10))  # prints [(2, {1}), (5, {1, 2})]
print(obj.point_between(1, 1))  # prints []

```
### Transforming Data Type
Methods return the data type named in the method as the outer return type.
#### as_dict
Transforms all data points in the TimeSeries to a mapping between the timestamp and the Python object.<br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.

_Output/Exceptions_
*  (`dict[int, Any]`): All data points in the form of a dictionary mapping timestamp to Python 
object.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
print(obj.as_dict())  # prints {}
obj.insert(1, ['hello'])  
print(obj.as_dict())  # prints {1: ['hello']}
```
#### as_list
Transforms all data points in the TimeSeries to a list of tuples containing the timestamp and the Python object.<br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.

_Output/Exceptions_
*  (`list[tuple[int, Any]]`): All data points in the form of a list of tuples with each tuple 
containing a timestamp and the Python object.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
print(obj.as_list())  # prints []
obj.insert(1, ['hello'])  
print(obj.as_list())  # prints [(1, ['hello'])]
```