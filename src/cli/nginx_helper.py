import click

from core.nginx import config


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.argument('output')
def load(filename, output):
    server, upstreams = config.load_configuration(filename)
    click.echo('### Upstreams ###')
    click.echo(upstreams)
    click.echo('### Server ###')
    click.echo(server)
    with open(output, 'w') as output_file:
        output_file.write(upstreams)
        output_file.write(server)
