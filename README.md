
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

## Running the Application with Docker

### Building the Docker Image

Before running the application, build the Docker image using the Dockerfile provided in the repository. Navigate to the directory containing the Dockerfile and run:

```bash
docker build -t weather-processor .
```

This command builds the Docker image with the tag `weather-processor`. You can replace `weather-processor` with a tag of your choice.

### Running the Application

To run the application in a Docker container, you need to:

1. **Map a Local Directory to the Container's Volume**: This allows the application to read input data from and write output data to your host machine.
2. **Provide the Source URL as an Argument**: This is the URL where the application will fetch weather data.

```bash
docker run -v /path/to/local/dir:/data weather-processor <source_url>
```

- `/path/to/local/dir`: Replace this with the path to the directory on your host machine where you want the application to read from and write data to.
- `<source_url>`: Replace this with the actual source URL for the weather data.

### Example

```bash
docker run -v /home/user/weather_data:/data weather-processor https://opendata.dwd.de/weather/nwp/icon-d2/grib/12/tot_prec/
```

In this example:
- `/home/user/weather_data` is the local directory on the host machine.
- `https://opendata.dwd.de/weather/nwp/icon-d2/grib/12/tot_prec/` is the source URL for fetching weather data.

This command will start a Docker container that runs the weather data processing application. The application will process data fetched from the provided URL and store the results in the specified local directory.

## Notes

- Ensure that the local directory you specify exists and has the necessary read/write permissions.
- The data in the specified local directory will be accessible inside the container under `/data`.

---
