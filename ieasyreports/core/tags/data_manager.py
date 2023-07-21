from typing import Optional
from datetime import datetime

from babel.dates import format_date


class DefaultDataManager:
    @classmethod
    def get_localized_date(
        cls, date: Optional[datetime] = None, language: str = 'en', date_format: str = 'long'
    ) -> str:
        date = date or datetime.today()
        return format_date(date, locale=language, format=date_format)
