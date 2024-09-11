import json

from konnsearch.event import Event


def test_event(sample_event):
    eventstring = json.dumps(sample_event)
    event = Event(eventstring)
    assert event.raw == eventstring
    assert event.key == json.loads(eventstring)["after"]["key"]
