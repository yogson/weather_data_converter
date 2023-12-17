from typing import Any

import xarray as xr
from numpy import ndarray

from utils import get_source_and_output_paths_from_context


def extract_regular_grid_data(_: Any, context: dict[str, Any]) -> ndarray:
    source_path, _ = get_source_and_output_paths_from_context(context)
    data = xr.open_dataset(source_path, engine="cfgrib")
    metadata = dict(
        min_lat=data.latitude.data.min(),
        max_lat=data.latitude.data.max(),
        min_lon=data.longitude.data.min(),
        max_lon=data.longitude.data.max(),
        lat_step=data.latitude.data[1] - data.latitude.data[0],
        lon_step=data.longitude.data[1] - data.longitude.data[0],
    )
    if data["step"].size > 1:
        tp_values = data["tp"].isel(step=0).values.ravel()
    else:
        tp_values = data["tp"].values.ravel()
    context["metadata"] = metadata
    return tp_values
