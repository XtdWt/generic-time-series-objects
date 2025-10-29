use pyo3::prelude::*;
use std::vec::Vec;

#[pyclass]
struct TimeSeriesObject {
    keys: Vec<i32>,
    values: Vec<Py<PyAny>>,
}

#[pymethods]
impl TimeSeriesObject {
    #[new]
    fn new() -> Self {
        TimeSeriesObject {keys: Vec::new(), values: Vec::new()}
    }

    fn add(&mut self, key: i32, value: Py<PyAny>) {
        self.keys.push(key);
        self.values.push(value);
    }

    fn get(&self, key: i32) -> &Py<PyAny> {
        let value = &self.values[key as usize];
        value
    }
}

#[pymodule]
fn rust_time_series_objects(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TimeSeriesObject>()?;
    Ok(())
}
