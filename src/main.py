import sys

from processor import WeatherDataProcessor
from settings import TEMP_DIR, OUTPUT_DIR, SOURCE_DIR
from utils import prepare_dir


def main(url: str):
    for _dir in (SOURCE_DIR, TEMP_DIR, OUTPUT_DIR):
        prepare_dir(_dir)
    WeatherDataProcessor(source=url).run()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No source URL provided.")
        sys.exit(1)

    source_url = sys.argv[1]
    main(source_url)
