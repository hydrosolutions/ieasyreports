import io
import re
from copy import copy
from typing import Any, Dict, List, Optional
import openpyxl
from openpyxl.cell import Cell, MergedCell
from openpyxl.formula.translate import Translator
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter, coordinate_to_tuple
from openpyxl.worksheet.worksheet import Worksheet
import os

from ieasyreports.core.tags.tag import Tag
from ieasyreports.settings import TagSettings
from ieasyreports.exceptions import (
    InvalidTagException, TemplateNotValidatedException, MultipleHeaderTagsException, MissingHeaderTagException,
    TemplateNotFoundException, MissingDataTagException
)


class DefaultReportGenerator:
    def __init__(
        self,
        tags: List[Tag],
        template: str,
        templates_directory_path: str,
        reports_directory_path: str,
        tag_settings: TagSettings,
        requires_header: bool = False
    ):
        self.tags = {tag.name: tag for tag in tags}
        self.template_filename = template
        self.templates_directory_path = templates_directory_path
        self.reports_directory_path = reports_directory_path
        self.template = self.open_template_file()
        self.tag_settings = tag_settings
        self.sheet = self.template.worksheets[0]

        self.validated = False

        self.requires_header_tag = requires_header
        self.header_tag_info = {}
        self.data_tags_info = []
        self.general_tags = {}

    def validate(self):
        self._check_tags()
        self._check_template_tags()
        self._validate_header_and_data_tags()
        self._validate_header_tag()
        self._validate_data_tags()
        self.validated = True

    def _get_template_full_path(self) -> str:
        return os.path.join(self.templates_directory_path, self.template_filename)

    def open_template_file(self) -> openpyxl.Workbook:
        template_path = self._get_template_full_path()
        try:
            workbook = openpyxl.load_workbook(template_path)
        except FileNotFoundError as e:
            raise TemplateNotFoundException(
                f"Cannot find {self.template_filename} in the {self.templates_directory_path} folder."
            )
        return workbook

    def iter_cells(self):
        for row in self.sheet.iter_rows():
            for cell in row:
                yield cell

    def _categorize_tag_by_type(self, tag, cell):
        tag_object = self.tags[tag["tag"]]

        if tag["tag_type"] == self.tag_settings.header_tag:
            if not self.header_tag_info:
                tag_object.set_context({"special": self.tag_settings.header_tag})
                self.header_tag_info["tag"] = tag_object
                self.header_tag_info["cell"] = cell
            else:
                raise MultipleHeaderTagsException("Multiple header tags found.")

        elif tag["tag_type"] == self.tag_settings.data_tag:
            tag_object.set_context({"special": self.tag_settings.data_tag})
            self.data_tags_info.append({"tag": tag_object, "cell": cell})

        else:
            if tag_object not in self.general_tags:
                self.general_tags[tag_object] = []

            self.general_tags[tag_object].append(cell)

    def _decode_template_tag(self, tag: str) -> Dict[str, str]:
        parts = tag.split(self.tag_settings.split_symbol)
        return {
            'tag': parts.pop(-1),
            'tag_type': parts.pop(-1) if parts else None
        }

    def _parse_template_tag(self, template_tag: str) -> list:
        try:
            tag_regex = rf"{self.tag_settings.tag_start_symbol}(.*?){self.tag_settings.tag_end_symbol}"
            return re.findall(tag_regex, template_tag)
        except TypeError:
            return []

    def _check_template_tags(self) -> None:
        for cell in self.iter_cells():
            if cell.value is None:
                continue

            for tag in self._parse_template_tag(cell.value):
                tag_info = self._decode_template_tag(tag)
                if tag_info["tag"] not in self.tags.keys():
                    raise InvalidTagException(f"The following tag is not supported: {tag_info['tag']}")

                self._categorize_tag_by_type(tag_info, cell)

    def _validate_header_and_data_tags(self) -> None:
        self._validate_header_tag()
        self._validate_data_tags()

    def _validate_header_tag(self) -> None:
        if self.requires_header_tag and not self.header_tag_info:
            raise MissingHeaderTagException("Header tag is missing in the template.")

    def _validate_data_tags(self) -> None:
        header_row = self.header_tag_info["cell"].row

        if not self.data_tags_info:
            raise MissingDataTagException("At least one DATA tag is required.")

        data_row = None
        for cell_info in self.data_tags_info:
            data_row_ = cell_info["cell"].row
            if data_row is None:
                data_row = data_row_
            if data_row != data_row_:
                raise InvalidTagException("All DATA tags must be in the same row.")
        if data_row - header_row != 1:
            raise InvalidTagException("DATA tags must be exactly 1 row below the HEADER tag.")

    def _check_tags(self) -> None:
        for tag in self.tags.values():
            if not isinstance(tag, Tag):
                raise InvalidTagException(
                    "All elements in the `tags` list must be a `Tag` instance."
                )

    def save_report(self, name: str, output_path: str):
        if output_path is None:
            output_path = self.reports_directory_path
        os.makedirs(output_path, exist_ok=True)

        if name is None:
            name = f"{self.template_filename.split('.xlsx')[0]}.xlsx"

        self.template.save(os.path.join(output_path, name))

    def _handle_general_tags(self):
        for tag, cells in self.general_tags.items():
            for cell in cells:
                try:
                    cell.value = tag.replace(cell.value)
                    print(cell)
                except Exception as e:
                    raise InvalidTagException(f"Error replacing tag {tag} in cell {cell.coordinate}: {e}")

    def _handle_header_and_data_tags(self, list_objects: list[Any]) -> None:
        grouped_data = self._create_header_grouping(list_objects)
        self._insert_empty_rows_for_data(grouped_data)
        header_dest_ranges, data_dest_ranges = self._get_cell_copy_ranges(grouped_data)
        print(header_dest_ranges)
        print(data_dest_ranges)

    def _get_cell_copy_ranges(
        self, grouped_data: dict[str, list[Any]]
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        header_tags_dest_ranges = []
        data_tags_dest_ranges = []
        original_header_row = self.header_tag_info["cell"].row
        original_header_col = self.header_tag_info["cell"].col_idx
        data_tags_row = original_header_row + 1
        current_row = original_header_row

        for header_value, header_items in grouped_data.items():
            print(f"HEADER: {header_value} goes into row {current_row}")
            if current_row != original_header_row:
                header_tags_dest_ranges.append((current_row, original_header_col))

            current_row += 1
            for item in header_items:
                print(f"ITEM: {item} goes into row {current_row}")
                if current_row != data_tags_row:
                    data_tags_dest_ranges.append((current_row, 1))

                current_row += 1

        return header_tags_dest_ranges, data_tags_dest_ranges

    def _create_header_grouping(self, list_objects: list[Any]) -> dict[str, list[Any]]:
        grouped_data = {}
        for obj in list_objects:
            self.header_tag_info["tag"].set_context({"obj": obj})
            header_value = self.header_tag_info["tag"].replace(self.header_tag_info["cell"].value, True)

            if header_value not in grouped_data:
                grouped_data[header_value] = []

            grouped_data[header_value].append(obj)

        return grouped_data

    def _insert_empty_rows_for_data(
        self, grouped_data: dict[str, list[Any]]
    ):
        # calculate the number of rows that need to be inserted
        num_of_new_rows = sum(len(objs) for objs in grouped_data.values()) + len(grouped_data) - 2

        # insert the rows
        original_header_row = self.header_tag_info["cell"].row
        data_tags_row = original_header_row + 1
        self.sheet.insert_rows(data_tags_row + 1, num_of_new_rows)

    @staticmethod
    def _copy_cell_style(self, src: Cell, dest: Cell):
        dest.value = src.value
        if src.has_style:
            dest.font = copy(src.font)
            dest.border = copy(src.border)
            dest.fill = copy(src.fill)
            dest.number_format = copy(src.number_format)
            dest.protection = copy(src.protection)
            dest.alignment = copy(src.alignment)

    def _add_global_tag_context(self, context: Dict[str, Any]):
        self.header_tag_info["tag"].set_context(context)
        for tag_info in self.data_tags_info:
            tag_info["tag"].set_context(context)
        for tag in self.general_tags:
            tag.set_context(context)

    def generate_report(
        self, list_objects: Optional[List[Any]] = None,
        output_path: Optional[str] = None, output_filename: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        as_stream: bool = False
    ) -> io.BytesIO | None:
        if not self.validated:
            raise TemplateNotValidatedException(
                "Template must be validated first. Did you forget to call the `.validate()` method?"
            )

        list_objects = list_objects or []

        if context:
            self._add_global_tag_context(context)

        # self._handle_general_tags()

        if self.header_tag_info:
            self._handle_header_and_data_tags(list_objects)

        if as_stream:
            output = io.BytesIO()
            self.template.save(output)
            output.seek(0)
            return output
        else:
            self.save_report(output_filename, output_path)
