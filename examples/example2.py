from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.core.tags import Tag, DefaultDataManager


def dummy_author_name():
    return "John Doe"


# Define tags
title_tag = Tag("TITLE", "Water Discharge Report")
author_tag = Tag(
    "AUTHOR",
    dummy_author_name
)
date_tag = Tag(
    "DATE",
    DefaultDataManager.get_localized_date
)

# create the ReportGenerator instance
report_generator = DefaultReportGenerator(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx'
)

report_generator.validate()
report_generator.generate_report(output_filename="example2.xlsx")
