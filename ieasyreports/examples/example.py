from ieasyreports.core.tags.tag import Tag
from ieasyreports.core.tags.tags import date_tag

from ieasyreports.utils import import_from_string
from ieasyreports.settings import Settings
from ieasyreports.core.tags.data_manager import DischargeDataManager

settings = Settings()

from .dummy_sites import SITES

region_tag = Tag(
    "SITE_REGION",
    lambda site: site.region,
    "Site region"
)

basin_tag = Tag(
    "SITE_BASIN",
    lambda site: site.basin,
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
    "DISHCARGE_MORNING",
    DischargeDataManager.get_station_measurement_data,
    "Morning measurement value for the discharge",
)

discharge_evening_tag = Tag(
    "DISHCARGE_EVENING",
    DischargeDataManager.get_station_measurement_data,
    "Evening measurement value for the discharge",
)

water_level_morning_tag = Tag(
    "WATER_LEVEL_MORNING",
    DischargeDataManager.get_station_measurement_data,
    "Morning measurement value for the water level",
)

water_level_evening_tag = Tag(
    "WATER_LEVEL_EVENING",
    DischargeDataManager.get_station_measurement_data,
    "Evening measurement value for the water level",
)


