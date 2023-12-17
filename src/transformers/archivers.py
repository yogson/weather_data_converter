import bz2
import gzip
from pathlib import Path
from typing import Any

from utils import get_source_and_output_paths_from_context


def compress_zip(data: bytes | None, context: dict[str, Any]) -> None:
    source_path, output_path = get_source_and_output_paths_from_context(context)
    if not source_path or not output_path:
        return None
    write_path = Path(output_path).with_suffix(".gzip")
    write_path.write_bytes(gzip.compress(data))


def uncompress_bzip(_: bytes | None, context: dict[str, Any]) -> None:
    source_path, output_path = get_source_and_output_paths_from_context(context)
    if not source_path or not output_path:
        return None
    with open(source_path, "rb") as sf:
        output_file = Path(output_path) / Path(source_path).name
        with open(output_file.with_suffix(""), "wb") as of:
            content = bz2.decompress(sf.read())
            of.write(content)
    context["source_path"] = output_file.with_suffix("")
