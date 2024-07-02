import re
from copy import copy
from typing import Any, Dict, List, Optional
import openpyxl
from openpyxl.cell import Cell
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

    @staticmethod
    def _copy_cell_style(src: Cell, dest: Cell) -> None:
        dest.font = copy(src.font)
        dest.border = copy(src.border)
        dest.fill = copy(src.fill)
        dest.number_format = copy(src.number_format)
        dest.protection = copy(src.protection)
        dest.alignment = copy(src.alignment)

    def _copy_range(
        self,
        range_start: tuple[int, int],
        range_end: tuple[int, int],
        dest_ranges: list[tuple[int, int]]
    ) -> None:
        source_rows = list(self.sheet.iter_rows(
            min_row=range_start[0], max_row=range_end[0], min_col=range_start[1], max_col=range_end[1])
        )
        for dest_range_start in dest_ranges:
            dest_row = dest_range_start[0]
            dest_col = dest_range_start[1]

            for row in source_rows:
                cells = row
                for cell in cells:
                    self._move_cell(
                        src_cell=cell,
                        dest_row=dest_row,
                        dest_col=dest_col,
                        preserve_original=True,
                        move_merged=True
                    )
                    dest_col += 1
                dest_row += 1

    def _move_cell(
        self, src_cell: Cell, dest_row: int, dest_col: int,
        preserve_original: bool = False, move_merged: bool = False
    ) -> Cell:
        worksheet = src_cell.parent
        cell_to_move = self._create_cell_to_move(src_cell, worksheet, preserve_original)
        self._perform_cell_move(worksheet, cell_to_move, dest_row, dest_col)
        self._update_cell_formula(cell_to_move, src_cell, dest_row, dest_col)

        if move_merged:
            self._handle_merged_cells(worksheet, src_cell, dest_row, dest_col)

        if not preserve_original:
            del worksheet._cells[(src_cell.row, src_cell.column)]

        return cell_to_move

    def _handle_merged_cells(
        self, worksheet: Worksheet, src_cell: Cell, dest_row: int, dest_col: int
    ) -> None:
        for merged_cell_range in worksheet.merged_cells.ranges:
            if src_cell.coordinate == merged_cell_range:
                start_cell, end_cell = str(merged_cell_range).split(':')
                start_row, start_col = coordinate_to_tuple(start_cell)
                end_row, end_col = coordinate_to_tuple(end_cell)

                row_diff = dest_row - src_cell.row
                col_diff = dest_col - src_cell.column

                new_start_row = start_row + row_diff
                new_start_col = start_col + col_diff
                new_end_row = end_row + row_diff
                new_end_col = end_col + col_diff

                new_start_cell = get_column_letter(new_start_col) + str(new_start_row)
                new_end_cell = get_column_letter(new_end_col) + str(new_end_row)

                new_range = f"{new_start_cell}:{new_end_cell}"

                # Unmerge the original range and merge the new range
                worksheet.unmerge_cells(str(merged_cell_range))
                worksheet.merge_cells(new_range)
                break  # Exit after the first relevant merged range is found

    def _create_cell_to_move(self, src_cell: Cell, worksheet: Worksheet, preserve_original: bool) -> Cell:
        if preserve_original:
            cell_to_move = worksheet.cell(row=src_cell.row, column=src_cell.column)
            cell_to_move.value = src_cell.value
            self._copy_cell_style(src_cell, cell_to_move)
        else:
            cell_to_move = src_cell

        return cell_to_move

    @staticmethod
    def _perform_cell_move(worksheet: Worksheet, cell_to_move: Cell, dest_row: int, dest_col: int) -> None:
        worksheet._move_cell(
            cell_to_move.row, cell_to_move.column, dest_row - cell_to_move.row, dest_col - cell_to_move.column
        )

    @staticmethod
    def _update_cell_formula(cell_to_move: Cell, src_cell: Cell, dest_row: int, dest_col: int) -> None:
        if cell_to_move.data_type == 'f':
            cell_to_move.value = Translator(
                cell_to_move.value,
                f"{get_column_letter(src_cell.column)}{src_cell.row}"
            ).translate_formula(
                f"{get_column_letter(dest_col)}{dest_row}"
            )


    def _unmerge_cells(self) -> list[Any]:
        template_merged_ranges = list(self.sheet.merged_cells.ranges)
        for merged_cell_range in template_merged_ranges:
            self.sheet.unmerge_cells(str(merged_cell_range))
        return template_merged_ranges

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

    def _handle_header_and_data_tags(
        self,
        list_objects: list[Any]
    ):
        grouped_data = self._group_data_by_header(list_objects)
        original_header_row = self.header_tag_info["cell"].row

        self.sheet.delete_rows(original_header_row, 2)

        for header_value, item_group in sorted(grouped_data.items()):
            self._write_header_value(
                header_value, original_header_row
            )
            self._write_data_rows(item_group, original_header_row)
            original_header_row += len(item_group) + 1

    def _group_data_by_header(self, list_objects: list[Any]) -> dict[str, list[Any]]:
        grouped_data = {}
        for list_obj in list_objects:
            self.header_tag_info["tag"].set_context({"obj": list_obj})
            header_value = self.header_tag_info["tag"].replace(self.header_tag_info["cell"].value)

            if header_value not in grouped_data:
                grouped_data[header_value] = []

            grouped_data[header_value].append(list_obj)

        return grouped_data

    def _write_header_value(self, header_value: str, row: int) -> None:
        self.sheet.insert_rows(row)
        _ = self.sheet.cell(row=row, column=self.header_tag_info["cell"].column, value=header_value)

    def _write_data_rows(self, item_group: list[Any], row: int) -> None:
        for item in item_group:
            self.sheet.insert_rows(row + 1)
            for data_tag in self.data_tags_info:
                tag = data_tag["tag"]
                tag.set_context({"obj": item})
                data = tag.replace(data_tag["cell"].value)
                cell = self.sheet.cell(row=row + 1, column=data_tag["cell"].column, value=data)
                self._copy_cell_style(data_tag["cell"], cell)
            row += 1

    def _add_global_tag_context(self, context: Dict[str, Any]):
        self.header_tag_info["tag"].set_context(context)
        for tag_info in self.data_tags_info:
            tag_info["tag"].set_context(context)
        for tag in self.general_tags:
            tag.set_context(context)

    def generate_report(
        self, list_objects: Optional[List[Any]] = None,
        output_path: Optional[str] = None, output_filename: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        if not self.validated:
            raise TemplateNotValidatedException(
                "Template must be validated first. Did you forget to call the `.validate()` method?"
            )

        list_objects = list_objects or []

        if context:
            self._add_global_tag_context(context)

        self._handle_general_tags()

        if self.header_tag_info:
            self._handle_header_and_data_tags(list_objects)

        self.save_report(output_filename, output_path)
