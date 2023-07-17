from typing import Any, Callable, Dict, Optional, Union

from ieasyreports.settings import Settings
from ieasyreports.exceptions import InvalidSpecialParameterException

settings = Settings()


class Tag:
    def __init__(
        self,
        name: str,
        get_value_fn: Union[Callable, str],
        description: Optional[str] = None,
        types: Optional[list[str]] = None,
        date_offset: Optional[Dict[str, int]] = None,
        custom_number_format_fn: Optional[Callable] = None
    ):
        self.name = name
        self.get_value_fn = get_value_fn
        self.description = description
        self.types = types
        self.date_offset = date_offset
        self.custom_number_format_fn = custom_number_format_fn

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return other == self.name

    def __hash__(self):
        return hash(self.name)

    def replace(self, content, **kwargs):
        if "special" in kwargs:
            full_tag = self.full_tag(special=kwargs.pop("special"))
        else:
            full_tag = self.full_tag()
        if full_tag in content:
            replacement_value = self.get_value_fn(**kwargs) if \
                self.has_callable_value_fn() else self.get_value_fn
            content = content.replace(full_tag, replacement_value)
        return content

    def has_callable_value_fn(self):
        return isinstance(self.get_value_fn, Callable)

    def has_custom_format(self):
        return self.custom_number_format_fn is not None

    def get_custom_format(self, value):
        if self.has_custom_format():
            return self.custom_number_format_fn(value)
        return value

    def full_tag(self, special=None):
        if special:
            if special not in (settings.header_tag, settings.data_tag):
                raise InvalidSpecialParameterException(f'{special} is not a supported value.')
            else:
                special_extension = f'{special}{settings.split_symbol}'
        else:
            special_extension = ''

        return f'{settings.tag_start_symbol}{special_extension}{self.name}{settings.tag_end_symbol}'
