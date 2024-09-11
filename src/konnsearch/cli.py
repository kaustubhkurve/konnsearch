"""
Defines the cli interface for konnsearch
"""

import json

import click

from .connect import Connection
from .connectors import ConnectorInventory


@click.group
def cli():
    click.echo("Welcome to konnsearch!")


@cli.command
@click.option(
    "--source", required=True, help="The name of the source connector",
    type=click.Choice(ConnectorInventory.get_available_source_connectors())
)
@click.option(
    "--sink", required=True, help="The name of the sink connector",
    type=click.Choice(ConnectorInventory.get_available_sink_connectors())
)
@click.option(
    "--source-config", type=click.File("r"),
    required=True, help="The path of the source connector config"
)
@click.option(
    "--sink-config", type=click.File("r"),
    required=True, help="The path of the sink connector config"
)
def sync(source, sink, source_config, sink_config):
    """
    Sync events between the source connector and sink connector.

    Requires the name of the source and sink connectors, and thier
    corresponding configuration files
    """
    source_cls = ConnectorInventory.get_source_connector(source)
    sink_cls = ConnectorInventory.get_sink_connector(sink)

    source_conf = json.loads(source_config.read())
    sink_conf = json.loads(sink_config.read())

    source = source_cls(**source_conf)
    sink = sink_cls(**sink_conf)

    connection = Connection(source, sink)
    connection.sync()


if __name__ == '__main__':
    cli()
