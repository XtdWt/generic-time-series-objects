use std::collections::HashMap;

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

    fn __len__(&self) -> usize {
        self.timestamps.len()
    }

    fn get_insertion_index(&self, ts: i32) -> usize {
        self.timestamps.binary_search(&ts).unwrap_or_else(|idx| idx)
    }

    fn insert(&mut self, ts: i32, value: Py<PyAny>) {
        if self.is_empty() || (ts > self.timestamps[self.timestamps.len()-1]) {
            self.timestamps.push(ts);
            self.values.push(value);
            return
        }

        let idx = self.get_insertion_index(ts);

        let current_ts_at_idx = self.timestamps[idx];
        if current_ts_at_idx == ts{
            self.values[idx] = value;
            return
        }

        self.timestamps.insert(idx, ts);
        self.values.insert(idx, value);
    }

    fn point_at(&self, ts: i32) -> Option<(&i32, &Py<PyAny>)> {
        if self.is_empty() {
            return None
        }
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
        if self.is_empty() {
            return None
        }
        let idx = self.get_insertion_index(ts);
        if self.timestamps[idx] == ts {
            Some((&self.timestamps[idx], &self.values[idx]))
        } else {
            None
        }
    }

    fn points_between(&self, start_ts: i32, end_ts: i32) -> Vec<(&i32,&Py<PyAny>)> {
        let start_idx = self.get_insertion_index(start_ts);
        let end_idx = self.get_insertion_index(end_ts);
        let mut return_vec = Vec::new();
        for idx in start_idx..end_idx {
            let point_ts = &self.timestamps[idx];
            let value_ts = &self.values[idx];
            return_vec.push((point_ts, value_ts))
        }
        return_vec
    }

    fn as_dict(&self) -> HashMap<&i32, &Py<PyAny>> {
        let mut return_dict = HashMap::new();
        for idx in 0..self.__len__() {
            let point_ts = &self.timestamps[idx];
            let value_ts = &self.values[idx];
            return_dict.insert(point_ts, value_ts);
        }
        return_dict
    }
}


#[pymodule]
fn generic_time_series_objects(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TimeSeriesObject>()?;
    Ok(())
}
