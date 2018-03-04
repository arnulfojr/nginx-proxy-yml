import click

from core.nginx import config


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
    server, upstreams = config.load_configuration(filename)
    echo(server, upstreams)


@cli.command()
@click.argument('filename')
@click.argument('output')
@click.option('-v', '--verbose', count=True)
def load(filename, output, verbose):
    server, upstreams = config.load_configuration(filename)
    if verbose:
        echo(server, upstreams)

    with open(output, 'w') as output_file:
        output_file.write(upstreams)
        output_file.write(server)

    click.echo(f'Configuration written in {output}')
