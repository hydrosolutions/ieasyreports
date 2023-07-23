from ieasyreports.core.tags.tag import Tag
from ieasyreports.utils import import_from_string
import datetime as dt
import random as rd
import ieasyhydro_sdk

from ieasyreports.settings import Settings

settings = Settings()
DataManager = import_from_string(settings.data_manager_class)


class Site:
    def __init__(self, name, river, code, basin):
        self.name = name
        self.river = river
        self.code = code
        self.basin = basin

    def __repr__(self):
        return self.name


class ForecastingResult:
    def __init__(
        self, site: Site, pentad: int, month_str: str, year: int, day_start: int,
        day_end: int, q_min: float, q_max: float, norm: float, perc_norm: float, q_danger: float
    ):
        self.site = site
        self.pentad = pentad
        self.month_str = month_str
        self.year = year
        self.day_start = day_start
        self.day_end = day_end
        self.q_min = q_min
        self.q_max = q_max
        self.norm = norm
        self.perc_norm = perc_norm
        self.q_danger = q_danger

    def __repr__(self):
        return f"{self.site} forecasting report"





# create the ReportGenerator instance
#report_generator = import_from_string(settings.template_generator_class)(
#    tags=[region_tag, river_tag, measurement_day_tag, water_level_tag, water_discharge_tag, author_tag, date_tag],
#    template='example2.xlsx',
#    requires_header=True
#)

#report_generator.validate()
#report_generator.generate_report(list_objects=rivers, output_filename="example4.xlsx")
