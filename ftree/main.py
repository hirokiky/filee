import click

from .save import save


cli = click.Group()
cli.add_command(save)
