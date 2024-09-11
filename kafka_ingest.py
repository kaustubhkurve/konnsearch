import os

from src.konnsearch.connect import Connection
from src.konnsearch.connectors.file import JSONSourceConnector
from src.konnsearch.connectors.kafka import KafkaSinkConnector

if __name__ == "__main__":
    kconfig = {
        "bootstrap.servers": "localhost:9092"
    }

    source = JSONSourceConnector(os.path.join(os.getcwd(), "stream.jsonl"))
    target = KafkaSinkConnector(kconfig, "cdc-events")

    connection = Connection(source, target)
    connection.sync()
