use pyo3::prelude::*;


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

    fn is_empty(&self) -> bool {
        self.timestamps.is_empty()
    }

    fn get_insertion_index(&self, ts: i32) -> usize {
        self.timestamps.binary_search(&ts).unwrap_or_else(|idx| idx)
    }

    fn insert(&mut self, ts: i32, value: Py<PyAny>) {
        if self.is_empty() || (ts > self.timestamps[self.timestamps.len()-1]) {
            self.timestamps.push(ts);
            self.values.push(value);
        } else {
            let idx = self.get_insertion_index(ts);
            self.timestamps.insert(idx, ts);
            self.values.insert(idx, value);
        }
    }

    fn point_at(&self, ts: i32) -> Option<(&i32, &Py<PyAny>)> {
        let idx = self.get_insertion_index(ts);
        if self.timestamps[idx] == ts {
            Some((&self.timestamps[idx], &self.values[idx]))
        } else if idx != 0 {
            Some((&self.timestamps[idx-1], &self.values[idx-1]))
        } else {
            None
        }
    }

    fn point_on(&self, ts: i32) -> Option<(&i32, &Py<PyAny>)> {
        let idx = self.get_insertion_index(ts);
        if self.timestamps[idx] == ts {
            Some((&self.timestamps[idx], &self.values[idx]))
        } else {
            None
        }
    }
}


#[pymodule]
fn rust_time_series_objects(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TimeSeriesObject>()?;
    Ok(())
}
