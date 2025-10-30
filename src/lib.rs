use pyo3::prelude::*;
use pyo3::exceptions::PyIndexError;


#[pyclass]
struct TimeSeriesObject {
    timestamps: Vec<i32>,
    values: Vec<Py<PyAny>>,
}


#[pymethods]
impl TimeSeriesObject {
    #[new]
    fn new() -> Self {
        TimeSeriesObject {timestamps: Vec::new(), values: Vec::new()}
    }

    fn get_insertion_index(&self, ts: i32) -> usize {
        self.timestamps.binary_search(&ts).unwrap_or_else(|idx| idx)
    }

    fn add(&mut self, ts: i32, value: Py<PyAny>) {
        if self.timestamps.is_empty() || (ts > self.timestamps[self.timestamps.len()-1]) {
            self.timestamps.push(ts);
            self.values.push(value);
        } else {
            let idx = self.get_insertion_index(ts);
            self.timestamps.insert(idx, ts);
            self.values.insert(idx, value);
        }
    }

    fn value_at(&self, ts: i32) -> &Py<PyAny> {
        let idx = self.get_insertion_index(ts);
        if self.timestamps[idx] == ts {
            &self.values[idx]
        } else if idx != 0 {
            &self.values[idx - 1]
        } else {
            &self.values[idx]
        }
    }

    fn value_on(&self, ts: i32) -> PyResult<&Py<PyAny>> {
        let idx = self.get_insertion_index(ts);
        if self.timestamps[idx] == ts {
            Ok(&self.values[idx])
        } else {
            let err_str = format!("No value found at timestamp: {}", ts);
             Err(PyIndexError::new_err(err_str))
        }
    }
}


#[pymodule]
fn rust_time_series_objects(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TimeSeriesObject>()?;
    Ok(())
}
