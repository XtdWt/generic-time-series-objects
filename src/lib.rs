use pyo3::prelude::*;
use std::vec::Vec;

#[pyclass]
struct TimeSeriesObject {
    keys: Vec<i32>,
    values: Vec<i32>,
}

#[pymethods]
impl TimeSeriesObject {
    #[new]
    fn new() -> Self {
        TimeSeriesObject {keys: Vec::new(), values: Vec::new()}
    }

    fn add(&mut self, key: i32, value: i32) {
        self.keys.push(key);
        self.values.push(value);
    }

    fn show(&self) {
        println!("{:?}", self.keys);
        println!("{:?}", self.values);
    }
}

#[pymodule]
fn rust_time_series_objects(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TimeSeriesObject>()?;
    Ok(())
}
