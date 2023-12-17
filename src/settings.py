import logging
from os import environ

from numpy import float32

TEMP_DIR = environ.get("TEMP_DIR", "temp")
SOURCE_DIR = environ.get("SOURCE_DIR", "source")
OUTPUT_DIR = environ.get("OUTPUT_DIR", "output")

CPU_CORES = int(environ.get("CPU_CORES", 0))
LOG_LEVEL = logging.INFO

NONE_SENTINEL = -100500.0
GRIB_MISSING_VALUE = 3.4028234663852886e38
WGF_HEADER_MULTIPLIER = 1000000
WGF_ARRAY_TYPE = float32

try:
    from local_settings import *  # noqa
except ImportError:
    pass
