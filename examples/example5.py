from pydantic import ImportString
from typing import Any, Callable

from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.core.tags import DefaultDataManager, Tag
from ieasyreports.settings import ReportGeneratorSettings, TagSettings


class CustomDataManager(DefaultDataManager):
    @classmethod
    def dummy_author_name(cls):
        return "Dummy Author"


class CustomReportGenerator(DefaultReportGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Inside the CustomReportGenerator")


class MyReportGeneratorSettings(ReportGeneratorSettings):
    data_manager_class: ImportString[Callable[[Any], Any]] = "examples.example5.CustomDataManager"
    template_generator_class: ImportString[Callable[[Any], Any]] = "examples.example5.CustomReportGenerator"


class MyTagSettings(TagSettings):
    tag_start_symbol: str = "<<"
    tag_end_symbol: str = ">>"


report_settings = MyReportGeneratorSettings()
tag_settings = MyTagSettings()


title_tag = Tag("TITLE", "Water Discharge Report", tag_settings)
author_tag = Tag("AUTHOR", report_settings.data_manager_class.dummy_author_name, tag_settings)
date_tag = Tag("DATE", report_settings.data_manager_class.get_localized_date, tag_settings)

report_generator = CustomReportGenerator(
    tags=[title_tag, author_tag, date_tag],
    template='example3.xlsx',
    reports_directory_path=report_settings.report_output_path,
    templates_directory_path=report_settings.templates_directory_path,
    tag_settings=tag_settings,
)

report_generator.validate()
report_generator.generate_report(output_filename="example5.xlsx")
