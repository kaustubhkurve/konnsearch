"""
Define an event class for easy access to event data
"""

import json


class Event:
    """
    Implements the encapsulating data structure for event objects.
    It takes a raw utf encoded string representing a cdc event and builds
    out commonly accessed/required attributes as instance members.
    """
    def __init__(self, ev):
        self.raw = ev
        self.parsed = json.loads(ev)

        self.before = self.parsed["before"]
        self.after = self.parsed["after"]
        self.key = self.parsed["after"]["key"]
        self.operation = self.parsed["op"]
        self.timestamp = self.parsed["ts_ms"]
