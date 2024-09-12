from unittest.mock import MagicMock

from konnsearch.connect import Connection


def test_connection():
    source, sink = MagicMock(), MagicMock()
    connection = Connection(source, sink)

    assert connection.source == source
    assert connection.sink == sink

    iterator = range(1, 10)
    source.configure_mock(**{"events.return_value": iterator})

    connection.sync()

    source.transfer_to.assert_called_once()
