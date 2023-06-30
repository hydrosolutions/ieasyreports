"""Console script for ieasyreports."""
import sys
import click

from ieasyreports.core.tags import Tag
from ieasyreports.utils import import_from_string
from ieasyreports.settings import Settings

from ieasyreports.core.tags.tags import title_tag, author_tag, date_tag

settings = Settings()


@click.command()
@click.option("--template_file", required=True, help="Name of the template file.")
def parse_template(template_file):
    try:
        report_generator = import_from_string(settings.template_generator_class)(
            tags=[date_tag, title_tag, author_tag],
            template=template_file
        )
        report_generator.validate()
        report_generator.generate_report()

    except (AttributeError, ImportError) as e:
        click.echo(f"The following error occurred: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(parse_template())  # pragma: no cover
