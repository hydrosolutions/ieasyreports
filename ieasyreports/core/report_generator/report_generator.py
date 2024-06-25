import re
from typing import Any, Dict, List, Optional
import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.merge import MergedCellRange
import os

from ieasyreports.core.tags.tag import Tag
from ieasyreports.settings import TagSettings
from ieasyreports.exceptions import (
    InvalidTagException, TemplateNotValidatedException, MultipleHeaderTagsException, MissingHeaderTagException,
    TemplateNotFoundException,
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
                self.header_tag_info["tag"] = tag_object
                self.header_tag_info["cell"] = cell
            else:
                raise MultipleHeaderTagsException("Multiple header tags found.")

        elif tag["tag_type"] == self.tag_settings.data_tag:
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

    def _check_merged_cells(self):
        self._has_merged_cells = bool(self.sheet.merged_cells.ranges)

    def validate(self):
        self._check_tags()
        self._check_template_tags()
        self._check_merged_cells()
        self._validate_header_tag()
        self._validate_data_tags()
        self.validated = True

    def save_report(self, name: str, output_path: str):
        if output_path is None:
            output_path = self.reports_directory_path
        os.makedirs(output_path, exist_ok=True)

        if name is None:
            name = f"{self.template_filename.split('.xlsx')[0]}.xlsx"

        self.template.save(os.path.join(output_path, name))

    def _handle_general_tags(self):
        context = {}
        for tag, cells in self.general_tags.items():
            for cell in cells:
                try:
                    cell.value = tag.replace(cell.value, context=context)
                except Exception as e:
                    raise InvalidTagException(f"Error replacing tag {tag} in cell {cell.coordinate}: {e}")

    def _unmerge_cells(self) -> list[MergedCellRange]:
        # identify merged cells
        template_merged_ranges = list(self.sheet.merged_cells.ranges)

        # Unmerge all cells in the sheet initially to avoid conflicts
        for merged_cell_range in template_merged_ranges:
            self.sheet.unmerge_cells(str(merged_cell_range))

        return template_merged_ranges

    def _merge_cells(self, row: int, original_merged_cell_ranges: list[MergedCellRange]):
        for merged_cell_range in original_merged_cell_ranges:
            merged_range = str(merged_cell_range).split(":")
            start_cell = merged_range[0]
            end_cell = merged_range[1]
            start_row = row
            end_row = row
            start_column = self.sheet[start_cell].column
            end_column = self.sheet[end_cell].column

            self.sheet.merge_cells(
                start_row=start_row, start_column=start_column, end_row=end_row, end_column=end_column
            )

    def _handle_header_and_data_tags(self, list_objects: list[Any], merged_cell_ranges: list[MergedCellRange]):
        grouped_data = self._group_data_by_header(list_objects)
        original_header_row = self.header_tag_info["cell"].row
        header_style, header_alignment, data_styles, data_alignments = self._get_styles()

        self.sheet.delete_rows(original_header_row, 2)

        for header_value, item_group in sorted(grouped_data.items()):
            self._write_header_value(
                header_value, original_header_row, header_style, header_alignment, merged_cell_ranges
            )
            self._write_data_rows(item_group, original_header_row, data_styles, data_alignments)
            original_header_row += len(item_group) + 1


    def _group_data_by_header(self, list_objects: list[Any]) -> dict[str, list[Any]]:
        grouped_data = {}
        for list_obj in list_objects:
            context = {"obj": list_obj, "special": self.tag_settings.header_tag}
            header_value = self.header_tag_info["tag"].replace(self.header_tag_info["cell"].value, context=context)

            if header_value not in grouped_data:
                grouped_data[header_value] = []

            grouped_data[header_value].append(list_obj)

        return grouped_data

    def _get_styles(self) -> tuple[Font, Alignment, list[Font], list[Alignment]]:
        header_style = self.header_tag_info["cell"].font.copy()
        header_alignment = self.header_tag_info["cell"].alignment.copy()
        data_styles = [data_tag["cell"].font.copy() for data_tag in self.data_tags_info]
        data_alignments = [data_tag["cell"].alignment.copy() for data_tag in self.data_tags_info]

        return header_style, header_alignment, data_styles, data_alignments

    def _write_header_value(
        self,
        header_value: str,
        row: int,
        style: Font,
        alignment: Alignment,
        merged_cell_ranges: list[MergedCellRange]
    ):
        self.sheet.insert_rows(row)
        self._merge_cells(row, merged_cell_ranges)
        cell = self.sheet.cell(row=row, column=self.header_tag_info["cell"].column, value=header_value)
        cell.font = style
        cell.alignment = alignment

    def _write_data_rows(
        self, item_group: list[Any], row: int, data_styles: list[Font], data_alignments: list[Alignment]
    ):
        context = {"special": self.tag_settings.data_tag}
        for item in item_group:
            context["obj"] = item
            self.sheet.insert_rows(row + 1)
            for idx, data_tag in enumerate(self.data_tags_info):
                tag = data_tag["tag"]
                data = tag.replace(data_tag["cell"].value, context=context)
                cell = self.sheet.cell(row=row + 1, column=data_tag["cell"].column, value=data)
                cell.font = data_styles[idx]
                cell.alignment = data_alignments[idx]

    def generate_report(
        self, list_objects: Optional[List[Any]] = None,
        output_path: Optional[str] = None, output_filename: Optional[str] = None
    ):
        if not self.validated:
            raise TemplateNotValidatedException(
                "Template must be validated first. Did you forget to call the `.validate()` method?"
            )

        list_objects = list_objects or []
        merged_cells = []

        self._handle_general_tags()
        if self._has_merged_cells:
            merged_cells = self._unmerge_cells()

        if self.header_tag_info:
            self._handle_header_and_data_tags(list_objects, merged_cells)

        self.save_report(output_filename, output_path)
