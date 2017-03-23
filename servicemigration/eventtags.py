import copy

default = {
    "Severity": 0,
    "Resolution": "",
    "Explanation": "",
    "EventClass": ""
}

def deserialize(data):
    """
    Parse data into an EventTags object.
    """
    eventTags = EventTags()
    eventTags._EventTags__data = data
    for key, val in data.iteritems():
        if key == "Severity":
            eventTags.severity = val
        elif key == "Resolution":
            eventTags.resolution = val
        elif key == "Explanation":
            eventTags.explanation = val
        elif key == "EventClass":
            eventTags.eventClass = val

    return eventTags

def serialize(eventTags):
    """
    Dump eventTags as data
    """
    d = copy.deepcopy(eventTags._EventTags__data)
    d["Severity"] = eventTags.severity
    d["Resolution"] = eventTags.resolution
    d["Explanation"] = eventTags.explanation
    d["EventClass"] = eventTags.eventClass

    return d

class EventTags(object):
    """
    Wraps a single EventTags object.
    """
    def __init__(self, severity=0, resolution="", explanation="", eventClass=""):
        self.__data = copy.deepcopy(default)
        self.severity = severity
        self.resolution = resolution
        self.explanation = explanation
        self.eventClass = eventClass
