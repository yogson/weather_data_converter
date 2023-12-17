import logging
from pathlib import Path
from typing import Any

from numpy import ndarray, save, load

from exceptions import ContextLost
from utils import get_source_and_output_paths_from_context
from utils.common import convert_filename_to_datetime, dir_name_by_datetime, save_json, make_dir, init_logger

logger = init_logger(__name__)


def save_np_array(np_array: ndarray, file_path: Path):
    save(file_path, np_array)


def read_np_array(file_path: Path) -> ndarray:
    return load(file_path)


def save_array_and_meta(np_array: ndarray, context: dict[str, Any]):
    source_path, output_path = get_source_and_output_paths_from_context(context)
    metadata = context.get("metadata")
    if not metadata:
        raise ContextLost()
    file_path = (Path(output_path) / Path(source_path).name).with_suffix(".npy")
    save_np_array(np_array, file_path)
    save_json(metadata, file_path.with_suffix("").with_suffix(".json"))


def write_wgf(data: bytes, context: dict[str, Any]) -> bytes:
    file_name = context.get("file_name")
    output_dir = context.get("output_dir")
    if not file_name or not output_dir:
        raise ContextLost()
    model_name = file_name.split("_")[0]
    date_time = convert_filename_to_datetime(file_name)
    dir_name = dir_name_by_datetime(date_time)
    model_dir = make_dir(Path(output_dir) / model_name)
    target_dir = make_dir(model_dir / dir_name)
    with open(target_dir / "PRATE.wgf4", "wb") as f:
        f.write(data)
    logger.info(f"Created file: {target_dir / 'PRATE.wgf4'}")
    return data
