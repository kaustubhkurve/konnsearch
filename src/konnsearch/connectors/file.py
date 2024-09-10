"""
The file module implements the json source connector to read
cdc events from a jsonl file
"""

import os

from ..event import Event
from ..connect import SourceConnector


class JSONSourceConnector(SourceConnector):
    """
    The JSON source connector reads cdc events from a jsonl file.
    """
    def __init__(self, path):
        if not os.path.isfile(path):
            raise RuntimeError(
                "JSONSourceConnector: The file path seems to be invalid"
            )
        self.path = path

    def events(self):
        """
        The events method opens the jsonl file, read the file
        one line at a time and returns a generator that yields
        one event object at a time.
        """
        with open(self.path) as f:
            for line in f:
                yield Event(line)
