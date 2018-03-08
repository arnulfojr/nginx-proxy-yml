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


def file_preview(filename):
    try:
        server, upstreams = nginx.config.load_configuration(filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1
    echo(server, upstreams)


def docker_preview(filename):
    network, me = networks.get_current()
    containers = nginx.docker.transform(network, me=me)
    try:
        server, upstreams = nginx.config.from_containers(containers, filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1
    echo(server, upstreams)


def write(filename, upstreams, server):
    with open(filename, 'w') as output_file:
        output_file.write(upstreams)
        output_file.write(server)
    click.echo(f'Configuration written in {filename}')


def docker_load(filename, output, verbose=None):
    network, me = networks.get_current()
    containers = nginx.docker.transform(network, me=me)
    try:
        server, upstreams = nginx.config.from_containers(containers, filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1
    write(output, upstreams, server)


def file_load(filename, output, verbose=None):
    try:
        server, upstreams = nginx.config.load_configuration(filename)
    except ValidationError as e:
        click.echo(json.dumps(e.errors))
        return 1

    if verbose:
        echo(server, upstreams)
    write(output, upstreams, server)


@cli.command()
@click.argument('mode')
@click.argument('filename')
def preview(mode, filename):
    if mode == 'docker':
        docker_preview(filename)
    else:
        file_preview(filename)


@cli.command()
@click.argument('mode')
@click.argument('filename')
@click.argument('output')
@click.option('-v', '--verbose', count=True)
def load(mode, filename, output, verbose):
    if mode == 'docker':
        docker_load(filename, output, verbose)
    else:
        file_load(filename, output, verbose)
