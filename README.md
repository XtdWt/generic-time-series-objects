# Generic Time Series Objects
Store Python objects in a time series to capture evolving data over time. Built to be highly
generic and capable of storing any python class, even custom, against a timestamp (integer) 
value. This project is built in rust, with [pyo3](https://github.com/PyO3/pyo3) bindings, and 
compiled using [maturin](https://github.com/PyO3/maturin). Tests are written in python 
(with pytest).

## TimeSeriesObject Interface
Methods to interact with the TimeSeriesObject Class:
### Dunder Methods

#### __init\_\_
Initialises the object with no arguments. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.

_Output/Exceptions_
*  **`None`** (`NoneType`): Initialises the object.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
```
#### __len\_\_
Returns the number of data points currently stored in the time series object. <br>
_Arguments_
*  **`self`** (`TimeSeriesObject`): The object itself.

_Output/Exceptions_
* (`int`): Number of timestamps inserted into the object.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
print(len(obj))  # prints 0
```
### Mutating Data
Methods return None for success and raises Exception if failed to perform operation.
#### insert
Inserts a Python object at a given timestamp. <br>
_Arguments_
*  **`ts`** (`int`): Timestamp of the data point.
*  **`value`** (`Any`): The Python object to be stored.
*  **`overwrite`** (`bool`): Defaults to `False`. Determines what to do if a provide timestamp already exists, if 
`overwrite=False`, raises Exception otherwise overwrites the existing data point.

_Output/Exceptions_
*  **`None`** (`NoneType`): Successfully inserted data point at timestamp.
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
*  **`ts`** (`int`): Timestamp of the point we want to update.
*  **`value`** (`Any`): The Python object we want to update with.

_Output/Exceptions_
*  **`None`** (`NoneType`): Successfully inserted Python object at timestamp.
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
*  **`ts`** (`int`): Timestamp of the point we want to delete.

_Output/Exceptions_
*  **`None`** (`NoneType`): Successfully deleted data point.
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
The data point on or before a certain timestamp<br>
_Arguments_
*  **`ts`** (`int`): Timestamp on or before the time we want to retrieve data for.

_Output/Exceptions_
*  **`point`** (`tuple[int, Any]`): The data point, as a tuple of timestamp and Python object, that was retrieved.
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
The data point exactly on a certain timestamp<br>
_Arguments_
*  **`ts`** (`int`): Timestamp exactly equal to the time we want to retrieve data for.

_Output/Exceptions_
*  **`point`** (`tuple[int, Any]`): The data point, as a tuple of timestamp and Python object, that was retrieved.
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
_Arguments_
*  **``** (``):

_Output/Exceptions_
*  **``** (``):

_Example:_
```python
```
### Transforming Data Type
#### as_dict
_Arguments_
*  **``** (``):

_Output/Exceptions_
*  **``** (``):

_Example:_
```python
```
#### as_list
_Arguments_
*  **``** (``):

_Output/Exceptions_
*  **``** (``):

_Example:_
```python
```