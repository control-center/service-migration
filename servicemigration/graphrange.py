import copy


default = {
    "end": "",
    "start": "",
}


def deserialize(data):
    """
    Parse data into a GraphRange.
    """
    graphrange = GraphRange()
    if not data:
        return graphrange
    graphrange._GraphRange__data = data
    graphrange.start = data.get("start", "")
    graphrange.end = data.get("end", "")
    return graphrange


def serialize(graphrange):
    """
    Dump a GraphRange as data.
    """
    if not graphrange:
        return None
    data = copy.deepcopy(graphrange._GraphRange__data)
    data["start"] = graphrange.start
    data["end"] = graphrange.end
    return data


class GraphRange(object):
    """
    Wraps a single GraphRange object.
    """
    def __init__(self, start="", end=""):
        self.__data = copy.deepcopy(default)
        self.start = start
        self.end = end
