import click

from ieasyreports.commands.parse_template import parse_template


@click.group()
def cli():
    pass


cli.add_command(parse_template)
