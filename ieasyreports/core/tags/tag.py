from typing import Any, Callable, Dict, Optional, Union


class Tag:
    def __init__(
        self,
        name: str,
        replacement_value: Union[Callable, str],
        description: Optional[str] = None,
        types: Optional[list[str]] = None,
        data: Optional[bool] = False,
        header: Optional[bool] = False,
        date_offset: Optional[Dict[str, int]] = None,
        custom_number_format_fn: Optional[Callable] = None
    ):
        self.name = name
        self.replacement_value = replacement_value
        self.description = description
        self.types = types
        self.data = data
        self.header = header
        self.date_offset = date_offset
        self.custom_number_format_fn = custom_number_format_fn

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return other == self.name

    def __hash__(self):
        return hash(self.name)

    def replace(self, content, context):
        if self.name in content:
            replacement_value = self.replacement_value(context) if \
                self.has_callable_value_fn() else self.replacement_value
            content = content.replace(self.name, replacement_value)
        return content

    def has_callable_value_fn(self):
        return isinstance(self.replacement_value, Callable)

    def has_custom_format(self):
        return self.custom_number_format_fn is not None

    def get_custom_format(self, value):
        if self.has_custom_format():
            return self.custom_number_format_fn(value)
        return value
