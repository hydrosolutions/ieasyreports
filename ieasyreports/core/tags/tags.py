from ieasyreports.core.tags import Tag

from ieasyreports.utils import import_from_string
from ieasyreports.settings import Settings

settings = Settings()
DataManager = import_from_string(settings.data_manager_class)


date_tag = Tag(
    'DATE',
    DataManager.get_localized_date,
    'Today\'s localized string.'
)
