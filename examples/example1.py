from ieasyreports.core.tags.tag import Tag
from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.settings import TagSettings, ReportGeneratorSettings

report_settings = ReportGeneratorSettings()
tag_settings = TagSettings()


def author_uppercase(author: str):
    return author.upper()


# Define tags
title_tag = Tag("TITLE", "Water Discharge Report", tag_settings)
author_tag = Tag("AUTHOR", "John Doe", tag_settings, custom_number_format_fn=author_uppercase)
date_tag = Tag("DATE", "January 1st, 2023", tag_settings)

# create the ReportGenerator instance
report_generator = DefaultReportGenerator(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx',
    reports_directory_path=report_settings.report_output_path,
    templates_directory_path=report_settings.templates_directory_path,
    tag_settings=tag_settings
)

report_generator.validate()
report_generator.generate_report()
