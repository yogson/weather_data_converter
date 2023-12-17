import struct
from pathlib import Path
from typing import Any

from numpy import ndarray, nan_to_num, array

from exceptions import ContextLost
from settings import (
    TEMP_DIR,
    NONE_SENTINEL,
    GRIB_MISSING_VALUE,
    WGF_HEADER_MULTIPLIER,
    WGF_ARRAY_TYPE,
)
from transformers.loaders import read_np_array
from utils.common import read_json


def subtract_previous_hour(_, context: dict[str, Any]) -> ndarray:
    files_pair = context.get("files_pair")
    if not files_pair:
        raise ContextLost()
    current_file_name, previous_file_name = files_pair[0], files_pair[1]
    metadata = read_json((Path(TEMP_DIR) / current_file_name).with_suffix(".json"))
    context["metadata"] = metadata
    context["file_name"] = current_file_name
    current_data = read_np_array((Path(TEMP_DIR) / current_file_name).with_suffix(".npy"))
    if previous_file_name:
        previous_data = read_np_array((Path(TEMP_DIR) / previous_file_name).with_suffix(".npy"))
        return current_data - previous_data
    return current_data


def replace_nan_with_sentinel(data: ndarray, _) -> ndarray:
    return nan_to_num(data, nan=NONE_SENTINEL)


def replace_grib_missing_value_with_sentinel(data: ndarray, _) -> ndarray:
    data[data == GRIB_MISSING_VALUE] = NONE_SENTINEL
    return data


def build_wgf(data: ndarray, context: dict[str, Any]) -> bytes:
    header = _build_wgf_header(context.get("metadata", {}))
    data = array(data, dtype=WGF_ARRAY_TYPE).tobytes()
    return header + data


def _build_wgf_header(metadata: dict) -> bytes:
    try:
        min_lat = int(metadata["min_lat"] * WGF_HEADER_MULTIPLIER)
        max_lat = int(metadata["max_lat"] * WGF_HEADER_MULTIPLIER)
        min_lon = int(metadata["min_lon"] * WGF_HEADER_MULTIPLIER)
        max_lon = int(metadata["max_lon"] * WGF_HEADER_MULTIPLIER)
        lat_step = int(metadata["lat_step"] * WGF_HEADER_MULTIPLIER)
        lon_step = int(metadata["lon_step"] * WGF_HEADER_MULTIPLIER)
    except KeyError as e:
        raise ContextLost(e)
    header_values = [
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        lat_step,
        lon_step,
        WGF_HEADER_MULTIPLIER,
    ]
    header_format = "i" * 7 + "f"
    return struct.pack(header_format, *header_values, NONE_SENTINEL)
