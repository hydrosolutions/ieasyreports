import re
from typing import Dict, List
import openpyxl
import os

from ieasyreports.core.tags.tag import Tag
from ieasyreports.settings import Settings
from ieasyreports.exceptions import (
    InvalidTagException, TemplateNotValidatedException, MultipleHeaderTagsException, MissingHeaderTagException,
    MissingDataTagException
)

settings = Settings()


class DefaultReportGenerator:
    def __init__(self, tags: List[Tag], template: str):
        self.tags = {tag.name: tag for tag in tags}
        self.template_filename = template
        self.template = self.open_template_file()
        self.sheet = self.template.worksheets[0]

        self.validated = False

        self.header_tag = None
        self.header_cell = None

        self.data_cells = []
        self.data_tags = set()

        self.general_tags = {}

    def _get_template_full_path(self) -> str:
        return os.path.join(settings.templates_directory_path, self.template_filename)

    def open_template_file(self) -> openpyxl.Workbook:
        template_path = self._get_template_full_path()
        workbook = openpyxl.load_workbook(template_path)
        return workbook

    def iter_cells(self):
        for row in self.sheet.iter_rows():
            for cell in row:
                yield cell

    def _categorize_tag_by_type(self, tag, cell):
        tag_object = self.tags[tag["tag"]]

        if tag["tag_type"] == settings.header_tag:
            if not self.header_tag:
                self.header_tag = tag_object
                self.header_cell = cell
            else:
                raise MultipleHeaderTagsException("Multiple header tags found.")

        elif tag["tag_type"] == settings.data_tag:
            self.data_tags.add(tag_object)
            self.data_cells.append(cell)

        else:
            if tag_object not in self.general_tags:
                self.general_tags[tag_object] = []

            self.general_tags[tag_object].append(cell)

    @staticmethod
    def _decode_template_tag(tag: str) -> Dict[str, str]:
        parts = tag.split(settings.split_symbol)
        return {
            'tag': parts.pop(-1),
            'tag_type': parts.pop(-1) if parts else None
        }

    @staticmethod
    def _parse_template_tag(template_tag: str) -> list:
        try:
            return re.findall(settings.tag_regex, template_tag)
        except TypeError:
            return []

    def _check_template_tags(self):
        for cell in self.iter_cells():
            if cell.value is None:
                continue

            for tag in self._parse_template_tag(cell.value):
                tag_info = self._decode_template_tag(tag)
                if tag_info["tag"] not in self.tags.keys():
                    raise InvalidTagException(f"The following tag is not supported: {tag_info['tag']}")

                self._categorize_tag_by_type(tag_info, cell)

    def _validate_header_tag(self):
        if not self.header_tag:
            raise MissingHeaderTagException("Header tag is missing in the template.")

    def _validate_data_tags(self):
        if not self.data_tags:
            raise MissingDataTagException("At least one data tag must be present in a template.L")

    def _check_tags(self):
        for tag in self.tags.values():
            if not isinstance(tag, Tag):
                raise InvalidTagException(
                    "All elements in the `tags` list must be a `Tag` instance."
                )

    def validate(self):
        self._check_tags()
        self._check_template_tags()
        self._validate_header_tag()
        self._validate_data_tags()
        self.validated = True

    def save_report(self, name: str):
        self.template.save(os.path.join(settings.report_output_path, name))

    def generate_report(self):
        if not self.validated:
            raise TemplateNotValidatedException(
                "Template must be validated first. Did you forget to call the `.validate()` method?"
            )
        for tag, cells in self.general_tags.items():
            for cell in cells:
                cell.value = tag.replace(cell.value, {})

        self.save_report("basic_report.xlsx")
