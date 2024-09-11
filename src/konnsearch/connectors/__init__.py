from .kafka import KafkaSourceConnector, KafkaSinkConnector
from .opensearch import OpenSearchSinkConnector
from .file import JSONSourceConnector


class ConnectorNotFound(Exception):
    """
    Indicates that the connection class could not be located
    """
    pass


class ConnectorInventory:
    """
    Stores the inventory for the connector classes.

    Currently, this is explicity specified as a class member.
    However, this could be extended to dynamically build the available
    classes under the connectors package by filtering the ones that are
    implementing the SourceConnector/SinkConnector abstract classes.
    """
    inventory = {
        "sources": {
            "json": JSONSourceConnector,
            "kafka": KafkaSourceConnector,
        },
        "sinks": {
            "kafka": KafkaSinkConnector,
            "opensearch": OpenSearchSinkConnector
        }
    }

    @classmethod
    def get_available_source_connectors(self):
        """
        Returns the list of available source connectors
        """
        return self.inventory["sources"].keys()

    @classmethod
    def get_available_sink_connectors(self):
        """
        Returns the list of available sink connectors
        """
        return self.inventory["sinks"].keys()

    @classmethod
    def get_source_connector(self, name):
        """
        Returns the source connector corresponding to a name identifier.
        Raises the ConnectorNotFound exception otherwise.
        """
        if name in self.inventory["sources"]:
            return self.inventory["sources"][name]

        raise ConnectorNotFound

    @classmethod
    def get_sink_connector(self, name):
        """
        Returns the sink connector corresponding to a name identifier.
        Raises the ConnectorNotFound exception otherwise.
        """
        if name in self.inventory["sinks"]:
            return self.inventory["sinks"][name]

        raise ConnectorNotFound
