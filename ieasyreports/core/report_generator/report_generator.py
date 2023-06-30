from typing import Dict, List
import openpyxl
import os

from ieasyreports.core.tags.tag import Tag
from ieasyreports.settings import Settings
from ieasyreports.exceptions import (
    InvalidTagException, TemplateNotValidatedException, MultipleHeaderTagsException
)

settings = Settings()


class DefaultReportGenerator:
    def __init__(self, tags: List[Tag], template: str):
        self.tags = {tag.name: tag for tag in tags}
        self.template_filename = template
        self.template = self.open_template_file()
        self.validated = False
        self.header_tag = None

    def _get_template_full_path(self) -> str:
        return os.path.join(settings.templates_directory_path, self.template_filename)

    def open_template_file(self) -> openpyxl.Workbook:
        template_path = self._get_template_full_path()
        workbook = openpyxl.load_workbook(template_path)
        return workbook

    def _check_tags(self):
        for tag in self.tags.values():
            if not isinstance(tag, Tag):
                raise InvalidTagException(
                    "All elements in the `tags` list must be a `Tag` instance."
                )

    def validate(self):
        self._check_tags()
        self.validated = True

    def save_report(self, name: str):
        self.template.save(os.path.join(settings.report_output_path, name))

    @staticmethod
    def decode_template_tag(tag: str) -> Dict[str, str]:
        parts = tag.split(settings.split_symbol)
        return {
            'tag': parts.pop(-1),
            'tag_type': parts.pop(-1) if parts else None
        }

    @staticmethod
    def parse_template_tag(template_tag: str) -> str:
        return template_tag.replace(settings.tag_start_symbol, "").replace(settings.tag_end_symbol, "")

    def validate_template_tag(self, tag: str, tag_type: str):
        if tag_type == settings.header_tag and self.header_tag:
            raise MultipleHeaderTagsException("Multiple header tags found.")

        if tag not in self.tags.keys():
            raise InvalidTagException(f"The following tag is not supported: {tag}")

    def generate_report(self):
        if not self.validated:
            raise TemplateNotValidatedException(
                "Template must be validated first. Did you forget to call the `.validate()` method?"
            )

        sheet = self.template.worksheets[0]

        for row in sheet.iter_rows():
            for cell in row:
                for tag_name, tag in self.tags.items():
                    tag_info = self.decode_template_tag(cell.value)
                    self.validate_template_tag(**tag_info)
                    if self.parse_template_tag(tag_info["tag"]) in str(cell.value):
                        cell.value = tag.replace(str(cell.value), {})

        self.save_report("basic_report.xlsx")
