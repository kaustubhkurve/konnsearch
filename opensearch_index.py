import os

from src.konnsearch.connect import Connection
from src.konnsearch.connectors.kafka import KafkaSourceConnector
from src.konnsearch.connectors.opensearch import OpenSearchSinkConnector

if __name__ == "__main__":
    kconsumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "kongconsumer",
        'auto.offset.reset': 'earliest'
    }

    source = KafkaSourceConnector(kconsumer_config, ["cdc-events"])
    target = OpenSearchSinkConnector("localhost", "9200", "cdc")

    connection = Connection(source, target)
    connection.sync()
