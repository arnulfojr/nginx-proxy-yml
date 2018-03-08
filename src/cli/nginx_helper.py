import click
import json

from core import nginx
from core.exc import ValidationError
from core.docker import networks


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
        server, upstreams = nginx.config.load_configuration(filename)
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
        server, upstreams = nginx.config.load_configuration(filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1

    if verbose:
        echo(server, upstreams)

    with open(output, 'w') as output_file:
        output_file.write(upstreams)
        output_file.write(server)

    click.echo(f'Configuration written in {output}')


@cli.command()
@click.argument('filename')
def docker_preview(filename):
    network, me = networks.get_current()
    containers = nginx.docker.transform(network, me=me)
    try:
        server, upstreams = nginx.config.from_containers(containers, filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1
    echo(server, upstreams)


@cli.command()
@click.argument('filename')
@click.argument('output')
def from_docker(filename, output):
    network, me = networks.get_current()
    containers = nginx.docker.transform(network, me=me)
    try:
        server, upstreams = nginx.config.from_containers(containers, filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1

    with open(output, 'w') as output_file:
        output_file.write(upstreams)
        output_file.write(server)

    click.echo(f'Configuration written in {output}')
