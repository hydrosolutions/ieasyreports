from ieasyreports.core.tags.tag import Tag
from ieasyreports.utils import import_from_string

from ieasyreports.settings import Settings

settings = Settings()

# Define tags
title_tag = Tag("TITLE", "Water Discharge Report")
author_tag = Tag("AUTHOR", "John Doe")
date_tag = Tag("DATE", "January 1st, 2023")

# create the ReportGenerator instance
report_generator = import_from_string(settings.template_generator_class)(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx'
)

report_generator.validate()
report_generator.generate_report()
