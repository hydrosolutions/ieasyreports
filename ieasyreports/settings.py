from typing import Any, Callable
from pydantic_settings import BaseSettings, SettingsConfigDict
from importlib.resources import path

from pydantic import Field, ImportString


def get_templates_directory_path() -> str:
    with path('ieasyreports', 'templates') as p:
        return str(p)


class ReportGeneratorSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ieasyreports_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    data_manager_class: ImportString[Callable[[Any], Any]] = \
        'ieasyreports.core.tags.DefaultDataManager'
    template_generator_class:  ImportString[Callable[[Any], Any]] = \
        'ieasyreports.core.report_generator.DefaultReportGenerator'
    templates_directory_path: str = Field(get_templates_directory_path())
    report_output_path: str = Field('reports')


class TagSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ieasyreports_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    header_tag: str = Field('HEADER')
    data_tag: str = Field('DATA')
    split_symbol: str = Field('.')
    tag_start_symbol: str = Field('{{')
    tag_end_symbol: str = Field('}}')
