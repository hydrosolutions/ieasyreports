The next example demonstrates the usage of the `Tag` class
when your replacement function need to receive some arguments.

The same familiar .xlsx template is still in use:

| Title     | Author     | Date     |
|-----------|------------|----------|
| {{TITLE}} | {{AUTHOR}} | {{DATE}} |

The code could look something like this:

```python
from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.core.tags import DefaultDataManager, Tag
from ieasyreports.settings import TagSettings, ReportGeneratorSettings
import datetime as dt

report_settings = ReportGeneratorSettings()
tag_settings = TagSettings()


class Author:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def get_latest_publication_title(self, title):
        return f"{title} by {self.first_name} {self.last_name}"


report_author = Author("John", "Doe")

# Define tags
title_tag = Tag(
    "TITLE",
    lambda author, title: author.get_latest_publication_title(title),
    tag_settings,
    value_fn_args={"author": report_author, "title": "Report title"}
)
author_tag = Tag(
    "AUTHOR",
    lambda author: f"{author.first_name} {author.last_name}",
    tag_settings,
    value_fn_args={"author": report_author}
)
date_tag = Tag(
    "DATE",
    DefaultDataManager.get_localized_date,
    tag_settings,
    value_fn_args={"date": dt.datetime(2023, 1, 1, 12, 0), "date_format": "medium", "language": "hr_HR"}
)

# create the ReportGenerator instance
report_generator = DefaultReportGenerator(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx',
    reports_directory_path=report_settings.report_output_path,
    templates_directory_path=report_settings.templates_directory_path,
    tag_settings=tag_settings
)

report_generator.validate()
report_generator.generate_report(output_filename="example3.xlsx")

```

This results in an `example3.xlsx` file in the `reports` folder.
The content of the report will be:

| Title                    | Author   | Date         |
|--------------------------|----------|--------------|
| Report title by John Doe | John Doe | 1. sij 2023. |
