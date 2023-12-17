from processor import WeatherDataProcessor
from settings import TEMP_DIR, OUTPUT_DIR, SOURCE_DIR
from utils import prepare_dir


def main():
    WeatherDataProcessor(source="https://opendata.dwd.de/weather/nwp/icon-d2/grib/12/tot_prec/").run()


if __name__ == "__main__":
    for _dir in (SOURCE_DIR, TEMP_DIR, OUTPUT_DIR):
        prepare_dir(_dir)
    main()
