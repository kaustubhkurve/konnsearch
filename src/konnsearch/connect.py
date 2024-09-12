"""
The connect module implements core functionality to transfer cdc
events from source to sink.

The connect module has no underlying information on what source
and sink implementations are. That should be imlpemented in concrete
source and sink classes.
"""

from abc import ABC, abstractmethod


class SourceConnector(ABC):
    """
    An abstract class that defines methods that must be implemented
    by the concrete source connectors
    """
    @abstractmethod
    def transfer_to(self, sink):
        """
        The transfer_to method implements the transfer of events from
        the source to sink.
        Internally, the source would need to call the sink's publish method
        to publish events.
        """
        pass


class SinkConnector(ABC):
    """
    An abstract class that defines methods that must be implemented
    by the concrete sink connectors
    """
    @abstractmethod
    def publish(self, events):
        """
        The publish method takes a list of events and
        publishes the events to the corresponding sink
        """
        pass

    @abstractmethod
    def get_batch_size(self):
        """
        Return the batch size recommended by the sink.
        This allows the source connector to pull the
        appropriate number of events, and send them to the sink
        """
        pass


class Connection:
    """
    The connection object represents a connection between a source and a sink.
    This makes it easy to plug in source and sink connnectors independently.

    Currently, it only implements a sync method to establish the connection
    and other common methods can be added later to make it more functional.
    """
    def __init__(self, source, sink, **kwargs):
        self.source = source
        self.sink = sink

    def sync(self):
        """
        The sync method creates a connection between the source and
        sink connectors.
        """
        self.source.transfer_to(self.sink)
