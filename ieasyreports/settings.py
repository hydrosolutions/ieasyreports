from pydantic_settings import BaseSettings, SettingsConfigDict
from importlib.resources import path

from pydantic import Field


def get_templates_directory_path() -> str:
    with path('ieasyreports', 'templates') as p:
        return str(p)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ieasyreports_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    data_manager_class: str = Field('ieasyreports.core.tags.data_manager.DefaultDataManager')
    template_generator_class: str = Field('ieasyreports.core.report_generator.report_generator.DefaultReportGenerator')
    templates_directory_path: str = Field(get_templates_directory_path())
    report_output_path: str = Field('reports')

    header_tag: str = Field('HEADER')
    data_tag: str = Field('DATA')
    split_symbol: str = Field('.')
    tag_start_symbol: str = Field('{{')
    tag_end_symbol: str = Field('}}')
