import click
import json

from core.nginx import config
from core.exc import ValidationError


@click.group()
def cli():
    pass


def echo(server, upstreams):
    click.echo('### Upstreams ###')
    click.echo(upstreams)
    click.echo('### Server ###')
    click.echo(server)


@cli.command()
@click.argument('filename')
def preview(filename):
    try:
        server, upstreams = config.load_configuration(filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1
    echo(server, upstreams)


@cli.command()
@click.argument('filename')
@click.argument('output')
@click.option('-v', '--verbose', count=True)
def load(filename, output, verbose):
    try:
        server, upstreams = config.load_configuration(filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1

    if verbose:
        echo(server, upstreams)

    with open(output, 'w') as output_file:
        output_file.write(upstreams)
        output_file.write(server)

    click.echo(f'Configuration written in {output}')
