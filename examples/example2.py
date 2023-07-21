from ieasyreports.core.tags.tag import Tag
from ieasyreports.utils import import_from_string

from ieasyreports.settings import Settings

settings = Settings()
DataManager = import_from_string(settings.data_manager_class)


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
    DataManager.get_localized_date
)

# create the ReportGenerator instance
report_generator = import_from_string(settings.template_generator_class)(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx'
)

report_generator.validate()
report_generator.generate_report(output_filename="example2.xlsx")
