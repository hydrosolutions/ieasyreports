The next example show how the grouping functionality in templates works.
To demonstrate, let's assume we're working with an `example2.xlsx` template
that looks like this:

| River name               | Measurement day                | Water level          | Discharge level          |
|--------------------------|--------------------------------|----------------------|--------------------------|
| {{HEADER.REGION}}        |                                |                      |                          |
| {{DATA.RIVER_NAME}}      | {{DATA.MEASUREMENT_TIMESTAMP}} | {{DATA.WATER_LEVEL}} | {{DATA.WATER_DISCHARGE}} |
| Generated by: {{AUTHOR}} |                                | {{DATE}}             |                          |


The expected output would be that the {{HEADER.REGION}} is replaced by each region from the input data and for
each river in each region some measurement data should be displayed. The example also shows the usage of the
`custom_number_format_fn` argument of a tag which handles the desired rounding of the value. While the most common
usage of this argument is to round numerical values output of a value function, it can be used for general formatting
of the output value (for example to uppercase a string etc.)

The following code could be used to achieve this. It contains both the definition of some dummy input data and
the already familiar definition and usage of the tags. If you run this example, you will get different values
since the dummy data is randomized, but the data itself is not important for this example.

```python
from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.core.tags import DefaultDataManager, Tag
from ieasyreports.settings import TagSettings, ReportGeneratorSettings
import datetime as dt
import random as rd

report_settings = ReportGeneratorSettings()
tag_settings = TagSettings()


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
        self.water_level = rd.uniform(0, 50)
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
measurements = [Measurement(rd.choice(rivers)) for _ in range(30)]


def get_measurement_data_for_river_and_day(river: River, day: dt.date, attr: str):
    for measurement in measurements:
        if measurement.measurement_dt == day and measurement.river == river:
            return getattr(measurement, attr, "")

    return "-"

def custom_round(num: float):
    if not isinstance(num, float):
        return num
    return round(num, 1)


target_day = Measurement.get_random_date()

region_tag = Tag(
    "REGION",
    lambda obj, **kwargs: obj.region,
    tag_settings,
    "Region where the river is located",
    header=True
)
river_tag = Tag(
    "RIVER_NAME",
    lambda obj, **kwargs: obj.name,
    tag_settings,
    "River name",
    data=True
)
measurement_day_tag = Tag(
    "MEASUREMENT_TIMESTAMP",
    lambda obj, **kwargs: get_measurement_data_for_river_and_day(obj, target_day, "measurement_dt"),
    tag_settings,
    "Day of the measurement",
    data=True
)
water_level_tag = Tag(
    "WATER_LEVEL",
    lambda obj, **kwargs: get_measurement_data_for_river_and_day(obj, target_day, "water_level"),
    tag_settings,
    "Water level value",
    custom_number_format_fn=custom_round,
    data=True
)
water_discharge_tag = Tag(
    "WATER_DISCHARGE",
    lambda obj, **kwargs: get_measurement_data_for_river_and_day(obj, target_day, "water_discharge"),
    tag_settings,
    "Water discharge value",
    custom_number_format_fn=custom_round,
    data=True
)
author_tag = Tag(
    "AUTHOR",
    "John Doe",
    tag_settings,
    "Report author name"
)
date_tag = Tag(
    "DATE",
    DefaultDataManager.get_localized_date,
    tag_settings,
    "Date when the report was generated"
)


# create the ReportGenerator instance
report_generator = DefaultReportGenerator(
    tags=[region_tag, river_tag, measurement_day_tag, water_level_tag, water_discharge_tag, author_tag, date_tag],
    template='example2.xlsx',
    reports_directory_path=report_settings.report_output_path,
    templates_directory_path=report_settings.templates_directory_path,
    tag_settings=tag_settings,
    requires_header=True
)

report_generator.validate()
report_generator.generate_report(list_objects=rivers, output_filename="example4.xlsx")

```
This results with the following generated report:

| River name             | Measurement day | Water level   | Discharge level |
|------------------------|-----------------|---------------|-----------------|
| Region A               |                 |               |                 |
| River 1                | 2024-07-28      | 2.3           | 10.1            |
| River 2                | 2024-07-28      | 14.9          | 7.0             |
| River 3                | 2024-07-28      | 23.7          | 23.1            |
| Region B               |                 |               |                 |
| River 4                | -               | -             | -               |
| River 5                | 2024-07-28      | 35.8          | 17.5            |
| Region C               |                 |               |                 |
| River 6                | 2024-07-28      | 25.2          | 8.3             |
| Region D               |                 |               |                 |
| River 7                | -               | -             | -               |
| Generated by: John Doe |                 | July 29, 2024 |                 |
