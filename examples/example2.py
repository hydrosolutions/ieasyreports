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
