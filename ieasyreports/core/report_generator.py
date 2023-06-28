from typing import Dict, List
import openpyxl

from ieasyreports.core.tag import Tag


class ReportGenerator:
    def __init__(self, tags: List[Tag], template: str):
        self.tags = {tag.name: tag for tag in tags}
        self.template = self.open_template_file(template)

    @staticmethod
    def open_template_file(template_name) -> openpyxl.Workbook:
        workbook = openpyxl.load_workbook(template_name)
        return workbook

    def generate_report(self, template: str, context: Dict) -> str:
        content = template
        for tag_name, tag in self.tags.items():
            if tag_name in content:
                content = tag.replace(content, context)

        return content
