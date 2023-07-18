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

from ieasyreports.examples.dummy_sites import Site, SITES

settings = Settings()


class DefaultReportGenerator:
    def __init__(self, tags: List[Tag], template: str):
        self.tags = {tag.name: tag for tag in tags}
        self.template_filename = template
        self.template = self.open_template_file()
        self.sheet = self.template.worksheets[0]

        self.validated = False

        self.header_tag_info = {}
        self.data_tags_info = []
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
        if not self.header_tag_info:
            raise MissingHeaderTagException("Header tag is missing in the template.")

    def _validate_data_tags(self):
        if not self.data_tags_info:
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

    def generate_report(self, sites: List[Site] = SITES):
        if not self.validated:
            raise TemplateNotValidatedException(
                "Template must be validated first. Did you forget to call the `.validate()` method?"
            )
        for tag, cells in self.general_tags.items():
            for cell in cells:
                cell.value = tag.replace(cell.value)
        print("tu sam")
        grouped_sites = {}
        for site in sites:
            header_value = self.header_tag_info["tag"].replace(
                self.header_tag_info["cell"].value,
                site=site,
                special="HEADER"
            )

            if header_value not in grouped_sites:
                grouped_sites[header_value] = []
            grouped_sites[header_value].append(site)

        original_header_row = self.header_tag_info["cell"].row
        original_data_row = self.data_tags_info[0]["cell"].row

        header_style = self.header_tag_info["cell"].font.copy()
        data_styles = [data_tag["cell"].font.copy() for data_tag in self.data_tags_info]

        self.sheet.delete_rows(original_header_row, 3)

        for header_value, site_group in sorted(grouped_sites.items()):
            # write the header value
            self.sheet.insert_rows(original_header_row)
            cell = self.sheet.cell(row=original_header_row, column=self.header_tag_info["cell"].column, value=header_value)
            cell.font = header_style

            for site in site_group:
                self.sheet.insert_rows(original_header_row + 1)
                for idx, data_tag in enumerate(self.data_tags_info):
                    tag = data_tag["tag"]
                    data = tag.replace(data_tag["cell"].value, site=site, special=settings.data_tag)
                    cell = self.sheet.cell(row=original_header_row + 1, column=data_tag["cell"].column, value=data)
                    cell.font = data_styles[idx]

            original_header_row += len(site_group) + 2
            original_data_row += len(site_group) + 2

        self.save_report("basic_report.xlsx")
