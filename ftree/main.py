import json

import click

from .models import FileTree


@click.command()
@click.option('--dir', default='.', help='Target dir to load')
def load(dir):
    ft = FileTree.load(dir)
    print(json.dumps(ft.to_dict(), ensure_ascii=False))


@click.command()
def save():
    inp = input()
    data = json.loads(inp)
    ft = FileTree.from_dict(data)
    ft.save()


cli = click.Group()
cli.add_command(save)
cli.add_command(load)
