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

_Output/Exceptioms_
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

_Output/Exceptioms_
* (`int`): Number of timestamps inserted into the object.

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
len(obj)
```
### Mutating Data
Methods return None for success and raises Exception if failed to perform operation.
#### insert
Inserts a Python object at a given timestamp. <br>
_Arguments_
*  **`ts`** (`int`): Timestamp of the data.
*  **`value`** (`Any`): The Python object data.
*  **`overwrite`** (`bool`): Defaults to `False`. Determines what to do if a provide timestamp already exists, if 
`overwrite=False`, raises Exception otherwise overwrites the existing data.

_Output/Exceptioms_
*  **`None`** (`NoneType`): Successfully inserted data at timestamp
* **`ValueError`** (`Exception`): Timestamp provided already has existing data and overwrite is set to False

_Example:_
```python
from generic_time_series_objects import TimeSeriesObject

obj = TimeSeriesObject()
obj.insert(1, {1, 2, 3})  # overwrite defaults to False
# obj.insert(1, {1, 2, 3})  # !raises ValueError
obj.insert(1, {1, 2, 3}, overwrite=True)
```
#### update
Updates the data at a given timestamp. <br>
_Arguments_
*  **`ts`** (`int`): Timestamp of the data.
*  **`value`** (`Any`): The Python object data.

_Output/Exceptioms_
*  **`None`** (`NoneType`): Successfully inserted data at timestamp
*  **`ValueError`** (`Exception`): TimeSeriesObject was empty and could not update
*  **`IndexError`** (`Exception`): Provided timestamp does not exist within TimeSeriesObject

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
### Retrieving Data Points
#### point_at
#### point_on
#### points_between
### Transforming Data Type
#### as_dict
#### as_list