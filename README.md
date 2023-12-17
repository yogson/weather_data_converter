
# Weather Data Processor

## Overview

`WeatherDataProcessor` is a Python class designed for asynchronous and parallel processing of weather data. It facilitates the reception, transformation, and storage of weather data files, specifically GRIB files.

## Components

- `WeatherDataProcessor`: The main class orchestrating the data processing.
- `receiver`: An asynchronous function to receive file paths.
- `load_pipeline` and `transform_pipeline`: Lists of functions representing the steps in the data processing pipelines.
- `Task`: A class representing individual processing tasks.
- `simple_worker`: A function that executes tasks from a queue.

## Workflow

1. **Initialization**:
   - Instance of `WeatherDataProcessor` is created with a data source URL.
   - Worker processes are spawned for parallel task execution.

2. **Data Reception**:
   - File paths are received asynchronously from the specified source.

3. **Loading Pipeline**:
   - For each file path, a task is created and queued.
   - Tasks in the `load_pipeline` perform initial processing steps like uncompressing and extracting data.

4. **Transform Pipeline**:
   - Processed files are paired and additional tasks are created for further processing.
   - Tasks in the `transform_pipeline` perform operations like data subtraction, sentinel value replacement, and binary file building.

5. **Task Processing**:
   - Each task is processed by worker processes in parallel.
   - Tasks involve reading data, applying transformations, and saving results.

6. **Completion**:
   - The program waits for all tasks to complete before finishing execution.

## Key Functions

- `_spawn_processes(num_proc)`: Spawns worker processes for parallel execution.
- `_set_task(context, pipeline)`: Creates and queues a task with the given context and pipeline.
- `_run()`: Orchestrates the entire data processing workflow.
- `run()`: Entry point to start the processing.

## Settings Module

The `settings` module in the `WeatherDataProcessor` application configures various parameters and constants used throughout the data processing workflow. These settings can be customized via environment variables or will default to predefined values.

### Configuration Parameters

- `TEMP_DIR`: The directory for temporary storage during processing. Default is `"temp"`. Can be set with the `TEMP_DIR` environment variable.
- `SOURCE_DIR`: The directory where source data files are stored. Default is `"source"`. Can be set with the `SOURCE_DIR` environment variable.
- `OUTPUT_DIR`: The directory where final processed files will be saved. Default is `"output"`. Can be set with the `OUTPUT_DIR` environment variable.
- `CPU_CORES`: The number of CPU cores to use for parallel processing. Defaults to the number of cores available on the machine. Can be set with the `CPU_CORES` environment variable.
- `LOG_LEVEL`: The logging level for the application. Set to `logging.INFO` by default.

### Constants

- `NONE_SENTINEL`: A floating-point value used as a sentinel (placeholder) in certain processing steps. Set to `-100500.0`.
- `GRIB_MISSING_VALUE`: The value used in GRIB files to represent missing data. Set to `3.4028234663852886e38`, a large float value.
- `WGF_HEADER_MULTIPLIER`: A multiplier used for scaling values in the WGF header. Set to `1000000`.
- `WGF_ARRAY_TYPE`: The data type used for arrays in WGF files. Set to `numpy.float32`.

---

## Usage

To use `WeatherDataProcessor`, instantiate it with a source URL and call the `run` method:

```python
processor = WeatherDataProcessor(source='http://example.com/data')
processor.run()
```

This will start the process of downloading, processing, and transforming the weather data files as per the defined pipelines.

---
