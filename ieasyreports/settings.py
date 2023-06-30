from pydantic import BaseSettings


class Settings(BaseSettings):
    data_manager_class: str = 'ieasyreports.core.tags.data_manager.DefaultDataManager'
    template_generator_class: str = 'ieasyreports.core.report_generator.report_generator.DefaultReportGenerator'
    templates_directory_path: str = 'templates'
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
