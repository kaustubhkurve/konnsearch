# Problem

We are building a search bar that lets people do fuzzy search on different Konnect entities (services, routes, nodes). 
You're in charge of creating the backend ingest to power that service built on top of a [CDC stream](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-create-events) generated by Debezium

We have provided a jsonl file containing some sample events that can be used to
simulate input stream.


Below are the tasks we want you to complete.

* develop a program that ingests the sample cdc events into a Kafka topic
* develop a program that persists the data from Kafka into Opensearch

# Solution

The package implements the tasks by building a connector framework:

The `konnsearch/connect` module defines a core contract for all connectors and the connection object to sync events between source and sink.

The connectors are implemented under `konnsearch/connectors` package. The following connectors are defined to implement the tasks:

* `JSONSourceConnector`: Acts a source event stream for jsonl events from a file
* `KafkaSourceConnector`: A source connector to stream events from a Kafka topic(s)
* `KafkaSinkConnector`: A sink connector to publish events to a Kafka topic
* `OpensearchSinkConnector`: A sink connector to index events to opensearch

The connector contract allows any source to connect to any sink. Hence events can be moved from one kafka topic to another by simply
using the KafkaSourceConnector as source and KafkaSinkConnector as a sink. New source and sink connectors can be added to support other workflows.

A basic CLI is implemented that makes it easier to execute the workflows. The cli requires config files for source and sink connectors.
The config files for local and docker based setup can be found under `conf` directory.

The general invocation of the cli is:
```
konnsearch sync --source <source-name> --sink <sink-name> --source-config <path-to-source-config> --sink-config <path-to-sink-config>
```

## Getting started

### Setting up the environment

1. Setup a python virtualenv (Make sure you have virtualenv installed) and activate it
```
virtualenv .venv
source .venv/bin/activate
```

2. Install konnsearch
```
pip install --editable .
```

3. Start services (Kafka, opensearch)
```
docker compose up -d
```

The Kafka cluster is accessible locally at `localhost:9092` or `kafka:29092` for services running inside the container network.

Kafka-UI can be accessed at `localhost:8080` to examine the ingested Kafka messages.

Opensearch is accessible locally at `localhost:9200` or `opensearch-node:9200` for services running inside the container network.

### Usage

#### Running from local

1. Make sure the virtualenv is activated

2. To ingest the events to Kafka from the jsonl file, run:
```
konnsearch sync --source json --sink kafka --source-config conf/local/sources/jsonl.json --sink-config conf/local/sinks/kafka.json
```

3. To index the events to Opensearch, run:
```
konnsearch sync --source kafka --sink opensearch --source-config conf/local/sources/kafka.json --sink-config conf/local/sinks/opensearch.json
```

4. Kafka UI can be used to inspect the messages in the Kafka topic

4. To query the opensearch API and check the indexed events, execute the following search request:
```
curl localhost:9200/cdc/_search
```

#### Running from a docker container

A simple dockerfile is present in the repository that can be used to build the konnsearch image. You can run konnsearch commands from within the container.

Notes:

1. The docker compose file is updated to add a specific network name (konnsearch) to all services defined in docker-compose.yaml. This allows us to attach our konnsearch container to the common network for it to be able to access all services.
2. The configuration files for docker setup are under `conf/docker`. Please ensure that config files are provided to konnsearch from the appropriate configuration directory.

##### Steps

1. Build the konnsearch image
```
docker build  . -t konnsearch:0.1.0
```

2. Run the konnsearch image in interactive mode (and attaching it to konnsearch network), and drop into the container shell
```
docker run -it --network konnsearch konnsearch:0.1.0 /bin/bash
```

3. To ingest the events to Kafka from the jsonl file, run:
```
konnsearch sync --source json --sink kafka --source-config conf/docker/sources/jsonl.json --sink-config conf/docker/sinks/kafka.json
```

4. To index the events to Opensearch, run:
```
konnsearch sync --source kafka --sink opensearch --source-config conf/docker/sources/kafka.json --sink-config conf/docker/sinks/opensearch.json
```

### Tests

The project uses pytest for testing. To run the test suite, execute:
```
pytest
```

### Shutdown

To tear down all services, run:
```
docker compose down
```

## Improvements

1. Centralised logging

## Resources

* `stream.jsonl` contains cdc events that need to be ingested
* `docker-compose.yaml` contains the skeleton services to help you get started
