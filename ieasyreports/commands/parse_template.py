"""Console script for ieasyreports."""
import sys
import click

from ieasyreports.utils import import_from_string
from ieasyreports.settings import Settings

settings = Settings()


@click.command()
@click.option("--template_file", help="Name of the template file.")
def parse_template(template_file):
    try:
        report_generator = import_from_string(settings.template_generator_class)()
        workbook = report_generator.open_template_file(template_file)
    except (AttributeError, ImportError) as e:
        click.echo(f"The following error occurred: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(parse_template())  # pragma: no cover
