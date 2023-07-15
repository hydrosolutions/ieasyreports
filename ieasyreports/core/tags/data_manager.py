from typing import Optional, Union
from datetime import datetime

from babel.dates import format_date

from ieasyreports.examples.dummy_data import DUMMY_MEASUREMENTS


class DefaultDataManager:
    @classmethod
    def get_localized_date(
        cls, date: Optional[datetime] = None, language: str = 'en', date_format: str = 'long'
    ) -> str:
        date = date or datetime.today()
        return format_date(date, locale=language, format=date_format)


class DischargeDataManager(DefaultDataManager):
    @classmethod
    def get_station_measurement_data(cls, station_id, time_of_day="morning", measurement="water_discharge"):
        station_measurements = DUMMY_MEASUREMENTS.get(station_id)
        if station_measurements is None:
            return ""

        try:
            return station_measurements["measurements"][f"{measurement}{time_of_day}"]
        except KeyError:
            return ""
