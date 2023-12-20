import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from settings import LOG_LEVEL


def prepare_dir(dir_path: str | Path):
    Path(dir_path).mkdir(exist_ok=True)
    for item in Path(dir_path).iterdir():
        if item.is_file():
            item.unlink()


def get_source_and_output_paths_from_context(
    context: dict[str, Any],
) -> tuple[Any, Any] | None:
    source_path = context.get("source_path")
    output_path = context.get("output_dir")
    return source_path, output_path


def convert_filename_to_datetime(filename) -> datetime:
    parts = filename.split("_")
    date_hour_str = parts[4]
    hour_shift_str = parts[5]
    date_hour = datetime.strptime(date_hour_str, "%Y%m%d%H")
    hour_shift = int(hour_shift_str)
    return date_hour + timedelta(hours=hour_shift)


def dir_name_by_datetime(date_time: datetime) -> str:
    formatted_datetime = date_time.strftime("%d.%m.%Y_%H:%M")
    timestamp = int(date_time.timestamp())
    return f"{formatted_datetime}_{timestamp}"


def read_json(file_path: Path) -> dict:
    return json.loads(file_path.read_text())


def save_json(data: dict, file_path: Path):
    file_path.write_text(json.dumps(data))


def make_dir(dir_path: str | Path) -> Path:
    path = Path(dir_path)
    path.mkdir(exist_ok=True)
    return path


def init_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(LOG_LEVEL)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
