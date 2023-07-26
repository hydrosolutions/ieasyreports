import re
from typing import Any, Dict, List, Optional
import openpyxl
import os

from ieasyreports.core.tags.tag import Tag
from ieasyreports.settings import Settings
from ieasyreports.exceptions import (
    InvalidTagException, TemplateNotValidatedException, MultipleHeaderTagsException, MissingHeaderTagException,
    TemplateNotFoundException
)

settings = Settings()


class DefaultReportGenerator:
    def __init__(self, tags: List[Tag], template: str, requires_header: bool = False):
        self.tags = {tag.name: tag for tag in tags}
        self.template_filename = template
        self.template = self.open_template_file()
        self.sheet = self.template.worksheets[0]

        self.validated = False

        self.requires_header_tag = requires_header
        self.header_tag_info = {}
        self.data_tags_info = []
        self.general_tags = {}

    def _get_template_full_path(self) -> str:
        return os.path.join(settings.templates_directory_path, self.template_filename)

    def open_template_file(self) -> openpyxl.Workbook:
        template_path = self._get_template_full_path()
        try:
            workbook = openpyxl.load_workbook(template_path)
        except FileNotFoundError as e:
            raise TemplateNotFoundException(
                f"Cannot find {self.template_filename} in the {settings.templates_directory_path} folder."
            )
        return workbook

    def iter_cells(self):
        for row in self.sheet.iter_rows():
            for cell in row:
                yield cell

    def _categorize_tag_by_type(self, tag, cell):
        tag_object = self.tags[tag["tag"]]

        if tag["tag_type"] == settings.header_tag:
            if not self.header_tag_info:
                self.header_tag_info["tag"] = tag_object
                self.header_tag_info["cell"] = cell
            else:
                raise MultipleHeaderTagsException("Multiple header tags found.")

        elif tag["tag_type"] == settings.data_tag:
            self.data_tags_info.append({"tag": tag_object, "cell": cell})

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
            tag_regex = rf"{settings.tag_start_symbol}(.*?){settings.tag_end_symbol}"
            return re.findall(tag_regex, template_tag)
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
        if self.requires_header_tag and not self.header_tag_info:
            raise MissingHeaderTagException("Header tag is missing in the template.")

    def _validate_data_tags(self):
        pass

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

    def save_report(self, name: str, output_path: str):
        if output_path is None:
            output_path = settings.report_output_path
        os.makedirs(output_path, exist_ok=True)

        if name is None:
            name = f"{self.template_filename.split('.xlsx')[0]}.xlsx"

        self.template.save(os.path.join(output_path, name))

    def generate_report(
        self, list_objects: Optional[List[Any]] = None,
        output_path: Optional[str] = None, output_filename: Optional[str] = None
    ):
        if not self.validated:
            raise TemplateNotValidatedException(
                "Template must be validated first. Did you forget to call the `.validate()` method?"
            )
        for tag, cells in self.general_tags.items():
            for cell in cells:
                cell.value = tag.replace(cell.value)

        if self.header_tag_info:
            grouped_data = {}
            list_objects = list_objects if list_objects else []
            for list_obj in list_objects:
                header_value = self.header_tag_info["tag"].replace(
                    self.header_tag_info["cell"].value,
                    special="HEADER",
                    obj=list_obj
                )

                if header_value not in grouped_data:
                    grouped_data[header_value] = []
                grouped_data[header_value].append(list_obj)

            original_header_row = self.header_tag_info["cell"].row
            header_style = self.header_tag_info["cell"].font.copy()
            data_styles = [data_tag["cell"].font.copy() for data_tag in self.data_tags_info]

            self.sheet.delete_rows(original_header_row, 2)

            for header_value, item_group in sorted(grouped_data.items()):
                # write the header value
                self.sheet.insert_rows(original_header_row)
                cell = self.sheet.cell(row=original_header_row, column=self.header_tag_info["cell"].column, value=header_value)
                cell.font = header_style

                for item in item_group:
                    self.sheet.insert_rows(original_header_row + 1)
                    for idx, data_tag in enumerate(self.data_tags_info):
                        tag = data_tag["tag"]
                        data = tag.replace(data_tag["cell"].value, obj=item, special=settings.data_tag)
                        cell = self.sheet.cell(row=original_header_row + 1, column=data_tag["cell"].column, value=data)
                        cell.font = data_styles[idx]

                original_header_row += len(item_group) + 1

        self.save_report(output_filename, output_path)
