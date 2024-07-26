# Customization

This section will cover how to customize and extend certain parts of the library.

Several parts of the library can be customized to with your needs. The customizable
parts of the library can be viewed in the `settings.py` file:

```python

from pydantic_settings import BaseSettings, SettingsConfigDict
from importlib.resources import path

from pydantic import Field


def get_templates_directory_path() -> str:
    with path('ieasyreports', 'templates') as p:
        return str(p)


class ReportGeneratorSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ieasyreports_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    data_manager_class: ImportString[Callable[[Any], Any]] = \
        'ieasyreports.core.tags.DefaultDataManager'
    template_generator_class:  ImportString[Callable[[Any], Any]] = \
        'ieasyreports.core.report_generator.DefaultReportGenerator'
    templates_directory_path: str = Field(get_templates_directory_path())
    report_output_path: str = Field('reports')


class TagSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ieasyreports_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    header_tag: str = Field('HEADER')
    data_tag: str = Field('DATA')
    split_symbol: str = Field('.')
    tag_start_symbol: str = Field('{{')
    tag_end_symbol: str = Field('}}')
```

The `ReportGeneratorSettings` and `TagSettings` classes defines the used settings and their default values which we will go over next.

## ReportGenerator class

### Data manager class:
This class serves as a class where you can define methods that you will pass to your Tags
as replacement functions. The library's default DataManager class is `ieasyreports.core.tags.data_manager.DefaultDataManager`
which has a built-in method to get a localized date string. The class can be extended with
your own data manager class where you can define additional methods that you can use in your tags.

### Template generator class:
The class holding all the logic the generating the reports. It is used for grouping the tags,
validating them based on some pre-defined rules, opening the initial template file and
saving the output report. If your templates have a specific structure and the current logic
doesn't result in a nice looking output report, you can extend the class with your own
and add some custom logic to fit your needs. This setting defaults to `ieasyreports.core.report_generator.report_generator.DefaultReportGenerator`

The value for both of these settings should be a string defining the import path of the class.

### Templates directory path
Specifies the path where the library will look for the template file given to the
template generator class. Defaults to the `templates` folder inside the library itself.

### Report output path
Specifies where will the generated report be stored. Defaults to the `reports` folder
in the same directory as the file that you're running. If the `reports` folder doesn't
exist, it will be created.


## Tag settings class

### Header tag
String representing the prefix that the library expects for header tags. Defaults
to `HEADER`.

### Data tag
String representing the prefix that the library expects for data tags. Defaults
to `DATA`.

### Split symbol
Symbol that separates the tag type from its name. Default to the dot symbol.

### Tag start symbol
String that represents the start of a tag inside the template. Defaults to `{{`.

### Tag end symbol
String that represents the start of a tag inside the template. Defaults to `{{`.

These settings enable you to completely change how the tags look like in the template files.
If you leave the default values as they are, then your tags need to look something like this:

```text
    {{HEADER.TAG_NAME}}
    {{DATA.OTHER_TAG_NAME}}
    {{YET_ANOTHER_TAG_NAME}}
```

But if you change the values for the tag start and end symbol to `<` and `>` and the split symbol
to `#`, then the same tags would look like this in templates:
```text
    <HEADER#TAG_NAME>
    <DATA#OTHER_TAG_NAME>
    <YET_ANOTHER_TAG_NAME>
```

## Overriding the default settings values

The settings class is implement using the `pydantic-settings` library.
The `model_config` attribute of the `Settings` class tells us how to override each of the settings.

### env_prefix
The value of this attribute is set to `ieasyreports_`. This means that in order to
override a setting, you need to have an environment variable with a prefix of `ieasyreports_`
and the name of the setting you want to override. For example, if you want to specify
another directory where the library will look for templates, you could have an environment
variable called `ieasyreports_templates_directory_path` with a value of `/my/new/templates/directory/path`.
The variable names are **CASE INSENSITIVE**.

### env_file
Another way to override the settings value is by having a .env file in the same directory
as the file you're executing. The environment variables in the file need to follow the
same rules - the need to be prefixed followed by the exact setting name.

### Instantiate new Settings instance
You can instantiate a new Settings instance and add new values to any setting
by passing it to the constructor.


The last important thing to note is the order in which the library will look for
the settings values which is this:

* values passed to the constructor
* env variables
* variable loaded from .env file
* default values defined in the Settings class


### Example

To provide your own values for the supported settings, you can pass the name of your
.env file to the `Settings` constructor, like this:

```python
from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.settings import ReportGeneratorSettings, TagSettings

report_generator_settings = ReportGeneratorSettings(_env_file=".env_custom")
tag_settings = TagSettings()

report_generator = DefaultReportGenerator(
    tags=[tag1, tag2],
    template='example1.xlsx',
    reports_directory_path=report_generator_settings.report_output_path,
    templates_directory_path=report_generator_settings.templates_directory_path,
    tag_settings=tag_settings
)
```

An alternative would be to create your own instance of the Settings class:

```python
from pydantic import ImportString
from typing import Any, Callable
from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.settings import ReportGeneratorSettings, TagSettings

class MyReportGeneratorSettingsViaClass(ReportGeneratorSettings):
    data_manager_class: ImportString[Callable[[Any], Any]] = "path.to.CustomDataManagerClass"

my_report_generator = MyReportGeneratorSettingsViaClass()
tag_settings = TagSettings()

report_generator = DefaultReportGenerator(
    tags=[tag1, tag2],
    template='example1.xlsx',
    reports_directory_path=report_generator_settings.report_output_path,
    templates_directory_path=report_generator_settings.templates_directory_path,
    tag_settings=tag_settings
)
```

## Extending the ReportGenerator

There might be cases that the default report generator doesn't handle as expected.
This is to be expected since it's very hard to have a generic solution that will
handle all the possible templates.

For that reason, the default report generator is made to be as modular as possible and
by extension, it's very easily extendable.

For example, if you wish to have different validation rules for your templates, you could
do it as follows:

```python
from pydantic import ImportString
from typing import Any, Callable
from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.settings import ReportGeneratorSettings, TagSettings


class MyReportGeneratorSettings(ReportGeneratorSettings):
    template_generator_class: ImportString[Callable[[Any], Any]] = "path.to.MyCustomReportGenerator"

report_generator_settings = MyReportGeneratorSettings()
tag_settings = TagSettings()

class MyCustomReportGenerator(DefaultReportGenerator):
    def validate(self):
        super().validate()
        # your own validation logic below


report_generator = MyCustomReportGenerator(
    tags=[tag1, tag2],
    template='example1.xlsx',
    reports_directory_path=report_generator_settings.report_output_path,
    templates_directory_path=report_generator_settings.templates_directory_path,
    tag_settings=tag_settings
)
```
