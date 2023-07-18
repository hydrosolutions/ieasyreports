from typing import Optional, Union
from datetime import datetime

from babel.dates import format_date

from ieasyreports.examples.dummy_data import DUMMY_MEASUREMENTS
from ieasyreports.examples.dummy_sites import Site


class DefaultDataManager:
    @classmethod
    def get_localized_date(
        cls, date: Optional[datetime] = None, language: str = 'en', date_format: str = 'long'
    ) -> str:
        date = date or datetime.today()
        return format_date(date, locale=language, format=date_format)


class DischargeDataManager(DefaultDataManager):
    @classmethod
    def get_station_measurement_data(
        cls, site: Site, time_of_day: str = "morning", measurement: str = "water_discharge"
    ):
        for station_measurement in DUMMY_MEASUREMENTS.values():
            if station_measurement.get("station_code") == site.site_code:
                try:
                    print(station_measurement)
                    return station_measurement["measurements"][f"{measurement}_{time_of_day}"]
                except KeyError:
                    return ""

        return ""
