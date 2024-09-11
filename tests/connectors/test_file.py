import json
from unittest.mock import patch, mock_open

import pytest

from konnsearch.connectors.file import JSONSourceConnector


@pytest.fixture
def jsonldata(sample_events):
    return "\n".join([json.dumps(e) for e in sample_events]) + "\n"


@patch("os.path.isfile")
def test_json_source_connector(osmock, jsonldata, sample_events):
    with patch("builtins.open", mock_open(read_data=jsonldata)):
        osmock.return_value = True
        json_source = JSONSourceConnector(path="abc")
        assert [e.parsed for e in json_source.events()] == sample_events


@patch("os.path.isfile")
def test_json_source_connector_invalid_file(osmock):
    osmock.return_value = False

    with pytest.raises(RuntimeError):
        JSONSourceConnector(path="abc")
