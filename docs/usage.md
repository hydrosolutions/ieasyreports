# Usage

This guide shows some basic usages of the library.

## Tag creation

iEasyReports revolves around the creation of Tag objects.
A Tag maps a placeholder in a template to a function that provides the actual data.
Here's an example of creating a `Tag`:

```python
from ieasyreports.core.tags.tag import Tag
from ieasyreports.settings import TagSettings

tag_settings = TagSettings()

author_tag = Tag(
    "AUTHOR",
    "John Doe",
    tag_settings,
    "Report author"
)
```

The first argument is the name of the tag as it appears in the template, the second argument is the actual value or a function
that returns the value and the third argument is an optional description.

Here are all the parameters that a Tag object accepts during instantiation:

- `name`: The name of the tag.
- `get_value_fn`: The function or string used to get the replacement value for the tag.
- `tag_settings`: Instance of `TagSettings` containing the details about the tag definition
- `description` (optional): A description of the tag.
- `value_fn_args`: Arguments that will be passed to the `get_value_fn`.
- `custom_number_format_fn` (optional): A custom function to format the tag's value.
- `header` (optional): Set to `True` if the tag is meant to be used as a header tag (for grouping purposes)
- `data` (optional): Set to `True` if the tag is meant to be used as a data tag (part of the grouping)


## DataManager Classes

DataManager classes encapsulate the logic required to access and format the data.
The DefaultDataManager class provides a basic example of a DataManager,
providing a method to format a date:

```python
from datetime import datetime as dt

from ieasyreports.core.tags import Tag
from ieasyreports.core.tags import DefaultDataManager
from ieasyreports.settings import TagSettings

tag_settings = TagSettings()

default_date_tag = Tag(
    "DEFAULT_DATE",
    DefaultDataManager.get_localized_date,
    tag_settings
)

argument_date_tag = Tag(
    "ARGUMENT_DATE",
    DefaultDataManager.get_localized_date,
    tag_settings,
    value_fn_args={"date": dt(2023, 1, 1, 12, 0), "date_format": "medium", "language": "hr_HR"}
)
```

The `argument_date_tag` showcases how to provide static arguments to the method from the data manager. For more complex
examples and dynamic value function arguments check the examples below.

## Examples
The following list of examples showcase the intended usage of the library.

### Example 1: Hardcoded tag replacement values
```{include} example1.md
```

### Example 2: Using functions to provide the replacement values
```{include} example2.md
```

### Example 3: Providing arguments to replacement value functions
```{include} example3.md
```

### Example 4: Use `header` tags for data grouping
```{include} example4.md
```

### Example 5: Customizing the library
```{include} example5.md
```
