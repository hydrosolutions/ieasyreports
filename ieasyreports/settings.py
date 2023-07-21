from pydantic import BaseSettings
from importlib.resources import path


def get_templates_directory_path() -> str:
    with path('ieasyreports', 'templates') as p:
        return str(p)


class Settings(BaseSettings):
    data_manager_class: str = 'ieasyreports.core.tags.data_manager.DefaultDataManager'
    template_generator_class: str = 'ieasyreports.core.report_generator.report_generator.DefaultReportGenerator'
    templates_directory_path: str = get_templates_directory_path()
    report_output_path: str = 'reports'

    header_tag: str = 'HEADER'
    data_tag: str = 'DATA'
    split_symbol: str = '.'
    tag_start_symbol: str = '{{'
    tag_end_symbol: str = '}}'
    tag_regex: str = rf"{tag_start_symbol}(.*?){tag_end_symbol}"

    class Config:
        env_prefix = 'ieasyhydro'
        env_file = '.env'
