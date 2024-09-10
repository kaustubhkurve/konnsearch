import os

from src.connect import Connection
from src.connectors.file import JSONSourceConnector
from src.connectors.kafka import KafkaSinkConnector, KafkaSourceConnector
from src.connectors.opensearch import OpenSearchSinkConnector

if __name__ == "__main__":
    kconfig = {
        "bootstrap.servers": "localhost:9092"
    }

    source = JSONSourceConnector(os.path.join(os.getcwd(), "stream.jsonl"))
    target = KafkaSinkConnector(kconfig, "cdc-events")

    connection = Connection(source, target)
    connection.sync()

    kconsumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "kongconsumer",
        'auto.offset.reset': 'earliest'
    }

    source = KafkaSourceConnector(kconsumer_config, ["cdc-events"])
    target = OpenSearchSinkConnector("localhost", "9200", "cdc")

    connection = Connection(source, target)
    connection.sync()
