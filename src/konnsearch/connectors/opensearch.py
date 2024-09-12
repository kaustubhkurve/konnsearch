"""
The opensearch module imlpements Opensearch connectors.
"""

import json

from ..connect import SinkConnector
from ..helpers import batched

from opensearchpy import OpenSearch


class OpenSearchSinkConnector(SinkConnector):
    """
    Implements the opensearch sink connector.

    It reads the source stream for events and uses the bulk API
    for index the events to opensearch.
    """
    def __init__(self, host, port, index_name, batchsize=10):
        self.client = OpenSearch(hosts=[{
            "host": host,
            "port": port
        }])

        self.index_name = index_name
        self.batchsize = batchsize

    def _bulk_body(self, events):
        """
        Prepares the body for the bulk index requests for the events.
        Note: We are letting opensearch auto assign document ids here.
        """
        body = ""
        for event in events:
            body += json.dumps({"index": {"_index": self.index_name}}) + "\n"
            body += json.dumps({"value": event.parsed}) + "\n"

        return body

    def _bulk_index(self, events):
        """
        Indexes the cdc events to elasticsearch using the bulk API.
        Similar to the Kafka connector, it implements a log and continue
        model for failures. The sink can be extended to support
        other mechanisms.
        """
        result = self.client.bulk(self._bulk_body(events))
        if result["errors"]:
            print("Errors during bulk operation", result)
        else:
            print("Indexed {} events".format(len(events)))

    def publish(self, stream):
        """
        Implements the publish contract for the opensearch sink connector.
        It consumes the source stream, and indexes the events to opensearch.
        """
        for events in batched(stream, self.batchsize):
            self._bulk_index(events)
