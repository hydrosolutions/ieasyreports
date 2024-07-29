This examples demonstrates how to use the Tag class when
you require a function for replacing the tags with some values.

For simplicity, let's say we're still working with the same `example1.xlsx` template:

| Title     | Author     | Date     |
|-----------|------------|----------|
| {{TITLE}} | {{AUTHOR}} | {{DATE}} |

For this example, the functions needed can be used without any arguments:

```python
from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.core.tags import Tag, DefaultDataManager
from ieasyreports.settings import TagSettings, ReportGeneratorSettings

report_settings = ReportGeneratorSettings()
tag_settings = TagSettings()


def dummy_author_name():
    return "John Doe"


# Define tags
title_tag = Tag("TITLE", "Water Discharge Report", tag_settings)
author_tag = Tag("AUTHOR", dummy_author_name, tag_settings)
date_tag = Tag("DATE", DefaultDataManager.get_localized_date, tag_settings)

# create the ReportGenerator instance
report_generator = DefaultReportGenerator(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx',
    reports_directory_path=report_settings.report_output_path,
    templates_directory_path=report_settings.templates_directory_path,
    tag_settings=tag_settings
)

report_generator.validate()
report_generator.generate_report(output_filename="example2.xlsx")
```


This should produce an `example2.xlsx` file in the `reports` folder, and it's content
should be the following:

| Title                  | Author   | Date            |
|------------------------|----------|-----------------|
| Water Discharge Report | John Doe | July 29, 2024   |

The value of the date tag depends on what date it is when running the script.
