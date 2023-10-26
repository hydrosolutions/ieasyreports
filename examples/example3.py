from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.core.tags import DefaultDataManager, Tag
import datetime as dt


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
    value_fn_args={"author": report_author, "title": "Report title"}
)
author_tag = Tag(
    "AUTHOR",
    lambda author: f"{author.first_name} {author.last_name}",
    value_fn_args={"author": report_author}
)
date_tag = Tag(
    "DATE",
    DefaultDataManager.get_localized_date,
    value_fn_args={"date": dt.datetime(2023, 1, 1, 12, 0), "date_format": "medium", "language": "hr_HR"}
)

# create the ReportGenerator instance
report_generator = DefaultReportGenerator(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx'
)

report_generator.validate()
report_generator.generate_report(output_filename="example3.xlsx")
