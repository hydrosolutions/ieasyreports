from typing import Any, Callable, Dict, Optional, Union

from ieasyreports.settings import TagSettings
from ieasyreports.exceptions import InvalidSpecialParameterException


class Tag:
    def __init__(
        self,
        name: str,
        get_value_fn: Union[Callable, str],
        tag_settings: TagSettings,
        value_fn_args: Optional[Dict[Any, Any]] = None,
        custom_number_format_fn: Optional[Callable] = None,
    ):
        self.name = name
        self.get_value_fn = get_value_fn
        self.value_fn_args = value_fn_args if value_fn_args else {}
        self.custom_number_format_fn = custom_number_format_fn
        self.settings = tag_settings

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
            replacement_value = str(self.get_value_fn(**kwargs, **self.value_fn_args)) if \
                self.has_callable_value_fn() else self.get_value_fn
            if self.has_custom_format():
                replacement_value = self.custom_number_format_fn(replacement_value)
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
            if special not in (self.settings.header_tag, self.settings.data_tag):
                raise InvalidSpecialParameterException(f'{special} is not a supported value.')
            else:
                special_extension = f'{special}{self.settings.split_symbol}'
        else:
            special_extension = ''

        return f'{self.settings.tag_start_symbol}{special_extension}{self.name}{self.settings.tag_end_symbol}'
