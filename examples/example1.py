from ieasyreports.core.tags.tag import Tag
from ieasyreports.core.report_generator import DefaultReportGenerator


def author_uppercase(author: str):
    return author.upper()


# Define tags
title_tag = Tag("TITLE", "Water Discharge Report")
author_tag = Tag("AUTHOR", "John Doe", custom_number_format_fn=author_uppercase)
date_tag = Tag("DATE", "January 1st, 2023")

# create the ReportGenerator instance
report_generator = DefaultReportGenerator(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx'
)

report_generator.validate()
report_generator.generate_report()
