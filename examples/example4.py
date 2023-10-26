import random

from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.core.tags import DefaultDataManager, Tag
import datetime as dt
import random as rd


class River:
    def __init__(self, river_id: int, name: str, region: str):
        self.id = river_id
        self.name = name
        self.region = region

    def __repr__(self):
        return self.name


class Measurement:
    def __init__(self, river: River):
        self.river = river
        self.measurement_dt = self.get_random_date()
        self.water_level = rd.uniform(-50, 50)
        self.water_discharge = rd.uniform(5, 25)

    def __repr__(self):
        return f"{self.river.name} measurement on {self.measurement_dt}"

    @classmethod
    def get_random_date(cls):
        end_dt = dt.datetime.now()
        start_date = end_dt - dt.timedelta(days=rd.randint(1, 10))

        random_dt = start_date + (end_dt - start_date) * rd.random()
        return random_dt.date()


river_1 = River(1, "River 1", "Region A")
river_2 = River(2, "River 2", "Region A")
river_3 = River(3, "River 3", "Region A")
river_4 = River(4, "River 4", "Region B")
river_5 = River(5, "River 5", "Region B")
river_6 = River(6, "River 6", "Region C")
river_7 = River(7, "River 7", "Region D")

rivers = [river_1, river_2, river_3, river_4, river_5, river_6, river_7]
measurements = [Measurement(random.choice(rivers)) for _ in range(30)]


def get_measurement_data_for_river_and_day(river: River, day: dt.date, attr: str):
    for measurement in measurements:
        if measurement.measurement_dt == day and measurement.river == river:
            return getattr(measurement, attr, "")

    return "-"


target_day = Measurement.get_random_date()

region_tag = Tag(
    "REGION",
    lambda obj: obj.region,
    "Region where the river is located"
)
river_tag = Tag(
    "RIVER_NAME",
    lambda obj: obj.name,
    "River name"
)
measurement_day_tag = Tag(
    "MEASUREMENT_TIMESTAMP",
    lambda obj: get_measurement_data_for_river_and_day(obj, target_day, "measurement_dt"),
    "Day of the measurement"
)
water_level_tag = Tag(
    "WATER_LEVEL",
    lambda obj: get_measurement_data_for_river_and_day(obj, target_day, "water_level"),
    "Water level value"
)
water_discharge_tag = Tag(
    "WATER_DISCHARGE",
    lambda obj: get_measurement_data_for_river_and_day(obj, target_day, "water_discharge"),
    "Water discharge value"
)
author_tag = Tag(
    "AUTHOR",
    "John Doe",
    "Report author name"
)
date_tag = Tag(
    "DATE",
    DefaultDataManager.get_localized_date,
    "Date when the report was generated"
)


# create the ReportGenerator instance
report_generator = DefaultReportGenerator(
    tags=[region_tag, river_tag, measurement_day_tag, water_level_tag, water_discharge_tag, author_tag, date_tag],
    template='example2.xlsx',
    requires_header=True
)

report_generator.validate()
report_generator.generate_report(list_objects=rivers, output_filename="example4.xlsx")
