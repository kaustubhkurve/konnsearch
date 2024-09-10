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
    def events(self):
        """
        The events method should return an iterator for the events
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
        The publish method takes an events iterator and
        publishes the events to the corresponding sink
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

        Currently, it simply passes the events iterator from the
        source connector to the sink connector.

        This allows the sink connector to get events based on it's
        needs.
        """
        eventstream = self.source.events()
        self.sink.publish(eventstream)
