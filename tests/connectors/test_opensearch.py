import json
from unittest.mock import patch, call

import pytest

from konnsearch.event import Event
from konnsearch.connectors.opensearch import OpenSearchSinkConnector


@pytest.fixture
def index_body(sample_event):
    return json.dumps({"index": {"_index": "testindex"}}) + \
        "\n" + json.dumps({"value": sample_event})


@patch("konnsearch.connectors.opensearch.OpenSearch")
def test_opensearch_sink_connector(osmock, sample_events, index_body):
    osinstance_mock = osmock.return_value
    osinstance_mock.configure_mock(**{"bulk.return_value": {"errors": None}})
    os_sink = OpenSearchSinkConnector(
        host="localhost",
        port="9200",
        index_name="testindex",
        batchsize=5
    )

    eventstream = [Event(json.dumps(d)) for d in sample_events]

    os_sink.publish(eventstream)
    osinstance_mock.bulk.assert_called()
    osinstance_mock.bulk.assert_has_calls([
        call("\n".join([index_body] * 12) + "\n")
    ], any_order=False)
