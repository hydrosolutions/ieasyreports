from pydantic import BaseSettings


class Settings(BaseSettings):
    data_manager_class: str = 'ieasyreports.core.tags.data_manager.DefaultDataManager'
    template_generator_class: str = 'ieasyreports.core.report_generator.report_generator.DefaultReportGenerator'

    class Config:
        env_prefix = 'ieasyhydro'
        env_file = '.env'
