from ieasyreports.core.tags.tag import Tag
from ieasyreports.core.tags.tags import date_tag

from ieasyreports.core.tags.data_manager import DischargeDataManager

title_tag = Tag(
    "TITLE",
    "Test report title",
    "Report title"
)

author_tag = Tag(
    "AUTHOR",
    "John Doe",
    "Report author"
)

region_tag = Tag(
    "SITE_REGION",
    lambda site: site.site_region,
    "Site region"
)

basin_tag = Tag(
    "SITE_BASIN",
    lambda site: site.site_basin,
    "Site river basin"
)

site_name_tag = Tag(
    "SITE_NAME",
    lambda site: site.name,
    "Site name"
)

site_code_tag = Tag(
    "SITE_CODE",
    lambda site: site.site_code
)

discharge_morning_tag = Tag(
    "DISCHARGE_MORNING",
    lambda site: DischargeDataManager.get_station_measurement_data(site, time_of_day="morning", measurement="water_discharge"),
    "Morning measurement value for the discharge",
)

discharge_evening_tag = Tag(
    "DISCHARGE_EVENING",
    lambda site: DischargeDataManager.get_station_measurement_data(site, time_of_day="evening", measurement="water_discharge"),
    "Evening measurement value for the discharge",
)

water_level_morning_tag = Tag(
    "WATER_LEVEL_MORNING",
    lambda site: DischargeDataManager.get_station_measurement_data(site, time_of_day="morning", measurement="water_level"),
    "Morning measurement value for the water level",
)

water_level_evening_tag = Tag(
    "WATER_LEVEL_EVENING",
    lambda site: DischargeDataManager.get_station_measurement_data(site, time_of_day="evening", measurement="water_level"),
    "Evening measurement value for the water level",
)

tags = [
    basin_tag, site_name_tag, discharge_morning_tag, discharge_evening_tag,
    water_level_morning_tag, water_level_evening_tag, date_tag, title_tag, author_tag
]
