from ieasyreports.core.report_generator import DefaultReportGenerator
from ieasyreports.core.tags import DefaultDataManager, Tag
from ieasyreports.settings import Settings

my_settings = Settings(_env_file="examples/.env_custom")


class MySettingsViaClass(Settings):
    report_output_path: str = 'custom/output/path'


class CustomDataManager(DefaultDataManager):
    @classmethod
    def dummy_author_name(cls):
        return "Dummy Author"


class CustomReportGenerator(DefaultReportGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"DEBUG: {self.settings}")


title_tag = Tag("TITLE", "Water Discharge Report")
author_tag = Tag(
    "AUTHOR",
    CustomDataManager.dummy_author_name()
)
date_tag = Tag(
    "DATE",
    CustomDataManager.get_localized_date
)


report_generator = CustomReportGenerator(
    tags=[title_tag, author_tag, date_tag],
    template='example1.xlsx',
    custom_settings=my_settings
    # custom_settings=MySettingsViaClass()
)

report_generator.validate()
report_generator.generate_report(output_filename="example5.xlsx")
