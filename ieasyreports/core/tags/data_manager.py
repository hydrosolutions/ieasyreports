from typing import Optional
from datetime import datetime

from babel.dates import format_date


class DefaultDataManager:
    @classmethod
    def get_localized_date(
        cls, **kwargs
    ) -> str:
        date = kwargs.get("date") or datetime.today()
        return format_date(date, locale=kwargs.get("language", "en"), format=kwargs.get("format", "long"))
