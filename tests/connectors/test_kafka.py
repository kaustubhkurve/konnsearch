import json
from unittest.mock import patch, MagicMock

import pytest

from konnsearch.event import Event
from konnsearch.connectors.kafka import (
    KafkaSourceConnector, KafkaSinkConnector, KafkaException
)


@pytest.fixture
def binary_sample_event(sample_event):
    return bytes(json.dumps(sample_event), "utf-8")


@patch("konnsearch.connectors.kafka.Consumer")
def test_kafka_source_connector(
        consumermock, binary_sample_event, sample_event
):
    message_mock = MagicMock()
    message_mock.configure_mock(**{
        "value.return_value": binary_sample_event, "error.return_value": None
    })

    consumerinstance_mock = consumermock.return_value
    consumerinstance_mock.configure_mock(**{
        "poll.side_effect": [
            message_mock, None, message_mock, KeyboardInterrupt
        ]
    })

    k_source = KafkaSourceConnector(
        config={"bootstrap.servers": "localhost"},
        topics=["test"]
    )

    result = list(k_source.events())

    consumerinstance_mock.subscribe.assert_called_once()
    consumerinstance_mock.poll.assert_called()
    consumerinstance_mock.close.assert_called()
    assert [r.parsed for r in result] == [sample_event] * 2


@patch("konnsearch.connectors.kafka.Consumer")
def test_kafka_source_connector_on_error(consumermock):
    message_mock = MagicMock()
    message_mock.configure_mock(**{
        "error.return_value": "internal kafka error"
    })

    consumerinstance_mock = consumermock.return_value
    consumerinstance_mock.configure_mock(**{
        "poll.side_effect": [
            message_mock, None, message_mock, KeyboardInterrupt
        ]
    })

    k_source = KafkaSourceConnector(
        config={"bootstrap.servers": "localhost"},
        topics=["test"]
    )

    with pytest.raises(KafkaException):
        list(k_source.events())

        consumerinstance_mock.subscribe.assert_called_once()
        consumerinstance_mock.poll.assert_called()
        consumerinstance_mock.close.assert_called()


@patch("konnsearch.connectors.kafka.Producer")
def test_kafka_sink_connector(producermock, sample_events):
    producerinstance_mock = producermock.return_value
    k_sink = KafkaSinkConnector(
        config={"bootstrap.servers": "localhost"},
        topic="test"
    )

    eventstream = [Event(json.dumps(ev)) for ev in sample_events]
    k_sink.publish(eventstream)

    producerinstance_mock.produce.assert_called()
