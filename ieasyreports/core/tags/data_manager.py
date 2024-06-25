from datetime import datetime

from babel.dates import format_date, format_time


class DefaultDataManager:
    @classmethod
    def get_localized_date(cls, **kwargs) -> str:
        date = kwargs.get("date") or datetime.today()
        return format_date(date, locale=kwargs.get("language", "en"), format=kwargs.get("format", "long"))

    @classmethod
    def get_localized_time(cls, **kwargs) -> str:
        time = kwargs.get("time") or datetime.now().time()
        return format_time(time, locale=kwargs.get("language", "en"), format=kwargs.get("format", "short"))
